from flask import Flask, request, jsonify
from openai import OpenAI
import os
import traceback

app = Flask(__name__)

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        system_message = {
            "role": "system",
            "content": "Você é o guardião da floresta"
        }
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                system_message,
                {"role": "user", "content": user_message}
            ]
        )
        
        return jsonify({"reply": completion.choices[0].message.content})
    
    except Exception as e:
        print("Erro na rota /chat:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
