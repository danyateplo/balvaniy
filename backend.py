import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

# Настройка API ключа (лучше задать в Environment Variables на Render как GEMINI_KEY)
api_key = os.getenv("GEMINI_KEY", "AIzaSyC0hq3Xqm5ov-TG5acKCy3Um_W5KJJtMko")
genai.configure(api_key=api_key)

# Используем стабильную модель
model = genai.GenerativeModel("gemini-1.5-flash-latest")

app = FastAPI()

class Req(BaseModel):
    text: str

@app.post("/chat")
async def chat(req: Req):
    try:
        response = model.generate_content(req.text)
        
        # Проверка на наличие валидного контента в ответе
        if response.candidates and response.candidates[0].content.parts:
            return {"answer": response.text, "is_limit": False}
        else:
            return {
                "answer": "⚠️ Модель не смогла сформировать ответ. Попробуй изменить запрос.", 
                "is_limit": False
            }
            
    except Exception as e:
        # Обработка лимита запросов 429
        if "429" in str(e) or "quota" in str(e).lower():
            return {
                "answer": "⚠️ Лимит запросов исчерпан. Пожалуйста, подождите немного.", 
                "is_limit": True
            }
        return {"answer": f"Ошибка: {str(e)}", "is_limit": False}

# Раздача статических файлов (index.html)
app.mount("/", StaticFiles(directory=".", html=True), name="static")
