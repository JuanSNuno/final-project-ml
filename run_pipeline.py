"""
run_pipeline.py
Script maestro para ejecutar el pipeline MLOps de preparación de datos y entrenamiento

Este script ejecuta todos los pasos del pipeline en secuencia:
1. Procesamiento de datos (data_processing.py)
2. Feature Engineering (ft_engineering.py)
3. Entrenamiento y Evaluación (model_training_evaluation.py)

Este script genera los artefactos necesarios para que run_full_system.py pueda
ejecutar la API y la UI de Streamlit. El monitoreo de drift se realiza en run_full_system.py.
"""

import sys
import subprocess
from pathlib import Path
import argparse


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


def main():
    """Función principal que orquesta el pipeline"""
    
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description="Ejecuta el pipeline MLOps de preparación de datos y entrenamiento",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python run_pipeline.py                    # Ejecuta pipeline completo
  python run_pipeline.py --skip-training    # Salta el entrenamiento (útil para testing)
        """
    )
    
    parser.add_argument(
        '--skip-training',
        action='store_true',
        help='Saltar el paso de entrenamiento de modelos (útil para testing)'
    )
    
    args = parser.parse_args()
    
    # Definir rutas de scripts
    project_root = Path(__file__).parent
    src_dir = project_root / "mlops_pipeline" / "src" / "scripts"
    
    scripts = [
        (src_dir / "data_processing.py", "PASO 1: Procesamiento de Datos"),
        (src_dir / "ft_engineering.py", "PASO 2: Feature Engineering"),
    ]
    
    if not args.skip_training:
        scripts.append(
            (src_dir / "model_training_evaluation.py", "PASO 3: Entrenamiento y Evaluación")
        )
    
    # Banner inicial
    print("\n" + "="*80)
    print("  🚀 PIPELINE MLOPS - ALZHEIMER'S DISEASE PREDICTION")
    print("="*80)
    print(f"\n📋 Configuración:")
    print(f"   - Procesamiento de datos: ✓")
    print(f"   - Feature Engineering: ✓")
    print(f"   - Entrenamiento: {'❌ (Saltado)' if args.skip_training else '✓'}")
    print("\n💡 Nota: Monitoreo de data drift se ejecutará en run_full_system.py")
    print("\n" + "="*80)
    
    input("\nPresiona ENTER para iniciar el pipeline...")
    
    # Ejecutar cada script en secuencia
    for script_path, description in scripts:
        if not script_path.exists():
            print(f"\n❌ ERROR: No se encontró el script {script_path}")
            print("Asegúrate de que todos los scripts estén en su lugar.")
            sys.exit(1)
        
        success = run_script(script_path, description)
        
        if not success:
            print(f"\n❌ El pipeline se detuvo debido a un error en: {description}")
            print("Por favor, revisa los mensajes de error anteriores.")
            sys.exit(1)
    
    # Pipeline completado
    print_section("✅ PIPELINE COMPLETADO EXITOSAMENTE")
    
    print("\n📦 Artefactos generados:")
    print("   - data/processed/cleaned_data.csv")
    print("   - data/processed/X_train.csv, X_test.csv, y_train.csv, y_test.csv")
    print("   - artifacts/preprocessor.joblib")
    if not args.skip_training:
        print("   - artifacts/best_model.joblib")
        print("   - artifacts/model_metadata.json")
        print("   - artifacts/model_evaluation_results.csv")
    
    # Mensaje final
    print("\n" + "="*80)
    print("  ✨ PIPELINE COMPLETADO")
    print("="*80)
    
    print("\n💡 Próximos pasos:")
    print("   1. Ejecutar run_full_system.py para iniciar API y UI")
    print("      python run_full_system.py")
    print("\n   2. O ejecutar manualmente:")
    print("      - API: python mlops_pipeline/src/scripts/model_deploy.py")
    print("      - UI: streamlit run mlops_pipeline/src/scripts/prediction_ui.py")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
