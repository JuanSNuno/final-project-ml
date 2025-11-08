"""
test_prediction_ui.py
Script para probar que la interfaz UI funciona correctamente

Verifica:
- Que la API está disponible
- Que los artefactos existen
- Que se puede hacer una predicción
- Que Streamlit está instalado
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def print_banner():
    """Imprime banner"""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║     🧠 TEST PREDICTION UI - PRE-FLIGHT CHECK                  ║
    ╚════════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Verifica versión de Python"""
    print("\n1️⃣  Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor} (se requiere 3.11+)")
        return False

def check_dependencies():
    """Verifica que estén instaladas las dependencias"""
    print("\n2️⃣  Verificando dependencias...")
    
    required = {
        'streamlit': 'Streamlit',
        'fastapi': 'FastAPI',
        'plotly': 'Plotly',
        'pandas': 'Pandas',
        'requests': 'Requests',
        'sklearn': 'Scikit-learn',
        'joblib': 'joblib'
    }
    
    all_ok = True
    for module, name in required.items():
        try:
            __import__(module)
            print(f"   ✓ {name}")
        except ImportError:
            print(f"   ✗ {name} (no instalado)")
            all_ok = False
    
    return all_ok

def check_artifacts():
    """Verifica que existan los artefactos"""
    print("\n3️⃣  Verificando artefactos del modelo...")
    
    artifacts_path = Path("mlops_pipeline/artifacts")
    required_files = ["best_model.joblib", "preprocessor.joblib"]
    
    all_ok = True
    for file in required_files:
        file_path = artifacts_path / file
        if file_path.exists():
            size = file_path.stat().st_size / 1024  # KB
            print(f"   ✓ {file} ({size:.1f} KB)")
        else:
            print(f"   ✗ {file} (no encontrado)")
            all_ok = False
    
    return all_ok

def check_ui_script():
    """Verifica que exista el script de UI"""
    print("\n4️⃣  Verificando script de UI...")
    
    ui_path = Path("mlops_pipeline/src/scripts/prediction_ui.py")
    if ui_path.exists():
        size = ui_path.stat().st_size
        print(f"   ✓ prediction_ui.py ({size} bytes)")
        return True
    else:
        print(f"   ✗ prediction_ui.py (no encontrado)")
        return False

def check_api_available():
    """Verifica que la API esté disponible"""
    print("\n5️⃣  Verificando disponibilidad de API...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("   ✓ API disponible en http://localhost:8000")
            return True
        else:
            print(f"   ⚠ API respondió con código {response.status_code}")
            print("   💡 Inicia API con: python mlops_pipeline/src/scripts/model_deploy.py")
            return False
    except requests.exceptions.ConnectionError:
        print("   ⚠ API no disponible (esto es OK para prueba)")
        print("   💡 Inicia API con: python mlops_pipeline/src/scripts/model_deploy.py")
        return False

def test_prediction():
    """Prueba hacer una predicción"""
    print("\n6️⃣  Probando predicción...")
    
    try:
        payload = {
            "Age": 70.0,
            "Gender": 1,
            "Ethnicity": 0,
            "EducationLevel": 2,
            "BMI": 25.5,
            "Smoking": 0,
            "AlcoholConsumption": 5.0,
            "PhysicalActivity": 6.5,
            "DietQuality": 7.0,
            "SleepQuality": 7.5,
            "FamilyHistoryAlzheimers": 1,
            "CardiovascularDisease": 0,
            "Diabetes": 0,
            "Depression": 0,
            "HeadInjury": 0,
            "Hypertension": 1,
            "SystolicBP": 140,
            "DiastolicBP": 85,
            "CholesterolTotal": 220.0,
            "CholesterolLDL": 130.0,
            "CholesterolHDL": 45.0,
            "CholesterolTriglycerides": 180.0,
            "MMSE": 24.0,
            "FunctionalAssessment": 7.5,
            "MemoryComplaints": 1,
            "BehavioralProblems": 0,
            "ADL": 5.5,
            "Confusion": 0,
            "Disorientation": 0,
            "PersonalityChanges": 0,
            "DifficultyCompletingTasks": 1,
            "Forgetfulness": 1
        }
        
        response = requests.post(
            "http://localhost:8000/predict",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            prob = result.get("probability", 0)
            print(f"   ✓ Predicción exitosa: {prob*100:.1f}% riesgo")
            return True
        else:
            print(f"   ✗ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ⚠ No se pudo probar (API no disponible): {e}")
        return False

def suggest_next_steps(checks):
    """Sugiere próximos pasos"""
    print("\n" + "="*70)
    
    if all(checks.values()):
        print("✅ TODOS LOS CHECKS PASARON")
        print("\nPróximos pasos:")
        print("1. Abre http://localhost:8501 en tu navegador")
        print("2. Completa el formulario de predicción")
        print("3. Haz clic en '🔮 Realizar Predicción'")
    else:
        print("⚠️  ALGUNOS CHECKS FALLARON")
        
        if not checks['api']:
            print("\n⚠️  La API no está disponible")
            print("   Terminal 1: python mlops_pipeline/src/scripts/model_deploy.py")
        
        if not checks['dependencies']:
            print("\n⚠️  Faltan dependencias")
            print("   pip install -r requirements.txt")
        
        if not checks['artifacts']:
            print("\n⚠️  Faltan artefactos del modelo")
            print("   python run_pipeline.py --full")

def main():
    """Función principal"""
    print_banner()
    
    checks = {
        'python': check_python_version(),
        'dependencies': check_dependencies(),
        'artifacts': check_artifacts(),
        'ui_script': check_ui_script(),
        'api': check_api_available(),
    }
    
    print("\n" + "="*70)
    print("RESUMEN DE CHECKS")
    print("="*70)
    
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check.upper()}")
    
    # Test de predicción solo si API está disponible
    if checks['api']:
        prediction_ok = test_prediction()
        checks['prediction'] = prediction_ok
    
    # Sugerencias
    suggest_next_steps(checks)
    
    print("\n" + "="*70)
    
    if all(checks.values()):
        print("\n🎉 Sistema listo para usar!")
        print("\nEjecuta:")
        print("   python run_full_system.py")
        sys.exit(0)
    else:
        print("\n❌ Soluciona los problemas anteriores antes de continuar")
        sys.exit(1)

if __name__ == "__main__":
    main()
