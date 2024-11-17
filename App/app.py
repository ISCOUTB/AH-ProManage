from fastapi import FastAPI, Request
from Backend.Usuarios import user
from Backend.Tareas import Tarea
from Backend.Proyectos import proyecto
from Backend.Auth import autenticacion
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from Backend.Auth.auth import verify_session_cookie
import uvicorn

templates = Jinja2Templates(directory="Frontend")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(BaseHTTPMiddleware, dispatch=verify_session_cookie)

#routers
app.include_router(user.router,prefix="/usuario",tags=["Usuario"])
app.include_router(Tarea.router,tags=["Tareas"])
app.include_router(proyecto.router,tags=["Proyecto"])
app.include_router(autenticacion.router,tags=["Autenticacion"])

@app.get("/")
async def home(request: Request):  
    return templates.TemplateResponse("home.html", {"request": request})

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8022)