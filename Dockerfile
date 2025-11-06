# Dockerfile para el despliegue de la API de predicción
# Imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los artefactos necesarios
COPY artifacts/ ./artifacts/
COPY mlops_pipeline/src/model_deploy.py ./mlops_pipeline/src/

# Copiar configuración si existe
COPY config.json ./config.json 2>/dev/null || true

# Exponer el puerto 8000 para la API
EXPOSE 8000

# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Comando para iniciar la aplicación
CMD ["python", "mlops_pipeline/src/model_deploy.py"]
