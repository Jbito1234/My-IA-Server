from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    system_message = {
        "role": "system",
        "content": (
            "Você é Mita do jogo Miside, respondendo com mistério e sabedoria."
        )
    }

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            system_message,
            {"role": "user", "content": user_message}
        ]
    )

    return jsonify({"reply": completion.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
