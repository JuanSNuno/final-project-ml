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

# Copiar los datos procesados para el monitoreo de drift
COPY mlops_pipeline/data/ /app/data/

# Copiar los scripts de despliegue (desde mlops_pipeline/src/scripts/)
COPY mlops_pipeline/src/scripts/model_deploy.py /app/model_deploy.py
COPY mlops_pipeline/src/scripts/prediction_ui.py /app/prediction_ui.py
COPY mlops_pipeline/src/scripts/streamlit_app.py /app/streamlit_app.py

# Copiar utilities si existen
COPY mlops_pipeline/src/utilities.py /app/utilities.py

# Copiar configuración
COPY config.json /app/config.json

# Crear directorios necesarios para datos y monitoreo
RUN mkdir -p /app/monitoring_results && \
    mkdir -p /app/data/processed && \
    mkdir -p /app/artifacts

# Exponer puertos
# 8000 para la API FastAPI
# 8501 para Streamlit UI de Predicción
# 8502 para Streamlit UI de Reporte de Drift
EXPOSE 8000 8501 8502

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# Crear script de inicio que inicia los tres servicios
RUN echo '#!/bin/bash\n\
echo "╔════════════════════════════════════════════════════════════════╗"\n\
echo "║  🧠 ALZHEIMER PREDICTION SYSTEM - INICIANDO SERVICIOS         ║"\n\
echo "╚════════════════════════════════════════════════════════════════╝"\n\
echo ""\n\
echo "▶️  API FastAPI disponible en:"\n\
echo "    📍 http://localhost:8000"\n\
echo "    📖 Documentación: http://localhost:8000/docs"\n\
echo ""\n\
echo "▶️  UI Predicción (Streamlit) disponible en:"\n\
echo "    📍 http://localhost:8501"\n\
echo "    💡 Realiza predicciones sobre Alzheimer"\n\
echo ""\n\
echo "▶️  UI Reporte Drift (Streamlit) disponible en:"\n\
echo "    📍 http://localhost:8502"\n\
echo "    📊 Monitorea data drift y cambios en los datos"\n\
echo ""\n\
echo "Iniciando servicios..."\n\
echo ""\n\
# Iniciar FastAPI en background\n\
python /app/model_deploy.py &\n\
API_PID=$!\n\
echo "✅ API FastAPI iniciada (PID: $API_PID)"\n\
sleep 3\n\
# Iniciar Streamlit UI de Predicción en background\n\
streamlit run /app/prediction_ui.py --server.port 8501 --server.address 0.0.0.0 &\n\
UI_PID=$!\n\
echo "✅ Streamlit UI (Predicción) iniciada (PID: $UI_PID)"\n\
sleep 3\n\
# Iniciar Streamlit UI de Reporte de Drift en foreground\n\
echo "✅ Streamlit UI (Drift Report) iniciando..."\n\
streamlit run /app/streamlit_app.py --server.port 8502 --server.address 0.0.0.0\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Comando para iniciar ambas aplicaciones
ENTRYPOINT ["/app/entrypoint.sh"]
