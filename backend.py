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
        # Настройка модели прямо в запросе
        genai.configure(api_key=req.api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(req.text)
        
        if response.candidates and response.candidates[0].content.parts:
            return {"answer": response.text, "status": "success"}
        else:
            return {"answer": "⚠️ Модель отклонила запрос по соображениям безопасности.", "status": "filtered"}
            
    except Exception as e:
        err = str(e)
        if "429" in err:
            return {"answer": "⏳ Лимит исчерпан. Подожди 30 секунд.", "status": "limit"}
        if "403" in err:
            return {"answer": "❌ Ключ заблокирован или неверен. Введи другой.", "status": "error"}
        return {"answer": f"Ошибка: {err}", "status": "error"}

app.mount("/", StaticFiles(directory=".", html=True), name="static")
