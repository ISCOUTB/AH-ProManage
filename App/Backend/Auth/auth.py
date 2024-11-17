from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import Response
from starlette.requests import Request
from Backend.Usuarios.modelo import Usuario
from database import SessionLocal

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, existing_token: str = None, expires_delta: timedelta | None = None):
   
    if existing_token:
        try:
            
            decoded_data = jwt.decode(existing_token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
            if "exp" in decoded_data and datetime.utcnow() > datetime.fromtimestamp(decoded_data["exp"]):
                print("El token existente ha expirado, generando uno nuevo.")
              
                return generate_new_token(data, expires_delta)
        except Exception as e:  
            print(f"Error al decodificar el token: {str(e)}")
           
            return generate_new_token(data, expires_delta)

    
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(days=10))
    data.update({"exp": expire.timestamp()})  
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_new_token(data: dict, expires_delta: timedelta | None):

    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(days=10))
    data.update({"exp": expire.timestamp()})  
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_session_cookie(request: Request, call_next):
    if request.url.path in ["/login", "/", "/registro","/imagenes", "/favicon.ico"]: 
        return await call_next(request)
    
    token = request.cookies.get("access_token")
    if not token:
        return Response("No autorizado", status_code=401)
    
    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user = payload.get("sub")
        
    except Exception as e:  
        print(f"Error al verificar el token: {str(e)}")
        return Response("Token inválido o expirado", status_code=401)
    
    return await call_next(request)

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    
    try:
       
        token = token.split(" ")[1] if token.startswith("Bearer ") else token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id = payload.get("Id_usuario")  
        email = payload.get("sub")  
       
        
        return {"user_id": user_id, "email": email}
    
    except Exception as e: 
        print(f"Error al verificar el token: {str(e)}")
        raise HTTPException(status_code=401, detail="Token is invalid or expired")




