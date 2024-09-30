
FROM python:3.11


WORKDIR /PROYECT-HJ-COPIA


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del proyecto a la imagen de Docker
COPY . .

# Exponer el puerto donde correrá la API
EXPOSE 8000

# Comando para correr la aplicación con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
