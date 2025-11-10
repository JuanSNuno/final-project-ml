# Resumen de Unificación de Scripts

## Cambios Realizados

Se han unificado y reorganizado los scripts `run_pipeline.py` y `run_full_system.py` para mejorar el flujo de ejecución y la experiencia del usuario.

---

## `run_pipeline.py` - Script de Preparación de Datos y Entrenamiento

### Propósito
Ejecutar el pipeline MLOps de preparación de datos y entrenamiento de modelos.

### Pasos que ejecuta
1. **PASO 1**: Procesamiento de Datos (`data_processing.py`)
2. **PASO 2**: Feature Engineering (`ft_engineering.py`)
3. **PASO 3**: Entrenamiento y Evaluación (`model_training_evaluation.py`)

### Cambios principales
- ✅ Se eliminaron las opciones `--deploy`, `--streamlit` y `--full` (ya no levanta la API)
- ✅ Se eliminó el paso 4 de monitoreo (drift reporting) - ahora va en `run_full_system.py`
- ✅ Se simplificó la documentación para enfocarse solo en preparación de datos y entrenamiento
- ✅ Se incluye un mensaje informativo sobre dónde ejecutar el monitoreo

### Artifacts Generados
```
- data/processed/cleaned_data.csv
- data/processed/X_train.csv, X_test.csv, y_train.csv, y_test.csv
- artifacts/preprocessor.joblib
- artifacts/best_model.joblib (si no usa --skip-training)
- artifacts/model_metadata.json (si no usa --skip-training)
- artifacts/model_evaluation_results.csv (si no usa --skip-training)
```

### Uso
```bash
# Ejecutar pipeline completo
python run_pipeline.py

# Saltar entrenamiento (útil para testing)
python run_pipeline.py --skip-training
```

---

## `run_full_system.py` - Script Unificado de Sistema Completo

### Propósito
Script unificado que:
1. Verifica si existen los artefactos necesarios
2. **Si no existen**, ejecuta automáticamente el pipeline completo
3. Inicia la API FastAPI
4. Inicia la interfaz Streamlit

### Características principales

#### 1. **Auto-Ejecución del Pipeline**
- ✅ Verifica si `best_model.joblib` y `preprocessor.joblib` existen
- ✅ Si faltan, ejecuta automáticamente el pipeline sin requerir ejecución previa de `run_pipeline.py`
- ✅ El usuario solo necesita ejecutar un comando

#### 2. **Ejecución Automática de Servicios**
- ✅ Inicia API FastAPI en puerto 8000 (en ventana separada en Windows)
- ✅ Inicia Streamlit en puerto 8501 (en foreground)
- ✅ Maneja interrupciones correctamente (CTRL+C)

### Flujo de Ejecución

```
┌─────────────────────────────────────────┐
│  python run_full_system.py              │
└──────────────┬──────────────────────────┘
               │
        ┌──────▼──────┐
        │ Verificar   │
        │ Artefactos  │
        └──────┬──────┘
               │
         ┌─────▼─────┐
    ┌────┤ ¿Existen? ├────┐
    │    └──────────┘    │
    │                    │
NO  │                    │  SÍ
    │                    │
 ┌──▼────────────────┐   │   ┌──────────────────┐
 │ Ejecutar Pipeline │   │   │ Continuar Directamente
 │ 1. Data Process   │   │   └────────┬─────────┘
 │ 2. FT Engineering │   │            │
 │ 3. Training       │   │            │
 └──┬────────────────┘   │   ┌────────▼────────┐
    │                    │   │ Iniciar API     │
    │                    │   │ FastAPI:8000    │
    └──────┬─────────────┘   └────────┬────────┘
           │                           │
           └───────────┬───────────────┘
                       │
                ┌──────▼──────────┐
                │ Iniciar Streamlit
                │ en Puerto 8501  │
                └─────────────────┘
```

### Artifacts Verificados
```
- best_model.joblib (requerido)
- preprocessor.joblib (requerido)
```

### URLs Disponibles Después de Iniciar
```
• API FastAPI
  - Base: http://localhost:8000
  - Documentación: http://localhost:8000/docs
  - Health Check: http://localhost:8000/health

• Streamlit UI
  - URL: http://localhost:8501
```

### Uso
```bash
# Ejecutar sistema completo (ejecuta pipeline si es necesario)
python run_full_system.py
```

---

## Comparativa de Flujos

### Antes (con Scripts Separados)
```
1. python run_pipeline.py --full
   ├── Procesamiento de datos
   ├── Feature Engineering
   ├── Entrenamiento
   ├── Monitoreo de Drift
   └── [ERROR si quería levantar API aquí]

2. python run_full_system.py
   ├── Verifica artefactos
   └── [ERROR si faltan artefactos]
```

### Después (Scripts Unificados)
```
1. python run_pipeline.py
   ├── Procesamiento de datos
   ├── Feature Engineering
   ├── Entrenamiento
   └── Listo para pasar al siguiente paso

2. python run_full_system.py
   ├── Verifica artefactos
   ├── Si faltan: Ejecuta pipeline automáticamente
   ├── Inicia API FastAPI
   └── Inicia Streamlit UI
```

---

## Ventajas de la Nueva Estructura

### Para el Usuario
✅ **Simplicidad**: Un único comando (`run_full_system.py`) para todo
✅ **Inteligencia**: Detecta automáticamente si falta ejecutar el pipeline
✅ **Menos Errores**: No hay que recordar ejecutar dos scripts
✅ **Feedback Claro**: Mensajes informativos sobre cada paso

### Para el Desarrollo
✅ **Separación de Responsabilidades**:
  - `run_pipeline.py`: Enfocado en datos y modelos
  - `run_full_system.py`: Enfocado en servicios y despliegue

✅ **Reutilización**: `run_pipeline.py` puede ejecutarse independientemente
✅ **Mantenibilidad**: Cada script tiene una responsabilidad clara

---

## Próximos Pasos Opcionales

### Para Monitoreo de Drift
Si deseas incluir el monitoreo de data drift después de los servicios, puedes:

1. Crear un script `run_monitoring.py` o
2. Integrarlo en `run_full_system.py` como un paso adicional

Esto permitiría:
```
python run_full_system.py
├── Pipeline (si es necesario)
├── Monitoreo de Drift
├── API FastAPI
└── Streamlit UI
```

---

## Notas Importantes

1. **Rutas de Scripts**: Se asume que los scripts están en:
   ```
   mlops_pipeline/src/scripts/
   ```

2. **Windows vs Linux/Mac**: 
   - En Windows: API se inicia en ventana separada
   - En Linux/Mac: API se inicia en background

3. **Requisitos**:
   - Python 3.7+
   - FastAPI y Streamlit instalados
   - Todos los scripts en su lugar

