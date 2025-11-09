# 📚 Arquitectura: Notebooks vs Scripts

**Fecha:** 9 de Noviembre, 2025  
**Proyecto:** Sistema MLOps para Predicción de Alzheimer

---

## 🎯 Filosofía del Proyecto

Este proyecto mantiene **DOS flujos de trabajo paralelos e independientes**:

### 1. 📓 Notebooks (Revisión Manual)
**Directorio:** `mlops_pipeline/src/notebooks/`

### 2. ⚙️ Scripts (Automatización)
**Directorio:** `mlops_pipeline/src/scripts/`

---

## 📓 Notebooks: Para Revisión y Comprensión

### Propósito

Los notebooks son **herramientas educativas y de revisión** que permiten:

- ✅ **Ejecución paso a paso** con explicaciones
- ✅ **Visualizaciones** de cada etapa del proceso
- ✅ **Experimentación** con parámetros
- ✅ **Comprensión profunda** del pipeline
- ✅ **Auditoría manual** del proceso

### Características Clave

#### 🔸 Autocontenidos
Cada notebook es **completamente independiente**:
- NO depende de notebooks anteriores
- NO depende de scripts externos
- NO requiere ejecución secuencial
- Carga datos desde el CSV original

#### 🔸 Educativos
- Comentarios extensos
- Explicaciones de cada paso
- Visualizaciones gráficas
- Interpretación de resultados

#### 🔸 Interactivos
- Permite modificar parámetros
- Experimentar con diferentes configuraciones
- Ver resultados inmediatos

---

## ⚙️ Scripts: Para Automatización

### Propósito

Los scripts son **herramientas de producción** que permiten:

- ✅ **Ejecución completa** del pipeline
- ✅ **Automatización** sin intervención manual
- ✅ **Reproducibilidad** exacta
- ✅ **Construcción de imagen Docker**
- ✅ **Deployment en producción**

### Características Clave

#### 🔸 Optimizados
- Código minimalista
- Sin visualizaciones innecesarias
- Enfocados en eficiencia

#### 🔸 Secuenciales
- Dependen de pasos anteriores
- Usan artefactos generados previamente
- Ejecución ordenada del pipeline

#### 🔸 Productivos
- Logging estructurado
- Manejo de errores robusto
- Preparados para automatización

---

## 📊 Comparación Detallada

| Aspecto | Notebooks 📓 | Scripts ⚙️ |
|---------|-------------|-----------|
| **Independencia** | ✅ Totalmente independientes | ❌ Dependen de pasos anteriores |
| **Carga de Datos** | Desde CSV original | Desde artefactos procesados |
| **Visualizaciones** | ✅ Múltiples gráficos | ❌ Mínimas o ninguna |
| **Documentación** | ✅ Extensiva inline | ⚠️ Docstrings básicos |
| **Propósito** | Educación y revisión | Producción y automatización |
| **Ejecución** | Manual, interactiva | Automática, en batch |
| **Audiencia** | Data Scientists, revisores | Pipeline automatizado, Docker |
| **Experimentación** | ✅ Fácil modificar y probar | ❌ Requiere editar código |
| **Tiempo de Ejecución** | Puede ser lento (visualizaciones) | Optimizado para velocidad |

---

## 🗂️ Estructura de Archivos

### Notebooks (`/notebooks/`)

```
notebooks/
├── 01_Cargar_datos.ipynb           # Carga y exploración inicial
├── 02_comprension_eda.ipynb        # Análisis exploratorio completo
├── 03_ft_engineering.ipynb         # Feature engineering ⭐ AUTOCONTENIDO
├── 04_model_training.ipynb         # Entrenamiento de modelos
├── 05_model_evaluation.ipynb       # Evaluación y métricas
├── 06_model_monitoring.ipynb       # Monitoreo y drift detection
└── 07_model_deploy.ipynb           # Deployment y predicciones
```

**Cada notebook:**
- Carga datos desde el CSV original
- Realiza su propia limpieza básica
- NO depende de notebooks anteriores
- Puede ejecutarse de forma aislada

---

### Scripts (`/scripts/`)

```
scripts/
├── data_processing.py              # Paso 1: Limpieza
│   └── Genera: cleaned_data.csv
│
├── ft_engineering.py               # Paso 2: Feature Engineering
│   ├── Lee: cleaned_data.csv
│   └── Genera: preprocessor.joblib, X_train.csv, X_test.csv
│
├── model_training_evaluation.py   # Paso 3: Entrenamiento
│   ├── Lee: X_train.csv, y_train.csv, preprocessor.joblib
│   └── Genera: best_model.joblib, metrics.json
│
├── model_monitoring.py             # Paso 4: Monitoreo
│   ├── Lee: best_model.joblib, nuevos datos
│   └── Genera: drift_report.csv
│
└── model_deploy.py                 # Paso 5: Deployment
    ├── Lee: best_model.joblib, preprocessor.joblib
    └── Genera: API/servicio
```

**Cada script:**
- Depende del output del script anterior
- Lee artefactos generados previamente
- Optimizado para ejecución secuencial
- Sin visualizaciones pesadas

---

## 🔄 Flujos de Trabajo

### Flujo 1: Revisión Manual con Notebooks

**Caso de uso:** Auditoría, comprensión, experimentación

```bash
# Abrir cualquier notebook en cualquier orden
jupyter notebook mlops_pipeline/src/notebooks/03_ft_engineering.ipynb

# Ejecutar celdas interactivamente
# Ver visualizaciones
# Modificar parámetros
# Experimentar
```

**Ventajas:**
- ✅ No requiere configuración previa
- ✅ Resultados visuales inmediatos
- ✅ Fácil de entender
- ✅ Ideal para presentaciones y demos

---

### Flujo 2: Ejecución Automatizada con Scripts

**Caso de uso:** Pipeline completo, producción, Docker

```bash
# Ejecutar pipeline completo (en orden)
python mlops_pipeline/src/scripts/data_processing.py
python mlops_pipeline/src/scripts/ft_engineering.py
python mlops_pipeline/src/scripts/model_training_evaluation.py
python mlops_pipeline/src/scripts/model_monitoring.py
python mlops_pipeline/src/scripts/model_deploy.py

# O usar el script de ejecución completa
python run_pipeline.py

# O construir imagen Docker
docker-compose up --build
```

**Ventajas:**
- ✅ Reproducibilidad exacta
- ✅ Automatización completa
- ✅ Listo para producción
- ✅ Integración con CI/CD

---

## 📝 Ejemplo: Feature Engineering

### Notebook: `03_ft_engineering.ipynb`

```python
# CARGA DATOS ORIGINALES
df_raw = pd.read_csv("../../alzheimers_disease_data.csv")

# LIMPIEZA DENTRO DEL NOTEBOOK
df = df_raw.drop(columns=['PatientID', 'DoctorInCharge'])
df = df.drop_duplicates()

# CREAR FEATURES DERIVADOS
df['Cholesterol_Ratio'] = df['CholesterolLDL'] / df['CholesterolHDL']

# VISUALIZAR
plt.hist(df['Cholesterol_Ratio'])
plt.show()

# CONSTRUIR PIPELINE
preprocessor = ColumnTransformer(...)
preprocessor.fit(X_train)

# TRANSFORMAR
X_train_transformed = preprocessor.transform(X_train)

# VISUALIZAR RESULTADO
plt.hist(X_train_transformed[:, 0])
plt.show()

# GUARDAR (opcional, para uso posterior)
joblib.dump(preprocessor, 'preprocessor.joblib')
```

**Características:**
- ✅ Autocontenido
- ✅ Con visualizaciones
- ✅ Paso a paso explicado

---

### Script: `ft_engineering.py`

```python
# LEE DATOS PROCESADOS DEL PASO ANTERIOR
df = pd.read_csv("data/processed/cleaned_data.csv")

# CREAR FEATURES DERIVADOS
df = create_derived_features(df)

# CONSTRUIR PIPELINE
preprocessor = create_preprocessor(...)
preprocessor.fit(X_train)

# TRANSFORMAR
X_train_transformed = preprocessor.transform(X_train)

# GUARDAR ARTEFACTOS (obligatorio para siguiente paso)
joblib.dump(preprocessor, 'artifacts/preprocessor.joblib')
X_train_df.to_csv('data/processed/X_train.csv')
```

**Características:**
- ✅ Optimizado
- ✅ Sin visualizaciones
- ✅ Genera artefactos para siguiente paso

---

## 🎓 Guía para Usuarios

### Si eres Data Scientist / Revisor / Auditor

**Usa los NOTEBOOKS:**

1. Abre cualquier notebook en VS Code o Jupyter
2. Ejecuta celda por celda
3. Observa visualizaciones
4. Modifica parámetros y experimenta
5. Comprende cada paso del proceso

**No necesitas:**
- Ejecutar notebooks en orden
- Tener artefactos previos
- Configuración especial

---

### Si eres DevOps / MLOps Engineer

**Usa los SCRIPTS:**

1. Ejecuta el pipeline completo:
   ```bash
   python run_pipeline.py
   ```

2. O construye Docker:
   ```bash
   docker-compose up --build
   ```

3. Los scripts se ejecutan en orden y generan todos los artefactos necesarios

**Necesitas:**
- Ejecutar scripts en orden secuencial
- Tener el CSV original en la ruta correcta
- Configuración en `config.json`

---

## ✅ Checklist de Verificación

### Para Notebooks

- [ ] Cada notebook puede ejecutarse de forma aislada
- [ ] No depende de notebooks anteriores
- [ ] Carga datos desde CSV original
- [ ] Incluye visualizaciones relevantes
- [ ] Tiene comentarios y explicaciones extensas
- [ ] Permite experimentación fácil

### Para Scripts

- [ ] Se ejecutan en orden secuencial
- [ ] Leen artefactos del paso anterior
- [ ] Generan artefactos para el siguiente paso
- [ ] Tienen logging apropiado
- [ ] Manejo de errores robusto
- [ ] Optimizados para producción

---

## 🔍 Preguntas Frecuentes

### ¿Por qué mantener dos versiones?

**Notebooks:** Para humanos (comprensión, revisión, experimentación)  
**Scripts:** Para máquinas (automatización, producción, CI/CD)

### ¿Los notebooks y scripts producen los mismos resultados?

Sí, cuando se ejecutan con los mismos parámetros y datos. Los notebooks muestran el proceso de forma educativa, los scripts lo automatizan.

### ¿Debo mantener ambos sincronizados?

Idealmente sí, pero:
- **Notebooks:** Pueden tener más visualizaciones y explicaciones
- **Scripts:** Pueden tener optimizaciones de producción

La lógica core debe ser la misma.

### ¿Qué uso para desarrollo y pruebas?

**Desarrollo inicial:** Notebooks (experimentación rápida)  
**Pruebas finales:** Scripts (verificar automatización)

### ¿Qué incluyo en Docker?

Solo los **SCRIPTS**. Los notebooks no van en la imagen Docker de producción.

---

## 📚 Referencias

- **Notebooks:** `mlops_pipeline/src/notebooks/`
- **Scripts:** `mlops_pipeline/src/scripts/`
- **Documentación EDA:** `docs/README_PIPELINE.md`
- **Guía de ejecución:** `docs/QUICKSTART.md`

---

## 🎯 Resumen Ejecutivo

| Característica | Notebooks 📓 | Scripts ⚙️ |
|----------------|-------------|-----------|
| **Para quién** | Humanos (revisión) | Máquinas (automatización) |
| **Independencia** | ✅ Total | ❌ Secuencial |
| **Visualizaciones** | ✅ Extensivas | ❌ Mínimas |
| **Uso principal** | Educación, auditoría | Producción, Docker |
| **Ejecución** | Manual, interactiva | Automática, batch |
| **En Docker** | ❌ No | ✅ Sí |

**Filosofía:** "Notebooks para mostrar, Scripts para producir"

---

**Documento actualizado:** 9 de Noviembre, 2025  
**Versión:** 2.0  
**Estado:** ✅ Implementado
