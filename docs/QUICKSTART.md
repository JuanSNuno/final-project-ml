# 🎯 GUÍA RÁPIDA DEL PIPELINE MLOps

## 🚀 Inicio Rápido

### 1️⃣ Instalar Dependencias
```powershell
pip install -r requirements.txt
```

### 2️⃣ Ejecutar Pipeline Completo
```powershell
python run_pipeline.py
```

## 📊 Flujo del Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PIPELINE MLOps SECUENCIAL                        │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────┐
    │ PASO 1: data_processing.py                                   │
    │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
    │ INPUT:  alzheimers_disease_data.csv                          │
    │ HACE:   Limpieza y preprocesamiento básico                   │
    │ OUTPUT: data/processed/cleaned_data.csv                      │
    └──────────────────────────────────────────────────────────────┘
                              ↓
    ┌──────────────────────────────────────────────────────────────┐
    │ PASO 2: ft_engineering.py                                    │
    │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
    │ INPUT:  data/processed/cleaned_data.csv                      │
    │ HACE:   ColumnTransformer + Train/Test Split                 │
    │ OUTPUT: - artifacts/preprocessor.joblib                      │
    │         - data/processed/X_train.csv, X_test.csv             │
    │         - data/processed/y_train.csv, y_test.csv             │
    └──────────────────────────────────────────────────────────────┘
                              ↓
    ┌──────────────────────────────────────────────────────────────┐
    │ PASO 3: model_training_evaluation.py                         │
    │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
    │ INPUT:  data/processed/X_train.csv, y_train.csv              │
    │ HACE:   Entrena 6 modelos y selecciona el mejor             │
    │ OUTPUT: - artifacts/best_model.joblib                        │
    │         - artifacts/model_metadata.json                      │
    │         - artifacts/model_evaluation_results.csv             │
    └──────────────────────────────────────────────────────────────┘
                              ↓
    ┌──────────────────────────────────────────────────────────────┐
    │ PASO 4: model_monitoring.py                                  │
    │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
    │ INPUT:  data/processed/cleaned_data.csv (baseline)           │
    │ HACE:   Calcula PSI, KS test, Chi-cuadrado                   │
    │ OUTPUT: - monitoring_results/drift_report.csv                │
    │         - monitoring_results/drift_summary.json              │
    └──────────────────────────────────────────────────────────────┘
                              ↓
    ┌──────────────────────────────────────────────────────────────┐
    │ DESPLIEGUE: model_deploy.py                                  │
    │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
    │ CARGA:  - artifacts/preprocessor.joblib                      │
    │         - artifacts/best_model.joblib                        │
    │ HACE:   API REST con FastAPI                                 │
    │ ACCESO: http://localhost:8000                                │
    │         http://localhost:8000/docs (Swagger)                 │
    └──────────────────────────────────────────────────────────────┘
                              │
    ┌─────────────────────────┴─────────────────────────────────────┐
    │ VISUALIZACIÓN: streamlit_app.py                              │
    │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
    │ LEE:    monitoring_results/*.csv, *.json                     │
    │ HACE:   Dashboard interactivo de monitoreo                   │
    │ ACCESO: http://localhost:8501                                │
    └──────────────────────────────────────────────────────────────┘
```

## 🎨 Comandos Útiles

### Ejecutar Pasos Individuales
```powershell
# Paso 1
python mlops_pipeline/src/data_processing.py

# Paso 2
python mlops_pipeline/src/ft_engineering.py

# Paso 3
python mlops_pipeline/src/model_training_evaluation.py

# Paso 4
python mlops_pipeline/src/model_monitoring.py

# Desplegar API
python mlops_pipeline/src/model_deploy.py

# Streamlit
streamlit run mlops_pipeline/src/streamlit_app.py
```

### Ejecutar con Opciones
```powershell
# Pipeline básico
python run_pipeline.py

# Con API
python run_pipeline.py --deploy

# Con Streamlit
python run_pipeline.py --streamlit

# Todo junto
python run_pipeline.py --full

# Sin entrenamiento (testing)
python run_pipeline.py --skip-training
```

## 🐋 Docker

```powershell
# Construir imagen
docker build -t alzheimer-api .

# Ejecutar contenedor
docker run -p 8000:8000 alzheimer-api

# Acceder
# http://localhost:8000
# http://localhost:8000/docs
```

## 🧪 Probar la API

```powershell
# Iniciar API en una terminal
python mlops_pipeline/src/model_deploy.py

# En otra terminal, ejecutar pruebas
python test_api.py
```

## 📊 Métricas de Data Drift

| Métrica | Sin Drift | Moderado | Crítico |
|---------|-----------|----------|---------|
| PSI     | < 0.1     | 0.1-0.25 | ≥ 0.25  |
| KS p-value | ≥ 0.05 | < 0.05   | < 0.01  |
| Cramér's V | < 0.1  | 0.1-0.3  | ≥ 0.3   |

## 📁 Archivos Clave

| Archivo | Descripción |
|---------|-------------|
| `run_pipeline.py` | Script maestro del pipeline |
| `config.json` | Configuración del proyecto |
| `Dockerfile` | Imagen Docker de la API |
| `requirements.txt` | Dependencias Python |
| `test_api.py` | Script de pruebas de la API |

## ⚠️ Notas Importantes

1. **Orden de Ejecución**: Los pasos deben ejecutarse en orden (1→2→3→4)
2. **Artefactos**: Cada paso guarda archivos que el siguiente paso necesita
3. **Docker**: Solo incluye la API, no todo el pipeline
4. **Monitoreo**: Streamlit lee archivos generados por model_monitoring.py

## 🆘 Solución de Problemas

### Error: "No se encontró el dataset limpio"
```powershell
# Ejecuta primero el paso 1
python mlops_pipeline/src/data_processing.py
```

### Error: "No se encontró preprocessor.joblib"
```powershell
# Ejecuta los pasos 1 y 2
python mlops_pipeline/src/data_processing.py
python mlops_pipeline/src/ft_engineering.py
```

### Error: "No se encontró best_model.joblib"
```powershell
# Ejecuta los pasos 1, 2 y 3
python run_pipeline.py
```

### La API no responde
```powershell
# Verifica que esté corriendo
# Debe mostrar: INFO: Uvicorn running on http://0.0.0.0:8000
python mlops_pipeline/src/model_deploy.py
```

## 📞 Estructura de la API

### Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Info general |
| GET | `/health` | Estado de salud |
| GET | `/model/info` | Info del modelo |
| POST | `/predict` | Predicción individual |
| POST | `/predict/batch` | Predicción en lote |

---

**¡Listo para producción! 🚀**
