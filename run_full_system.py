"""
run_full_system.py
Script unificado que ejecuta el pipeline MLOps, genera reportes de drift y luego inicia 
la API y UIs de Streamlit

Este script:
1. Verifica si existen los artefactos necesarios
2. Si no existen, ejecuta automáticamente el pipeline completo
3. Ejecuta el monitoreo de data drift
4. Inicia la API FastAPI
5. Inicia la interfaz Streamlit de predicción
6. Inicia la interfaz Streamlit de reportes de drift

Servicios disponibles:
- API FastAPI: http://localhost:8000
  - Documentación: http://localhost:8000/docs
- UI Predicción: http://localhost:8501
- UI Reporte Drift: http://localhost:8502

Uso:
    python run_full_system.py
"""

import subprocess
import time
import os
import sys
import platform
from pathlib import Path

def print_banner():
    """Imprime banner de bienvenida"""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║     🧠 ALZHEIMER PREDICTION SYSTEM - FULL DEPLOYMENT          ║
    ║                                                                ║
    ║  Starting all services...                                     ║
    ╚════════════════════════════════════════════════════════════════╝
    """)

def print_service_info(service: str, port: int, url: str):
    """Imprime información de servicio"""
    print(f"\n✓ {service}")
    print(f"  Puerto: {port}")
    print(f"  URL: {url}")

def print_section(title):
    """Imprime una sección visual"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def run_script(script_path, description):
    """
    Ejecuta un script de Python y maneja errores
    
    Args:
        script_path: Path al script a ejecutar
        description: Descripción del paso
    
    Returns:
        bool: True si exitoso, False si falló
    """
    print_section(description)
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✅ {description} completado exitosamente\n")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error en {description}")
        print(f"Código de salida: {e.returncode}\n")
        return False
    
    except Exception as e:
        print(f"\n❌ Error inesperado en {description}: {e}\n")
        return False

def run_pipeline_if_needed():
    """
    Ejecuta el pipeline MLOps si no existen los artefactos necesarios
    
    Returns:
        bool: True si el pipeline se ejecutó o ya existían artefactos, False si hubo error
    """
    artifacts_path = Path("mlops_pipeline/artifacts")
    
    required_files = [
        "best_model.joblib",
        "preprocessor.joblib"
    ]
    
    print("\n🔍 Verificando artefactos necesarios...")
    
    missing_files = []
    for file in required_files:
        file_path = artifacts_path / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ FALTA: {file}")
            missing_files.append(file)
    
    # Si no faltan archivos, todo está bien
    if not missing_files:
        print("  ✓ Todos los artefactos están presentes")
        return True
    
    # Si faltan artefactos, ejecutar el pipeline
    print(f"\n⚠️  Faltan {len(missing_files)} artefacto(s)")
    print("   Se ejecutará automáticamente el pipeline MLOps...\n")
    
    time.sleep(2)
    
    # Definir rutas de scripts
    project_root = Path(__file__).parent
    src_dir = project_root / "mlops_pipeline" / "src" / "scripts"
    
    scripts = [
        (src_dir / "data_processing.py", "PASO 1: Procesamiento de Datos"),
        (src_dir / "ft_engineering.py", "PASO 2: Feature Engineering"),
        (src_dir / "model_training_evaluation.py", "PASO 3: Entrenamiento y Evaluación"),
    ]
    
    # Ejecutar cada script en secuencia
    for script_path, description in scripts:
        if not script_path.exists():
            print(f"\n❌ ERROR: No se encontró el script {script_path}")
            print("Asegúrate de que todos los scripts estén en su lugar.")
            return False
        
        success = run_script(script_path, description)
        
        if not success:
            print(f"\n❌ El pipeline se detuvo debido a un error en: {description}")
            print("Por favor, revisa los mensajes de error anteriores.")
            return False
    
    print_section("✅ PIPELINE COMPLETADO EXITOSAMENTE")
    print("\n📦 Artefactos generados:")
    print("   - data/processed/cleaned_data.csv")
    print("   - data/processed/X_train.csv, X_test.csv, y_train.csv, y_test.csv")
    print("   - artifacts/preprocessor.joblib")
    print("   - artifacts/best_model.joblib")
    print("   - artifacts/model_metadata.json")
    print("   - artifacts/model_evaluation_results.csv")
    
    return True

def get_api_script_path():
    """Obtiene la ruta al script de API"""
    return Path("mlops_pipeline/src/scripts/model_deploy.py")

def get_ui_script_path():
    """Obtiene la ruta al script de UI de predicción"""
    return Path("mlops_pipeline/src/scripts/prediction_ui.py")

def get_drift_report_script_path():
    """Obtiene la ruta al script de reporte de drift de Streamlit"""
    # Puede ser streamlit_app.py con una página de drift, o un script específico
    return Path("mlops_pipeline/src/scripts/streamlit_app.py")

def run_monitoring_if_needed():
    """
    Ejecuta el monitoreo de data drift si es necesario
    
    Returns:
        bool: True si se ejecutó o ya existía, False si hubo error
    """
    monitoring_path = Path("mlops_pipeline/monitoring_results")
    drift_report = monitoring_path / "drift_report.csv"
    
    print("\n🔍 Verificando reporte de drift...")
    
    if drift_report.exists():
        print("  ✓ Reporte de drift ya existe")
        return True
    
    print("  ✗ Reporte de drift no encontrado")
    print("   Se ejecutará automáticamente el monitoreo...\n")
    
    time.sleep(2)
    
    # Ejecutar monitoreo
    project_root = Path(__file__).parent
    src_dir = project_root / "mlops_pipeline" / "src" / "scripts"
    
    monitoring_script = src_dir / "model_monitoring.py"
    
    if not monitoring_script.exists():
        print(f"\n❌ ERROR: No se encontró el script {monitoring_script}")
        return False
    
    success = run_script(monitoring_script, "PASO 4: Monitoreo de Data Drift")
    
    if not success:
        print("\n⚠️  Advertencia: El monitoreo de drift falló")
        print("   Continuando con los otros servicios...\n")
        return False
    
    return True

def start_api():
    """Inicia la API FastAPI"""
    print("\n🚀 Iniciando API FastAPI...")
    
    script_path = get_api_script_path()
    
    if not script_path.exists():
        print(f"❌ No encontrado: {script_path}")
        sys.exit(1)
    
    # Usar pythonw en Windows si es posible (para no mostrar consola extra)
    if platform.system() == "Windows":
        # Crear archivo batch para ejecutar en otra ventana
        batch_content = f"""@echo off
cd /d "{Path.cwd()}"
python "{script_path.absolute()}"
pause
"""
        batch_file = Path("_start_api.bat")
        batch_file.write_text(batch_content)
        
        print(f"  Script: {script_path}")
        print("  ⏳ Esperando 5 segundos para que la API inicie...")
        
        # Ejecutar en otra ventana
        os.system(f'start "API FastAPI - Alzheimer" "{batch_file.absolute()}"')
        time.sleep(5)
    else:
        # En Linux/Mac, usar & para background
        os.system(f"python {script_path} &")
        print(f"  Script: {script_path}")
        print("  ⏳ Esperando 5 segundos para que la API inicie...")
        time.sleep(5)

def start_streamlit():
    """Inicia Streamlit UI de predicción"""
    print("\n🎨 Iniciando Streamlit UI - Predicción...")
    
    script_path = get_ui_script_path()
    
    if not script_path.exists():
        print(f"❌ No encontrado: {script_path}")
        sys.exit(1)
    
    print(f"  Script: {script_path}")
    print(f"  Puerto: 8501")
    print(f"  URL: http://localhost:8501")
    
    # Streamlit se ejecuta en foreground
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(script_path),
        "--server.port", "8501",
        "--server.address", "localhost"
    ]
    
    subprocess.run(cmd)

def start_drift_report():
    """Inicia Streamlit UI de reporte de drift"""
    print("\n📊 Iniciando Streamlit UI - Reporte de Drift...")
    
    script_path = get_drift_report_script_path()
    
    if not script_path.exists():
        print(f"❌ No encontrado: {script_path}")
        print("   Se iniciará solo el servicio de predicción")
        return False
    
    print(f"  Script: {script_path}")
    print(f"  Puerto: 8502")
    print(f"  URL: http://localhost:8502")
    
    # Streamlit se ejecuta en foreground
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(script_path),
        "--server.port", "8502",
        "--server.address", "localhost"
    ]
    
    subprocess.run(cmd)
    return True

def main():
    """Función principal"""
    try:
        # Banner
        print_banner()
        
        # Verificar y ejecutar pipeline si es necesario
        pipeline_success = run_pipeline_if_needed()
        
        if not pipeline_success:
            print("\n❌ No se pudo completar el pipeline")
            print("   Por favor, revisa los errores anteriores")
            sys.exit(1)
        
        # Ejecutar monitoreo de drift si es necesario
        print_section("Verificando Monitoreo de Data Drift")
        run_monitoring_if_needed()
        
        # Mostrar plan
        print("\n📋 Plan de ejecución:")
        print("  1. Iniciará API FastAPI en puerto 8000")
        print("  2. Esperará 5 segundos")
        print("  3. Iniciará Streamlit (Predicción) en puerto 8501")
        print("  4. Iniciará Streamlit (Reporte Drift) en puerto 8502")
        print("\n💡 Presiona CTRL+C en la última ventana para detener todo")
        
        input("\nPresiona ENTER para continuar...")
        
        # Iniciar API
        start_api()
        
        print_service_info("API FastAPI", 8000, "http://localhost:8000")
        print_service_info("Streamlit - Predicción", 8501, "http://localhost:8501")
        print_service_info("Streamlit - Reporte Drift", 8502, "http://localhost:8502")
        
        print("\n" + "="*70)
        print("✓ SERVICIOS INICIADOS CORRECTAMENTE")
        print("="*70)
        print("\n📌 URLs disponibles:")
        print("  • API FastAPI")
        print("    - Base: http://localhost:8000")
        print("    - Documentación: http://localhost:8000/docs")
        print("    - Health Check: http://localhost:8000/health")
        print("\n  • UI Predicción")
        print("    - URL: http://localhost:8501")
        print("    - Haz predicciones sobre Alzheimer")
        print("\n  • UI Reporte Drift")
        print("    - URL: http://localhost:8502")
        print("    - Monitorea data drift y cambios en los datos")
        print("\n💡 Abre los URLs en tu navegador para acceder a los servicios\n")
        
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Sistema detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
