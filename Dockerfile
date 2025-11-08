# Dockerfile para el despliegue de la API y UI de predicción
# Imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los artefactos necesarios (desde mlops_pipeline/artifacts/)
COPY mlops_pipeline/artifacts/ /app/artifacts/

# Copiar los scripts de despliegue (desde mlops_pipeline/src/scripts/)
COPY mlops_pipeline/src/scripts/model_deploy.py /app/model_deploy.py
COPY mlops_pipeline/src/scripts/prediction_ui.py /app/prediction_ui.py

# Copiar configuración
COPY config.json /app/config.json

# Crear directorio para monitoring results
RUN mkdir -p /app/monitoring_results

# Exponer puertos
# 8000 para la API FastAPI
# 8501 para Streamlit
EXPOSE 8000 8501

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# Crear script de inicio que inicia ambos servicios
RUN echo '#!/bin/bash\n\
echo "🚀 Iniciando Servicios..."\n\
echo ""\n\
echo "▶️  FastAPI en http://localhost:8000"\n\
echo "▶️  Streamlit en http://localhost:8501"\n\
echo ""\n\
# Iniciar FastAPI en background\n\
python /app/model_deploy.py &\n\
sleep 3\n\
# Iniciar Streamlit en foreground\n\
streamlit run /app/prediction_ui.py\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Comando para iniciar ambas aplicaciones
ENTRYPOINT ["/app/entrypoint.sh"]
