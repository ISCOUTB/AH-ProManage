from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .modelo import Estado
from .esquema import EstadoEsquema
from database import SessionLocal

class EstadoRepo:

    def obtener_estados(self) -> list[EstadoEsquema]:
        try:
            with SessionLocal() as session:
                estados = session.query(Estado).all()
                return [EstadoEsquema.from_orm(estado) for estado in estados]
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al obtener los estados: {e}")

    def obtener_estado_id(self, id_estado: int) -> EstadoEsquema:
        try:
            with SessionLocal() as session:
                estado = session.query(Estado).filter(Estado.id_estado == id_estado).first()
                if not estado:
                    raise ValueError("Estado no encontrado")
                return EstadoEsquema.from_orm(estado)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al buscar el estado: {e}")

    def crear_estado(self, estado: EstadoEsquema) -> EstadoEsquema:
        try:
            with SessionLocal() as session:
                nuevo_estado = Estado(**estado.dict())
                session.add(nuevo_estado)
                session.commit()
                session.refresh(nuevo_estado)
                return EstadoEsquema.from_orm(nuevo_estado)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al crear el estado: {e}")
        
    def eliminar_estado(self, id_estado: int) -> str:
        try:
            with SessionLocal() as session:
                estado = session.query(Estado).filter(Estado.id_estado == id_estado).first()
                if not estado:
                    raise ValueError("Estado no encontrado")
                session.delete(estado)
                session.commit()
                return "Estado eliminado exitosamente"
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al eliminar el estado: {e}")
