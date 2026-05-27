from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class AgricultorCreate(BaseModel):
    cedula: str
    nombre: str
    area: float
    cultivo: str
    inversion: float
    fecha: date
    ubicacion_cultivo: Optional[str] = None

class AgricultorResponse(BaseModel):
    id: int
    cedula: str
    nombre: str
    area: float
    cultivo: str
    inversion: float
    fecha: date

    class Config:
        from_attributes = True

class AgricultoresLista(BaseModel):
    agricultores: List[AgricultorCreate]