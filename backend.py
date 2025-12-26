from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai

# 🔑 ВСТАВЬ СВОЙ КЛЮЧ
genai.configure(api_key="AIzaSyC0hq3Xqm5ov-TG5acKCy3Um_W5KJJtMko")

model = genai.GenerativeModel("models/gemini-2.5-flash")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

app = FastAPI()

class Req(BaseModel):
    text: str

@app.post("/chat")
def chat(req: Req):
    try:
        r = model.generate_content(req.text)
        return {"answer": r.text, "is_limit": False}
    except Exception as e:
        # Проверяем на ошибку лимита (Quota Exceeded)
        if "429" in str(e) or "quota" in str(e).lower():
            return {
                "answer": "⚠️ Лимит запросов исчерпан. Пожалуйста, подождите немного.", 
                "is_limit": True
            }
        return {"answer": f"Ошибка: {str(e)}", "is_limit": False}

# отдаём index.html
app.mount("/", StaticFiles(directory=".", html=True), name="static")

