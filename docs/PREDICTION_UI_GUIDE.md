# 🧠 Prediction UI - Manual de Usuario

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
4. [Ejecución](#ejecución)
5. [Características](#características)
6. [Guía de Usuario](#guía-de-usuario)
7. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Descripción General

**Prediction UI** es una interfaz profesional y moderna construida con Streamlit que permite:

- ✅ Realizar predicciones individuales de riesgo de Alzheimer
- ✅ Procesar lotes de pacientes (batch prediction)
- ✅ Visualizar resultados con gráficos interactivos
- ✅ Descargar reportes en CSV
- ✅ Obtener recomendaciones personalizadas basadas en riesgo

### Arquitectura

```
┌─────────────────────────────────────┐
│   Prediction UI (Streamlit)         │
│   Puerto 8501                        │
└────────────┬──────────────────────┘
             │ Requests HTTP
             ▼
┌─────────────────────────────────────┐
│   API FastAPI (model_deploy.py)     │
│   Puerto 8000                        │
└────────────┬──────────────────────┘
             │ Carga Modelos
             ▼
┌─────────────────────────────────────┐
│   Artefactos Entrenados             │
│   - preprocessor.joblib             │
│   - best_model.joblib               │
└─────────────────────────────────────┘
```

---

## 📦 Requisitos

### Localmente

- Python 3.11+
- pip o conda
- API FastAPI ejecutándose en `http://localhost:8000`

### En Docker

- Docker instalado
- Docker Compose (opcional, pero recomendado)

---

## 🔧 Instalación

### Opción 1: Instalación Local

```bash
# 1. Navega al directorio del proyecto
cd c:\Users\jsanc\OneDrive\Documentos\U\ML\final-project-ml

# 2. Instala las dependencias
pip install -r requirements.txt

# 3. Verifica que tienes Streamlit
pip list | grep streamlit
```

### Opción 2: Instalación con Docker

```bash
# 1. Construye la imagen Docker
docker build -t alzheimer-ui .

# 2. La imagen incluye todo lo necesario
```

---

## 🚀 Ejecución

### Opción 1: Ejecución Local (2 terminales)

**Terminal 1 - Iniciar API:**
```bash
cd mlops_pipeline\src\scripts
python model_deploy.py
```

Verás:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Terminal 2 - Iniciar UI:**
```bash
cd c:\Users\jsanc\OneDrive\Documentos\U\ML\final-project-ml
streamlit run mlops_pipeline/src/scripts/prediction_ui.py
```

Verás:
```
You can now view your Streamlit app in your browser.

  URL: http://localhost:8501
```

### Opción 2: Ejecución con Docker (simplificada)

```bash
# Construir imagen
docker build -t alzheimer-ui .

# Ejecutar contenedor
docker run -p 8000:8000 -p 8501:8501 alzheimer-ui
```

El contenedor iniciará automáticamente:
- API en `http://localhost:8000`
- UI en `http://localhost:8501`

### Opción 3: Usando Docker Compose (Recomendado)

Crea archivo `docker-compose.yml`:

```yaml
version: '3.8'

services:
  alzheimer-system:
    build: .
    container_name: alzheimer-prediction-system
    ports:
      - "8000:8000"  # API FastAPI
      - "8501:8501"  # Streamlit UI
    environment:
      - PYTHONUNBUFFERED=1
      - STREAMLIT_SERVER_HEADLESS=true
    volumes:
      - ./mlops_pipeline/artifacts:/app/artifacts:ro
      - ./mlops_pipeline/monitoring_results:/app/monitoring_results
    restart: unless-stopped
```

Luego ejecuta:
```bash
docker-compose up
```

---

## ✨ Características

### 1. 📋 Predicción Individual

- **Interfaz Intuitiva:** Formulario organizado por secciones
- **35 Parámetros:** Todos los factores de riesgo incluidos
- **Valores por Defecto:** Datos de ejemplo precargados
- **Validación:** Campos con rango de valores válidos

**Secciones:**
- ✓ Información General (edad, género, BMI)
- ✓ Factores de Riesgo Médicos (enfermedades, antecedentes)
- ✓ Indicadores Cognitivos (MMSE, memoria, confusión)
- ✓ Valores de Laboratorio (presión, colesterol)
- ✓ Estilos de Vida (alcohol, ejercicio, sueño)
- ✓ Otros Síntomas (comportamiento, tareas)

**Resultado:**
- 🎯 Gauge chart con probabilidad
- 📊 Clasificación de riesgo (Alto/Moderado/Bajo)
- 💡 Recomendaciones personalizadas
- 📈 Historial en la sesión

### 2. 📊 Predicción por Lote

Dos formas de procesamiento:

**Opción A: Cargar CSV**
1. Descarga plantilla
2. Completa datos de múltiples pacientes
3. Sube el archivo
4. Obtén predicciones para todos
5. Descarga resultados

**Opción B: Datos Manuales**
- Plantilla predefinida
- Fácil personalización

**Resultados:**
- ✓ Tabla con todas las predicciones
- ✓ Estadísticas del lote
- ✓ Gráficos de distribución
- ✓ Descarga de resultados

### 3. ℹ️ Información del Sistema

- 🔍 Detalles del modelo
- 📊 Estado de la API
- ⏱️ Timestamps
- 📈 Historial de predicciones
- 📚 Características disponibles

---

## 📖 Guía de Usuario

### Paso 1: Acceder a la Interfaz

1. Abre tu navegador
2. Ve a `http://localhost:8501`
3. Verás la interfaz de bienvenida

### Paso 2: Verificar Conexión a la API

En la parte superior verás:
- 🟢 **API Conectada:** Todo está listo
- 🔴 **API No Disponible:** Verifica que la API esté ejecutándose

### Paso 3: Realizar Predicción Individual

1. **Selecciona la pestaña:** "📋 Predicción Individual"
2. **Completa el formulario:**
   - Usa valores por defecto o personaliza
   - Expande secciones según necesites
3. **Visualiza el resumen** en el panel derecho
4. **Haz clic** en "🔮 Realizar Predicción"
5. **Interpreta los resultados:**
   - 🟢 Bajo riesgo (< 40%)
   - 🟡 Riesgo moderado (40-70%)
   - 🔴 Alto riesgo (> 70%)

### Paso 4: Procesar Lote de Pacientes

1. **Selecciona la pestaña:** "📊 Predicción por Lote"
2. **Descarga la plantilla** (botón azul)
3. **Completa los datos** en Excel o Google Sheets
4. **Sube el archivo** CSV
5. **Haz clic** en "🔮 Predecir Lote"
6. **Descarga resultados** cuando termine

### Paso 5: Consultar Información

1. **Selecciona la pestaña:** "ℹ️ Información del Sistema"
2. **Ver detalles del modelo**
3. **Revisar historial de predicciones**
4. **Exportar si es necesario**

---

## 🎨 Interfaz Visualmente

```
┌─────────────────────────────────────────────────────────────┐
│  🧠 Alzheimer Prediction System                             │
│  ### Sistema Inteligente de Predicción de Alzheimer         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  🟢 Conectada  | Modelo: RandomForest  | Hora: 14:30:25    │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┬─────────────────────────────────────┐
│  📋 Predicción       │ Resumen del Paciente:               │
│  Individual          │ • Edad: 70 años                     │
│                      │ • Género: Masculino                 │
│ [Formulario]         │ • BMI: 25.5                         │
│                      │ • Riesgos: 3 detectados             │
│ [🔮 Predicción]      │ • MMSE: 24/30                       │
└──────────────────────┴─────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  🔴 ALTO RIESGO                                              │
│  75.3%                                                       │
│  Probabilidad de Alzheimer                                   │
│                                                              │
│  Modelo: RandomForest                                        │
│  Clasificación: Positivo (Riesgo)                           │
│  Timestamp: 2025-11-08 14:30:45                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Configuración Avanzada

### Cambiar Puerto Streamlit

```bash
streamlit run mlops_pipeline/src/scripts/prediction_ui.py --server.port 8502
```

### Cambiar URL de API

Edita `prediction_ui.py` línea ~28:
```python
API_URL = "http://tu-servidor.com:8000"
```

### Modo Oscuro

En Streamlit (☰ Menú → Settings → Theme → Dark)

### Ejecutar en Red Local

```bash
streamlit run mlops_pipeline/src/scripts/prediction_ui.py \
  --server.address 0.0.0.0 \
  --server.port 8501
```

Luego accede desde otra máquina:
```
http://tu-ip:8501
```

---

## ⚠️ Solución de Problemas

### ❌ "API no disponible"

**Problema:** Streamlit no puede conectar a la API

**Soluciones:**
1. Verifica que la API está ejecutándose:
   ```bash
   curl http://localhost:8000/health
   ```
2. Si no responde, inicia la API:
   ```bash
   python mlops_pipeline/src/scripts/model_deploy.py
   ```
3. Espera 3 segundos y recarga Streamlit

### ❌ "FileNotFoundError: preprocessor.joblib"

**Problema:** Artefactos no encontrados

**Soluciones:**
1. Verifica que existen:
   ```bash
   ls mlops_pipeline/artifacts/
   ```
2. Si faltan, entrena el modelo:
   ```bash
   python run_pipeline.py --full
   ```

### ❌ Streamlit no carga

**Problema:** Puerto 8501 en uso

**Soluciones:**
```bash
# Ver qué está usando el puerto
netstat -ano | findstr :8501

# Usar puerto diferente
streamlit run prediction_ui.py --server.port 8502
```

### ❌ Docker no inicia

**Problema:** Puertos en uso o dockerfile inválido

**Soluciones:**
```bash
# Detener contenedores anteriores
docker stop $(docker ps -q)

# Reconstruir imagen
docker build --no-cache -t alzheimer-ui .

# Ejecutar con puerto diferente
docker run -p 8000:8000 -p 8502:8501 alzheimer-ui
```

### ⚠️ Respuesta lenta de predicciones

**Causa probable:** API sobrecargada

**Soluciones:**
1. Aumenta timeout en `prediction_ui.py`:
   ```python
   response = requests.post(..., timeout=20)  # De 10 a 20
   ```
2. Reinicia la API
3. Ejecuta predicciones de una en una

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Predicción Rápida

1. Abre Streamlit
2. Deja valores por defecto
3. Haz clic en "🔮 Realizar Predicción"
4. Obtén resultado en segundos

### Ejemplo 2: Predicción Personalizada

1. Ajusta todos los parámetros al paciente real
2. Verifica el resumen en el panel derecho
3. Envía predicción
4. Lee recomendaciones

### Ejemplo 3: Análisis de Lote

1. Descarga plantilla CSV
2. Completa con 10+ pacientes
3. Sube archivo
4. Analiza distribución de riesgos
5. Exporta resultados para informe

---

## 🔐 Notas de Seguridad

⚠️ **IMPORTANTE:**

- Esta es una herramienta de **apoyo diagnóstico**
- **NO reemplaza** evaluación médica profesional
- Los resultados deben ser interpretados por especialistas
- Siempre consulta con un médico para diagnóstico definitivo
- No almacena datos de pacientes (solo en sesión de navegador)

---

## 📞 Soporte

Para problemas o sugerencias:

1. Verifica los logs de la API:
   ```bash
   # En terminal de API
   ```

2. Verifica los logs de Streamlit:
   ```bash
   # En terminal de Streamlit
   ```

3. Consulta el README principal del proyecto

---

## 🚀 Próximas Mejoras

- [ ] Autenticación de usuarios
- [ ] Almacenamiento de datos en base de datos
- [ ] Integración con sistemas médicos (HL7/FHIR)
- [ ] Exportación a PDF
- [ ] Gráficos de comparación entre pacientes
- [ ] API de webhooks para integraciones

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0
