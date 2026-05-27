#paquetes: fastapi, uvicorn, sqlalchemy, psycopg2-binary, geoalchemy2, shapely
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from geoalchemy2.shape import from_shape
from shapely import wkt
import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Bienvenida
@app.get("/")
def saludar():
    return "Hola, bienvenido a la API de Papaap"

# ✅ Test conexión DB
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "estado": "✅ Conectado",
            "base_de_datos": "papaapp_db",
            "mensaje": "Conexión a PostgreSQL exitosa"
        }
    except Exception as e:
        return {"estado": "❌ Error", "detalle": str(e)}

# ✅ Formulario de ejemplo
@app.get("/crear_agricultor")
def formulario_agricultor():
    return {
        "instrucciones": "Envía un POST a /crear_agricultor con el siguiente formato JSON",
        "ejemplo": {
            "cedula": "1234567890",
            "nombre": "Carlos Pérez",
            "area": 5.50,
            "cultivo": "Papa",
            "inversion": 3500000.00,
            "fecha": "2024-03-15",
            "ubicacion_cultivo": "POLYGON((-74.0 4.7, -74.1 4.7, -74.1 4.8, -74.0 4.8, -74.0 4.7))"
        }
    }

# ✅ Crear un agricultor
@app.post("/crear_agricultor", response_model=schemas.AgricultorResponse)
def crear_agricultor(agricultor: schemas.AgricultorCreate, db: Session = Depends(get_db)):
    if db.query(models.Agricultor).filter(models.Agricultor.cedula == agricultor.cedula).first():
        raise HTTPException(status_code=400, detail="Ya existe un agricultor con esa cédula")

    datos = agricultor.model_dump()
    if datos.get("ubicacion_cultivo"):
        datos["ubicacion_cultivo"] = from_shape(wkt.loads(datos["ubicacion_cultivo"]), srid=4326)

    nuevo = models.Agricultor(**datos)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# ✅ Cargar lista de agricultores desde JSON
@app.post("/cargar_agricultores", response_model=List[schemas.AgricultorResponse])
def cargar_agricultores(datos: schemas.AgricultoresLista, db: Session = Depends(get_db)):
    guardados = []
    for a in datos.agricultores:
        if db.query(models.Agricultor).filter(models.Agricultor.cedula == a.cedula).first():
            continue

        d = a.model_dump()
        if d.get("ubicacion_cultivo"):
            d["ubicacion_cultivo"] = from_shape(wkt.loads(d["ubicacion_cultivo"]), srid=4326)

        nuevo = models.Agricultor(**d)
        db.add(nuevo)
        guardados.append(nuevo)

    db.commit()
    for g in guardados:
        db.refresh(g)
    return guardados

# ✅ Listar todos los agricultores
@app.get("/agricultores", response_model=List[schemas.AgricultorResponse])
def listar_agricultores(db: Session = Depends(get_db)):
    return db.query(models.Agricultor).all()