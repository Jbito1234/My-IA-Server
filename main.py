import os
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Cria o app FastAPI
app = FastAPI()

# Pega a API key do ambiente (configure no Render como GROQ_API_KEY)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# URL base da API do Groq
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Modelo para receber a pergunta do Roblox
class Question(BaseModel):
    question: str

# Endpoint principal para receber perguntas do Roblox
@app.post("/ask")
async def ask_question(q: Question):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",  # rápido e gratuito
        "messages": [
            {"role": "user", "content": q.question}
        ]
    }

    response = requests.post(GROQ_URL, headers=headers, json=data)
    response_json = response.json()

    try:
        answer = response_json["choices"][0]["message"]["content"]
    except Exception:
        answer = "Erro ao gerar resposta. Tente novamente."

    return {"answer": answer}

# Endpoint de health check (UptimeRobot)
@app.get("/health")
@app.head("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})
