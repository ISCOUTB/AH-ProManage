from pydantic import BaseModel

class EstadoEsquema(BaseModel):
    Id: int
    Nombre: str

    class Config:
        orm_mode = True
