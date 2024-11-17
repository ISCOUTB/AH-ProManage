from fastapi import APIRouter, HTTPException,Depends, Request
from .esquema import Actualizar_usuario
from .repositorio import UsuarioRepo
from Backend.Auth.auth import get_current_user


router = APIRouter()


@router.get("/{id_usuario}")
async def obtener_usuario(
    id_usuario: int,
    current_user: dict = Depends(get_current_user)  
):
    repo = UsuarioRepo()
    user_id = current_user.get("user_id")  
    try:
        
        if user_id != id_usuario:
            raise HTTPException(
                status_code=403, detail="No tienes permiso para acceder a este usuario."
            )
        
        usuario = repo.obtener_usuario_id(id_usuario)
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id_usuario}")
async def modificar_usuario(
    id_usuario: int,
    usuario: Actualizar_usuario,
    current_user: dict = Depends(get_current_user)  
):
    repo = UsuarioRepo()
    user_id = current_user.get("user_id")
    try:
       
        if user_id != id_usuario:
            raise HTTPException(
                status_code=403, detail="No tienes permiso para modificar este usuario."
            )
        
        usuario_actualizado = repo.actualizar_usuario(id_usuario, usuario)
        return usuario_actualizado
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id_usuario}")
async def eliminar_usuario(
    id_usuario: int,
    current_user: dict = Depends(get_current_user)  
):
    repo = UsuarioRepo()
    user_id = current_user.get("user_id")  
    try:
       
        if user_id != id_usuario:
            raise HTTPException(
                status_code=403, detail="No tienes permiso para eliminar este usuario."
            )
        
        mensaje = repo.eliminar_usuario(id_usuario)
        return {"message": mensaje}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
