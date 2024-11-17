from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .modelo import Usuario
from .esquema import Usuario_esq, Actualizar_usuario
from .modelo import Usuario
from database import SessionLocal


class UsuarioRepo:
    
    def obtener_usuario_id(self, id_usuario: int) -> Usuario_esq:
     try:
        with SessionLocal() as session:
            usuario = session.query(Usuario).filter(Usuario.Id_usuario == id_usuario).first()
            if not usuario:
                raise ValueError("Usuario no encontrado")
            return Usuario_esq.from_orm(usuario)
     except SQLAlchemyError as e:
        raise RuntimeError(f"Error al buscar el usuario: {e}")

    
    
    def eliminar_usuario(self, id_usuario: int, user_id: int) -> str:
     try:
        with SessionLocal() as session:
            usuario_db = session.query(Usuario).filter(Usuario.Id_usuario == id_usuario).first()
            if not usuario_db:
                raise ValueError("Usuario no encontrado para eliminar")


            if usuario_db.Id_usuario != user_id:
                raise ValueError("No tienes permiso para eliminar este usuario")

            session.delete(usuario_db)
            session.commit()
            return "Usuario eliminado correctamente"
     except SQLAlchemyError as e:
        raise RuntimeError(f"Error al eliminar el usuario: {e}")


    def actualizar_usuario(self, id_usuario: int, usuario: Actualizar_usuario, user_id: int) -> Usuario_esq:
      try:
        with SessionLocal() as session:
            usuario_db = session.query(Usuario).filter(Usuario.Id_usuario == id_usuario).first()
            if not usuario_db:
                raise ValueError("Usuario no encontrado para actualizar")

           
            if usuario_db.Id_usuario != user_id:
                raise ValueError("No tienes permiso para modificar este usuario")

           
            for key, value in usuario.dict(exclude_unset=True).items():
                if value is not None:
                    setattr(usuario_db, key, value)
            
            session.commit()
            session.refresh(usuario_db)
            return Usuario_esq.from_orm(usuario_db)
      except SQLAlchemyError as e:
        raise RuntimeError(f"Error al actualizar el usuario: {e}")

    def obtener_usuario_email(self, email: str) -> Usuario_esq:
     try:
        with SessionLocal() as session:
            usuario = session.query(Usuario).filter(Usuario.Email == email).first()
            if not usuario:
                raise ValueError("Usuario no encontrado")
            return Usuario_esq.from_orm(usuario)
     except SQLAlchemyError as e:
        raise RuntimeError(f"Error al buscar el usuario: {e}") from e


    def crear_usuario(self, usuario: Usuario_esq) -> Usuario_esq:
       try:
        with SessionLocal() as session:
          
            existing_user = session.query(Usuario).filter(Usuario.Email == usuario.Email).first()
            if existing_user:
                raise ValueError("El correo electrónico ya está en uso.")

           
            nuevo_usuario = Usuario(**usuario.dict())
            session.add(nuevo_usuario)
            session.commit()
            session.refresh(nuevo_usuario)
            return Usuario_esq.from_orm(nuevo_usuario)
       except IntegrityError as e:
        raise RuntimeError("Error de integridad al crear el usuario. Es posible que el email ya esté en uso.") from e
       except SQLAlchemyError as e:
        raise RuntimeError(f"Error al crear el usuario: {e}") from e




