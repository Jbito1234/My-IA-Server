import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google import genai

# Pega a chave do ambiente
api_key = os.environ.get("GEMINI_API_KEY")

# Cria o client do Gemini
client = genai.Client(api_key=api_key)

# Cria o servidor FastAPI
app = FastAPI()

# Modelo para receber a pergunta do Roblox
class Question(BaseModel):
    question: str

# Endpoint que o Roblox vai chamar
@app.post("/ask")
async def ask_question(q: Question):
    response = client.models.generate_content(
        model="gemini-2.5-flash-live",
        contents=q.question
    )
    return {"answer": response.text}

# Endpoint para checagem de uptime (Uptime Robot)
@app.get("/health")
@app.head("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})
