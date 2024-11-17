from pydantic import BaseModel, EmailStr

class Usuario_esq(BaseModel):
    Id_usuario: int
    Primer_nombre: str
    Segundo_nombre: str | None = None
    Primer_apellido: str
    Segundo_apellido: str
    Email: EmailStr
    Contraseña: str
    Posicion: str
    Telefono: int

    class Config:
        from_attributes = True
        
class Actualizar_usuario(BaseModel):
        Primer_nombre: str | None = None
        Segundo_nombre: str | None = None
        Primer_apellido: str | None = None
        Segundo_apellido: str | None = None
        Email: EmailStr | None = None
        Contraseña: str | None = None
        Posicion: str | None = None
        Telefono: int | None = None