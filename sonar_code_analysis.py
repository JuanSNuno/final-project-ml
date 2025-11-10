"""
sonar_code_analysis.py
Script para analizar la calidad del código ejecutando análisis locales
Detecta: código duplicado, complejidad ciclomática, funciones largas, malas prácticas
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import ast
import re
from collections import defaultdict

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_python_files(directory):
    """Obtiene todos los archivos Python del proyecto"""
    python_files = []
    exclude_dirs = {'__pycache__', '.git', '.venv', 'venv', 'env', 'node_modules'}
    
    for root, dirs, files in os.walk(directory):
        # Eliminar directorios excluidos
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.py') and not file.startswith('test_'):
                python_files.append(os.path.join(root, file))
    
    return sorted(python_files)


def analyze_cyclomatic_complexity(file_path):
    """Analiza la complejidad ciclomática de un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except:
        return {}
    
    complexity_data = {}
    
    class ComplexityVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            complexity = self._calculate_complexity(node)
            complexity_data[node.name] = {
                'line': node.lineno,
                'complexity': complexity
            }
            self.generic_visit(node)
        
        def visit_AsyncFunctionDef(self, node):
            complexity = self._calculate_complexity(node)
            complexity_data[node.name] = {
                'line': node.lineno,
                'complexity': complexity
            }
            self.generic_visit(node)
        
        def _calculate_complexity(self, node):
            complexity = 1
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                    complexity += 1
                elif isinstance(child, ast.BoolOp):
                    complexity += len(child.values) - 1
            return complexity
    
    visitor = ComplexityVisitor()
    visitor.visit(tree)
    return complexity_data


def analyze_function_length(file_path):
    """Identifica funciones demasiado largas (>50 líneas)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return {}
    
    long_functions = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except:
        return {}
    
    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            # Calcular longitud de la función
            if hasattr(node, 'end_lineno'):
                length = node.end_lineno - node.lineno + 1
            else:
                # Fallback si no tiene end_lineno
                length = 0
            
            if length > 50:
                long_functions[node.name] = {
                    'line': node.lineno,
                    'length': length
                }
            self.generic_visit(node)
        
        def visit_AsyncFunctionDef(self, node):
            if hasattr(node, 'end_lineno'):
                length = node.end_lineno - node.lineno + 1
            else:
                length = 0
            
            if length > 50:
                long_functions[node.name] = {
                    'line': node.lineno,
                    'length': length
                }
            self.generic_visit(node)
    
    visitor = FunctionVisitor()
    visitor.visit(tree)
    return long_functions


def detect_duplicate_code(python_files):
    """Detecta código duplicado entre archivos"""
    file_contents = {}
    duplicates = defaultdict(list)
    
    # Lectura de contenidos
    for file in python_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Normalizar espacios en blanco
                normalized = re.sub(r'\s+', ' ', content)
                file_contents[file] = normalized
        except:
            pass
    
    # Buscar fragmentos duplicados (funciones o bloques de código)
    for file1 in python_files:
        try:
            with open(file1, 'r', encoding='utf-8') as f:
                lines1 = f.readlines()
        except:
            continue
        
        for i in range(len(lines1) - 5):
            chunk = ''.join(lines1[i:i+10])
            chunk_normalized = re.sub(r'\s+', ' ', chunk).strip()
            
            if len(chunk_normalized) < 50:
                continue
            
            # Buscar en otros archivos
            for file2 in python_files:
                if file1 >= file2:  # Evitar duplicados
                    continue
                
                try:
                    with open(file2, 'r', encoding='utf-8') as f:
                        content2 = f.read()
                except:
                    continue
                
                if chunk_normalized in re.sub(r'\s+', ' ', content2):
                    key = (file1, file2)
                    if len(duplicates[key]) < 3:  # Limitar resultados
                        duplicates[key].append({
                            'file1_line': i,
                            'chunk_preview': chunk[:80]
                        })
    
    return dict(duplicates)


def analyze_code_style(file_path):
    """Detecta problemas de estilo y malas prácticas"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return issues
    
    for i, line in enumerate(lines, 1):
        # Detectar líneas muy largas
        if len(line.rstrip()) > 120:
            issues.append({
                'line': i,
                'type': 'long_line',
                'message': f'Línea muy larga ({len(line.rstrip())} caracteres)',
                'severity': 'warning'
            })
        
        # Detectar nombres de variable cortos en funciones
        if re.search(r'def\s+\w+.*:\s*\n', line):
            # Buscar variables de una letra
            matches = re.findall(r'\b[a-z]\b', line)
            if matches:
                issues.append({
                    'line': i,
                    'type': 'unclear_variable',
                    'message': f'Variables de nombre poco claro detectadas',
                    'severity': 'info'
                })
        
        # Detectar código comentado
        if line.strip().startswith('#') and not line.strip().startswith('# '):
            if re.search(r'[a-zA-Z0-9_=\(\)]', line):
                issues.append({
                    'line': i,
                    'type': 'commented_code',
                    'message': 'Código comentado detectado',
                    'severity': 'info'
                })
    
    return issues


def run_pylint_analysis(python_files):
    """Ejecuta pylint si está disponible"""
    try:
        import subprocess
        result = subprocess.run(
            ['pylint', '--disable=all', '--enable=too-many-branches,too-many-locals,R0911'] + python_files[:5],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr
    except:
        return "Pylint no disponible. Ejecute: pip install pylint"


def generate_report(analysis_results, output_file=None):
    """Genera un reporte en formato markdown y JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    report = []
    report.append("# 📊 Análisis de Calidad de Código - SonarCloud Local")
    report.append(f"\n**Fecha de análisis:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Proyecto:** Alzheimer Disease Prediction - MLOps Pipeline")
    
    # Resumen ejecutivo
    report.append("\n## 📋 Resumen Ejecutivo")
    report.append(f"- **Archivos analizados:** {analysis_results['total_files']}")
    report.append(f"- **Funciones con complejidad alta (>5):** {analysis_results['high_complexity_count']}")
    report.append(f"- **Funciones largas (>50 líneas):** {analysis_results['long_functions_count']}")
    report.append(f"- **Bloques de código duplicado detectados:** {analysis_results['duplicate_count']}")
    report.append(f"- **Problemas de estilo:** {analysis_results['style_issues_count']}")
    
    # Detalle de complejidad ciclomática
    if analysis_results['high_complexity_functions']:
        report.append("\n## ⚠️ Complejidad Ciclomática Excesiva (>5)")
        report.append("\nFunciones que superan la complejidad recomendada:\n")
        report.append("| Archivo | Función | Línea | Complejidad | Acción |\n")
        report.append("|---------|---------|-------|-------------|--------|\n")
        
        for file_path, functions in analysis_results['high_complexity_functions'].items():
            for func_name, info in functions.items():
                complexity = info['complexity']
                line = info['line']
                severity = "🔴 CRÍTICO" if complexity > 10 else "🟠 ALTO"
                file_rel = file_path.replace(analysis_results['project_root'] + '\\', '')
                report.append(f"| {file_rel} | `{func_name}()` | {line} | {complexity} | {severity} - Refactorizar |\n")
    
    # Detalle de funciones largas
    if analysis_results['long_functions']:
        report.append("\n## 📏 Funciones Demasiado Largas (>50 líneas)")
        report.append("\nFunciones que deberían ser divididas en funciones más pequeñas:\n")
        report.append("| Archivo | Función | Línea | Longitud | Recomendación |\n")
        report.append("|---------|---------|-------|----------|---------------|\n")
        
        for file_path, functions in analysis_results['long_functions'].items():
            for func_name, info in functions.items():
                length = info['length']
                line = info['line']
                severity = "🔴 MUY LARGO" if length > 100 else "🟠 LARGO"
                file_rel = file_path.replace(analysis_results['project_root'] + '\\', '')
                report.append(f"| {file_rel} | `{func_name}()` | {line} | {length} líneas | {severity} - Dividir en funciones |\n")
    
    # Detalle de código duplicado
    if analysis_results['duplicates']:
        report.append("\n## 🔄 Código Duplicado")
        report.append("\nFragmentos similares encontrados entre archivos:\n")
        
        for (file1, file2), duplicates in list(analysis_results['duplicates'].items())[:5]:
            file1_rel = file1.replace(analysis_results['project_root'] + '\\', '')
            file2_rel = file2.replace(analysis_results['project_root'] + '\\', '')
            report.append(f"\n### {file1_rel} ↔️ {file2_rel}\n")
            report.append("Considere usar funciones compartidas o herencia.\n")
    
    # Problemas de estilo
    if analysis_results['style_issues']:
        report.append("\n## 🎨 Problemas de Estilo y Buenas Prácticas")
        report.append("\n| Archivo | Línea | Tipo | Descripción |\n")
        report.append("|---------|-------|------|-------------|\n")
        
        for file_path, issues in list(analysis_results['style_issues'].items())[:10]:
            file_rel = file_path.replace(analysis_results['project_root'] + '\\', '')
            for issue in issues[:3]:
                report.append(f"| {file_rel} | {issue['line']} | {issue['type']} | {issue['message']} |\n")
    
    # Recomendaciones
    report.append("\n## ✅ Recomendaciones de Mejora")
    report.append("""
1. **Refactorizar funciones complejas**
   - Dividir funciones con complejidad > 5 en funciones más pequeñas
   - Usar patrones de diseño (Strategy, Builder, etc.)

2. **Reducir tamaño de funciones**
   - Máximo 50 líneas por función
   - Cada función debe hacer una única cosa

3. **Eliminar código duplicado**
   - Usar clases base y herencia
   - Extraer funciones compartidas
   - DRY (Don't Repeat Yourself)

4. **Mejorar legibilidad**
   - Usar nombres descriptivos para variables
   - Agregar docstrings a funciones complejas
   - Mantener líneas < 120 caracteres

5. **Próximos pasos**
   - Integrar SonarCloud en CI/CD (GitHub Actions)
   - Ejecutar análisis automáticos en cada PR
   - Establecer métricas de calidad en el proyecto
""")
    
    # Versión JSON
    json_report = {
        'timestamp': timestamp,
        'summary': {
            'total_files': analysis_results['total_files'],
            'high_complexity_count': analysis_results['high_complexity_count'],
            'long_functions_count': analysis_results['long_functions_count'],
            'duplicate_blocks': analysis_results['duplicate_count'],
            'style_issues': analysis_results['style_issues_count']
        },
        'high_complexity_functions': {
            str(k): v for k, v in analysis_results['high_complexity_functions'].items()
        },
        'long_functions': {
            str(k): v for k, v in analysis_results['long_functions'].items()
        },
        'style_issues': {
            str(k): v for k, v in analysis_results['style_issues'].items()
        }
    }
    
    # Guardar reportes
    report_dir = Path('docs/sonarcloud_reports')
    report_dir.mkdir(parents=True, exist_ok=True)
    
    md_file = report_dir / f"sonar_analysis_{timestamp}.md"
    json_file = report_dir / f"sonar_analysis_{timestamp}.json"
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)
    
    return '\n'.join(report), md_file, json_file


def main():
    """Función principal"""
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}")
    print("=" * 80)
    print("🔍 ANÁLISIS DE CALIDAD DE CÓDIGO - SonarCloud Local")
    print("=" * 80)
    print(f"{Colors.ENDC}\n")
    
    project_root = Path(__file__).parent
    
    # Obtener archivos Python
    print("📂 Buscando archivos Python...")
    python_files = get_python_files(str(project_root / 'mlops_pipeline' / 'src'))
    
    if not python_files:
        print(f"{Colors.FAIL}No se encontraron archivos Python.{Colors.ENDC}")
        return
    
    print(f"✓ Se encontraron {len(python_files)} archivos Python\n")
    
    analysis_results = {
        'project_root': str(project_root),
        'total_files': len(python_files),
        'high_complexity_functions': {},
        'high_complexity_count': 0,
        'long_functions': {},
        'long_functions_count': 0,
        'duplicates': {},
        'duplicate_count': 0,
        'style_issues': {},
        'style_issues_count': 0
    }
    
    # Análisis de complejidad ciclomática
    print("📊 Analizando complejidad ciclomática...")
    for file_path in python_files:
        complexity_data = analyze_cyclomatic_complexity(file_path)
        
        high_complexity = {
            func: info for func, info in complexity_data.items() if info['complexity'] > 5
        }
        
        if high_complexity:
            analysis_results['high_complexity_functions'][file_path] = high_complexity
            analysis_results['high_complexity_count'] += len(high_complexity)
    
    print(f"✓ Encontradas {analysis_results['high_complexity_count']} funciones con complejidad alta\n")
    
    # Análisis de longitud de funciones
    print("📏 Analizando longitud de funciones...")
    for file_path in python_files:
        long_funcs = analyze_function_length(file_path)
        
        if long_funcs:
            analysis_results['long_functions'][file_path] = long_funcs
            analysis_results['long_functions_count'] += len(long_funcs)
    
    print(f"✓ Encontradas {analysis_results['long_functions_count']} funciones largas\n")
    
    # Análisis de código duplicado
    print("🔄 Buscando código duplicado...")
    duplicates = detect_duplicate_code(python_files)
    analysis_results['duplicates'] = duplicates
    analysis_results['duplicate_count'] = len(duplicates)
    
    if duplicates:
        print(f"✓ Encontrados {len(duplicates)} bloques de código potencialmente duplicado\n")
    else:
        print("✓ No se encontró código duplicado significativo\n")
    
    # Análisis de estilo
    print("🎨 Analizando estilo y buenas prácticas...")
    for file_path in python_files:
        style_issues = analyze_code_style(file_path)
        
        if style_issues:
            analysis_results['style_issues'][file_path] = style_issues
            analysis_results['style_issues_count'] += len(style_issues)
    
    print(f"✓ Encontrados {analysis_results['style_issues_count']} problemas de estilo\n")
    
    # Generar reporte
    print("📝 Generando reportes...")
    report_text, md_file, json_file = generate_report(analysis_results)
    
    print(f"\n{Colors.OKGREEN}")
    print("=" * 80)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 80)
    print(f"{Colors.ENDC}\n")
    
    print(f"📄 Reportes generados:")
    print(f"   - Markdown: {md_file}")
    print(f"   - JSON: {json_file}")
    print(f"\n💡 Próximos pasos:")
    print(f"   1. Revisar los reportes generados")
    print(f"   2. Refactorizar funciones con alta complejidad")
    print(f"   3. Dividir funciones largas en componentes más pequeños")
    print(f"   4. Eliminar código duplicado")
    print(f"   5. Integrar SonarCloud en CI/CD")
    
    print(f"\n{Colors.OKBLUE}Para configurar SonarCloud en GitHub Actions:{Colors.ENDC}")
    print(f"   1. Ir a https://sonarcloud.io")
    print(f"   2. Crear organización: 'juansnuno'")
    print(f"   3. Importar repositorio")
    print(f"   4. Configurar token en GitHub Secrets (SONAR_TOKEN)")


if __name__ == "__main__":
    main()
