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
    r = model.generate_content(req.text)
    return {"answer": r.text}

# отдаём index.html
app.mount("/", StaticFiles(directory=".", html=True), name="static")
