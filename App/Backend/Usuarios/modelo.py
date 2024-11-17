from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    __tablename__ = "Usuario"

    Id_usuario = Column(Integer, primary_key=True, index=True)
    Primer_nombre = Column(String(50), nullable=False)
    Segundo_nombre = Column(String(50), nullable=True)
    Primer_apellido = Column(String(50), nullable=False)
    Segundo_apellido = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False, unique=True)
    Contraseña = Column(String(255), nullable=False)
    Posicion = Column(String(255), nullable=False)
    Telefono = Column(Integer, nullable=False)




