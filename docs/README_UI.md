# 🧠 Alzheimer Prediction System - MLOps Pipeline Completo

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

**Sistema Profesional de Predicción de Alzheimer con Machine Learning**

[Inicio Rápido](#-inicio-rápido) • 
[Características](#-características) • 
[Documentación](#-documentación) • 
[Docker](#-deployment-con-docker)

</div>

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Inicio Rápido](#-inicio-rápido)
3. [Características](#-características)
4. [Arquitectura](#-arquitectura)
5. [Componentes](#-componentes)
6. [Instalación](#-instalación)
7. [Uso](#-uso)
8. [Deployment con Docker](#-deployment-con-docker)
9. [API Documentation](#-api-documentation)
10. [Monitoreo](#-monitoreo)
11. [Troubleshooting](#-troubleshooting)
12. [Documentación Adicional](#-documentación-adicional)

---

## 📝 Descripción General

Sistema completo de Machine Learning operativo (MLOps) para predecir riesgo de enfermedad de Alzheimer basado en:

- **35 características** médicas, cognitivas y de estilo de vida
- **6 algoritmos** de ML con evaluación automática
- **API REST** profesional con FastAPI
- **UI Profesional** con Streamlit para predicciones
- **Monitoreo de Datos** con detección de drift
- **Containerización** con Docker para fácil deployment

### 🎯 Objetivos Cumplidos

✅ Pipeline secuencial de procesamiento de datos  
✅ Ingeniería de características automática  
✅ Entrenamiento y evaluación de modelos  
✅ Deployment con API REST  
✅ Interfaz gráfica profesional  
✅ Monitoreo de rendimiento y drift  
✅ Docker containerization  
✅ Documentación completa  

---

## ⚡ Inicio Rápido

### Opción 1: Un Solo Comando (Recomendado)

```powershell
python run_full_system.py
```

Esto:
1. ✅ Verifica artefactos
2. ✅ Inicia API (puerto 8000)
3. ✅ Inicia UI Streamlit (puerto 8501)
4. ✅ Abre navegador automáticamente

**Luego accede a:** http://localhost:8501

### Opción 2: Con Docker

```powershell
docker-compose up
```

**Luego accede a:**
- UI: http://localhost:8501
- API: http://localhost:8000

### Opción 3: Manual - 2 Terminales

**Terminal 1:**
```powershell
python mlops_pipeline/src/scripts/model_deploy.py
```

**Terminal 2:**
```powershell
streamlit run mlops_pipeline/src/scripts/prediction_ui.py
```

---

## ✨ Características

### 🎨 Interfaz de Usuario (Prediction UI)

**Predicción Individual:**
- Formulario completo con 35 parámetros
- Organizado por secciones médicas
- Valores por defecto precompletados
- Gauge chart interactivo con probabilidad
- Recomendaciones personalizadas por riesgo
- Clasificación: Alto/Moderado/Bajo riesgo

**Predicción por Lote:**
- Carga plantilla CSV
- Procesa múltiples pacientes
- Descarga resultados
- Estadísticas y gráficos

**Información del Sistema:**
- Estado de API
- Detalles del modelo
- Historial de predicciones
- Estadísticas en tiempo real

### 🚀 API REST (FastAPI)

Endpoints disponibles:

```
GET  /health                    - Estado de la API
GET  /model/info               - Información del modelo
POST /predict                  - Predicción individual
POST /predict/batch            - Predicción por lote
```

Documentación interactiva en: http://localhost:8000/docs

### 📊 Pipeline de Datos

```
Raw Data (.csv)
     ↓
[1] Data Processing (limpieza)
     ↓
[2] Feature Engineering (transformación)
     ↓
[3] Model Training (6 algoritmos)
     ↓
[4] Model Deploy (API REST)
     ↓
[5] Monitoring (drift detection)
     ↓
[6] UI (Streamlit Dashboard)
```

### 📈 Monitoreo de Datos

- **PSI (Population Stability Index):** Detección de cambios en distribución
- **KS Test (Kolmogorov-Smirnov):** Comparación de distribuciones
- **Chi-squared Test:** Análisis de variables categóricas
- **Cramér's V:** Fuerza de asociación

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO FINAL                             │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
┌──────────────────┐          ┌──────────────────┐
│   Streamlit UI   │          │  Browser (API)   │
│   (8501)         │          │  (8000)          │
└─────────┬────────┘          └────────┬─────────┘
          │                            │
          └────────────┬───────────────┘
                       ▼
        ┌──────────────────────────┐
        │   FastAPI Server         │
        │   (model_deploy.py)      │
        │   (8000)                 │
        └─────────────┬────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    ┌──────────────┐       ┌──────────────┐
    │ Preprocessor │       │  Best Model  │
    │ (joblib)     │       │  (joblib)    │
    └──────────────┘       └──────────────┘
```

---

## 📦 Componentes

### Scripts del Pipeline

| Script | Descripción | Entrada | Salida |
|--------|-------------|---------|--------|
| `data_processing.py` | Carga y limpia datos | CSV raw | `cleaned_data.csv` |
| `ft_engineering.py` | Preprocesamiento | `cleaned_data.csv` | `preprocessor.joblib`, datasets |
| `model_training_evaluation.py` | Entrena 6 modelos | Datasets | `best_model.joblib`, métricas |
| `model_deploy.py` | API REST | Artefactos | Predicciones vía HTTP |
| `model_monitoring.py` | Detección de drift | Datos | `drift_report.csv` |
| `streamlit_app.py` | Dashboard de monitoreo | Reportes | Visualizaciones |
| `prediction_ui.py` | Interfaz profesional | API | Predicciones interactivas |

### Archivos de Configuración

- `requirements.txt` - Dependencias Python
- `config.json` - Parámetros de configuración
- `Dockerfile` - Containerización
- `docker-compose.yml` - Orquestación de servicios
- `sonar-project.properties` - Configuración SonarCloud

### Documentación

- `README.md` - Este archivo
- `QUICK_START_UI.md` - Guía de inicio rápido
- `PREDICTION_UI_GUIDE.md` - Manual completo de la UI
- `README_PIPELINE.md` - Documentación del pipeline
- `IMPLEMENTATION_SUMMARY.md` - Resumen de implementación

---

## 🔧 Instalación

### Requisitos Previos

- **Python 3.11+**
- **pip** (gestor de paquetes)
- **Docker** (opcional, para containerización)
- **Docker Compose** (opcional, recomendado)

### Instalación Local

```bash
# 1. Clonar o descargar el proyecto
cd c:\Users\jsanc\OneDrive\Documentos\U\ML\final-project-ml

# 2. Crear ambiente virtual (recomendado)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar instalación
python -c "import streamlit; import fastapi; print('✓ Dependencias OK')"
```

### Verificar Artefactos

```bash
# Debe existir:
ls mlops_pipeline/artifacts/
# - best_model.joblib
# - preprocessor.joblib

# Si no existen, entrena el modelo:
python run_pipeline.py --full
```

---

## 🚀 Uso

### Ejecución Completa del Sistema

**Opción A: Un Comando (Recomendado)**
```powershell
python run_full_system.py
```

**Opción B: Docker Compose (Producción)**
```powershell
docker-compose up
```

**Opción C: Manual - 2 Terminales**

Terminal 1 (API):
```powershell
python mlops_pipeline/src/scripts/model_deploy.py
```

Terminal 2 (UI):
```powershell
streamlit run mlops_pipeline/src/scripts/prediction_ui.py
```

### URLs de Acceso

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Streamlit UI** | http://localhost:8501 | Interfaz principal |
| **API REST** | http://localhost:8000 | Endpoints |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Health Check** | http://localhost:8000/health | Estado |

### Flujo de Usuario

```
1. Abre http://localhost:8501 en navegador
   ↓
2. Selecciona "📋 Predicción Individual"
   ↓
3. Completa datos del paciente (o usa valores por defecto)
   ↓
4. Haz clic en "🔮 Realizar Predicción"
   ↓
5. Obtén resultado:
   - Probabilidad (gauge chart)
   - Nivel de riesgo (Alto/Moderado/Bajo)
   - Recomendaciones personalizadas
   ↓
6. Exporta o continúa
```

### Predicción por Lote

```
1. Ve a "📊 Predicción por Lote"
   ↓
2. Descarga plantilla CSV
   ↓
3. Completa múltiples pacientes en Excel
   ↓
4. Sube el archivo
   ↓
5. El sistema procesa todos
   ↓
6. Descarga resultados con predicciones
```

---

## 🐳 Deployment con Docker

### Opción 1: Docker Compose (Recomendado)

```bash
# Construir imagen (primera vez)
docker-compose build

# Ejecutar
docker-compose up

# En otra terminal, ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### Opción 2: Docker Directo

```bash
# Construir imagen
docker build -t alzheimer-prediction-system .

# Ejecutar
docker run -d \
  --name alzheimer-api \
  -p 8000:8000 \
  -p 8501:8501 \
  alzheimer-prediction-system

# Ver logs
docker logs -f alzheimer-api

# Detener
docker stop alzheimer-api
```

### Variables de Entorno Docker

```yaml
PYTHONUNBUFFERED=1           # Output unbuffered
STREAMLIT_SERVER_HEADLESS=true  # Sin browser automático
STREAMLIT_SERVER_PORT=8501      # Puerto de Streamlit
STREAMLIT_SERVER_ADDRESS=0.0.0.0 # Acceso desde cualquier IP
```

### Health Check

```bash
curl http://localhost:8000/health

# Respuesta exitosa:
# {"status": "healthy", "model": "loaded", "timestamp": "2025-11-08T14:30:45"}
```

---

## 📡 API Documentation

### Endpoint: /health

```bash
GET http://localhost:8000/health

Response:
{
  "status": "healthy",
  "model": "loaded",
  "timestamp": "2025-11-08T14:30:45"
}
```

### Endpoint: /model/info

```bash
GET http://localhost:8000/model/info

Response:
{
  "model_name": "RandomForestClassifier",
  "accuracy": 0.95,
  "features": 35,
  "version": "1.0"
}
```

### Endpoint: /predict (Individual)

```bash
POST http://localhost:8000/predict

Request:
{
  "Age": 70,
  "Gender": 1,
  "BMI": 25.5,
  "MMSE": 24,
  "FamilyHistoryAlzheimers": 1,
  ... (otros 30 campos)
}

Response:
{
  "prediction": 1,
  "probability": 0.753,
  "model_name": "RandomForestClassifier",
  "timestamp": "2025-11-08T14:30:45"
}
```

### Endpoint: /predict/batch (Lote)

```bash
POST http://localhost:8000/predict/batch

Request:
[
  {Age: 70, ...},
  {Age: 65, ...},
  ...
]

Response:
[
  {prediction: 1, probability: 0.753},
  {prediction: 0, probability: 0.298},
  ...
]
```

**Documentación interactiva:** http://localhost:8000/docs

---

## 📊 Monitoreo

### Ejecutar Monitoreo

```bash
python mlops_pipeline/src/scripts/model_monitoring.py
```

Genera:
- `monitoring_results/drift_report.csv` - Métricas detalladas
- `monitoring_results/drift_summary.json` - Resumen

### Visualizar Dashboard de Monitoreo

```bash
streamlit run mlops_pipeline/src/scripts/streamlit_app.py
```

Accede a: http://localhost:8501

Muestra:
- Distribución de features
- Indicadores de drift
- Alertas de cambios
- Histórico temporal

---

## 🔄 Pipeline Completo

Para ejecutar el pipeline completo (datos → modelo → deployment):

```bash
python run_pipeline.py --full
```

Flags disponibles:
- `--full` - Ejecutar todo el pipeline
- `--skip-training` - Usar modelo existente
- `--deploy` - Iniciar API después
- `--streamlit` - Iniciar UI después

---

## 📋 Estructura de Directorios

```
final-project-ml/
├── mlops_pipeline/
│   ├── src/
│   │   ├── scripts/
│   │   │   ├── data_processing.py
│   │   │   ├── ft_engineering.py
│   │   │   ├── model_training_evaluation.py
│   │   │   ├── model_deploy.py          # API FastAPI
│   │   │   ├── model_monitoring.py
│   │   │   ├── streamlit_app.py          # Dashboard
│   │   │   └── prediction_ui.py          # ✨ NUEVO UI
│   │   └── notebboks/                   # Jupyter notebooks
│   ├── artifacts/
│   │   ├── best_model.joblib            # Modelo entrenado
│   │   ├── preprocessor.joblib          # Transformador
│   │   ├── model_metadata.json
│   │   └── model_evaluation_results.csv
│   ├── data/
│   │   └── processed/
│   │       ├── cleaned_data.csv
│   │       ├── X_train.csv
│   │       └── X_test.csv
│   └── monitoring_results/
│       ├── drift_report.csv
│       └── drift_summary.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── config.json
├── run_pipeline.py
├── run_full_system.py
├── test_api.py
├── README.md                     # Este archivo
├── QUICK_START_UI.md
├── PREDICTION_UI_GUIDE.md
├── README_PIPELINE.md
└── IMPLEMENTATION_SUMMARY.md
```

---

## 🔍 Troubleshooting

### ❌ "API no disponible"

```bash
# Verificar que está ejecutándose
curl http://localhost:8000/health

# Si falla, iniciar API
python mlops_pipeline/src/scripts/model_deploy.py
```

### ❌ "Streamlit no carga"

```bash
# Puerto en uso, cambiar
streamlit run mlops_pipeline/src/scripts/prediction_ui.py --server.port 8502

# O matar proceso
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### ❌ "Artefactos no encontrados"

```bash
# Entrenar modelo
python run_pipeline.py --full

# Verificar que existen
ls mlops_pipeline/artifacts/
```

### ❌ Error en Docker

```bash
# Reconstruir sin cache
docker build --no-cache -t alzheimer-prediction-system .

# Ver logs detallados
docker run -it alzheimer-prediction-system

# O con docker-compose
docker-compose logs -f
```

---

## 📚 Documentación Adicional

| Documento | Contenido |
|-----------|----------|
| **QUICK_START_UI.md** | Guía rápida de inicio (5 min) |
| **PREDICTION_UI_GUIDE.md** | Manual completo de usuario |
| **README_PIPELINE.md** | Documentación técnica del pipeline |
| **IMPLEMENTATION_SUMMARY.md** | Resumen de implementación |
| **SONARCLOUD_SETUP.md** | Configuración de análisis de código |

---

## 🛠️ Comandos Útiles

```bash
# Entrenar modelo
python run_pipeline.py --full

# Iniciar API sola
python mlops_pipeline/src/scripts/model_deploy.py

# Iniciar Streamlit UI
streamlit run mlops_pipeline/src/scripts/prediction_ui.py

# Iniciar Dashboard de Monitoreo
streamlit run mlops_pipeline/src/scripts/streamlit_app.py

# Correr monitoreo
python mlops_pipeline/src/scripts/model_monitoring.py

# Probar API
python test_api.py

# Iniciar todo automáticamente
python run_full_system.py

# Docker compose
docker-compose up
docker-compose down
docker-compose logs -f
```

---

## 📊 Rendimiento del Modelo

El modelo se entrena con 6 algoritmos diferentes:

1. **LogisticRegression** - Baseline rápido
2. **RandomForest** - Árbol ensemble
3. **GradientBoosting** - Boosting clásico
4. **SVM** - Support Vector Machine
5. **KNeighborsClassifier** - KNN
6. **DecisionTree** - Árbol simple

**Selecciona automáticamente** el mejor basado en:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

---

## 🔐 Notas de Seguridad

⚠️ **IMPORTANTE:**

- Esta es una herramienta de **apoyo diagnóstico**
- **NO reemplaza** evaluación médica profesional
- Los resultados deben ser interpretados por especialistas
- Siempre consulta con un médico para diagnóstico definitivo

---

## 📄 Licencia

Este proyecto está bajo licencia MIT.

---

## 👨‍💻 Autor

Desarrollado como parte del programa de ML final project.

**Versión:** 1.0  
**Última actualización:** Noviembre 2025

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

<div align="center">

**[⬆ Volver al inicio](#-alzheimer-prediction-system---mlops-pipeline-completo)**

Para preguntas o soporte, consulta la documentación detallada en los archivos MD adjuntos.

</div>
