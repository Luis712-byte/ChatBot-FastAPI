# Chatbot de IA con Aprendizaje Automático

Este proyecto es un **chatbot** simple que utiliza almacenamiento en un archivo JSON para aprender nuevas respuestas basadas en las preguntas que los usuarios hacen. El chatbot está construido con **FastAPI** para la API y utiliza un modelo de pregunta-respuesta basado en un archivo JSON.

## Descripción

El chatbot permite al usuario hacer preguntas, y si la pregunta ya ha sido respondida anteriormente, el chatbot devolverá la respuesta almacenada. Si el chatbot no conoce la respuesta, pedirá al usuario que proporcione una, y la almacenará para futuras interacciones.

## Tecnologías

- **Python**: Lenguaje de programación principal.
- **FastAPI**: Framework para crear la API REST.
- **Pydantic**: Para la validación de datos en las solicitudes de la API.
- **JSON**: Para almacenar las preguntas y respuestas en un archivo.

## Requisitos

1. Python 3.x
2. Instalar las dependencias desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
