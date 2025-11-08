# 🚀 INICIO RÁPIDO - Prediction UI

## ⚡ 3 Maneras de Ejecutar el Sistema

### ✅ Opción 1: Un Comando Simple (Recomendado - Local)

```powershell
python run_full_system.py
```

**Esto hará automáticamente:**
- Verifica artefactos del modelo
- Inicia API FastAPI (puerto 8000)
- Inicia Streamlit UI (puerto 8501)
- Abre navegador en `http://localhost:8501`

---

### ✅ Opción 2: Docker Compose (Recomendado - Producción)

**Requisito:** Docker y Docker Compose instalados

```powershell
# Construir imagen (primera vez)
docker-compose build

# Ejecutar sistema completo
docker-compose up
```

Luego accede a:
- **UI:** http://localhost:8501
- **API:** http://localhost:8000

**Para detener:**
```powershell
docker-compose down
```

---

### ✅ Opción 3: Manual - 2 Terminales (Control Total)

**Terminal 1 - API:**
```powershell
cd mlops_pipeline\src\scripts
python model_deploy.py
```

Verás: `INFO: Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 - UI:**
```powershell
streamlit run mlops_pipeline/src/scripts/prediction_ui.py
```

Verás: `Local URL: http://localhost:8501`

---

## 🔗 Acceder a la Interfaz

Una vez que el sistema está ejecutándose:

1. Abre tu navegador favorito
2. Ve a: **http://localhost:8501**
3. Verás la interfaz profesional

### URLs Disponibles

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **UI Streamlit** | http://localhost:8501 | Interfaz gráfica principal |
| **API** | http://localhost:8000 | Endpoints REST |
| **Docs API** | http://localhost:8000/docs | Swagger UI con documentación |
| **Health Check** | http://localhost:8000/health | Estado de la API |

---

## ✨ Funcionalidades Principales

### 📋 Predicción Individual
- Formulario completo con 35 parámetros
- Organizado por secciones (médica, cognitiva, etc.)
- Valores por defecto precompletados
- Resultados con gráfico gauge interactivo

### 📊 Predicción por Lote
- Descarga plantilla CSV
- Sube múltiples pacientes
- Obtén predicciones masivas
- Descarga resultados

### 📈 Información del Sistema
- Detalles del modelo
- Estado de la API
- Historial de predicciones
- Estadísticas

---

## 🛠️ Requisitos

### Local
- Python 3.11+
- pip (gestor de paquetes)
- Navegador moderno

### Docker
- Docker CE
- Docker Compose

---

## ⚠️ Si Algo No Funciona

### Error: "API no disponible"
```powershell
# Verificar que API está ejecutándose
curl http://localhost:8000/health

# Si no responde, inicia API en otra terminal
python mlops_pipeline\src\scripts\model_deploy.py
```

### Error: "Puerto en uso"
```powershell
# Cambiar puerto Streamlit
streamlit run mlops_pipeline/src/scripts/prediction_ui.py --server.port 8502
```

### Error: "Artefactos no encontrados"
```powershell
# Entrena el modelo primero
python run_pipeline.py --full
```

---

## 📚 Documentación Completa

Para más detalles, lee: **PREDICTION_UI_GUIDE.md**

Contiene:
- Guía detallada de usuario
- Configuración avanzada
- Solución de problemas
- Ejemplos de uso

---

## 🎯 Flujo Típico

```
1. Ejecuta:       python run_full_system.py
                           ↓
2. Abre navegador: http://localhost:8501
                           ↓
3. Selecciona pestaña: "📋 Predicción Individual"
                           ↓
4. Completa datos del paciente
                           ↓
5. Haz clic en: "🔮 Realizar Predicción"
                           ↓
6. Obtén resultado con recomendaciones
```

---

## 🐳 Usando Docker

### Opción A: Con Docker Compose (Simplest)

```powershell
docker-compose up
```

### Opción B: Comando Docker directo

```powershell
# Construir
docker build -t alzheimer-ui .

# Ejecutar
docker run -p 8000:8000 -p 8501:8501 alzheimer-ui
```

### Ver logs
```powershell
docker-compose logs -f
```

### Detener
```powershell
docker-compose down
```

---

## 💡 Tips

✅ **Para desarrollo local:** Opción 1 (run_full_system.py)

✅ **Para producción:** Opción 2 (Docker Compose)

✅ **Para máximo control:** Opción 3 (2 terminales)

✅ **En tu máquina local:** API y UI en localhost

✅ **En servidor remoto:** Configura firewall y cambiar localhost por 0.0.0.0

---

**Versión 1.0 | Noviembre 2025**

¿Preguntas? Consulta PREDICTION_UI_GUIDE.md
