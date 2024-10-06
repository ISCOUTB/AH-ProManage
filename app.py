from fastapi import FastAPI 
import uvicorn 
from Backend import user, tarea_asig, proyecto, proy_asig, Tarea, Estado



app = FastAPI()

#routers
app.include_router(user.router,prefix="/Usuario",tags=["Usuario"])
app.include_router(tarea_asig.router, prefix="/Tarea_asig",tags=["Asignacion de tareas"])
app.include_router(Tarea.router, prefix="/Tareas",tags=["Tareas"] )
app.include_router(proy_asig.router, prefix="/Proyecto_asig",tags=["Asignacion de proyectos"])
app.include_router(proyecto.router, prefix="/Proyectos", tags=["Proyectos"])
app.include_router(Estado.router, prefix="/Estados", tags=["Estados"])



@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)