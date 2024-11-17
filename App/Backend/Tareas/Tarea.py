from fastapi import APIRouter, HTTPException, Depends, Request
from .esquema import TareaCreacion, ActualizarTarea,TareaEsquema
from .repositorio import TareaRepo
from fastapi.templating import Jinja2Templates
from Backend.Auth.auth import get_current_user


router = APIRouter()

templates = Jinja2Templates(directory="Frontend")


@router.get("/proyectos/{id_proyecto}/tareas")
async def obtener_tareas_proyecto(request: Request, id_proyecto: int, id_estado: int = None):
    repo = TareaRepo()
    try:
       
   
        tareas = repo.obtener_tareas(id_proyecto=id_proyecto, id_estado=id_estado)

        if not tareas:
            raise HTTPException(status_code=404, detail="No se encontraron tareas para el proyecto especificado.")

       
        return templates.TemplateResponse("kaban.html", {
            "request": request,
            "tareas": tareas
        })
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/proyectos/{id_proyecto}/crear", response_model=TareaEsquema)
async def crear_tarea(tarea: TareaCreacion, id_proyecto: int, request: Request):
    
    repo_tarea = TareaRepo()
    try:
        
        tarea_creada = repo_tarea.crear_tarea(tarea=tarea, id_proyecto=id_proyecto)
        return tarea_creada
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/proyectos/{id_proyecto}/tareas/{id_tarea}")
async def actualizar_tarea(
    id_proyecto: int,
    id_tarea: int,
    tarea: ActualizarTarea,
    current_user: dict = Depends(get_current_user)
):
    repo = TareaRepo()
    user_id = current_user.get("user_id")  
    try:
       
        tarea_actualizada = repo.actualizar_tarea(user_id=user_id, id_proyecto=id_proyecto, id_tarea=id_tarea, tarea=tarea)
        return tarea_actualizada
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/proyectos/{id_proyecto}/tareas/{id_tarea}")
async def eliminar_tarea(
    id_proyecto: int,
    id_tarea: int,
    current_user: dict = Depends(get_current_user)
):
    repo = TareaRepo()
    user_id = current_user.get("user_id")  # Obtén el ID del usuario autenticado
    try:
       
        mensaje = repo.eliminar_tarea(user_id=user_id, id_proyecto=id_proyecto, id_tarea=id_tarea)
        return {"message": mensaje}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))