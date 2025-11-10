# 📝 Guía de Refactorización del Código

## Funciones a Refactorizar (Prioridad)

### 1. CRÍTICA: model_monitoring.py :: analyze_drift()

**Problema:** Complejidad 16, 84 líneas

**Solución propuesta:**

```python
# Crear clase DriftAnalyzer
class DriftAnalyzer:
    """Analiza data drift usando múltiples métricas estadísticas"""
    
    def __init__(self, baseline_df, thresholds=None):
        self.baseline = baseline_df
        self.thresholds = thresholds or {
            'psi': 0.25,
            'ks': 0.1,
            'chi_square': 0.05
        }
        self.results = {}
    
    def analyze(self, current_df):
        """Ejecuta análisis completo de drift"""
        self._calculate_psi(current_df)
        self._perform_ks_test(current_df)
        self._perform_chi_square(current_df)
        return self._compile_results()
    
    def _calculate_psi(self, current_df):
        """Calcula Population Stability Index"""
        # Lógica PSI
        pass
    
    def _perform_ks_test(self, current_df):
        """Realiza Kolmogorov-Smirnov test"""
        # Lógica KS
        pass
    
    def _perform_chi_square(self, current_df):
        """Realiza Chi-square test"""
        # Lógica Chi-square
        pass
    
    def _compile_results(self):
        """Compila resultados en formato estándar"""
        return {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.results,
            'has_drift': any(v > t for v, t in zip(
                self.results.values(),
                self.thresholds.values()
            ))
        }
```

**Beneficios:**
- Complejidad por método: 3-4
- Reutilizable
- Testeable
- Fácil de extender

---

### 2. CRÍTICA: streamlit_app.py :: load_data()

**Problema:** Complejidad 12, lógica mezclada

**Solución:** Crear data_manager.py

```python
# data_manager.py
import streamlit as st
import pandas as pd
from utilities import get_data_dir, validate_dataframe

class DataManager:
    """Gesiona carga y caché de datos"""
    
    @staticmethod
    @st.cache_data
    def load_data():
        """Carga datos con caché"""
        # Lógica de carga
        pass
    
    @staticmethod
    def validate_data(df):
        """Valida estructura de datos"""
        required_cols = [...]
        validate_dataframe(df, required_cols)
        return True
```

---

### 3. CRÍTICA: streamlit_app.py :: analyze_drift()

**Problema:** Complejidad 11, lógica de UI mezclada

**Solución:** Separar en componentes

```python
# drift_ui.py
class DriftUI:
    def __init__(self, model, data):
        self.model = model
        self.data = data
    
    def render(self):
        st.subheader("Análisis de Drift")
        # UI logic
        results = self._run_analysis()
        self._display_results(results)
    
    def _run_analysis(self):
        # Usa DriftAnalyzer
        pass
    
    def _display_results(self, results):
        # Mostrar resultados
        pass
```

---

## Patrones de Refactorización

### 1. Extract Method
Cuando una función tiene responsabilidades múltiples:
```python
# ANTES
def process_data(df):
    # Validar
    if df.empty: raise ValueError()
    # Transformar
    df['new_col'] = df['col1'] + df['col2']
    # Guardar
    df.to_csv('output.csv')

# DESPUÉS
def process_data(df):
    _validate(df)
    df = _transform(df)
    _save(df)

def _validate(df):
    if df.empty: raise ValueError()

def _transform(df):
    df['new_col'] = df['col1'] + df['col2']
    return df

def _save(df):
    df.to_csv('output.csv')
```

### 2. Extract Class
Para encapsular complejidad:
```python
# CREAR clase especializada
class MetricsCalculator:
    def calculate_accuracy(self, y_true, y_pred):
        pass
    
    def calculate_precision(self, y_true, y_pred):
        pass
    
    def calculate_f1(self, y_true, y_pred):
        pass
```

### 3. Replace Magic Numbers con Constants
```python
# ANTES
if complexity > 10:  # ¿Por qué 10?

# DESPUÉS
MAX_ALLOWED_COMPLEXITY = 10
if complexity > MAX_ALLOWED_COMPLEXITY:
```

---

## Checklist de Refactorización

- [ ] Funciones críticas refactorizadas
  - [ ] model_monitoring.py :: analyze_drift()
  - [ ] streamlit_app.py :: load_data()
  - [ ] streamlit_app.py :: analyze_drift()

- [ ] Crear módulos compartidos
  - [ ] utilities.py
  - [ ] data_manager.py
  - [ ] drift_analyzer.py

- [ ] Mejorar documentación
  - [ ] Agregar docstrings
  - [ ] Agregar type hints
  - [ ] Actualizar README

- [ ] Tests
  - [ ] Unit tests para nuevas clases
  - [ ] Integration tests

- [ ] Validación
  - [ ] Re-ejecutar análisis
  - [ ] Verificar mejoras en SonarCloud
  - [ ] Code review

---

## Recursos

- [Martin Fowler Refactoring](https://refactoring.guru/)
- [Clean Code Principles](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [Python Best Practices](https://pep8.org/)
