"""
setup_monitoring.py
Script rápido para generar los archivos de monitoreo necesarios para Streamlit
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("="*80)
    print("  🔧 CONFIGURACIÓN RÁPIDA DE MONITOREO")
    print("="*80)
    print("\nEste script ejecutará model_monitoring.py para generar los archivos")
    print("necesarios para la visualización en Streamlit.\n")
    
    src_dir = Path(__file__).parent / "mlops_pipeline" / "src"
    monitoring_script = src_dir / "model_monitoring.py"
    
    if not monitoring_script.exists():
        print(f"❌ Error: No se encontró {monitoring_script}")
        return
    
    print("🚀 Ejecutando model_monitoring.py...\n")
    
    try:
        result = subprocess.run(
            [sys.executable, str(monitoring_script)],
            check=True
        )
        
        print("\n" + "="*80)
        print("  ✅ CONFIGURACIÓN COMPLETADA")
        print("="*80)
        print("\nAhora puedes ejecutar Streamlit:")
        print("  streamlit run mlops_pipeline/src/streamlit_app.py")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error al ejecutar el script de monitoreo")
        print(f"Código de error: {e.returncode}")
        print("\n💡 Asegúrate de haber ejecutado primero el pipeline:")
        print("  python run_pipeline.py")
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
