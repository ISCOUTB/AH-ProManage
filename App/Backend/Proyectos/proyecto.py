from fastapi import APIRouter, HTTPException, Request
from .esquema import ProyectoEsquema, ActualizarProyecto,crear_proyecto
from .repositorio import ProyectoRepo
from Backend.Tareas.repositorio import TareaRepo
from Backend.Usuarios.repositorio import UsuarioRepo
from Backend.Auth.auth import get_current_user
from fastapi.templating import Jinja2Templates
from typing import List
from fastapi import APIRouter,  HTTPException


router = APIRouter()
templates = Jinja2Templates(directory="Frontend")


@router.get("/proyectos/{id_proyecto}")
async def informacion_proyecto(request: Request, id_proyecto: int):

    current_user = get_current_user(request)
    user_id = current_user.get("user_id")  
    proyecto_repo = ProyectoRepo()
    tarea_repo = TareaRepo()

    try:
       
        proyecto = proyecto_repo.obtener_proyecto_id(id_proyecto, user_id)
       
        
    
        tareas = tarea_repo.obtener_tareas(id_proyecto)
     
        
       
        return templates.TemplateResponse("proyecto.html", {
            "request": request,
            "proyecto": proyecto,
            "tareas": tareas
        })
    except ValueError as e:
        print(f"Error: {str(e)}")  
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        print(f"Error inesperado: {str(e)}")  
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/proyectos", response_model=List[ProyectoEsquema])  
async def obtener_proyectos(request: Request):
    current_user = get_current_user(request)
    user_id = current_user.get("user_id")  

   
    repo_proyecto = ProyectoRepo()
    proyectos = repo_proyecto.obtener_proyectos_por_usuario(user_id)  

    if not proyectos:
        raise HTTPException(status_code=404, detail="No se encontraron proyectos para este usuario")

    return proyectos  


@router.patch("/proyectos/{id_proyecto}", response_model=ProyectoEsquema)
async def modificar_proyecto(
    id_proyecto: int, 
    proyecto: ActualizarProyecto, 
    request: Request,
    user_id: int
):
    current_user = get_current_user(request)
    Usuario = current_user.get("user_id") 

    repo = ProyectoRepo()
    try:
     
        proyecto_actualizado = repo.actualizar_proyecto(id_proyecto, proyecto, user_id)
        return proyecto_actualizado
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/proyectos", response_model=ProyectoEsquema)
async def crear_proyecto(proyecto: crear_proyecto, request: Request):
    current_user = get_current_user(request)
    user_id = current_user.get("user_id")

 
    repo_proyecto = ProyectoRepo()
    try:
        proyecto_creado = repo_proyecto.crear_proyecto(proyecto, user_id)
        return proyecto_creado
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/proyectos/{id_proyecto}")
async def eliminar_proyecto(request: Request, id_proyecto: int):
    
    current_user = get_current_user(request)
    user_id = current_user.get("user_id")

    repo = ProyectoRepo()
    try:
      
        mensaje = repo.eliminar_proyecto(id_proyecto, user_id)
        return {"message": mensaje}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))





