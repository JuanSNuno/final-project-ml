# Guía de Uso del Sistema Unificado

## 📋 Descripción General

El sistema ahora se ejecuta con un único comando que automáticamente:

1. ✅ Verifica si existen los artefactos del modelo
2. 🔄 Ejecuta el pipeline completo (si es necesario)
3. 📊 Ejecuta el monitoreo de data drift (si es necesario)
4. 🚀 Inicia 3 servicios simultáneamente:
   - API FastAPI (puerto 8000)
   - UI Predicción Streamlit (puerto 8501)
   - UI Reporte Drift Streamlit (puerto 8502)
5. 🎯 Abre un panel de control interactivo

---

## 🚀 Cómo Usar

### Opción 1: Usar el Script Maestro (Recomendado)

```bash
python run_full_system.py
```

Este script:
- Verifica automáticamente los artefactos del modelo
- Si faltan, ejecuta el pipeline completo
- Inicia todos los servicios en background
- Abre un panel de control interactivo

### Opción 2: Ejecutar solo el Pipeline

```bash
python run_pipeline.py
```

Este script:
- Ejecuta solo preparación de datos y entrenamiento
- No inicia los servicios
- Útil para actualizar el modelo sin iniciar la interfaz

---

## 🎮 Panel de Control Interactivo

Después de que se inicien todos los servicios, verás un menú como este:

```
================================================================================
  🧠 ALZHEIMER PREDICTION SYSTEM - PANEL DE CONTROL
================================================================================

✅ SERVICIOS ACTIVOS:

  1️⃣  API FastAPI
      📍 URL: http://localhost:8000
      📖 Documentación: http://localhost:8000/docs
      🏥 Health Check: http://localhost:8000/health

  2️⃣  UI Predicción (Streamlit)
      📍 URL: http://localhost:8501
      💡 Haz predicciones sobre Alzheimer

  3️⃣  UI Reporte Drift (Streamlit)
      📍 URL: http://localhost:8502
      📊 Monitorea data drift y cambios en los datos

================================================================================
🎯 ACCIONES DISPONIBLES:
================================================================================

  [1] Abrir API en navegador
  [2] Abrir UI Predicción en navegador
  [3] Abrir UI Reporte Drift en navegador
  [4] Abrir todas las UIs
  [0] Salir (detener todos los servicios)
```

### Opciones del Panel de Control

| Opción | Acción |
|--------|--------|
| **1** | Abre la documentación de la API FastAPI en el navegador |
| **2** | Abre la interfaz de predicción de Alzheimer |
| **3** | Abre el reporte de monitoreo de data drift |
| **4** | Abre todas las interfaces en el navegador |
| **0** | Cierra el sistema y detiene todos los servicios |

---

## 🌐 URLs de los Servicios

Una vez que todo esté corriendo, tienes acceso a:

### 1. API FastAPI
- **URL Base**: http://localhost:8000
- **Documentación Interactiva**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Redoc**: http://localhost:8000/redoc

**Endpoints principales**:
- `POST /predict` - Hacer una predicción
- `GET /health` - Verificar estado de la API
- `GET /model-info` - Información del modelo

### 2. UI Predicción (Streamlit)
- **URL**: http://localhost:8501
- **Función**: Interfaz gráfica para hacer predicciones
- **Features**:
  - Ingresa características del paciente
  - Obtén predicción de riesgo de Alzheimer
  - Visualiza probabilidades
  - Explainability del modelo

### 3. UI Reporte Drift (Streamlit)
- **URL**: http://localhost:8502
- **Función**: Monitoreo de data drift
- **Features**:
  - Visualiza cambios en los datos
  - Detecta problemas de drift
  - Reportes temporales
  - Métricas de rendimiento

---

## 📂 Estructura de Archivos

```
proyecto/
├── run_full_system.py          # Script maestro (USAR ESTE)
├── run_pipeline.py              # Script de pipeline independiente
├── mlops_pipeline/
│   ├── src/scripts/
│   │   ├── data_processing.py
│   │   ├── ft_engineering.py
│   │   ├── model_training_evaluation.py
│   │   ├── model_monitoring.py
│   │   ├── model_deploy.py      # API FastAPI
│   │   ├── prediction_ui.py      # UI Predicción
│   │   └── streamlit_app.py      # UI Reporte Drift
│   ├── artifacts/
│   │   ├── best_model.joblib
│   │   ├── preprocessor.joblib
│   │   └── model_metadata.json
│   ├── data/processed/
│   │   └── (datos procesados)
│   └── monitoring_results/
│       └── drift_report.csv
```

---

## 🔄 Flujo de Ejecución Completo

```
python run_full_system.py
        │
        ├─→ Verificar artefactos
        │   ├─ Si existen → Continuar
        │   └─ Si no → Ejecutar pipeline
        │
        ├─→ Ejecutar Pipeline (si es necesario)
        │   ├─ PASO 1: Procesamiento de Datos
        │   ├─ PASO 2: Feature Engineering
        │   └─ PASO 3: Entrenamiento y Evaluación
        │
        ├─→ Ejecutar Monitoreo de Drift
        │
        ├─→ Iniciar Servicios en Background
        │   ├─ API FastAPI (puerto 8000)
        │   ├─ UI Predicción (puerto 8501)
        │   └─ UI Reporte Drift (puerto 8502)
        │
        └─→ Mostrar Panel de Control Interactivo
            ├─ [1] Abrir API
            ├─ [2] Abrir UI Predicción
            ├─ [3] Abrir UI Reporte Drift
            ├─ [4] Abrir todas
            └─ [0] Salir
```

---

## ⚙️ Requisitos del Sistema

- Python 3.7 o superior
- FastAPI
- Streamlit
- scikit-learn
- pandas
- numpy
- joblib

### Instalar dependencias:
```bash
pip install -r requirements.txt
```

---

## 🐛 Solución de Problemas

### Los servicios no abren en el navegador

**Solución**: Abre manualmente estas URLs en tu navegador:
- API: http://localhost:8000/docs
- Predicción: http://localhost:8501
- Reporte Drift: http://localhost:8502

### Puertos en uso

Si algún puerto está ocupado, verás un error. Soluciona así:

**Windows**:
```powershell
# Encontrar qué proceso usa el puerto
netstat -ano | findstr :8000

# Matar el proceso
taskkill /PID <PID> /F
```

**Linux/Mac**:
```bash
# Encontrar qué proceso usa el puerto
lsof -i :8000

# Matar el proceso
kill -9 <PID>
```

### El pipeline falla

1. Verifica que todos los scripts estén en `mlops_pipeline/src/scripts/`
2. Comprueba que el archivo de datos exista: `alzheimers_disease_data.csv`
3. Revisa los logs de error
4. Intenta ejecutar `python run_pipeline.py` manualmente

---

## 📊 Características del Sistema

### ✅ Auto-Pipeline
- Detecta automáticamente si faltan artefactos
- Ejecuta el pipeline sin intervención manual

### ✅ Multi-Servicio
- API para predicciones programáticas
- Interfaz web para predicciones manuales
- Dashboard de monitoreo de drift

### ✅ Panel de Control
- Menú interactivo y amigable
- Acceso con un click a cualquier servicio
- Cierre ordenado de servicios

### ✅ Cross-Platform
- Soporta Windows, Linux y macOS
- Gestión inteligente de procesos en background

---

## 🎯 Casos de Uso

### Desarrollo
```bash
# Actualizar modelo y probar inmediatamente
python run_full_system.py
# Seleccionar opción [2] para la UI
```

### Producción
```bash
# Ejecutar el sistema completo
python run_full_system.py
# Acceder a API en http://localhost:8000/docs
```

### Monitoreo
```bash
# Ver cambios en los datos
python run_full_system.py
# Seleccionar opción [3] para reporte de drift
```

### Testing
```bash
# Ejecutar solo pipeline sin servicios
python run_pipeline.py --skip-training
```

---

## 📝 Notas Importantes

1. **First Run**: La primera ejecución puede tomar más tiempo (entrenamiento del modelo)
2. **Subsequent Runs**: Las ejecuciones posteriores son más rápidas (verifica artefactos)
3. **Logs**: Cada servicio genera logs en su propia ventana
4. **Stability**: El sistema mantiene los servicios corriendo incluso si el panel se cierra

---

## 🔗 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [scikit-learn](https://scikit-learn.org/)

---

**Último actualizado**: Noviembre 10, 2025

