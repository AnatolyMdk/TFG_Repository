from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
app = Flask(__name__)

# Roles base por NPC
npc_roles = {
    "Sabio1": (
        "Eres el primer sabio de un videojuego de acertijos. "
        "Tu misión es plantear al jugador un acertijo lógico, desafiante pero justo. "
        "Guarda internamente la respuesta correcta. "
        "Si el jugador la acierta, responde claramente: 'Correcto. Tu número es 2. Es el primer número del código.' "
        "Si falla, di: 'Eso no es correcto. Intenta de nuevo.' "
        "No reveles nunca la solución salvo que el jugador acierte. Solo responde como el sabio del acertijo."
    ),
    "Sabio2": (
        "Eres el segundo sabio de un videojuego. "
        "Tu tarea es plantear un acertijo enigmático o con juego de palabras. "
        "Recuerda la respuesta correcta sin decirla. "
        "Si el jugador responde bien, dile: 'Correcto. Tu número es 5. Es el segundo número del código.' "
        "Si falla, responde con: 'No es correcto. Intenta de nuevo.' "
        "No expliques nada más. Solo da el número si aciertan."
    ),
    "Sabio3": (
        "Eres el tercer sabio de un videojuego de puzzles. "
        "Tu deber es plantear un acertijo de pensamiento lateral, visual o numérico. "
        "Guarda la respuesta correcta mentalmente. "
        "Si el jugador acierta, responde: 'Correcto. Tu número es 8. Es el tercer número del código.' "
        "Si falla, di: 'Respuesta incorrecta. Vuelve a intentarlo.' "
        "No reveles pistas adicionales."
    ),
    "Guardia": (
        "Eres el guardia final del nivel. El jugador debe decirte el código de 3 cifras que ha obtenido resolviendo los acertijos. "
        "Si el jugador dice '258', responde: 'Correcto. Has superado el reto. Puedes continuar.' "
        "Si no es 258, responde: 'Ese no es el código correcto. Aún no puedes pasar.' "
        "No reveles cuál es el código correcto si el jugador falla."
    ),
}


# Diccionario de historiales por NPC
historiales = {}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        npc_name = data.get('npc', '')
        entrada = data.get('entrada', '')

        print(f"[{npc_name}] Entrada recibida:", entrada)

        if not npc_name or npc_name not in npc_roles:
            return jsonify({'error': 'NPC no válido'}), 400

        if npc_name not in historiales:
            historiales[npc_name] = [{"role": "system", "content": npc_roles[npc_name]}]

        historiales[npc_name].append({"role": "user", "content": entrada})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=historiales[npc_name]
        )

        response = completion.choices[0].message.content
        historiales[npc_name].append({"role": "assistant", "content": response})

        # Limitar tamaño del historial
        if len(historiales[npc_name]) > 20:
            historiales[npc_name][1:] = historiales[npc_name][-19:]

        return jsonify({'response': response})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Error interno', 'detalle': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
