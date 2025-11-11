# 🧠 Sistema MLOps para Predicción de Enfermedad de Alzheimer

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.1-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2.2-orange.svg)](https://scikit-learn.org/)

## 📋 Descripción General del Proyecto

Este proyecto implementa un **pipeline completo de MLOps** para la predicción de la enfermedad de Alzheimer, abarcando desde la exploración inicial de datos hasta el despliegue y monitoreo continuo del modelo en producción. El sistema está diseñado siguiendo las mejores prácticas de Machine Learning Operations (MLOps), incluyendo:

- **Análisis Exploratorio de Datos (EDA)**: Comprensión profunda de los datos clínicos relacionados con el Alzheimer
- **Feature Engineering**: Transformación y creación de características relevantes para mejorar el rendimiento del modelo
- **Entrenamiento de Modelos**: Desarrollo y comparación de múltiples algoritmos de Machine Learning
- **Evaluación y Validación**: Métricas comprehensivas para asegurar la calidad del modelo
- **Despliegue Automatizado**: API REST con FastAPI y interfaces de usuario interactivas con Streamlit
- **Monitoreo Continuo**: Detección de drift en datos y métricas de rendimiento en tiempo real
- **Containerización**: Solución lista para producción con Docker y Docker Compose

El proyecto está estructurado para facilitar tanto la **revisión manual** de los procesos de desarrollo (mediante notebooks interactivos) como la **ejecución automatizada** del pipeline completo (mediante scripts modulares).

---

## 📁 Estructura del Proyecto

```
final-project-ml/
│
├── 📊 alzheimers_disease_data.csv        # Dataset principal
├── ⚙️ config.json                         # Configuración del proyecto
├── 🐳 docker-compose.yml                  # Orquestación de contenedores
├── 🐳 Dockerfile                          # Imagen Docker del sistema
├── 📦 requirements.txt                    # Dependencias Python
├── 🚀 run_full_system.py                  # Ejecutor del sistema completo
├── 🔄 run_pipeline.py                     # Ejecutor del pipeline MLOps
├── 🛠️ set_up.bat                          # Script de configuración (Windows)
├── 📈 setup_monitoring.py                 # Configurador de monitoreo
├── 🔍 sonar-project.properties           # Configuración SonarQube
│
├── 📚 docs/
│   └── Rubrica/                          # 📋 Documentación de cumplimiento
│       ├── ANALISIS_CUMPLIMIENTO_DESPLIEGUE.md
│       ├── ANALISIS_CUMPLIMIENTO_EDA.md
│       ├── ANALISIS_CUMPLIMIENTO_FT_ENGINEERING.md
│       ├── ANALISIS_CUMPLIMIENTO_MODEL_TRAINING.md
│       └── ANALISIS_CUMPLIMIENTO_MONITORING.md
│
└── 🔧 mlops_pipeline/
    ├── 📦 artifacts/                     # Modelos y artefactos entrenados
    │   ├── best_model.joblib
    │   ├── preprocessor.joblib
    │   ├── model_evaluation_results.csv
    │   └── model_metadata.json
    │
    ├── 💾 data/                          # Datos procesados
    │   └── processed/
    │       ├── cleaned_data.csv
    │       ├── X_train.csv
    │       ├── X_test.csv
    │       ├── y_train.csv
    │       └── y_test.csv
    │
    ├── 📊 monitoring_results/            # Resultados de monitoreo
    │   ├── drift_report.csv
    │   └── drift_summary.json
    │
    └── 💻 src/
        ├── utilities.py                  # Utilidades compartidas
        │
        ├── 📓 notebooks/                 # 🔍 Para revisión manual del evaluador
        │   ├── Cargar_datos.ipynb
        │   ├── comprension_eda.ipynb
        │   ├── ft_engineering.ipynb
        │   ├── model_training.ipynb
        │   ├── model_monitoring.ipynb
        │   
        │   
        │
        └── 🎯 scripts/                   # ⚙️ Corazón del pipeline MLOps
            ├── data_processing.py
            ├── ft_engineering.py
            ├── model_training_evaluation.py
            ├── heuristic_model.py
            ├── model_deploy.py
            ├── model_monitoring.py
            ├── prediction_ui.py
            └── streamlit_app.py
```

---

## 📓 Carpeta `src/notebooks/` - Revisión Manual

Los notebooks en `mlops_pipeline/src/notebooks/` están diseñados para la **revisión manual por parte del evaluador**. Cada notebook documenta de forma interactiva y visual un paso específico del pipeline de MLOps:

| Notebook | Descripción |
|----------|-------------|
| `Cargar_datos.ipynb` | Carga inicial y exploración preliminar del dataset |
| `comprension_eda.ipynb` | Análisis Exploratorio de Datos completo con visualizaciones |
| `ft_engineering.ipynb` | Proceso de Feature Engineering y transformación de variables |
| `model_training.ipynb` | Entrenamiento de modelos y comparación de algoritmos |
| `model_evaluation.ipynb` | Evaluación detallada del modelo con múltiples métricas |
| `model_deploy.ipynb` | Demostración del despliegue del modelo |
| `model_monitoring.ipynb` | Análisis de drift y monitoreo continuo |

Estos notebooks permiten **visualizar paso a paso** el desarrollo del proyecto, incluyendo gráficos, análisis estadísticos y decisiones técnicas tomadas durante el proceso.

---

## 🎯 Carpeta `src/scripts/` - Corazón del Pipeline

Los scripts en `mlops_pipeline/src/scripts/` constituyen el **núcleo funcional** del sistema MLOps. Estos scripts son modulares, reutilizables y están diseñados para la **ejecución automatizada** del pipeline completo:

| Script | Función |
|--------|---------|
| `data_processing.py` | Limpieza, validación y preprocesamiento de datos |
| `ft_engineering.py` | Transformación de features y creación de variables derivadas |
| `model_training_evaluation.py` | Entrenamiento, evaluación y selección del mejor modelo |
| `heuristic_model.py` | Implementación de modelo baseline heurístico |
| `model_deploy.py` | API REST con FastAPI para servir predicciones |
| `model_monitoring.py` | Sistema de monitoreo y detección de drift |
| `prediction_ui.py` | Interfaz de usuario para predicciones individuales |
| `streamlit_app.py` | Dashboard interactivo para visualización de resultados |

Estos scripts permiten ejecutar el **pipeline completo de forma automatizada** mediante `run_pipeline.py` o `run_full_system.py`.

---

## 📋 Carpeta `docs/Rubrica/` - Análisis de Cumplimiento

En el directorio `docs/Rubrica/` se encuentra la documentación completa del **análisis de cumplimiento** de todos los requisitos del proyecto:

| Documento | Contenido |
|-----------|-----------|
| `ANALISIS_CUMPLIMIENTO_EDA.md` | Validación del Análisis Exploratorio de Datos |
| `ANALISIS_CUMPLIMIENTO_FT_ENGINEERING.md` | Verificación del Feature Engineering |
| `ANALISIS_CUMPLIMIENTO_MODEL_TRAINING.md` | Evaluación del entrenamiento de modelos |
| `ANALISIS_CUMPLIMIENTO_DESPLIEGUE.md` | Comprobación del despliegue del sistema |
| `ANALISIS_CUMPLIMIENTO_MONITORING.md` | Validación del sistema de monitoreo |

Cada documento detalla cómo se cumplieron los requisitos específicos de cada fase del proyecto, incluyendo referencias a código, notebooks y resultados obtenidos.

---

## 🚀 Instrucciones de Instalación y Ejecución

### 📋 Prerrequisitos

- **Python 3.11** o superior
- **Docker Desktop** (para ejecución con contenedores)
- **Git** (para clonar el repositorio)

### 🔧 Opción 1: Ejecución con Entorno Virtual

#### 1️⃣ Clonar el Repositorio

```powershell
git clone https://github.com/JuanSNuno/final-project-ml.git
cd final-project-ml
```

#### 2️⃣ Crear y Activar Entorno Virtual

**Opción A: Usar el script automatizado (Recomendado para Windows)**

```powershell
# Ejecutar el script de configuración automática
.\set_up.bat
```

Este script automáticamente:
- Crea el entorno virtual (`.venv`)
- Activa el entorno virtual
- Actualiza pip a la última versión
- Instala todas las dependencias desde `requirements.txt`
- Registra el kernel de Jupyter para trabajar con notebooks

**Opción B: Configuración manual**

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (PowerShell)
.\venv\Scripts\Activate.ps1

# O si usas CMD
.\venv\Scripts\activate.bat

# Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# (Opcional) Registrar kernel de Jupyter
python -m pip install ipykernel
python -m ipykernel install --user --name=ml-venv --display-name="ML Project Python"
```

#### 3️⃣ Ejecutar el Pipeline Completo

```powershell
# Ejecutar pipeline MLOps completo (preprocesamiento, entrenamiento, evaluación)
python run_pipeline.py

# O ejecutar el sistema completo (API + UI + Monitoreo)
python run_full_system.py
```

#### 4️⃣ Acceder a las Interfaces

Una vez ejecutado el sistema:

- **API FastAPI**: http://localhost:8000
- **Documentación API (Swagger)**: http://localhost:8000/docs
- **UI de Predicción (Streamlit)**: http://localhost:8501
- **Dashboard de Monitoreo**: http://localhost:8502

### 🐳 Opción 2: Ejecución con Docker

#### 1️⃣ Construir la Imagen Docker

```powershell
docker build -t alzheimer-prediction-system .
```

#### 2️⃣ Ejecutar con Docker Compose

```powershell
# Iniciar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Detener los servicios
docker-compose down
```

#### 3️⃣ Acceder a las Interfaces

Los servicios estarán disponibles en:

- **API FastAPI**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **UI de Predicción**: http://localhost:8501
- **Dashboard de Monitoreo**: http://localhost:8502

#### 4️⃣ Verificar Estado del Contenedor

```powershell
# Ver contenedores en ejecución
docker ps

# Verificar logs del contenedor
docker logs alzheimer-prediction-system

# Acceder al contenedor (si es necesario)
docker exec -it alzheimer-prediction-system /bin/bash
```

---

## 🧪 Ejecutar Tests

```powershell
# Ejecutar tests con pytest
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=mlops_pipeline --cov-report=html
```

---

## 📚 Documentación Adicional

- **Análisis de Cumplimiento**: Ver carpeta `docs/Rubrica/`
- **Notebooks Interactivos**: Ver carpeta `mlops_pipeline/src/notebooks/`
- **API Documentation**: http://localhost:8000/docs (cuando el sistema esté corriendo)

---

## 👥 Autor

**Juan S. Nuno**

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico para el curso de Machine Learning.

---

## 🆘 Solución de Problemas Comunes

### Error al activar entorno virtual en PowerShell

Si encuentras errores de permisos al activar el entorno virtual:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Puerto ya en uso

Si algún puerto está ocupado, puedes cambiar los puertos en `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"    # Cambiar 8000 por otro puerto
  - "8503:8501"    # Cambiar 8501 por otro puerto
```

### Problemas con Docker

```powershell
# Limpiar contenedores e imágenes anteriores
docker-compose down -v
docker system prune -a

# Reconstruir desde cero
docker-compose build --no-cache
docker-compose up -d
```

---

## 📞 Contacto

Para preguntas o sugerencias sobre este proyecto, por favor contactar al autor.

---

**¡Gracias por revisar este proyecto! 🚀**
