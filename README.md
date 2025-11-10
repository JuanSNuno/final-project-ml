# 🧠 Sistema MLOps para Predicción de Alzheimer

**Pipeline completo de Machine Learning con monitoreo de Data Drift**

[![Python](https://img.shields.io/badge/Python-3.11.9-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2.2-orange.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [Caso de Negocio](#-caso-de-negocio)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Componentes Principales](#-componentes-principales)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso del Sistema](#-uso-del-sistema)
- [Resultados y Hallazgos](#-resultados-y-hallazgos)
- [Monitoreo y Alertas](#-monitoreo-y-alertas)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)

---

## 🎯 Caso de Negocio

### Contexto

La detección temprana de la enfermedad de Alzheimer es crucial para mejorar la calidad de vida de los pacientes y optimizar los tratamientos.

### Problema

Los métodos de diagnóstico actuales presentan limitaciones:
- **Costo elevado** de pruebas especializadas
- **Acceso limitado** a especialistas
- **Diagnóstico tardío** cuando los síntomas ya son evidentes
- **Variabilidad** en la interpretación clínica

### Solución Propuesta

Sistema automatizado de Machine Learning que:
1. **Predice el riesgo** de Alzheimer basándose en datos clínicos y de estilo de vida
2. **Monitorea continuamente** la calidad de los datos y rendimiento del modelo
3. **Detecta drift** en distribuciones para asegurar predicciones confiables
4. **Genera alertas** automáticas cuando se requiere reentrenamiento

### Impacto Esperado

- 🎯 **Detección temprana**: Identificar pacientes en riesgo antes de síntomas severos
- 💰 **Reducción de costos**: Priorizar recursos médicos
- 📊 **Escalabilidad**: Desplegable en cualquier centro de salud
- 🔄 **Sostenibilidad**: Monitoreo continuo asegura precisión a largo plazo

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                        CAPA DE DATOS                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   Raw Data     │→│  Validation    │→│  Clean Data    │   │
│  │  (CSV/DB)      │  │   & Quality    │  │  (Processed)   │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   CAPA DE PREPROCESAMIENTO                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ColumnTransformer (scikit-learn)                       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │   │
│  │  │ Numeric  │  │ Nominal  │  │ Ordinal  │             │   │
│  │  │ Pipeline │  │ Pipeline │  │ Pipeline │             │   │
│  │  └──────────┘  └──────────┘  └──────────┘             │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   CAPA DE MODELADO                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │  Logistic  │  │   Random   │  │  Gradient  │               │
│  │ Regression │  │   Forest   │  │  Boosting  │  + 2 más      │
│  └────────────┘  └────────────┘  └────────────┘               │
│                          ↓                                       │
│  ┌──────────────────────────────────────────────┐              │
│  │  Model Selection (Best by F1-Score)         │              │
│  │  🏆 Gradient Boosting: 94.65% accuracy      │              │
│  └──────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   CAPA DE MONITOREO                              │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   Data Drift   │  │   Alertas      │  │  Recomendaciones│   │
│  │   Detection    │→│   Automáticas  │→│  Reentrenamiento│   │
│  │   (PSI, KS)    │  │   (Semáforo)   │  │   (Triggers)    │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   CAPA DE VISUALIZACIÓN                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │        Streamlit Dashboard                                │  │
│  │  - Métricas en tiempo real                                │  │
│  │  - Comparación de distribuciones                          │  │
│  │  - Alertas visuales                                       │  │
│  │  - Recomendaciones automatizadas                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
final-project-ml/
│
├── mlops_pipeline/
│   └── src/
│       ├── comprension_eda.ipynb          # Análisis exploratorio genérico
│       ├── ft_engineering.ipynb           # Feature engineering + modelado
│       ├── model_monitoring.ipynb         # Monitoreo de data drift
│       ├── streamlit_app.py               # Dashboard interactivo
│       └── set_up.bat                     # Script de configuración
│
├── config.json                            # Configuración general
├── requirements.txt                       # Dependencias Python
├── README.md                              # Este archivo
└── alzheimers_disease_data.csv           # Dataset principal
```

---

## 🔧 Componentes Principales

### 1. **comprension_eda.ipynb** - Análisis Exploratorio

✅ Detección automática de tipos de variables  
✅ Estadísticas descriptivas completas  
✅ Análisis de valores faltantes  
✅ Detección de outliers (método IQR)  
✅ Visualización de distribuciones  
✅ Matriz de correlaciones mejorada  

### 2. **ft_engineering.ipynb** - Ingeniería de Características

**Pipeline de Preprocesamiento**:
- Numeric Pipeline: Imputer (median) + StandardScaler
- Nominal Pipeline: Imputer (mode) + OneHotEncoder
- Ordinal Pipeline: Imputer (mode) + OrdinalEncoder

**Modelos Entrenados**:
| Modelo | Accuracy | F1-Score |
|--------|----------|----------|
| **Gradient Boosting** 🏆 | **94.65%** | **94.65%** |
| Random Forest | 94.19% | 94.14% |
| SVM | 83.49% | 83.31% |
| Logistic Regression | 81.63% | 81.61% |
| KNN | 70.70% | 69.02% |

### 3. **model_monitoring.ipynb** - Monitoreo de Drift

**Métricas Implementadas**:
- **PSI** (Population Stability Index)
- **KS Test** (Kolmogorov-Smirnov)
- **JS Divergence** (Jensen-Shannon)
- **Chi-Square** test para categóricas

**Sistema de Alertas**:
- 🟢 **OK**: PSI < 0.1 → Monitoreo regular
- 🟡 **MODERADO**: 0.1 ≤ PSI < 0.2 → Aumentar frecuencia
- 🔴 **CRÍTICO**: PSI ≥ 0.2 → Reentrenamiento URGENTE

### 4. **streamlit_app.py** - Dashboard Interactivo

**Funcionalidades**:
- 📊 Dashboard General con métricas clave
- 📈 Comparación de distribuciones interactiva
- 📋 Tabla detallada con filtros
- 💡 Recomendaciones automatizadas

**Ejecutar la aplicación**:
```bash
streamlit run mlops_pipeline/src/streamlit_app.py
```

---

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.11.9
- Git

### Instalación

#### 1. Clonar el repositorio
```bash
git clone https://github.com/JuanSNuno/final-project-ml.git
cd final-project-ml
```

#### 2. Ejecutar script de configuración (Windows)
```bash
set_up.bat
```

#### 3. Configuración manual (alternativa)
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

---

## 📊 Uso del Sistema

### Workflow Completo

#### **Paso 1: Análisis Exploratorio**
```bash
jupyter notebook mlops_pipeline/src/comprension_eda.ipynb
```
- Ejecutar todas las celdas
- Revisar visualizaciones y estadísticas
- Identificar características importantes

#### **Paso 2: Feature Engineering y Modelado**
```bash
jupyter notebook mlops_pipeline/src/ft_engineering.ipynb
```
- Ejecutar pipeline de preprocesamiento
- Entrenar 5 modelos de clasificación
- Seleccionar mejor modelo (Gradient Boosting)

#### **Paso 3: Monitoreo de Drift**
```bash
jupyter notebook mlops_pipeline/src/model_monitoring.ipynb
```
- Cargar datos de referencia y actuales
- Calcular métricas de drift
- Generar reporte de alertas

#### **Paso 4: Dashboard Interactivo**
```bash
streamlit run mlops_pipeline/src/streamlit_app.py
```
- Abrir en navegador: `http://localhost:8501`
- Explorar visualizaciones
- Descargar reportes

---

## 🔍 Resultados y Hallazgos

### Dataset

- **Registros**: 2,149 pacientes
- **Variables**: 35 (33 features + 1 target + 1 ID)
- **Target**: Diagnosis (0 = No Alzheimer, 1 = Alzheimer)
- **Distribución**: 64.6% Clase 0, 35.4% Clase 1

### Análisis Exploratorio - Hallazgos

**Variables más Correlacionadas con Diagnosis**:
| Variable | Correlación | Interpretación |
|----------|-------------|----------------|
| MMSE | -0.62 | Fuerte negativa |
| FunctionalAssessment | -0.48 | Negativa moderada |
| MemoryComplaints | +0.35 | Positiva moderada |

### Performance del Mejor Modelo

**Gradient Boosting**:
```
Train Accuracy: 96.80%
Test Accuracy:  94.65%
Precision:      94.64%
Recall:         94.65%
F1-Score:       94.65%
```

**Ventajas**:
- ✅ Balance bias-variance óptimo (2.15% diferencia train-test)
- ✅ Excelente generalización
- ✅ Robusto a outliers
- ✅ Maneja bien desbalanceo de clases

### Monitoreo de Drift

**Resultados de Simulación**:
```
Score de Riesgo: 3/99 (3.0%)
Variables críticas: 0
Variables moderadas: 1
Variables OK: 32 (97%)

Nivel de Riesgo: 🟢 BAJO
Acción: Continuar monitoreo regular
```

---

## 🚨 Monitoreo y Alertas

### Sistema de Alertas de Tres Niveles

#### 🟢 **VERDE (OK)**
- PSI < 0.1
- Acción: Continuar monitoreo regular
- Frecuencia: Revisión quincenal

#### 🟡 **AMARILLO (Moderado)**
- 0.1 ≤ PSI < 0.2
- Acción: Aumentar frecuencia de monitoreo
- Frecuencia: Revisión semanal

#### 🔴 **ROJO (Crítico)**
- PSI ≥ 0.2
- Acción: URGENTE - Reentrenamiento del modelo
- Frecuencia: Monitoreo diario

---

## 🛠️ Tecnologías Utilizadas

### Core
- Python 3.11.9
- Jupyter Notebook
- Git

### Machine Learning
- scikit-learn 1.2.2
- pandas 1.5.3
- numpy 1.24.3
- scipy 1.15.3

### Visualización
- matplotlib 3.7.1
- seaborn 0.12.2
- Streamlit

---

## 📚 Referencias

1. **scikit-learn**: https://scikit-learn.org/
2. **Streamlit**: https://docs.streamlit.io/
3. **Population Stability Index**: [PSI Guide](https://www.listendata.com/2015/05/population-stability-index.html)
4. **MLOps**: [Google MLOps Guide](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

Desarrollado por: Juan S. Nuño | Rama: `developer`

</div>