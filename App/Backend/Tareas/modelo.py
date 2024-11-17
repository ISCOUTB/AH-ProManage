from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class Tarea(Base):
    __tablename__ = 'Tarea'
    
    Id_tarea = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String, index=True)
    Descripcion = Column(String)
    Fecha_vencimiento = Column(String)
    Id_estado = Column(Integer)
    Id_proyecto = Column(Integer, ForeignKey('Proyecto.Id_proyecto'))  
    



