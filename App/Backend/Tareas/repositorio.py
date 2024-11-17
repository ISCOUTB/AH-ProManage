from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .modelo import Tarea
from .esquema import TareaEsquema, ActualizarTarea, TareaCreacion
from database import SessionLocal
from Backend.Proyectos.modelo import Proyecto

class TareaRepo:
    def obtener_tareas(self, id_proyecto: int = None, id_estado: int = None) -> list[TareaEsquema]:
     
      try:
        with SessionLocal() as session:
            query = session.query(Tarea)
            if id_proyecto is not None:
                query = query.filter(Tarea.Id_proyecto == id_proyecto)
            if id_estado is not None:
                query = query.filter(Tarea.Id_estado == id_estado)
                
            tareas = query.all()
            return [TareaEsquema.from_orm(tarea) for tarea in tareas]
      except SQLAlchemyError as e:
        raise RuntimeError(f"Error al obtener las tareas: {e}")
   
    def crear_tarea(self, tarea: TareaCreacion, id_proyecto: int) -> TareaEsquema:
    
     try:
        with SessionLocal() as session:
           
            nueva_tarea = Tarea(**tarea.dict(), Id_proyecto=id_proyecto)  # Usamos solo Id_proyecto

            session.add(nueva_tarea)
            session.commit()
            session.refresh(nueva_tarea)

       
            return TareaEsquema.from_orm(nueva_tarea)
     except SQLAlchemyError as e:
        raise RuntimeError(f"Error al crear la tarea: {e}")

        
    def actualizar_tarea(self, user_id: int, id_proyecto: int, id_tarea: int, tarea: ActualizarTarea) -> TareaEsquema:
    
     try:
        with SessionLocal() as session:
           
            tarea_db = session.query(Tarea).join(Proyecto).filter(
                Tarea.Id_tarea == id_tarea,
                Proyecto.Id_proyecto== id_proyecto,
                Proyecto.Id_usuario == user_id
            ).first()

            if not tarea_db:
                raise ValueError("La tarea no pertenece al proyecto o al usuario.")

            
            for key, value in tarea.dict(exclude_unset=True).items():
                if value is not None:
                    setattr(tarea_db, key, value)
            
            session.commit()
            session.refresh(tarea_db)
            return TareaEsquema.from_orm(tarea_db)
     except SQLAlchemyError as e:
        raise RuntimeError(f"Error al actualizar la tarea: {e}")


  
    def eliminar_tarea(self, user_id: int, id_proyecto: int, id_tarea: int) -> str:
    
     try:
        with SessionLocal() as session:
            
            tarea = session.query(Tarea).join(Proyecto).filter(
                Tarea.Id_tarea == id_tarea,
                Proyecto.Id_proyecto == id_proyecto,
                Proyecto.Id_usuario == user_id
            ).first()

            if not tarea:
                raise ValueError("La tarea no pertenece al proyecto o al usuario.")

            session.delete(tarea)
            session.commit()
            return "Tarea eliminada exitosamente"
     except SQLAlchemyError as e:
        raise RuntimeError(f"Error al eliminar la tarea: {e}")




    