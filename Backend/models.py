from sqlalchemy import Column, Integer, String, Numeric, Date
from geoalchemy2 import Geometry
from database import Base

class Agricultor(Base):
    __tablename__ = "agricultor"

    id                = Column(Integer, primary_key=True, index=True)
    cedula            = Column(String(20), nullable=False, unique=True)
    nombre            = Column(String(150), nullable=False)
    area              = Column(Numeric(10, 2), nullable=False)
    cultivo           = Column(String(100), nullable=False)
    inversion         = Column(Numeric(12, 2), nullable=False)
    fecha             = Column(Date, nullable=False)
    ubicacion_cultivo = Column(Geometry("POLYGON", srid=4326), nullable=True)