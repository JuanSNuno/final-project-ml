# ⚡ REFERENCIAS RÁPIDAS

## 🚀 Iniciar el Sistema

```bash
# Opción 1: Un Comando (Recomendado)
python run_full_system.py

# Opción 2: Docker Compose
docker-compose up

# Opción 3: Manual - Terminal 1
python mlops_pipeline/src/scripts/model_deploy.py

# Opción 3: Manual - Terminal 2
streamlit run mlops_pipeline/src/scripts/prediction_ui.py
```

## 🌐 URLs Principales

| Servicio | URL |
|----------|-----|
| **UI Principal** | http://localhost:8501 |
| **API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/health |

## 📖 Documentación (Por Tiempo)

| Tiempo | Documento | Contenido |
|--------|-----------|----------|
| ⚡ 5 min | QUICK_START_UI.md | Inicio rápido |
| 🕐 30 min | PREDICTION_UI_GUIDE.md | Guía completa |
| 📚 60 min | README_UI.md | Documentación técnica |
| 🎯 Variable | DOCUMENTATION_INDEX.md | Guía personalizada |

## 🔧 Comandos Útiles

```bash
# Testing
python test_prediction_ui.py

# Entrenar modelo
python run_pipeline.py --full

# Ver logs API
tail -f *.log

# Limpiar Docker
docker-compose down
docker system prune

# Reconstruir Docker
docker-compose build --no-cache
```

## 🎨 Interfaz - 3 Funciones Principales

### 1️⃣ Predicción Individual
```
Formulario → 35 parámetros → Predecir → Resultado + Recomendaciones
```

### 2️⃣ Predicción por Lote
```
Descargar Plantilla → Rellenar CSV → Subir → Resultados + Gráficos
```

### 3️⃣ Información del Sistema
```
Detalles Modelo → Historial → Estadísticas
```

## ⚠️ Problemas Comunes

| Problema | Solución |
|----------|----------|
| "API no disponible" | `python mlops_pipeline/src/scripts/model_deploy.py` |
| "Puerto en uso" | `streamlit run ... --server.port 8502` |
| "Artefactos no encontrados" | `python run_pipeline.py --full` |
| "ModuleNotFoundError" | `pip install -r requirements.txt` |

## 📊 Parámetros API

### Endpoint: POST /predict

```json
{
  "Age": 70,
  "Gender": 1,
  "BMI": 25.5,
  "MMSE": 24,
  "FamilyHistoryAlzheimers": 1,
  ... (otros 30 campos)
}
```

**Respuesta:**
```json
{
  "prediction": 1,
  "probability": 0.753,
  "model_name": "RandomForestClassifier"
}
```

## 🐳 Docker Quick Commands

```bash
# Build
docker build -t alzheimer-ui .

# Run
docker run -p 8000:8000 -p 8501:8501 alzheimer-ui

# Compose
docker-compose up          # Start
docker-compose down        # Stop
docker-compose logs -f     # Logs
```

## 📱 Tecnologías

- **Frontend:** Streamlit + Plotly
- **Backend:** FastAPI + Uvicorn
- **ML:** scikit-learn + joblib
- **Data:** Pandas + NumPy
- **Container:** Docker + Docker Compose

## 🎯 Archivos Principales

| Archivo | Propósito |
|---------|-----------|
| `prediction_ui.py` | Interfaz Streamlit |
| `model_deploy.py` | API FastAPI |
| `run_full_system.py` | Orquestación |
| `docker-compose.yml` | Docker |
| `requirements.txt` | Dependencias |

## 📊 Rendimiento

| Métrica | Valor |
|---------|-------|
| Setup Time | ~30 seg |
| First Prediction | ~2 seg |
| Batch (1000 registros) | ~1 min |
| UI Load | ~3 seg |
| API Response | <2 seg |

## 🔐 Seguridad

- ✅ No almacena datos en disco
- ✅ Validación Pydantic
- ✅ Medical disclaimer
- ✅ Error handling

## 📝 Parámetros (35 total)

**Médicos (7):** Smoking, Diabetes, CardiovascularDisease, Hypertension, Depression, HeadInjury, FamilyHistoryAlzheimers

**Cognitivos (7):** MMSE, ADL, MemoryComplaints, Confusion, Disorientation, PersonalityChanges, FunctionalAssessment

**Laboratorio (7):** SystolicBP, DiastolicBP, CholesterolTotal, CholesterolLDL, CholesterolHDL, CholesterolTriglycerides

**Lifestyle (4):** AlcoholConsumption, PhysicalActivity, DietQuality, SleepQuality

**Otros (3+):** Age, Gender, BMI, EducationLevel, BehavioralProblems, DifficultyCompletingTasks, Forgetfulness, Ethnicity

## 🎓 Curvas de Aprendizaje

```
Tiempo Total Requerido:

⚡ 5 minutos   → Ejecutar sistema
🕐 30 minutos  → Usar completamente
📚 1-2 horas   → Entender arquitectura
🏗️ 3+ horas    → Customizar sistema
```

## 🌐 Acceso Remoto

```bash
# Exponer en red local
streamlit run prediction_ui.py --server.address 0.0.0.0 --server.port 8501

# Acceder desde otra PC
http://192.168.x.x:8501
```

## 📚 Lectura Recomendada

1. **Empezar:** QUICK_START_UI.md
2. **Usar:** PREDICTION_UI_GUIDE.md
3. **Entender:** README_UI.md
4. **Arquitectura:** README_PIPELINE.md
5. **Ayuda:** DOCUMENTATION_INDEX.md

## 💾 Backup

```bash
# Copiar artefactos
cp -r mlops_pipeline/artifacts backup_artifacts

# Copiar resultados
cp -r monitoring_results backup_monitoring
```

## 🔄 Actualizar Dependencias

```bash
pip install -r requirements.txt --upgrade
```

## 📊 Ver Estructura

```bash
tree /F /S mlops_pipeline/
# O en Windows
dir /s /b mlops_pipeline/
```

## 🧪 Verificación

```bash
# Test sistema
python test_prediction_ui.py

# Verificar API
curl http://localhost:8000/health

# Verificar instalación Python
python --version
pip list
```

## 🎛️ Configurar Streamlit

Editar: `~/.streamlit/config.toml`

```ini
[theme]
base="light"
primaryColor="#0066cc"

[client]
showErrorDetails=true
```

## 📱 Comandos Windows PowerShell

```powershell
# Cambiar puerto (si está en uso)
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Ver procesos Python
Get-Process python

# Instalar paquete
pip install plotly

# Virtualenv
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 🚀 Una Línea para Comenzar

```powershell
cd "C:\Users\jsanc\OneDrive\Documentos\U\ML\final-project-ml"; python run_full_system.py
```

---

**Versión:** 1.0 | **Última actualización:** Noviembre 2025

¿Necesitas más? Consulta DOCUMENTATION_INDEX.md
