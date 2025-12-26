import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai

app = FastAPI()

class Req(BaseModel):
    text: str
    api_key: str

@app.post("/chat")
async def chat(req: Req):
    try:
        # Очищаем ключ от пробелов и лишних символов
        clean_key = req.api_key.strip()
        genai.configure(api_key=clean_key)
        
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(req.text)
        
        if response.candidates and response.candidates[0].content.parts:
            return {"answer": response.text, "status": "ok"}
        else:
            return {"answer": "🤖 Модель не смогла ответить. Попробуй другой вопрос.", "status": "error"}
            
    except Exception as e:
        err = str(e)
        if "429" in err:
            return {"answer": "⏳ Лимит! Подожди 20-30 секунд.", "status": "limit"}
        return {"answer": f"Ошибка: {err}", "status": "error"}

app.mount("/", StaticFiles(directory=".", html=True), name="static")
