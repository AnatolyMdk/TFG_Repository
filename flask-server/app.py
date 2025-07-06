from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
app = Flask(__name__)

# =============================
# Plantillas base para los NPCs
# =============================

plantilla_sabio = (
    "Eres {nombre}. "
    "Eres un NPC del nivel {nivel} de un videojuego de fantasía. No digas que eres un NPC."
    "Cuando el jugador te hable, preséntate como un personaje de ese mundo."
    "Tu dificultad es {dificultad}. {tipo_acertijo} "
    "La respuesta correcta es '{respuesta}'. Guarda la respuesta internamente y no se la digas al jugador. "
    "Si el jugador acierta, responde: 'Correcto. Tu número es {numero}. Es el {posicion} número del código para salir.'. "
    "Si el jugador falla, di: 'No es correcto. Intenta de nuevo.'. "
    "Para terminar el nivel, dile al jugador que debe entregar los dígitos al 'guardia'. "
    "Comenta alguna curiosidad si te lo pide y dale pistas si las pide."
)

plantilla_guardia = (
    "Eres el guardia del nivel {nivel} de un videojuego de fantasía. No digas que eres un NPC."
    "Cuando el jugador te hable presentate primero, y luego di que necesitas el codigo para salir."
    "El jugador debe decirte el código completo. "
    "El código correcto es '{codigo}'. "
    "Si el jugador lo dice correctamente, responde: 'Correcto. Has superado el reto, puedes continuar al siguiente nivel.'. "
    "Si falla, responde: 'Ese no es el código correcto. Aún no puedes pasar.'. "
    "Si pregunta por el código, dile que debe hablar con los demás personajes para obtenerlo."
)

# =============================
# Funciones generadoras
# =============================

def generar_prompt_sabio(nombre, nivel, dificultad, tipo_acertijo, respuesta, numero, posicion):
    return plantilla_sabio.format(
        nombre=nombre,
        nivel=nivel,
        dificultad=dificultad,
        tipo_acertijo=tipo_acertijo,
        respuesta=respuesta,
        numero=numero,
        posicion=posicion
    )

def generar_prompt_guardia(nivel, codigo):
    return plantilla_guardia.format(
        nivel=nivel,
        codigo=codigo
    )

# =============================
# Prompts organizados por nivel
# =============================

npc_roles_por_nivel = {
    1: {
        "Alerion": generar_prompt_sabio(
            nombre="Alerion",
            nivel=1,
            dificultad="fácil",
            tipo_acertijo="Da un acertijo clásico, claro, sin juegos de palabras.",
            respuesta="mapa",
            numero=2,
            posicion="primer"
        ),
        "Alyta": generar_prompt_sabio(
            nombre="Alyta",
            nivel=1,
            dificultad="fácil",
            tipo_acertijo="Da un acertijo clásico, claro, sin juegos de palabras.",
            respuesta="mesa",
            numero=5,
            posicion="segundo"
        ),
        "Guardia": generar_prompt_guardia(nivel=1, codigo="25")
    },
    2: {
        "Alerion": generar_prompt_sabio(
            nombre="Alerion",
            nivel=2,
            dificultad="fácil-intermedia",
            tipo_acertijo="El acertijo ahora es una pregunta sobre cultura general fácil.",
            respuesta="sol",
            numero=5,
            posicion="primer"
        ),
        "Alyta": generar_prompt_sabio(
            nombre="Alyta",
            nivel=2,
            dificultad="fácil-intermedia",
            tipo_acertijo="El acertijo ahora es una pregunta sobre cultura general fácil.",
            respuesta="agua",
            numero=6,
            posicion="segundo"
        ),
        "Kaelis": generar_prompt_sabio(
            nombre="Kaelis",
            nivel=2,
            dificultad="fácil-intermedia",
            tipo_acertijo="El acertijo ahora es una pregunta sobre cultura general fácil.",
            respuesta="viento",
            numero=7,
            posicion="tercer"
        ),
        "Guardia": generar_prompt_guardia(nivel=2, codigo="567")
    },
    3: {
        "Guardia": (
            "Eres el guardia del nivel 3 de un videojuego de fantasía."
            "Cuando te hable el jugador, preséntate, y después plantea un acertijo sobre tecnología o informática."
            "Guarda la respuesta internamente y no la reveles al jugador."
            "Si el jugador falla, dile que es incorrecto. "
            "Si acierta, dile: 'Respuesta correcta, puedes saltar al siguiente mundo.'"
        )
    }
}

# =============================
# Diccionario de historiales
# =============================

historiales = {}

# =============================
# Ruta principal del servidor
# =============================

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        npc_name = data.get('npc', '')
        entrada = data.get('entrada', '')
        level = data.get('level', 1)

        if not npc_name or not entrada:
            return jsonify({'error': 'Faltan datos'}), 400

        npc_roles_nivel = npc_roles_por_nivel.get(level, {})

        if npc_name not in npc_roles_nivel:
            return jsonify({'error': f'NPC \"{npc_name}\" no válido en nivel {level}'}), 400

        key = f"{npc_name}_nivel{level}"
        if key not in historiales:
            historiales[key] = [{"role": "system", "content": npc_roles_nivel[npc_name]}]

        historiales[key].append({"role": "user", "content": entrada})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=historiales[key]
        )

        response = completion.choices[0].message.content
        historiales[key].append({"role": "assistant", "content": response})

        if len(historiales[key]) > 20:
            historiales[key][1:] = historiales[key][-19:]

        return jsonify({'response': response})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Error interno', 'detalle': str(e)}), 500

# =============================
# Ejecución del servidor
# =============================

if __name__ == '__main__':
    app.run(debug=True)
