"""
advanced_code_analysis.py
Script avanzado para análisis detallado usando pylint y radon
Genera reportes completos sobre calidad del código
"""

import subprocess
import json
import re
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET


def run_radon_analysis(python_files):
    """Ejecuta radon para análisis de complejidad y mantenibilidad"""
    print("\n🔧 Ejecutando Radon para análisis de complejidad...")
    
    radon_results = {
        'complexity': {},
        'metrics': {}
    }
    
    # Análisis de complejidad ciclomática
    for file_path in python_files:
        try:
            result = subprocess.run(
                ['radon', 'cc', file_path, '-a', '-j'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.stdout:
                data = json.loads(result.stdout)
                radon_results['complexity'][file_path] = data
        except Exception as e:
            print(f"  ⚠️  Error analizando {file_path}: {e}")
    
    # Análisis de métricas de mantenibilidad
    for file_path in python_files:
        try:
            result = subprocess.run(
                ['radon', 'mi', file_path, '-j'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.stdout:
                data = json.loads(result.stdout)
                radon_results['metrics'][file_path] = data
        except Exception as e:
            pass
    
    return radon_results


def run_pylint_analysis(python_files):
    """Ejecuta pylint para análisis detallado de problemas"""
    print("🔍 Ejecutando Pylint para análisis de problemas...")
    
    pylint_results = {
        'warnings': [],
        'errors': [],
        'refactoring': [],
        'convention': []
    }
    
    for file_path in python_files:
        try:
            result = subprocess.run(
                ['pylint', file_path, '--rcfile=.pylintrc', '-f', 'json'],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.stdout:
                try:
                    issues = json.loads(result.stdout)
                    for issue in issues:
                        category = issue['category'].lower()
                        if category in pylint_results:
                            pylint_results[category].append({
                                'file': file_path,
                                'line': issue['line'],
                                'message': issue['message'],
                                'symbol': issue['symbol'],
                                'type': issue['type']
                            })
                except:
                    pass
        except Exception as e:
            pass
    
    return pylint_results


def analyze_maintainability(radon_results):
    """Analiza índice de mantenibilidad"""
    maintainability_report = {
        'excellent': [],  # 100 - 80
        'good': [],       # 80 - 60
        'fair': [],       # 60 - 40
        'poor': [],       # < 40
    }
    
    for file_path, metrics in radon_results.get('metrics', {}).items():
        if isinstance(metrics, dict) and 'mi' in metrics:
            mi_score = metrics['mi']
            file_name = Path(file_path).name
            
            if mi_score >= 80:
                maintainability_report['excellent'].append((file_name, mi_score))
            elif mi_score >= 60:
                maintainability_report['good'].append((file_name, mi_score))
            elif mi_score >= 40:
                maintainability_report['fair'].append((file_name, mi_score))
            else:
                maintainability_report['poor'].append((file_name, mi_score))
    
    return maintainability_report


def generate_comprehensive_report(radon_results, pylint_results, output_dir='docs/sonarcloud_reports'):
    """Genera reporte completo"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    report = []
    report.append("# 🔬 Análisis Avanzado de Calidad de Código")
    report.append(f"\n**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Herramientas:** Radon, Pylint, Análisis personalizado")
    
    # Sección de complejidad
    report.append("\n## 📊 Análisis de Complejidad Ciclomática (Radon)")
    report.append("\n### Funciones por Complejidad\n")
    report.append("| Severidad | Rango | Interpretación |\n")
    report.append("|-----------|-------|----------------|\n")
    report.append("| 🟢 Simple | 1-5 | Fácil de mantener |\n")
    report.append("| 🟡 Moderada | 6-10 | Puede mejorar |\n")
    report.append("| 🟠 Compleja | 11-20 | Refactorizar pronto |\n")
    report.append("| 🔴 Muy Compleja | >20 | Refactorizar urgente |\n")
    
    # Analizar complejidad por archivo
    complexity_summary = {}
    for file_path, data in radon_results.get('complexity', {}).items():
        if isinstance(data, dict):
            for key, value in data.items():
                if key != 'TOTAL':
                    complexity_summary[file_path] = complexity_summary.get(file_path, {})
                    if isinstance(value, dict) and 'complexity' in value:
                        complexity_summary[file_path][key] = value['complexity']
    
    # Sección de índice de mantenibilidad
    report.append("\n## 🏥 Índice de Mantenibilidad (MI)")
    report.append("\nEl MI evalúa qué tan fácil es mantener y entender el código:\n")
    
    maintainability = analyze_maintainability(radon_results)
    
    if maintainability['excellent']:
        report.append("### ✅ Excelente (80-100)\n")
        for file, score in maintainability['excellent']:
            report.append(f"- {file}: {score:.1f}")
        report.append("\n")
    
    if maintainability['good']:
        report.append("### 🟢 Bueno (60-80)\n")
        for file, score in maintainability['good']:
            report.append(f"- {file}: {score:.1f}")
        report.append("\n")
    
    if maintainability['fair']:
        report.append("### 🟡 Aceptable (40-60)\n")
        for file, score in maintainability['fair']:
            report.append(f"- {file}: {score:.1f}")
        report.append("\n")
    
    if maintainability['poor']:
        report.append("### 🔴 Pobre (<40)\n")
        for file, score in maintainability['poor']:
            report.append(f"- {file}: {score:.1f} - **REQUIERE REFACTORIZACIÓN**")
        report.append("\n")
    
    # Sección de problemas detectados por Pylint
    report.append("\n## 🐛 Problemas Detectados (Pylint)\n")
    
    total_issues = sum(len(v) for v in pylint_results.values())
    report.append(f"**Total de problemas:** {total_issues}\n")
    
    if pylint_results['errors']:
        report.append(f"\n### 🔴 Errores ({len(pylint_results['errors'])})\n")
        for issue in pylint_results['errors'][:10]:
            report.append(f"- **{issue['symbol']}** (línea {issue['line']}): {issue['message']}\n")
    
    if pylint_results['warnings']:
        report.append(f"\n### 🟠 Advertencias ({len(pylint_results['warnings'])})\n")
        for issue in pylint_results['warnings'][:10]:
            report.append(f"- **{issue['symbol']}** (línea {issue['line']}): {issue['message']}\n")
    
    if pylint_results['refactoring']:
        report.append(f"\n### 🟡 Oportunidades de Refactorización ({len(pylint_results['refactoring'])})\n")
        for issue in pylint_results['refactoring'][:10]:
            report.append(f"- **{issue['symbol']}**: {issue['message']}\n")
    
    if pylint_results['convention']:
        report.append(f"\n### 📋 Convenciones de Código ({len(pylint_results['convention'])})\n")
        report.append("*Primeros 10 problemas:*\n")
        for issue in pylint_results['convention'][:10]:
            report.append(f"- **{issue['symbol']}**: {issue['message']}\n")
    
    # Plan de mejora
    report.append("\n## 📈 Plan de Mejora Priorizado\n")
    report.append("""
### Fase 1: Crítico (Semana 1-2)
1. Refactorizar funciones con complejidad > 15
2. Dividir funciones con > 100 líneas
3. Resolver todos los errores detectados por Pylint

### Fase 2: Alto (Semana 3-4)
1. Reducir complejidad de funciones 10-15 a < 10
2. Dividir funciones de 50-100 líneas
3. Resolver advertencias críticas

### Fase 3: Mejoras (Semana 5-6)
1. Mejorar índice de mantenibilidad
2. Optimizar código duplicado
3. Cumplir con convenciones de código

### Integración de SonarCloud
1. Crear cuenta en https://sonarcloud.io
2. Conectar con GitHub
3. Configurar workflow en GitHub Actions
4. Establecer Quality Gate
""")
    
    # Guardar reportes
    report_file = output_path / f"advanced_analysis_{timestamp}.md"
    json_file = output_path / f"advanced_analysis_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    # Guardar JSON con datos detallados
    json_data = {
        'timestamp': timestamp,
        'summary': {
            'total_files': len(radon_results.get('complexity', {})),
            'total_issues': total_issues,
            'maintainability': {
                'excellent': len(maintainability['excellent']),
                'good': len(maintainability['good']),
                'fair': len(maintainability['fair']),
                'poor': len(maintainability['poor'])
            }
        },
        'pylint_issues': {
            'errors': len(pylint_results.get('errors', [])),
            'warnings': len(pylint_results.get('warnings', [])),
            'refactoring': len(pylint_results.get('refactoring', [])),
            'convention': len(pylint_results.get('convention', []))
        }
    }
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    return report_file, json_file


def main():
    project_root = Path(__file__).parent
    python_files = [
        str(f) for f in (project_root / 'mlops_pipeline' / 'src' / 'scripts').glob('*.py')
        if f.name != '__init__.py'
    ]
    
    if not python_files:
        print("❌ No se encontraron archivos Python")
        return
    
    print(f"\n📂 Analizando {len(python_files)} archivos...\n")
    
    # Ejecutar análisis
    radon_results = run_radon_analysis(python_files)
    pylint_results = run_pylint_analysis(python_files)
    
    # Generar reportes
    print("\n📝 Generando reportes...\n")
    report_file, json_file = generate_comprehensive_report(radon_results, pylint_results)
    
    print(f"✅ Reportes generados:")
    print(f"   - {report_file}")
    print(f"   - {json_file}")


if __name__ == "__main__":
    main()
