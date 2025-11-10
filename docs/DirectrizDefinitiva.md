# PROMPT PARA GITHUB COPILOT

## 1. ROL Y CONTEXTO

Eres un ingeniero experto en MLOps y un desarrollador senior de Python. Tu especialidad es tomar notebooks de experimentación y refactorizarlos en pipelines de machine learning modulares, robustos y listos para producción.

Estoy trabajando en un proyecto final de Machine Learning (basado en el documento `PROYECTO FINAL ML.pdf` adjunto). Actualmente, tengo un repositorio con varios archivos `.ipynb` y `.py` (`Cargar_datos.ipynb`, `comprension_eda.ipynb`, `ft_engineering.py`, `model_training_evaluation.py`, `model_deploy.py`, `model_monitoring.py`, y una app de Streamlit).

**El problema principal es que estos archivos no están conectados.** No funcionan como un pipeline secuencial; el output de un script no se convierte en el input del siguiente.

## 2. OBJETIVO PRINCIPAL

Tu tarea es analizar todo el código existente en mi repositorio y refactorizarlo para crear un pipeline secuencial y cohesivo que cumpla con todos los requisitos del PDF. El flujo de datos debe ser explícito: los artefactos (datasets procesados, transformadores, modelos) deben ser guardados por un script y cargados por el siguiente.

## 3. SECUENCIA DEL PIPELINE (REQUISITOS PASO A PASO)

Debes modificar los scripts para que ejecuten la siguiente secuencia lógica:

### Paso 1: `Cargar_datos.ipynb` y `comprension_eda.ipynb`
* **Acción:** Refactoriza la lógica de carga y limpieza de `Cargar_datos.ipynb` en un script `.py` (ej. `src/data_processing.py`).
* [cite_start]Este script debe tomar `Base_de_datos.csv` [cite: 25] como entrada.
* [cite_start]Debe realizar las limpiezas básicas identificadas en el EDA (manejo de nulos, corrección de tipos de datos)[cite: 42, 44].
* **Output:** Debe guardar el dataset limpio (ej. en `data/processed/cleaned_data.csv`).
* [cite_start]El notebook `comprension_eda.ipynb` debe ser actualizado para *usar* este script de limpieza y *solo* realizar análisis exploratorio (gráficos, `describe()`, etc.)[cite: 46, 51, 52], no debe ser parte del pipeline de ejecución.

### Paso 2: `ft_engineering.py`
* **Input:** Debe cargar el `cleaned_data.csv` del paso anterior.
* **Acción:**
    1.  [cite_start]Debe definir el `ColumnTransformer` siguiendo la estructura exacta del PDF (numeric `SimpleImputer`; categoric `SimpleImputer` + `OneHotEncoder`; categoric ordinales `SimpleImputer` + `OrdinalEncoder`) [cite: 61-70].
    2.  Debe separar los datos en conjuntos de entrenamiento y evaluación (train/test split).
    3.  Debe *ajustar* (`.fit()`) el `ColumnTransformer` **solo con los datos de entrenamiento**.
    4.  Debe *transformar* los datos de entrenamiento y evaluación.
* **Output:**
    1.  [cite_start]Guardar el `ColumnTransformer` ajustado como un artefacto (ej. `artifacts/preprocessor.joblib`)[cite: 61].
    2.  Guardar los datasets transformados (ej. `data/processed/X_train.csv`, `data/processed/y_train.csv`, `data/processed/X_test.csv`, `data/processed/y_test.csv`).

### Paso 3: `model_training_evaluation.py`
* **Input:** Debe cargar los datasets de entrenamiento y evaluación (`X_train.csv`, `y_train.csv`, etc.) del Paso 2.
* **Acción:**
    1.  [cite_start]Debe entrenar y evaluar *múltiples* modelos de clasificación/regresión supervisada[cite: 71].
    2.  [cite_start]Debe usar funciones reutilizables para la evaluación (generar métricas, gráficos comparativos)[cite: 77, 78].
    3.  [cite_start]Debe seleccionar el *mejor* modelo basado en las métricas de performance, consistencia y escalabilidad[cite: 72].
* **Output:** Guardar el objeto del *mejor modelo* entrenado como un artefacto (ej. `artifacts/best_model.joblib`).

### Paso 4: `model_deploy.py`
* **Input:**
    1.  [cite_start]Debe cargar el `preprocessor.joblib` del Paso 2[cite: 109].
    2.  [cite_start]Debe cargar el `best_model.joblib` del Paso 3[cite: 109].
* **Acción:**
    1.  [cite_start]Debe crear una API (usando FastAPI o Flask)[cite: 111].
    2.  [cite_start]Debe definir un endpoint `/predict` que reciba datos *crudos* (en JSON)[cite: 111].
    3.  La lógica del endpoint debe:
        a.  Tomar los datos JSON crudos y convertirlos a un DataFrame.
        b.  Aplicar las transformaciones usando el `preprocessor.joblib` cargado.
        c.  Realizar la predicción usando el `best_model.joblib` cargado.
        d.  [cite_start]Retornar la predicción[cite: 110].
    4.  [cite_start]Crear el `Dockerfile` necesario para construir la imagen de esta API[cite: 113, 115].

### Paso 5: `model_monitoring.py` y App de Streamlit
* **Input:**
    1.  [cite_start]El script de monitoreo (`model_monitoring.py`) debe tener acceso a los datos de entrenamiento (ej. `data/processed/X_train.csv`) para usarlos como *baseline*[cite: 83].
    2.  Debe poder recibir nuevos datos de predicción (simulados o reales).
* **Acción:**
    1.  [cite_start]`model_monitoring.py`: Debe implementar las métricas de data drift (PSI, KS test, Chi-cuadrado) [cite: 87-90] para comparar los datos nuevos contra el *baseline* de entrenamiento.
    2.  **Output:** Debe guardar los resultados de estas métricas (ej. en un `json` o `csv` de métricas).
    3.  [cite_start]**App Streamlit:** Refactoriza la app de Streamlit [cite: 91] [cite_start]para que *lea* los resultados del script de monitoreo y visualice los dashboards de data drift (indicadores de alerta, evolución temporal, etc.) [cite: 93-98].

## 4. INSTRUCCIONES ADICIONALES
* [cite_start]**Mantén la Estructura:** No alteres la estructura de carpetas (`mlops_pipeline/src/`)[cite: 17].
* **Modularidad:** Asegúrate de que los scripts `.py` sean importables y contengan funciones claras (ej. `def train_model(...)`, `def load_data(...)`).
* [cite_start]**requirements.txt:** Asegúrate de que el `requirements.txt` [cite: 27, 35] esté completo con todas las librerías necesarias (scikit-learn, pandas, fastapi, uvicorn, streamlit, etc.).
* [cite_start]**SonarCloud:** Prepara el código para que sea analizable por SonarCloud, evitando duplicación de código y siguiendo buenas prácticas[cite: 120, 122].

## 5. TAREA A REALIZAR

Por favor, analiza mi código actual y proporcióna el código **completo y refactorizado** para cada uno de los siguientes archivos, asegurándote de que se conecten en el pipeline descrito:

1.  `src/data_processing.py` (Nuevo, basado en `Cargar_datos.ipynb`)
2.  `src/ft_engineering.py` (Refactorizado)
3.  `src/model_training_evaluation.py` (Refactorizado)
4.  `src/model_deploy.py` (Refactorizado, incluyendo la lógica de API)
5.  `src/model_monitoring.py` (Refactorizado)
6.  `streamlit_app.py` (Refactorizado para leer los outputs de monitoreo)
7.  `Dockerfile` (Para el `model_deploy.py`)
8.  `requirements.txt` (Actualizado)

[cite_start](Opcional: puedes proponer un script `run_pipeline.py` o `setup.bat` [cite: 29] que ejecute los pasos 1, 2 y 3 en secuencia).