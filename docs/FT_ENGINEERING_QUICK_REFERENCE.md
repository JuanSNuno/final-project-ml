# 🎯 Feature Engineering - Quick Reference Guide

Una guía rápida de consulta para comprender y usar el Feature Engineering Pipeline.

---

## 📋 Tabla de Acceso Rápido

| Pregunta | Sección | Archivo |
|----------|---------|---------|
| ¿Qué features se crearon? | Sección 2 | ft_engineering.ipynb |
| ¿Por qué cada feature? | Sección 2.1 | ft_engineering.ipynb |
| ¿Cómo funciona el pipeline? | Sección 4 | ft_engineering.ipynb |
| ¿Cómo se dividen los datos? | Sección 5 | ft_engineering.ipynb |
| ¿Qué decisiones se tomaron? | Sección 8.5 | ft_engineering.ipynb |
| ¿Qué artefactos se guardaron? | Sección 8 | ft_engineering.ipynb |

---

## 🔍 6 Features Derivados - Cheat Sheet

### 1️⃣ Cholesterol_Ratio_LDL_HDL
```
Fórmula: LDL / HDL
Rango típico: 0.5 - 5.0
Por qué: Indicador CV establecido
Clínica: ↑ LDL/HDL = ↑ riesgo demencia
```

### 2️⃣ Cholesterol_Total_HDL_Ratio  
```
Fórmula: Total / HDL
Rango típico: 2.0 - 6.0
Por qué: Otro índice CV importante
Clínica: Complementario a LDL/HDL
```

### 3️⃣ Mean_Arterial_Pressure (MAP)
```
Fórmula: Diastolic + (Systolic - Diastolic) / 3
Rango típico: 60 - 120 mmHg
Por qué: Mejor indicador de perfusión cerebral
Clínica: ↓ MAP = ↓ perfusión = ↑ neurodegeneración
```

### 4️⃣ Age_Squared
```
Fórmula: Age²
Por qué: Relación NO-LINEAL edad-Alzheimer
Clínica: Riesgo aumenta exponencialmente
ML: Permite detectar interacciones cuadráticas
```

### 5️⃣ Age_FH_Interaction
```
Fórmula: Age × FamilyHistoryAlzheimers
Por qué: Sinergia edad-genética
Clínica: Gen. predisposición más relevante en edad avanzada
ML: Captura interacción multiplicativa
```

### 6️⃣ CV_Risk_Score
```
Fórmula: CardiovascularDisease + Diabetes + Hypertension
Rango: 0 - 3 (suma de condiciones)
Por qué: Índice agregado de carga CV
Clínica: Mayor score = mayor riesgo demencia
```

---

## 🔧 Pipelines - Configuración Rápida

### Transformadores Aplicados

```python
Numéricos (20 vars)          Categóricos (11 vars)
    ↓                             ↓
SimpleImputer(median)    SimpleImputer(most_frequent)
    ↓                             ↓
StandardScaler()         OneHotEncoder(sparse=False)
    ↓                             ↓
N(μ=0, σ=1)          Vars binarias 0-1
```

### Parámetros Clave

| Parámetro | Valor | Por Qué |
|-----------|-------|--------|
| test_size | 0.2 | Estándar ML (80-20) |
| stratify | sí | Mantiene proporciones clases |
| random_state | 42 | Reproducibilidad |
| StandardScaler | with_mean=True, with_std=True | z-score |
| OneHotEncoder | sparse_output=False | Compatible todos modelos |
| handle_unknown | 'ignore' | Robustez producción |

---

## 📊 Datos Antes y Después

### Antes del Pipeline
```
Muestras: 2,149
Features: 31 (+ 2 IDs)
├── Numéricos: 20 (en diferentes escalas)
├── Categóricos: 9 (sin codificar)
└── IDs: 2 (a eliminar)
```

### Después del Pipeline
```
Train: 1,720 muestras (80%)
Test: 429 muestras (20%)
Features: ~40 
├── Todos escalados a N(0,1)
├── Categóricos codificados (one-hot)
└── Listos para modeling
```

---

## 🛡️ Control de Calidad - Checklist

```
Antes de usar los datos:
☑ ¿Se cargó el CSV original?
☑ ¿Se eliminaron los IDs?
☑ ¿Se crearon 6 features derivados?
☑ ¿Se imputaron valores faltantes?
☑ ¿Se escalaron variables numéricas?
☑ ¿Se codificaron variables categóricas?
☑ ¿Se hizo split 80-20 estratificado?
☑ ¿No hay data leakage?
☑ ¿Se guardaron los artefactos?
```

---

## 📦 Artefactos Generados

### Para Usar Directamente

**1. preprocessor.joblib**
```python
import joblib
preprocessor = joblib.load('preprocessor.joblib')
X_new_transformed = preprocessor.transform(X_new)
```

**2. Datasets CSV**
```python
import pandas as pd
X_train = pd.read_csv('X_train.csv')
X_test = pd.read_csv('X_test.csv')
y_train = pd.read_csv('y_train.csv')
y_test = pd.read_csv('y_test.csv')
```

**3. Metadata JSON**
```python
import json
with open('feature_engineering_metadata.json') as f:
    meta = json.load(f)
print(f"Features originales: {meta['n_features_original']}")
print(f"Features transformados: {meta['n_features_transformed']}")
```

---

## ⚙️ Decisiones de Diseño - TL;DR

| Decisión | Alternativas | Elegida | Por Qué |
|----------|-------------|---------|--------|
| Imputación numérica | Media, mediana, moda | Mediana | Robusta ante outliers |
| Imputación categórica | Moda, eliminación, forward-fill | Moda | Preserva distribución |
| Escalado | MinMax, Robust, Standard | Standard | ML algorithms típicos |
| Codificación | OHE, Label, Ordinal | OneHot | Variables nominales |
| Split ratio | 70-30, 80-20, 90-10 | 80-20 | Estándar, buen balance |
| Estratificación | Sí, No | Sí | Mantiene proporciones |

---

## 🐛 Troubleshooting

### Problema: "No se encuentra el CSV"
```
Solución: Verificar que alzheimers_disease_data.csv está en raíz del proyecto
Ubicación esperada: project_root/alzheimers_disease_data.csv
```

### Problema: "Values infinitos en features"
```
Solución: Ocurre con ratios (LDL/HDL si HDL=0)
Acción: Pipeline imputa estos valores → No es error
```

### Problema: "Preprocessor no funciona en nuevos datos"
```
Solución 1: Asegurar que nuevos datos tienen mismas columnas
Solución 2: Revisar que valores faltantes se imputaron
Solución 3: Revisar que rangos de valores son similares
```

### Problema: "Diferentes resultados en runs diferentes"
```
Solución: Verificar que random_state=42 está configurado
También en: train_test_split, GridSearchCV, modelos con aleatoriedad
```

---

## 🚀 Uso en Próximas Fases

### En Model Training
```python
# Cargar datos ya transformados
X_train = pd.read_csv('mlops_pipeline/data/processed/X_train.csv')
y_train = pd.read_csv('mlops_pipeline/data/processed/y_train.csv').squeeze()

# Entrenar modelo
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
```

### En Producción
```python
# Cargar preprocessor
preprocessor = joblib.load('mlops_pipeline/artifacts/preprocessor.joblib')

# Transformar nuevo paciente
X_new = preprocessor.transform([[age, colesterol, ...]])

# Predecir
prediction = model.predict(X_new)
```

---

## 📈 Métricas de Transformación

```
Estadísticas X_train transformado:
├── Forma: (1,720, ~40)
├── Min:    -3.45
├── Max:    +4.12
├── Mean:   ≈0.02 ✓ (cerca de 0)
└── Std:    ≈0.95 ✓ (cerca de 1)

Verificación: ✅ StandardScaler funcionó correctamente
```

---

## 📚 Referencias de Literatura

- **Framingham Heart Study** - Lipid profiles y demencia
- **Vascular Risk Factors** - Perfusión cerebral y neurodegeneration  
- **Age-Related Cognitive Decline** - Relaciones no-lineales edad
- **Genetic Predisposition** - Interacciones edad-genética

---

## ✅ Checklist Final

```
Antes de proceder a Model Training:

1. ☑ Verificar que 6 features derivados existen
2. ☑ Verificar que preprocessor se carga sin errores
3. ☑ Verificar que X_train y X_test tienen ~40 columnas
4. ☑ Verificar que no hay NaN en datos transformados
5. ☑ Verificar que meta['n_features_transformed'] ≈ 40
6. ☑ Revisar distribuciones post-transformación
7. ☑ Confirmar estratificación en y_train y y_test
```

---

**🎯 Estado Final: LISTO PARA MODEL TRAINING** ✨

---

*Quick Reference v1.0*  
*Proyecto: MLOps Alzheimer Prediction*  
*Última actualización: 9 de noviembre, 2025*
