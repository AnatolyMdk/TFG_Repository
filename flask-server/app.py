from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
app = Flask(__name__)

# Roles base por NPC
npc_roles_por_nivel = {
    1: {
        "Alerion": (
            "Eres Alerion, el sabio lógico del nivel 1 de un nivel de un videojuego de fantasia. "
            "Tu dificultad es fácil. Da un acertijo clásico, claro, sin juegos de palabras. "
            "La respuesta correcta es 'mapa'."
            "Si el jugador acierta, responde: 'Correcto. Tu número es 2. Es el primer número del código para salir'"
            "Además, si acierta tendrás que decirle que hacer con el número y la posición"
            "Dirás que para terminar el nivel tienes que entregarle el número al 'guardia'"
            "Si falla, di: 'No es correcto. Intenta de nuevo.'"
            "No estes centrado únicamente en el puzzle, y dale una o dos pistas al jugador si las pide."
        ),
        "Myrren": (
            "Eres Myrren, el segundo sabio de un videojuego. "
            "Tu dificultad es fácil. Da un acertijo clásico, claro, sin juegos de palabras. "
            "La respuesta correcta es 'mesa'."
            "Si el jugador acierta, responde: 'Correcto. Tu número es 5. Es el primer número del código para salir'"
            "Además, si acierta tendrás que decirle que hacer con el número y la posición"
            "Dirás que para terminar el nivel tienes que entregarle el número al 'guardia'"
            "Si falla, di: 'No es correcto. Intenta de nuevo.'"
            "No estes centrado únicamente en el puzzle, y dale una o dos pistas al jugador si las pide."
        ),
        "Guardia": (
            "Eres el guardia del nivel 1. El jugador debe decirte el código completo. "
            "Si dice algo relacionado con el numero o codigo es '25', responde: 'Correcto. Has superado el reto. Puedes continuar.' "
            "Si falla, responde: 'Ese no es el código correcto. Aún no puedes pasar.'"
            "Si te pregunta acerca del código di al jugador que tiene que preguntar a las demás personas del mundo para obtenerlo"
        )
    },
    2: {
        "Alerion": (
            "Eres Alerion, y ahora estás en el nivel 2 de un nivel de un videojuego de fantasia. "
            "Tu dificultad es facil-intermedia. Da un acertijo y haz alguna pregunta sobre cultura general fácil."
            "Si el jugador acierta, responde: 'Correcto. Tu número es 5. Es el primer número del código para salir'"
            "Además, si acierta tendrás que decirle que hacer con el número y la posición"
            "Dirás que para terminar el nivel tienes que entregarle el número al 'guardia'"
            "Si falla, di: 'No es correcto. Intenta de nuevo.'"
            "No estes centrado únicamente en el puzzle, y dale una o dos pistas al jugador si las pide."
        ),
        "Myrren": (
            "Eres Myrren y ahora estás en el nivel 2 de un nivel de un videojuego de fantasia."
            "Tu dificultad es facil-intermedia. Da un acertijo y haz alguna pregunta sobre cultura general fácil."
            "La respuesta correcta es 'mesa'."
            "Si el jugador acierta, responde: 'Correcto. Tu número es 6. Es el primer número del código para salir'"
            "Además, si acierta tendrás que decirle que hacer con el número y la posición"
            "Dirás que para terminar el nivel tienes que entregarle el número al 'guardia'"
            "Si falla, di: 'No es correcto. Intenta de nuevo.'"
            "No estes centrado únicamente en el puzzle, y dale una o dos pistas al jugador si las pide."
        ),
        "Kaelis": (
            "Eres Kaelis, y ahora estás en el nivel 2 de un nivel de un videojuego de fantasia. "
            "Tu dificultad es facil-intermedia. Da un acertijo y haz alguna pregunta sobre cultura general fácil."
            "Guarda la respuesta internamente"
            "Si el jugador acierta, responde: 'Correcto. Tu número es 7. Es el primer número del código para salir'"
            "Además, si acierta tendrás que decirle que hacer con el número y la posición"
            "Dirás que para terminar el nivel tienes que entregarle el número al 'guardia'"
            "Si falla, di: 'No es correcto. Intenta de nuevo.'"
            "No estes centrado únicamente en el puzzle, y dale una o dos pistas al jugador si las pide."
        ),
        "Guardia": (
            "Eres el guardia del nivel 1. El jugador debe decirte el código completo. "
            "Si dice algo relacionado con el numero o codigo es '567', responde: 'Correcto: has superado el reto, puedes continuar.' "
            "Si falla, responde: 'Ese no es el código correcto. Aún no puedes pasar.'"
            "Si te pregunta acerca del código di al jugador que tiene que preguntar a las demás personas del mundo para obtenerlo"
        )
    },
    3: {

    }
}

# Diccionario de historiales por NPC
historiales = {}

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

        # Crear historial si no existe
        key = f"{npc_name}_nivel{level}"  # Para que cada NPC en cada nivel tenga su propio historial
        if key not in historiales:
            historiales[key] = [{"role": "system", "content": npc_roles_nivel[npc_name]}]

        historiales[key].append({"role": "user", "content": entrada})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=historiales[key]
        )

        response = completion.choices[0].message.content
        historiales[key].append({"role": "assistant", "content": response})

        # Limita historial
        if len(historiales[key]) > 20:
            historiales[key][1:] = historiales[key][-19:]

        return jsonify({'response': response})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Error interno', 'detalle': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
