#paquetes: fastapi, uvicorn 
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def saludar():
    return "Hola, bienvenido a la API de Papaap"




@app.get("/crear_agricultor")
def crear_agricultor():
    return "Cambiar esto por la funcionalidad"


