"""
run_full_system.py
Script para iniciar tanto la API como la UI de Streamlit automáticamente

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

def check_artifacts():
    """Verifica que existan los artefactos necesarios"""
    artifacts_path = Path("mlops_pipeline/artifacts")
    
    required_files = [
        "best_model.joblib",
        "preprocessor.joblib"
    ]
    
    print("\n🔍 Verificando artefactos...")
    
    for file in required_files:
        file_path = artifacts_path / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ FALTA: {file}")
            print(f"\n❌ Artefactos incompletos. Ejecuta primero:")
            print(f"   python run_pipeline.py --full")
            sys.exit(1)
    
    print("  ✓ Todos los artefactos están presentes")

def get_api_script_path():
    """Obtiene la ruta al script de API"""
    return Path("mlops_pipeline/src/scripts/model_deploy.py")

def get_ui_script_path():
    """Obtiene la ruta al script de UI"""
    return Path("mlops_pipeline/src/scripts/prediction_ui.py")

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
    """Inicia Streamlit UI"""
    print("\n🎨 Iniciando Streamlit UI...")
    
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

def main():
    """Función principal"""
    try:
        # Banner
        print_banner()
        
        # Verificar artefactos
        check_artifacts()
        
        # Mostrar plan
        print("\n📋 Plan de ejecución:")
        print("  1. Iniciará API FastAPI en puerto 8000")
        print("  2. Esperará 5 segundos")
        print("  3. Iniciará Streamlit en puerto 8501")
        print("  4. Abre navegador en http://localhost:8501")
        
        input("\nPresiona ENTER para continuar...")
        
        # Iniciar API
        start_api()
        
        print_service_info("API FastAPI", 8000, "http://localhost:8000")
        print_service_info("Streamlit UI", 8501, "http://localhost:8501")
        
        print("\n" + "="*70)
        print("✓ SERVICIOS INICIADOS CORRECTAMENTE")
        print("="*70)
        print("\n📌 URLs disponibles:")
        print("  • API: http://localhost:8000")
        print("    - Documentación: http://localhost:8000/docs")
        print("    - Health check: http://localhost:8000/health")
        print("\n  • UI: http://localhost:8501")
        print("\n💡 Tu navegador debería abrir automáticamente.")
        print("   Si no, visita: http://localhost:8501\n")
        
        # Iniciar Streamlit (en foreground)
        start_streamlit()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Sistema detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
