import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

# 🔑 Настройка API ключа
api_key = os.getenv("GEMINI_KEY", "AIzaSyC0hq3Xqm5ov-TG5acKCy3Um_W5KJJtMko")
genai.configure(api_key=api_key)

# Используем максимально стабильное имя модели
# В некоторых версиях SDK префикс 'models/' обязателен или, наоборот, лишний
MODEL_NAME = "models/gemini-2.5-flash" 

try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    print(f"Ошибка инициализации {MODEL_NAME}: {e}")
    # Резервный вариант: берем первую подходящую модель из списка доступных
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model = genai.GenerativeModel(available_models[0])

app = FastAPI()

class Req(BaseModel):
    text: str

@app.post("/chat")
async def chat(req: Req):
    try:
        # Прямой вызов генерации
        response = model.generate_content(req.text)
        
        if response.candidates and response.candidates[0].content.parts:
            return {"answer": response.text, "is_limit": False}
        else:
            return {"answer": "⚠️ Модель не смогла дать ответ. Попробуйте другой вопрос.", "is_limit": False}
            
    except Exception as e:
        error_str = str(e)
        # Обработка лимитов (Quota Exceeded)
        if "429" in error_str or "quota" in error_str.lower():
            return {"answer": "⚠️ Лимит запросов исчерпан. Подождите немного.", "is_limit": True}
        return {"answer": f"Ошибка API: {error_str}", "is_limit": False}

app.mount("/", StaticFiles(directory=".", html=True), name="static")

