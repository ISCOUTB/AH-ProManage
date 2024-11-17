from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .modelo import Proyecto  
from .esquema import ProyectoEsquema, ActualizarProyecto, crear_proyecto
from Backend.Usuarios.modelo import Usuario
from Backend.Tareas.repositorio import TareaRepo 
from database import SessionLocal

class ProyectoRepo:
   def obtener_proyectos_por_usuario(self, user_id: int) -> list[ProyectoEsquema]:
    try:
        with SessionLocal() as session:
           
            usuario = session.query(Usuario).filter(Usuario.Id_usuario == user_id).first()
            print(f"User ID para la consulta: {user_id}")
            if not usuario:
                raise ValueError("Usuario no encontrado")
            
           
            proyectos = session.query(Proyecto).filter(Proyecto.Id_usuario == usuario.Id_usuario).all()
            return [ProyectoEsquema.from_orm(proyecto) for proyecto in proyectos]
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error al obtener los proyectos: {e}")



   def obtener_proyecto_id(self, id_proyecto: int, user_id: int) -> ProyectoEsquema:
       
        try:
            with SessionLocal() as session:
                proyecto = session.query(Proyecto).filter(
                    Proyecto.Id_proyecto == id_proyecto,
                    Proyecto.Id_usuario == user_id
                ).first()
                print(f"User ID para la consulta: {user_id}")
                if not proyecto:
                    raise ValueError("Proyecto no encontrado o no pertenece al usuario")
                return ProyectoEsquema.from_orm(proyecto)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al buscar el proyecto: {e}")

   def crear_proyecto(self, proyecto: crear_proyecto, user_id: int) -> ProyectoEsquema:

    try:
        with SessionLocal() as session:
            nuevo_proyecto = Proyecto(**proyecto.dict(), Id_usuario=user_id)
            session.add(nuevo_proyecto)
            session.commit()
            session.refresh(nuevo_proyecto)
            return ProyectoEsquema.from_orm(nuevo_proyecto)
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error al crear el proyecto: {e}")


   def actualizar_proyecto(self, id_proyecto: int, proyecto: ActualizarProyecto, user_id: int) -> ProyectoEsquema:
      
        try:
            with SessionLocal() as session:
                proyecto_db = session.query(Proyecto).filter(
                    Proyecto.Id_proyecto == id_proyecto,
                    Proyecto.Id_usuario == user_id
                ).first()
                if not proyecto_db:
                    raise ValueError("Proyecto no encontrado para actualizar o no pertenece al usuario")

                for key, value in proyecto.dict(exclude_unset=True).items():
                    if value is not None:
                        setattr(proyecto_db, key, value)
                
                session.commit()
                session.refresh(proyecto_db)
                return ProyectoEsquema.from_orm(proyecto_db)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al actualizar el proyecto: {e}")

   def eliminar_proyecto(self, id_proyecto: int, user_id: int) -> str:
      
        try:
            with SessionLocal() as session:
                proyecto = session.query(Proyecto).filter(
                    Proyecto.Id_proyecto == id_proyecto,
                    Proyecto.Id_usuario == user_id
                ).first()
                if not proyecto:
                    raise ValueError("Proyecto no encontrado o no pertenece al usuario")
                session.delete(proyecto)
                session.commit()
                return "Proyecto eliminado exitosamente"
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al eliminar el proyecto: {e}")

   def obtener_proyecto_con_tareas(self, id_proyecto: int, user_id: int) -> dict:
    
        try:
            with SessionLocal() as session:
                proyecto = session.query(Proyecto).filter(
                    Proyecto.Id_proyecto == id_proyecto,
                    Proyecto.Id_usuario == user_id
                ).first()
                if not proyecto:
                    raise ValueError("Proyecto no encontrado o no pertenece al usuario")
                
                tarea_repo = TareaRepo()
                tareas = tarea_repo.obtener_tareas(id_proyecto)

                return {
                    'proyecto': ProyectoEsquema.from_orm(proyecto),
                    'tareas': tareas
                }
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error al obtener el proyecto y sus tareas: {e}")
