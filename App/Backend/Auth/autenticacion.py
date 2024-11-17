from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from .auth import create_access_token, hash_password, verify_password, get_current_user
from ..Usuarios.esquema import Usuario_esq
from ..Usuarios.repositorio import UsuarioRepo
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="Frontend")

# Ruta para la página de login
@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Ruta para la página de registro
@router.get("/registro")
async def registro_page(request: Request):
    return templates.TemplateResponse("registrarse.html", {"request": request})

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    repo = UsuarioRepo()
    try:
        usuario = repo.obtener_usuario_email(form_data.username)
        
        if not verify_password(form_data.password, usuario.Contraseña):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        # Crear el token de acceso
        access_token = create_access_token(data={"sub": usuario.Email, "Id_usuario": usuario.Id_usuario})

        
        # Establecer el token en una cookie segura
        response = RedirectResponse(url="/Bienvenido", status_code=303)
        response.set_cookie(
            key="access_token", value=f"Bearer {access_token}", httponly=True, secure=True, max_age=1800, samesite="lax"
        )
        return response
    
    except ValueError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/registro")
async def register(
    Primer_nombre: str = Form(...),
    Segundo_nombre: str = Form(''),
    Primer_apellido: str = Form(...),
    Segundo_apellido: str = Form(...),
    Email: str = Form(...),
    Contraseña: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
    
        usuario = Usuario_esq(
            Primer_nombre=Primer_nombre,
            Segundo_nombre=Segundo_nombre,
            Primer_apellido=Primer_apellido,
            Segundo_apellido=Segundo_apellido,
            Email=Email,
            Contraseña=hash_password(Contraseña)  
        )

        repo = UsuarioRepo()
        
        
        if repo.obtener_usuario_email(Email):
            raise HTTPException(status_code=400, detail="El usuario ya existe")

       
        nuevo_usuario = repo.crear_usuario(usuario)

        
        return RedirectResponse(url="/login", status_code=303)
    
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/Bienvenido", response_class=HTMLResponse)
async def bienvenido(request: Request, current_user: dict = Depends(get_current_user)):
  
    user_id = current_user.get("user_id")
    
    
    repo = UsuarioRepo()
    try:
        usuario = repo.obtener_usuario_id(user_id)  
    except ValueError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
   
    return templates.TemplateResponse("dasboard.html", {"request": request, "usuario": usuario})

@router.get("/logout")
async def logout():
    """
    Endpoint para cerrar la sesión del usuario.
    Elimina la cookie del token de acceso.
    """
    response = RedirectResponse(url="/", status_code=303)  
    response.delete_cookie(key="access_token")  
    return response
