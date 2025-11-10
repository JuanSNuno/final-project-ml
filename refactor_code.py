"""
refactor_code.py
Script para ejecutar refactorizaciones automáticas de código
Aplica patrones de mejora identificados en análisis de SonarCloud
"""

import os
from pathlib import Path


def fix_long_lines(file_path, max_length=120):
    """Corrige líneas muy largas"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return False
    
    modified = False
    new_lines = []
    
    for line in lines:
        # Si la línea es muy larga (pero no es un docstring o URL)
        if len(line.rstrip()) > max_length and not line.strip().startswith('"""') and not line.strip().startswith("'''"):
            # Si es un comentario, intenta dividirlo
            if line.strip().startswith('#'):
                # Dividir comentario largo
                comment_text = line.strip()[1:].strip()
                indent = len(line) - len(line.lstrip())
                words = comment_text.split()
                current_line = '#'
                
                for word in words:
                    if len(current_line) + len(word) + 2 > max_length:
                        new_lines.append(' ' * indent + current_line + '\n')
                        current_line = '# ' + word
                    else:
                        current_line += ' ' + word
                
                if current_line.strip() != '#':
                    new_lines.append(' ' * indent + current_line + '\n')
                    modified = True
                    continue
        
        new_lines.append(line)
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    
    return modified


def add_type_hints(file_path):
    """Agrega type hints donde falta"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False
    
    # Este es un ejemplo simple - en producción sería más sofisticado
    # Buscar definiciones de funciones sin type hints en parámetros
    import re
    
    pattern = r'def\s+(\w+)\(([^)]*)\):'
    
    def add_hints(match):
        func_name = match.group(1)
        params = match.group(2)
        
        # Si ya tiene type hints, no modificar
        if ':' in params or params.strip() == '':
            return match.group(0)
        
        # Agregar type hints básicos
        param_list = [p.strip() for p in params.split(',') if p.strip()]
        hinted_params = ', '.join([f"{p}: Any" for p in param_list])
        
        return f"def {func_name}({hinted_params}) -> Any:"
    
    # No aplicar automáticamente para evitar errores
    return False


def improve_docstrings(file_path):
    """Mejora docstrings incompletos"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return False
    
    modified = False
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Si es definición de función sin docstring
        if line.strip().startswith('def ') and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            
            # Checar si tiene docstring
            if not next_line.startswith('"""') and not next_line.startswith("'''"):
                # Agregar docstring vacío como placeholder
                indent = len(lines[i]) - len(lines[i].lstrip()) + 4
                # new_lines.append(' ' * indent + '"""TODO: Agregar docstring"""\n')
                # modified = True
                pass
        
        i += 1
    
    return modified


def create_utility_module():
    """Crea módulo para código compartido (reduce duplicación)"""
    
    utility_code = '''"""
utilities.py
Módulo de utilidades compartidas para reducir código duplicado
"""

from pathlib import Path
import json
from typing import Dict, Any


def load_config(config_name: str = "config.json") -> Dict[str, Any]:
    """Carga archivo de configuración JSON"""
    config_path = Path(__file__).parent.parent / config_name
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    
    return {}


def get_project_root() -> Path:
    """Obtiene la raíz del proyecto"""
    return Path(__file__).parent.parent.parent


def get_data_dir(subdir: str = "") -> Path:
    """Obtiene directorio de datos"""
    root = get_project_root()
    data_dir = root / "mlops_pipeline" / "data" / subdir
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_artifacts_dir() -> Path:
    """Obtiene directorio de artefactos"""
    root = get_project_root()
    artifacts = root / "mlops_pipeline" / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    return artifacts


def validate_dataframe(df, required_columns: list) -> bool:
    """Valida que un dataframe tenga las columnas requeridas"""
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {missing}")
    return True


def save_results(data: Dict[str, Any], filename: str, directory: str = "artifacts") -> Path:
    """Guarda resultados en JSON"""
    output_dir = get_project_root() / "mlops_pipeline" / directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / filename
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return output_file
'''
    
    utilities_path = Path(__file__).parent / 'mlops_pipeline' / 'src' / 'utilities.py'
    
    if not utilities_path.exists():
        utilities_path.parent.mkdir(parents=True, exist_ok=True)
        with open(utilities_path, 'w', encoding='utf-8') as f:
            f.write(utility_code)
        return True
    
    return False


def create_refactor_guide():
    """Crea guía de refactorización detallada"""
    
    guide = '''# 📝 Guía de Refactorización del Código

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
'''
    
    guide_path = Path(__file__).parent / 'docs' / 'REFACTORING_GUIDE.md'
    
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    return guide_path


def main():
    print("\n🔧 Iniciando refactorizaciones automáticas...\n")
    
    project_root = Path(__file__).parent
    scripts_dir = project_root / 'mlops_pipeline' / 'src' / 'scripts'
    
    # Listar archivos
    py_files = list(scripts_dir.glob('*.py'))
    
    # 1. Crear módulo de utilidades
    print("📦 Creando módulo de utilidades compartidas...")
    if create_utility_module():
        print("✅ utilities.py creado")
    else:
        print("✓ utilities.py ya existe")
    
    # 2. Crear guía de refactorización
    print("📝 Creando guía de refactorización...")
    guide_path = create_refactor_guide()
    print(f"✅ Guía creada: {guide_path}")
    
    # 3. Mostrar resumen
    print("\n" + "="*70)
    print("RESUMEN DE REFACTORIZACIONES")
    print("="*70 + "\n")
    
    print("✅ Completadas automáticamente:")
    print("   - Módulo utilities.py (código compartido)")
    print("   - Guía REFACTORING_GUIDE.md")
    
    print("\n⚠️  Requieren refactorización manual:")
    print("   1. model_monitoring.py :: analyze_drift()")
    print("   2. streamlit_app.py :: load_data()")
    print("   3. streamlit_app.py :: analyze_drift()")
    print("   4. ft_engineering.py :: identify_feature_types()")
    print("   5. model_training_evaluation.py :: evaluate_model()")
    
    print("\n📊 Próximos pasos:")
    print("   1. Leer REFACTORING_GUIDE.md")
    print("   2. Ejecutar refactorizaciones manualmente")
    print("   3. Re-ejecutar análisis: python sonar_code_analysis.py")
    print("   4. Validar mejoras en SonarCloud")


if __name__ == "__main__":
    main()
