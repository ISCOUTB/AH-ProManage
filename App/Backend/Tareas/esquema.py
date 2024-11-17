from pydantic import BaseModel
from datetime import date
from typing import Optional

class TareaEsquema(BaseModel):
    Id_tarea: Optional[int]
    Nombre: str
    Descripcion: str
    Fecha_vencimiento: date
    Id_proyecto: int
    Id_estado: int


    class Config:
        from_attributes = True

class ActualizarTarea(BaseModel):
    Nombre: str | None = None
    Descripcion: str | None = None
    Fecha_vencimiento: date | None = None
    Id_estado: int | None = None
    
class TareaCreacion(BaseModel):
    Nombre: str
    Descripcion: str
    Fecha_vencimiento: date
    Id_estado: int
    class Config:
        from_attributes = True


