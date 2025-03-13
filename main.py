import json
import os
import re
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

DATA_FILE = "data/chatbot_data.json"

if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        pares = json.load(file)
else:
    pares = {}

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Question(BaseModel):
    pregunta: str
    respuesta: str = None

def normalizar_pregunta(pregunta):
    pregunta = re.sub(r'[^\w\s]', '', pregunta.lower().strip())
    pregunta = re.sub(r'[áàäâ]', 'a', pregunta)
    pregunta = re.sub(r'[éèëê]', 'e', pregunta)
    pregunta = re.sub(r'[íìïî]', 'i', pregunta)
    pregunta = re.sub(r'[óòöô]', 'o', pregunta)
    pregunta = re.sub(r'[úùüû]', 'u', pregunta)
    return pregunta

def obtener_respuesta(pregunta):
    pregunta_normalizada = normalizar_pregunta(pregunta)
    if pregunta_normalizada in pares:
        return pares[pregunta_normalizada]
    else:
        return None

def guardar_respuesta(pregunta, respuesta):
    pregunta_normalizada = normalizar_pregunta(pregunta)
    pares[pregunta_normalizada] = respuesta
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(pares, file, indent=4, ensure_ascii=False)

@app.post("/preguntar")
async def preguntar(question: Question):
    respuesta = obtener_respuesta(question.pregunta)
    if respuesta:
        return {"respuesta": respuesta}
    else:
        if question.respuesta:
            guardar_respuesta(question.pregunta, question.respuesta)
            return {"respuesta": f"Gracias, ahora sé la respuesta a esa pregunta: {question.respuesta}"}
        else:
            return {"respuesta": "No sé la respuesta a esa pregunta. ¿Cómo debería responder?"}

@app.get("/pares")
async def obtener_pares():
    return pares

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat/")
async def chat(message: str):
    respuesta = obtener_respuesta(message)
    if respuesta:
        return {"respuesta": respuesta}
    else:
        return {"respuesta": "No sé la respuesta a esa pregunta. ¿Cómo debería responder?"}

@app.post("/aprender/")
async def aprender(question: Question):
    if question.pregunta and question.respuesta:
        guardar_respuesta(question.pregunta, question.respuesta)
        return {"mensaje": f"Gracias, ahora sé la respuesta a esa pregunta: {question.respuesta}"}
    else:
        raise HTTPException(status_code=400, detail="Faltan campos en el cuerpo de la petición")
