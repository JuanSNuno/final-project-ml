"""
Script de verificación de configuración de SonarCloud
Verifica que todo esté configurado correctamente antes de hacer push
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_mark(condition, success_msg, fail_msg):
    """Imprime un check mark o X dependiendo de la condición"""
    if condition:
        print(f"✅ {success_msg}")
        return True
    else:
        print(f"❌ {fail_msg}")
        return False

def check_sonar_properties():
    """Verifica la existencia y contenido del archivo sonar-project.properties"""
    print_header("Verificando sonar-project.properties")
    
    sonar_file = Path("sonar-project.properties")
    if not sonar_file.exists():
        check_mark(False, "", "Archivo sonar-project.properties no encontrado")
        return False
    
    check_mark(True, "Archivo sonar-project.properties encontrado", "")
    
    content = sonar_file.read_text(encoding='utf-8')
    
    # Verificar propiedades clave
    checks = {
        "sonar.projectKey": "sonar.projectKey" in content,
        "sonar.organization": "sonar.organization" in content,
        "sonar.sources": "sonar.sources" in content,
    }
    
    all_good = True
    for prop, exists in checks.items():
        if check_mark(exists, f"{prop} está configurado", f"{prop} NO está configurado"):
            # Extraer el valor
            for line in content.split('\n'):
                if line.strip().startswith(prop):
                    value = line.split('=', 1)[1].strip()
                    print(f"   Valor: {value}")
        else:
            all_good = False
    
    return all_good

def check_workflow_file():
    """Verifica la existencia del archivo de workflow de GitHub Actions"""
    print_header("Verificando GitHub Actions Workflow")
    
    workflow_file = Path(".github/workflows/sonarcloud.yml")
    exists = workflow_file.exists()
    
    check_mark(
        exists,
        "Archivo .github/workflows/sonarcloud.yml encontrado",
        "Archivo .github/workflows/sonarcloud.yml NO encontrado"
    )
    
    if exists:
        content = workflow_file.read_text(encoding='utf-8')
        has_sonar_token = "SONAR_TOKEN" in content
        check_mark(
            has_sonar_token,
            "Configuración de SONAR_TOKEN encontrada en el workflow",
            "SONAR_TOKEN NO configurado en el workflow"
        )
        return has_sonar_token
    
    return False

def check_source_directory():
    """Verifica que el directorio de código fuente existe"""
    print_header("Verificando Directorio de Código Fuente")
    
    source_dir = Path("mlops_pipeline/src")
    exists = source_dir.exists() and source_dir.is_dir()
    
    check_mark(
        exists,
        f"Directorio de fuentes encontrado: {source_dir}",
        f"Directorio de fuentes NO encontrado: {source_dir}"
    )
    
    if exists:
        py_files = list(source_dir.rglob("*.py"))
        print(f"   📄 Archivos Python encontrados: {len(py_files)}")
        return True
    
    return False

def check_git_configuration():
    """Verifica la configuración de Git"""
    print_header("Verificando Configuración de Git")
    
    try:
        # Verificar si es un repositorio Git
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            check_mark(True, "Repositorio Git inicializado", "")
        else:
            check_mark(False, "", "NO es un repositorio Git")
            return False
        
        # Obtener la rama actual
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            branch = result.stdout.strip()
            print(f"   📍 Rama actual: {branch}")
        
        # Verificar remote
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            remote_url = result.stdout.strip()
            print(f"   🌐 Remote URL: {remote_url}")
            
            # Verificar si es el repositorio correcto
            if "JuanSNuno" in remote_url and "final-project-ml" in remote_url:
                check_mark(True, "Remote configurado correctamente", "")
                return True
            else:
                check_mark(
                    False,
                    "",
                    "Remote NO coincide con el repositorio esperado"
                )
                return False
        else:
            check_mark(False, "", "No hay remote configurado")
            return False
            
    except FileNotFoundError:
        check_mark(False, "", "Git no está instalado o no está en el PATH")
        return False

def check_python_files():
    """Verifica archivos Python para análisis"""
    print_header("Verificando Archivos Python")
    
    source_dir = Path("mlops_pipeline/src")
    if not source_dir.exists():
        check_mark(False, "", "Directorio de fuentes no existe")
        return False
    
    py_files = list(source_dir.rglob("*.py"))
    notebook_files = list(source_dir.rglob("*.ipynb"))
    
    print(f"   📄 Archivos .py: {len(py_files)}")
    print(f"   📓 Archivos .ipynb: {len(notebook_files)} (excluidos del análisis)")
    
    if py_files:
        print("\n   Archivos Python a analizar:")
        for py_file in sorted(py_files)[:10]:  # Mostrar solo los primeros 10
            try:
                rel_path = py_file.relative_to(Path.cwd())
            except ValueError:
                # Si no se puede obtener la ruta relativa, usar el nombre del archivo
                rel_path = py_file
            print(f"      - {rel_path}")
        
        if len(py_files) > 10:
            print(f"      ... y {len(py_files) - 10} más")
        
        check_mark(True, "Archivos Python encontrados para análisis", "")
        return True
    else:
        check_mark(False, "", "No se encontraron archivos Python para analizar")
        return False

def print_next_steps():
    """Imprime los siguientes pasos a seguir"""
    print_header("Siguientes Pasos")
    
    print("""
📋 Para completar la configuración de SonarCloud:

1. 🔐 Configurar SONAR_TOKEN en GitHub:
   - Ve a: https://github.com/JuanSNuno/final-project-ml/settings/secrets/actions
   - Crea un secret llamado: SONAR_TOKEN
   - Obtén el token desde: https://sonarcloud.io/account/security/

2. 🏗️ Crear el proyecto en SonarCloud:
   - Ve a: https://sonarcloud.io
   - Click en "+" > "Analyze new project"
   - Selecciona el repositorio: final-project-ml
   - Verifica el projectKey (debe ser: JuanSNuno_final-project-ml)

3. ✅ Verificar la configuración:
   - Haz un commit y push a la rama certification
   - Revisa el workflow en: https://github.com/JuanSNuno/final-project-ml/actions
   
4. 📊 Ver los resultados:
   - Dashboard: https://sonarcloud.io/dashboard?id=JuanSNuno_final-project-ml

📖 Para más detalles, consulta: docs/SONARCLOUD_SETUP.md
    """)

def main():
    """Función principal"""
    print("\n" + "🔍 Verificador de Configuración de SonarCloud".center(60))
    print("=" * 60)
    
    # Ejecutar todas las verificaciones
    checks = [
        ("Archivo de propiedades", check_sonar_properties()),
        ("Workflow de GitHub Actions", check_workflow_file()),
        ("Directorio de código fuente", check_source_directory()),
        ("Configuración de Git", check_git_configuration()),
        ("Archivos Python", check_python_files()),
    ]
    
    # Resumen
    print_header("Resumen de Verificación")
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    for name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n📊 Resultado: {passed}/{total} verificaciones pasadas")
    
    if passed == total:
        print("\n🎉 ¡Configuración completa! Puedes proceder con el análisis de SonarCloud.")
        print("⚠️  IMPORTANTE: Asegúrate de que el SONAR_TOKEN esté configurado en GitHub.")
    else:
        print("\n⚠️  Hay problemas con la configuración. Por favor, revisa los errores arriba.")
    
    # Imprimir siguientes pasos
    print_next_steps()
    
    # Código de salida
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
