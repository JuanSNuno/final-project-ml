# 🚀 Pipeline MLOps - Alzheimer's Disease Prediction

Pipeline completo de MLOps para predicción de Alzheimer usando Machine Learning.

## 📋 Descripción del Proyecto

Este proyecto implementa un pipeline end-to-end de MLOps que incluye:
- ✅ Procesamiento y limpieza de datos
- ✅ Feature Engineering con ColumnTransformer
- ✅ Entrenamiento y evaluación de múltiples modelos
- ✅ Despliegue como API REST con FastAPI
- ✅ Monitoreo de Data Drift (PSI, KS test, Chi-cuadrado)
- ✅ Dashboard de visualización con Streamlit
- ✅ Containerización con Docker

## 🏗️ Estructura del Proyecto

```
final-project-ml/
├── mlops_pipeline/
│   └── src/
│       ├── data_processing.py              # Paso 1: Carga y limpieza de datos
│       ├── ft_engineering.py               # Paso 2: Feature Engineering
│       ├── model_training_evaluation.py    # Paso 3: Entrenamiento y evaluación
│       ├── model_deploy.py                 # Paso 4: API de despliegue
│       ├── model_monitoring.py             # Paso 5: Monitoreo de drift
│       └── streamlit_app.py                # Dashboard de visualización
├── data/
│   └── processed/                          # Datasets procesados
├── artifacts/                              # Modelos y transformadores
├── monitoring_results/                     # Reportes de monitoreo
├── run_pipeline.py                         # Script maestro del pipeline
├── Dockerfile                              # Configuración de Docker
├── requirements.txt                        # Dependencias
└── config.json                             # Configuración del proyecto
```

## 🔧 Instalación

### Requisitos Previos
- Python 3.10+
- pip

### Instalar Dependencias

```powershell
pip install -r requirements.txt
```

## 🚀 Uso

### Opción 1: Ejecutar Pipeline Completo (Recomendado)

```powershell
# Pipeline básico (pasos 1-4)
python run_pipeline.py

# Pipeline completo con despliegue y visualización
python run_pipeline.py --full

# Solo pipeline con API
python run_pipeline.py --deploy

# Solo pipeline con Streamlit
python run_pipeline.py --streamlit
```

### Opción 2: Ejecutar Pasos Individuales

#### Paso 1: Procesamiento de Datos
```powershell
python mlops_pipeline/src/data_processing.py
```
**Output:** `data/processed/cleaned_data.csv`

#### Paso 2: Feature Engineering
```powershell
python mlops_pipeline/src/ft_engineering.py
```
**Output:** 
- `artifacts/preprocessor.joblib`
- `data/processed/X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`

#### Paso 3: Entrenamiento y Evaluación
```powershell
python mlops_pipeline/src/model_training_evaluation.py
```
**Output:**
- `artifacts/best_model.joblib`
- `artifacts/model_metadata.json`
- `artifacts/model_evaluation_results.csv`

#### Paso 4: Monitoreo de Data Drift
```powershell
python mlops_pipeline/src/model_monitoring.py
```
**Output:**
- `monitoring_results/drift_report.csv`
- `monitoring_results/drift_summary.json`

#### Paso 5: Desplegar API
```powershell
python mlops_pipeline/src/model_deploy.py
```
**Acceso:**
- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs

#### Paso 6: Dashboard de Visualización
```powershell
streamlit run mlops_pipeline/src/streamlit_app.py
```

## 🐋 Docker

### Construir Imagen
```powershell
docker build -t alzheimer-api .
```

### Ejecutar Contenedor
```powershell
docker run -p 8000:8000 alzheimer-api
```

### Acceder a la API
- URL: http://localhost:8000
- Documentación: http://localhost:8000/docs

## 📊 API Endpoints

### GET /
Información general de la API

### GET /health
Estado de salud de la API

### GET /model/info
Información del modelo cargado

### POST /predict
Realizar una predicción

**Ejemplo de Request:**
```json
{
  "Age": 75.0,
  "Gender": 1,
  "Ethnicity": 0,
  "EducationLevel": 2,
  "BMI": 25.5,
  "Smoking": 0,
  "AlcoholConsumption": 5.0,
  "PhysicalActivity": 6.5,
  "DietQuality": 7.0,
  "SleepQuality": 7.5,
  "FamilyHistoryAlzheimers": 1,
  ...
}
```

**Respuesta:**
```json
{
  "prediction": 1,
  "probability": 0.87,
  "model_name": "Random Forest"
}
```

### POST /predict/batch
Realizar predicciones en lote

## 📈 Monitoreo de Data Drift

El pipeline implementa tres métricas principales de data drift:

1. **PSI (Population Stability Index)**
   - PSI < 0.1: Sin cambio significativo
   - 0.1 ≤ PSI < 0.25: Cambio moderado
   - PSI ≥ 0.25: Cambio significativo

2. **Test de Kolmogorov-Smirnov (KS)**
   - Mide diferencias en distribuciones acumuladas
   - p-value < 0.05 indica drift significativo

3. **Chi-cuadrado (Variables categóricas)**
   - Mide cambios en distribución de categorías
   - Incluye Cramér's V como medida del tamaño del efecto

## 📊 Dashboard Streamlit

El dashboard incluye:
- 📊 Resumen ejecutivo con métricas clave
- 📈 Visualización de distribuciones (baseline vs actual)
- 📋 Tabla detallada de métricas de drift
- 💡 Recomendaciones automatizadas
- 🎨 Gráficos interactivos

## 🧪 Modelos Entrenados

El pipeline evalúa múltiples algoritmos:
- Logistic Regression
- Random Forest
- Gradient Boosting
- Decision Tree
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)

El mejor modelo se selecciona automáticamente basado en:
- F1-Score (métrica principal)
- Test Accuracy
- Bajo overfitting

## 📁 Artefactos Generados

### `/data/processed/`
- `cleaned_data.csv`: Dataset limpio
- `X_train.csv`, `X_test.csv`: Features transformados
- `y_train.csv`, `y_test.csv`: Target

### `/artifacts/`
- `preprocessor.joblib`: ColumnTransformer ajustado
- `best_model.joblib`: Mejor modelo entrenado
- `model_metadata.json`: Metadata del modelo
- `model_evaluation_results.csv`: Resultados de evaluación

### `/monitoring_results/`
- `drift_report.csv`: Reporte detallado de drift
- `drift_summary.json`: Resumen de drift

## 🔧 Configuración

Edita `config.json` para ajustar parámetros:

```json
{
  "project": "final-project-ml",
  "data_path": "alzheimers_disease_data.csv",
  "training": {
    "test_size": 0.2,
    "random_state": 42
  }
}
```

## 🛠️ Desarrollo

### Estructura de Pipeline

El pipeline sigue un flujo secuencial donde cada paso guarda artefactos que son consumidos por el siguiente:

```
Data Processing → Feature Engineering → Model Training → Model Deployment
                                              ↓
                                         Monitoring ← Streamlit Dashboard
```

### Buenas Prácticas Implementadas

- ✅ Separación de concerns (cada script tiene una responsabilidad única)
- ✅ Artefactos versionables (joblib para modelos y transformadores)
- ✅ Configuración externalizada (config.json)
- ✅ Logging informativo en cada paso
- ✅ Validación de datos y manejo de errores
- ✅ Código modular y reutilizable
- ✅ Documentación inline y docstrings

## 📝 Notas

- Los datos deben estar en formato CSV con las columnas esperadas
- El modelo debe ser reentrenado si se detecta drift significativo
- La API carga los artefactos al inicio (preprocessor + modelo)
- Streamlit lee los reportes de monitoreo desde archivos

## 🤝 Contribuciones

Este proyecto es parte de un ejercicio académico de MLOps.

## 📄 Licencia

Proyecto académico - Universidad

---

**Desarrollado con ❤️ para el curso de Machine Learning**
