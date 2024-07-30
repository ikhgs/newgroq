import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Lire la variable d'environnement
api_key = os.getenv('GROQ_API_KEY')

# Initialiser le client avec la clé API
client = Groq(api_key=api_key)

@app.route('/', methods=['GET'])
def home():
    # Lire le paramètre de requête 'ask'
    question = request.args.get('ask', default='Citer les étapes de la fécondation', type=str)

    # Créer la complétion
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collecter la réponse
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return jsonify({"response": response})

# Vercel n'utilise pas cette section
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
