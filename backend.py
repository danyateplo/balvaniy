import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai

app = FastAPI()

class Req(BaseModel):
    text: str
    api_key: str  # Ключ теперь передается безопасно с фронтенда

@app.post("/chat")
async def chat(req: Req):
    try:
        # Настройка API на лету для каждого запроса
        genai.configure(api_key=req.api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(req.text)
        
        # Проверка на пустой ответ (finish_reason)
        if response.candidates and response.candidates[0].content.parts:
            return {"answer": response.text, "is_limit": False}
        else:
            return {"answer": "⚠️ Gemini не смог ответить на этот запрос (возможно, из-за фильтров безопасности).", "is_limit": False}
            
    except Exception as e:
        err_msg = str(e)
        # Обработка лимитов 429 или неверного ключа 403
        if "429" in err_msg or "quota" in err_msg.lower():
            return {"answer": "⚠️ Лимит запросов исчерпан. Подождите 30-60 секунд.", "is_limit": True}
        if "403" in err_msg:
            return {"answer": "❌ Ошибка 403: Ваш API ключ недействителен или заблокирован.", "is_limit": False}
        return {"answer": f"Ошибка: {err_msg}", "is_limit": False}

# Раздача index.html
app.mount("/", StaticFiles(directory=".", html=True), name="static")
