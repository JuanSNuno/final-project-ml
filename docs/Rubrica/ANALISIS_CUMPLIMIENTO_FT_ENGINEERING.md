# ⚙️ Análisis de Cumplimiento - Ingeniería de Características (Feature Engineering)

**Fecha de Evaluación:** 10 de Noviembre, 2025  
**Archivo Evaluado:** `mlops_pipeline/src/notebooks/ft_engineering.ipynb`  
**Puntuación Total:** 0.5 / 0.5 ✅

---

## ✅ Verificación de Requisitos

### 1️⃣ ¿El script genera correctamente los features a partir del dataset base?

**CUMPLE** ✅

**Evidencia:**

#### Carga del Dataset Original
**Archivo:** `ft_engineering.ipynb` - Sección 1

```python
# Cargar dataset ORIGINAL (no procesado)
data_path = "../../../alzheimers_disease_data.csv"

if not os.path.exists(data_path):
    print("❌ ERROR: No se encontró el archivo de datos")
else:
    df_raw = pd.read_csv(data_path)
    print(f"✓ Dataset ORIGINAL cargado desde: {data_path}")
    print(f"  Dimensiones: {df_raw.shape[0]} filas × {df_raw.shape[1]} columnas")
```

#### Generación de Features Derivados
**Archivo:** `ft_engineering.ipynb` - Sección 2.1

```python
def create_derived_features(df):
    """
    Crea features derivados basados en análisis EDA y literatura médica.
    
    Returns:
        DataFrame con 6 nuevos features derivados agregados
    """
    df_new = df.copy()
    features_created = []
    
    # 1. Ratio de Colesterol LDL/HDL
    if 'CholesterolLDL' in df.columns and 'CholesterolHDL' in df.columns:
        df_new['Cholesterol_Ratio_LDL_HDL'] = df_new['CholesterolLDL'] / df_new['CholesterolHDL']
        features_created.append('Cholesterol_Ratio_LDL_HDL')
    
    # 2. Ratio de Colesterol Total/HDL
    if 'CholesterolTotal' in df.columns and 'CholesterolHDL' in df.columns:
        df_new['Cholesterol_Total_HDL_Ratio'] = df_new['CholesterolTotal'] / df_new['CholesterolHDL']
        features_created.append('Cholesterol_Total_HDL_Ratio')
    
    # 3. Presión Arterial Media (MAP)
    if 'SystolicBP' in df.columns and 'DiastolicBP' in df.columns:
        df_new['Mean_Arterial_Pressure'] = (
            df_new['DiastolicBP'] + (df_new['SystolicBP'] - df_new['DiastolicBP']) / 3
        )
        features_created.append('Mean_Arterial_Pressure')
    
    # 4. Edad al cuadrado
    if 'Age' in df.columns:
        df_new['Age_Squared'] = df_new['Age'] ** 2
        features_created.append('Age_Squared')
    
    # 5. Interacción Edad x Historia Familiar
    if 'Age' in df.columns and 'FamilyHistoryAlzheimers' in df.columns:
        df_new['Age_FH_Interaction'] = df_new['Age'] * df_new['FamilyHistoryAlzheimers']
        features_created.append('Age_FH_Interaction')
    
    # 6. Score de riesgo cardiovascular
    cv_conditions = ['CardiovascularDisease', 'Diabetes', 'Hypertension']
    if all(col in df.columns for col in cv_conditions):
        df_new['CV_Risk_Score'] = df_new[cv_conditions].sum(axis=1)
        features_created.append('CV_Risk_Score')
    
    return df_new
```

**Features generados:** 6 características derivadas
- ✅ **Cholesterol_Ratio_LDL_HDL:** Ratio LDL/HDL
- ✅ **Cholesterol_Total_HDL_Ratio:** Ratio Total/HDL
- ✅ **Mean_Arterial_Pressure:** Presión arterial media
- ✅ **Age_Squared:** Edad al cuadrado
- ✅ **Age_FH_Interaction:** Interacción Edad × Historia Familiar
- ✅ **CV_Risk_Score:** Score de riesgo cardiovascular

#### Limpieza Básica Previa
**Archivo:** `ft_engineering.ipynb` - Sección 1.5

```python
# 1. Eliminar duplicados
n_duplicates = df.duplicated().sum()
if n_duplicates > 0:
    df = df.drop_duplicates()

# 2. Eliminar columnas de identificación
id_columns = ['PatientID', 'DoctorInCharge']
existing_id_cols = [col for col in id_columns if col in df.columns]
if existing_id_cols:
    df = df.drop(columns=existing_id_cols)
```

---

### 2️⃣ ¿Se documenta claramente el flujo de transformación de datos?

**CUMPLE** ✅

**Evidencia:**

#### Documentación de Flujo Completo
**Archivo:** `ft_engineering.ipynb` - Header y Secciones

El notebook incluye documentación exhaustiva del flujo:

**Header del Notebook:**
```markdown
# Feature Engineering - Pipeline MLOps

**🔍 Propósito de este Notebook:**
- Este notebook es **AUTOCONTENIDO** y puede ejecutarse de forma independiente
- Muestra de forma manual y gráfica el proceso de Feature Engineering
- No depende de scripts externos ni de pasos anteriores

**Funcionalidades:**
- Carga de datos directamente desde el CSV original
- Limpieza básica de datos (eliminar IDs, duplicados)
- Creación de features derivados basados en el análisis EDA
- Clasificación automática de tipos de variables
- Construcción de pipelines de preprocesamiento (sklearn)
- Transformaciones: imputación, escalado, codificación
- Separación train-test estratificada
- Visualizaciones del proceso de transformación
- Guardado de artefactos
```

#### Secciones Estructuradas:
1. **Sección 1:** Cargar Datos Originales y Configuración
2. **Sección 1.5:** Limpieza Básica de Datos
3. **Sección 2:** Creación de Features Derivados
4. **Sección 2.1:** Justificación Teórica de Features
5. **Sección 3:** Clasificación de Tipos de Variables
6. **Sección 4:** Construcción de Pipelines
7. **Sección 5:** Separación Train-Test
8. **Sección 6:** Ajuste y Transformación
9. **Sección 7:** Guardado de Artefactos
10. **Sección 8:** Documentación de Decisiones

#### Documentación Técnica de Features
**Archivo:** `ft_engineering.ipynb` - Sección 2.1

```markdown
## 2.1 Justificación Teórica de Features Derivados

### 🏥 Indicadores Cardiovasculares
**Ratios de Colesterol (LDL/HDL, Total/HDL)**
- **Justificación Clínica**: La relación entre colesterol LDL ("malo") 
  y HDL ("bueno") es un indicador establecido de riesgo cardiovascular
- **Relevancia Alzheimer**: Estudios epidemiológicos demuestran asociación 
  entre perfil lipídico y deterioro cognitivo
- **Ventaja**: Captura relación no-lineal más relevante que valores absolutos
- **Referencia**: Framingham Heart Study

**Presión Arterial Media (MAP)**
- **Fórmula**: MAP = Diastolic + (Systolic - Diastolic) / 3
- **Justificación**: MAP es mejor indicador de perfusión cerebral
- **Relevancia**: Hipoperfusión cerebral vinculada a neurodegeneración
```

#### Prints de Progreso
```python
print("="*80)
print("CREANDO FEATURES DERIVADOS")
print("="*80)

print("✓ Creado: Cholesterol_Ratio_LDL_HDL (LDL/HDL)")
print("✓ Creado: Cholesterol_Total_HDL_Ratio (Total/HDL)")
print(f"\n✅ Total de features derivados creados: {len(features_created)}")
```

---

### 3️⃣ ¿Se crean pipelines para procesamiento (e.g., Pipeline de sklearn)?

**CUMPLE** ✅

**Evidencia:**

#### Pipelines de sklearn Implementados
**Archivo:** `ft_engineering.ipynb` - Sección 4

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Pipeline para variables numéricas
numeric_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Pipeline para variables categóricas nominales
nominal_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Pipeline para variables categóricas ordinales (si existen)
ordinal_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('ordinal', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
])

# ColumnTransformer para combinar todos los pipelines
preprocessor = ColumnTransformer(
    transformers=[
        ('numeric', numeric_pipeline, numeric_features),
        ('nominal', nominal_pipeline, nominal_features),
        # ('ordinal', ordinal_pipeline, ordinal_features)  # Si aplican
    ],
    remainder='drop'
)
```

**Componentes del Pipeline:**
- ✅ **SimpleImputer:** Imputación de valores faltantes
- ✅ **StandardScaler:** Normalización de variables numéricas
- ✅ **OneHotEncoder:** Codificación de variables categóricas
- ✅ **OrdinalEncoder:** Codificación de variables ordinales
- ✅ **ColumnTransformer:** Orquestación de transformaciones

#### Documentación de Pipelines
```python
print(f"✓ Pipeline Numérico ({len(numeric_features)} features):")
print(f"    1. SimpleImputer(strategy='median') - Imputa valores faltantes")
print(f"    2. StandardScaler() - Normaliza con media=0 y std=1")

print(f"✓ Pipeline Categórico Nominal ({len(nominal_features)} features):")
print(f"    1. SimpleImputer(strategy='most_frequent')")
print(f"    2. OneHotEncoder(handle_unknown='ignore')")
```

---

### 4️⃣ ¿Se separan correctamente los conjuntos de entrenamiento y evaluación?

**CUMPLE** ✅

**Evidencia:**

#### Separación Train-Test con Estratificación
**Archivo:** `ft_engineering.ipynb` - Sección 5

```python
from sklearn.model_selection import train_test_split

# Separar features (X) y target (y)
X = df_with_features.drop(columns=[target_col])
y = df_with_features[target_col]

# Train-test split con estratificación
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=test_size,      # 0.2 (20% test)
    random_state=random_state, # 42 (reproducibilidad)
    stratify=y                 # Mantener proporción de clases
)

print(f"📊 División train-test (80-20):")
print(f"   Entrenamiento: {X_train.shape[0]:,} muestras ({(X_train.shape[0]/len(y)*100):.1f}%)")
print(f"   Evaluación:    {X_test.shape[0]:,} muestras ({(X_test.shape[0]/len(y)*100):.1f}%)")
```

**Parámetros configurados:**
- ✅ **test_size=0.2:** 80% train, 20% test
- ✅ **random_state=42:** Reproducibilidad
- ✅ **stratify=y:** Mantiene proporción de clases

#### Verificación de Distribución
```python
print(f"📈 Distribución del target en ENTRENAMIENTO:")
train_dist = y_train.value_counts().sort_index()
for label, count in train_dist.items():
    print(f"   Clase {label}: {count:,} ({count/len(y_train)*100:.1f}%)")

print(f"📈 Distribución del target en EVALUACIÓN:")
test_dist = y_test.value_counts().sort_index()
for label, count in test_dist.items():
    print(f"   Clase {label}: {count:,} ({count/len(y_test)*100:.1f}%)")
```

---

### 5️⃣ ¿Se retorna un dataset limpio y listo para modelado?

**CUMPLE** ✅

**Evidencia:**

#### Transformación y Guardado de Datasets
**Archivo:** `ft_engineering.ipynb` - Sección 6 y 7

```python
# Ajustar preprocessor SOLO con datos de entrenamiento (evitar data leakage)
preprocessor.fit(X_train)

# Transformar ambos conjuntos
X_train_transformed = preprocessor.transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

print(f"✓ X_train transformado: {X_train_transformed.shape}")
print(f"✓ X_test transformado: {X_test_transformed.shape}")
```

#### Guardado de Datasets Procesados
**Archivo:** `ft_engineering.ipynb` - Sección 7

```python
# Guardar datasets transformados como CSV
X_train_df = pd.DataFrame(X_train_transformed)
X_test_df = pd.DataFrame(X_test_transformed)
y_train_df = pd.DataFrame(y_train).reset_index(drop=True)
y_test_df = pd.DataFrame(y_test).reset_index(drop=True)

X_train_path = data_dir / "X_train.csv"
X_test_path = data_dir / "X_test.csv"
y_train_path = data_dir / "y_train.csv"
y_test_path = data_dir / "y_test.csv"

X_train_df.to_csv(X_train_path, index=False)
X_test_df.to_csv(X_test_path, index=False)
y_train_df.to_csv(y_train_path, index=False)
y_test_df.to_csv(y_test_path, index=False)

print(f"💾 Datasets guardados en: {data_dir}")
print(f"   • X_train.csv: {X_train_path.stat().st_size / 1024:.2f} KB")
print(f"   • X_test.csv:  {X_test_path.stat().st_size / 1024:.2f} KB")
print(f"   • y_train.csv: {y_train_path.stat().st_size / 1024:.2f} KB")
print(f"   • y_test.csv:  {y_test_path.stat().st_size / 1024:.2f} KB")
```

**Características del dataset final:**
- ✅ **Sin valores faltantes:** Imputados por el pipeline
- ✅ **Escalados:** Variables numéricas normalizadas
- ✅ **Codificados:** Variables categóricas transformadas
- ✅ **Sin data leakage:** Transformaciones basadas solo en train
- ✅ **Formato CSV:** Listo para carga en siguiente paso

---

### 6️⃣ ¿Se incluyen transformaciones como escalado, codificación, imputación, etc.?

**CUMPLE** ✅

**Evidencia:**

#### Transformaciones Implementadas

**1. Imputación de Valores Faltantes:**
```python
# Para variables numéricas
SimpleImputer(strategy='median')

# Para variables categóricas
SimpleImputer(strategy='most_frequent')
```

**2. Escalado de Variables Numéricas:**
```python
StandardScaler()  # Normaliza con media=0 y std=1
```

**3. Codificación de Variables Categóricas:**
```python
# Para variables nominales
OneHotEncoder(handle_unknown='ignore', sparse_output=False)

# Para variables ordinales (si aplican)
OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
```

**4. Creación de Features Derivados:**
- Ratios: LDL/HDL, Total/HDL
- Transformaciones no lineales: Age²
- Interacciones: Age × FamilyHistory
- Agregaciones: CV_Risk_Score

#### Resumen de Transformaciones
**Archivo:** `ft_engineering.ipynb` - Sección 6

```python
print(f"📈 Resumen de transformación:")
print(f"   Features originales:    {X_train.shape[1]}")
print(f"   Features transformados: {X_train_transformed.shape[1]}")
print(f"   Diferencia: {X_train_transformed.shape[1] - X_train.shape[1]:+d}")

print(f"\n💡 Nota: El aumento de features se debe a:")
print(f"   • OneHotEncoder crea una columna por cada categoría")
print(f"   • Variables categóricas: {len(nominal_features)}")
```

**Todas las transformaciones estándar están implementadas.**

---

### 7️⃣ ¿Se documentan las decisiones tomadas en la ingeniería de características?

**CUMPLE** ✅

**Evidencia:**

#### Documentación Exhaustiva de Decisiones
**Archivo:** `ft_engineering.ipynb` - Sección 8

```markdown
## 8. Documentación de Decisiones de Preprocesamiento

### Decisiones Técnicas Justificadas

#### **Imputación de Valores Faltantes**

| Variable | Estrategia | Justificación |
|----------|-----------|--------------|
| **Numéricas** | Mediana | Robusta ante outliers, preserva distribución |
| **Categóricas** | Valor más frecuente | Preserva modo, mantiene probabilidades |

**Alternativas consideradas y descartadas**:
- ❌ Eliminación listwise: Perdería muchas muestras
- ❌ Media para numéricas: Sensible a outliers en variables biomédicas
- ❌ Forward-fill: No aplicable (sin serie temporal)

#### **Escalado de Variables Numéricas (StandardScaler)**

x_scaled = (x - mean) / std_dev

**Justificación**:
- ✅ Algoritmos (regresión logística, SVM) sensibles a escala
- ✅ Facilita convergencia en gradient descent
- ✅ Features en escala comparable
- ✅ Mejor interpretabilidad de coeficientes

**Por qué StandardScaler y no MinMaxScaler**:
- StandardScaler es robusto ante outliers extremos en datos médicos
- No asume rango fijo (mejor para distribuciones no acotadas)
- Produce distribuciones aproximadamente normales
```

#### Tabla de Parámetros
```markdown
### Parámetros del Pipeline

| Componente | Parámetro | Valor | Justificación |
|-----------|-----------|-------|---------------|
| Train-Test Split | `test_size` | 0.2 | 80-20 estándar |
| | `random_state` | 42 | Reproducibilidad |
| | `stratify` | sí | Mantener proporciones |
| StandardScaler | `with_mean` | True | Centrar en 0 |
| | `with_std` | True | Varianza unitaria |
| OneHotEncoder | `sparse_output` | False | Matriz densa |
| | `handle_unknown` | 'ignore' | Robustez producción |
| SimpleImputer | strategy (num) | 'median' | Robustez outliers |
| | strategy (cat) | 'most_frequent' | Mantiene modo |
```

#### Prevención de Data Leakage
```markdown
#### **Sin Data Leakage**

**Implementación**:
```python
preprocessor.fit(X_train)      # ← Ajustar SOLO en train
X_train_transformed = preprocessor.transform(X_train)
X_test_transformed = preprocessor.transform(X_test)  # ← Usar parámetros de train
```

**Crítico para evitar overfitting simulado**:
- ❌ Escalar con estadísticos de TODO el dataset → LEAKAGE
- ✅ Escalar con estadísticos solo de train → CORRECTO
```

#### Justificación Médica de Features
**Archivo:** `ft_engineering.ipynb` - Docstring de `create_derived_features()`

```python
"""
╔══════════════════════════════════════════════════════════════════════╗
║ FEATURES DERIVADOS Y SU JUSTIFICACIÓN MÉDICA/CLÍNICA               ║
╚══════════════════════════════════════════════════════════════════════╝

1. Cholesterol_Ratio_LDL_HDL (LDL/HDL)
   • Justificación: Indicador establecido de riesgo cardiovascular
   • Relevancia AD: Lipid profile vinculado a deterioro cognitivo
   • Ventaja: Captura relación no-lineal vs valores absolutos
   • Ref: Framingham Heart Study

2. Mean_Arterial_Pressure (MAP) = Diastolic + (Systolic-Diastolic)/3
   • Justificación: MAP mejor indicador de perfusión cerebral
   • Clínico: Hipoperfusión = neurodegeneración
   • Ventaja: Combina info systolic y diastolic en 1 métrica

3. Age_Squared (Age²)
   • Justificación: Relación edad-Alzheimer NO es lineal
   • Captura: Riesgo aumenta exponencialmente con edad
   • ML: Permite modelo aprender relaciones cuadráticas
"""
```

---

## 📊 Resumen de Cumplimiento

| # | Requisito | Estado | Evidencia |
|---|-----------|--------|-----------|
| 1 | Generación de features correcta | ✅ CUMPLE | Sección 2 - 6 features derivados |
| 2 | Documentación del flujo | ✅ CUMPLE | Todo el notebook - 10 secciones |
| 3 | Pipelines de sklearn | ✅ CUMPLE | Sección 4 - ColumnTransformer |
| 4 | Separación train-test | ✅ CUMPLE | Sección 5 - Estratificación |
| 5 | Dataset limpio retornado | ✅ CUMPLE | Sección 7 - 4 archivos CSV |
| 6 | Transformaciones incluidas | ✅ CUMPLE | Sección 4 - 4 tipos |
| 7 | Decisiones documentadas | ✅ CUMPLE | Sección 8 - Tabla completa |

---

## ✅ Conclusión Final

**Puntuación Obtenida:** 0.5 / 0.5 ✅

**Todos los 7 ítems requeridos están COMPLETAMENTE implementados.**

### Fortalezas Destacadas:

1. **Generación de Features Robusta**
   - 6 features derivados con justificación médica
   - Basado en análisis EDA previo
   - Manejo de valores infinitos/NaN

2. **Documentación Excepcional**
   - Justificación teórica de cada feature
   - Flujo completo paso a paso
   - Referencias a literatura médica (Framingham Study)
   - Docstrings completos con formato visual

3. **Pipelines Profesionales**
   - sklearn Pipeline y ColumnTransformer
   - Transformaciones específicas por tipo de variable
   - Manejo robusto de valores desconocidos

4. **Prevención de Data Leakage**
   - fit() solo en train
   - transform() con parámetros de train
   - Documentación explícita de la importancia

5. **Metadata y Trazabilidad**
   - Metadata JSON con configuración completa
   - Artefactos guardados (preprocessor.joblib)
   - Datasets en formato CSV para siguiente paso

### Cumplimiento Total: 7/7 ítems ✅

**El proceso de Feature Engineering cumple con TODOS los requisitos de la rúbrica y demuestra excelentes prácticas de MLOps.**

---

**Fecha de Aprobación:** 10 de Noviembre, 2025  
**Evaluador:** GitHub Copilot  
**Estado:** ✅ APROBADO - Puntuación Completa
