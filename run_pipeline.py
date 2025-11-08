"""
run_pipeline.py
Script maestro para ejecutar el pipeline MLOps completo

Este script ejecuta todos los pasos del pipeline en secuencia:
1. Procesamiento de datos (data_processing.py)
2. Feature Engineering (ft_engineering.py)
3. Entrenamiento y Evaluación (model_training_evaluation.py)
4. Monitoreo (model_monitoring.py)

Opcionalmente puede desplegar el modelo y lanzar Streamlit.
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
        description="Ejecuta el pipeline MLOps completo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python run_pipeline.py                    # Ejecuta pipeline básico (pasos 1-4)
  python run_pipeline.py --deploy           # Incluye despliegue de API
  python run_pipeline.py --streamlit        # Incluye Streamlit
  python run_pipeline.py --full             # Ejecuta todo (incluye deploy y streamlit)
  python run_pipeline.py --skip-training    # Salta el entrenamiento (útil para testing)
        """
    )
    
    parser.add_argument(
        '--deploy',
        action='store_true',
        help='Incluir despliegue de la API después del pipeline'
    )
    
    parser.add_argument(
        '--streamlit',
        action='store_true',
        help='Lanzar la aplicación Streamlit después del pipeline'
    )
    
    parser.add_argument(
        '--full',
        action='store_true',
        help='Ejecutar pipeline completo incluyendo deploy y streamlit'
    )
    
    parser.add_argument(
        '--skip-training',
        action='store_true',
        help='Saltar el paso de entrenamiento de modelos (útil para testing)'
    )
    
    args = parser.parse_args()
    
    # Si se especifica --full, activar todo
    if args.full:
        args.deploy = True
        args.streamlit = True
    
    # Definir rutas de scripts
    project_root = Path(__file__).parent
    src_dir = project_root / "mlops_pipeline" / "src" / "Scripts"
    
    scripts = [
        (src_dir / "data_processing.py", "PASO 1: Procesamiento de Datos"),
        (src_dir / "ft_engineering.py", "PASO 2: Feature Engineering"),
    ]
    
    if not args.skip_training:
        scripts.append(
            (src_dir / "model_training_evaluation.py", "PASO 3: Entrenamiento y Evaluación")
        )
    
    scripts.append(
        (src_dir / "model_monitoring.py", "PASO 4: Monitoreo de Data Drift")
    )
    
    # Banner inicial
    print("\n" + "="*80)
    print("  🚀 PIPELINE MLOPS - ALZHEIMER'S DISEASE PREDICTION")
    print("="*80)
    print(f"\n📋 Configuración:")
    print(f"   - Procesamiento de datos: ✓")
    print(f"   - Feature Engineering: ✓")
    print(f"   - Entrenamiento: {'❌ (Saltado)' if args.skip_training else '✓'}")
    print(f"   - Monitoreo: ✓")
    print(f"   - Despliegue API: {'✓' if args.deploy else '❌'}")
    print(f"   - Streamlit: {'✓' if args.streamlit else '❌'}")
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
    
    # Pipeline básico completado
    print_section("✅ PIPELINE BÁSICO COMPLETADO EXITOSAMENTE")
    
    print("\n📦 Artefactos generados:")
    print("   - data/processed/cleaned_data.csv")
    print("   - data/processed/X_train.csv, X_test.csv, y_train.csv, y_test.csv")
    print("   - artifacts/preprocessor.joblib")
    if not args.skip_training:
        print("   - artifacts/best_model.joblib")
        print("   - artifacts/model_metadata.json")
        print("   - artifacts/model_evaluation_results.csv")
    print("   - monitoring_results/drift_report.csv")
    print("   - monitoring_results/drift_summary.json")
    
    # Opciones post-pipeline
    if args.deploy:
        print_section("PASO 5: Despliegue de la API")
        print("🚀 Iniciando servidor de API...")
        print("   URL: http://localhost:8000")
        print("   Docs: http://localhost:8000/docs")
        print("\n⚠️  Presiona CTRL+C para detener el servidor\n")
        
        try:
            subprocess.run(
                [sys.executable, str(src_dir / "model_deploy.py")],
                check=True
            )
        except KeyboardInterrupt:
            print("\n\n✅ Servidor de API detenido")
        except Exception as e:
            print(f"\n❌ Error al iniciar la API: {e}")
    
    if args.streamlit:
        print_section("PASO 6: Aplicación Streamlit")
        print("🎨 Iniciando aplicación Streamlit...")
        print("   La aplicación se abrirá en tu navegador\n")
        print("⚠️  Presiona CTRL+C para detener Streamlit\n")
        
        try:
            subprocess.run(
                ["streamlit", "run", str(src_dir / "streamlit_app.py")],
                check=True
            )
        except KeyboardInterrupt:
            print("\n\n✅ Aplicación Streamlit detenida")
        except Exception as e:
            print(f"\n❌ Error al iniciar Streamlit: {e}")
    
    # Mensaje final
    print("\n" + "="*80)
    print("  ✨ PIPELINE COMPLETADO")
    print("="*80)
    
    if not args.deploy and not args.streamlit:
        print("\n💡 Próximos pasos:")
        print("   1. Revisar los artefactos generados en las carpetas artifacts/ y data/processed/")
        print("   2. Desplegar la API con: python mlops_pipeline/src/model_deploy.py")
        print("   3. Visualizar resultados con: streamlit run mlops_pipeline/src/streamlit_app.py")
        print("   4. Construir imagen Docker con: docker build -t alzheimer-api .")
        print("\n   O ejecuta el pipeline completo con: python run_pipeline.py --full")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
