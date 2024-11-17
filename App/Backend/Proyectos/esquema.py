from pydantic import BaseModel
from datetime import date

class ProyectoEsquema(BaseModel):
    Id_proyecto: int
    Nombre: str
    Descripcion: str
    Fecha_inicio: date
    Fecha_final: date
    Id_estado: int
    Id_usuario: int

    class Config:
        from_attributes = True 

class ActualizarProyecto(BaseModel):
    Nombre: str | None = None
    Descripcion: str | None = None
    Fecha_inicio: date | None = None
    Fecha_final: date | None = None
    Id_estado: int | None = None
    
 
class crear_proyecto(BaseModel):
    Nombre: str
    Descripcion: str
    Fecha_inicio: date
    Fecha_final: date
    Id_estado: int
   
       
    