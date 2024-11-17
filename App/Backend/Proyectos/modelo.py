from sqlalchemy import Column, Integer, String, Date
from database import Base

class Proyecto(Base):
    __tablename__ = "Proyecto"
    Id_proyecto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(String(250), nullable=False)
    Fecha_inicio = Column(Date, nullable=False)
    Fecha_final = Column(Date, nullable=False)
    Id_estado = Column(Integer, nullable=False)
    Id_usuario = Column(Integer, nullable=False)


