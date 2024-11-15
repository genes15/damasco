# Define la imagen base
FROM python:3.11

# Establece el directorio de trabajo en el directorio raíz del proyecto (fuera de /app)
WORKDIR /damasco

# Copia el contenido de `project` en el directorio de trabajo en el contenedor
COPY . /damasco

# Instala las dependencias
RUN pip install -r app/requirements.txt

# Comando de inicio para el servidor de FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
