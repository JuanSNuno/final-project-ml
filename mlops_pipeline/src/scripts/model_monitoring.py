"""
model_monitoring.py
Paso 5 del Pipeline MLOps: Monitoreo de Data Drift

Este script implementa métricas de data drift para detectar cambios
en la distribución de los datos comparando datos actuales con el baseline.
Calcula: PSI, KS test, Chi-cuadrado y guarda los resultados.
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from scipy import stats
from scipy.stats import ks_2samp, chi2_contingency
from scipy.spatial.distance import jensenshannon


def load_baseline_data():
    """Carga los datos de entrenamiento como baseline"""
    print("="*80)
    print("CARGANDO DATOS BASELINE")
    print("="*80)
    
    project_root = Path(__file__).parent.parent.parent
    
    # Cargar datos de entrenamiento originales (antes de transformación)
    cleaned_data_path = project_root / "data" / "processed" / "cleaned_data.csv"
    
    if not cleaned_data_path.exists():
        raise FileNotFoundError(
            f"No se encontró el dataset limpio: {cleaned_data_path}\n"
            "Por favor, ejecuta primero data_processing.py"
        )
    
    df = pd.read_csv(cleaned_data_path)
    
    print(f"\n✓ Baseline cargado desde: {cleaned_data_path}")
    print(f"  Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
    
    return df


def simulate_current_data(baseline_df, drift_percentage=0.2):
    """
    Simula datos actuales tomando una muestra del baseline.
    En producción, estos serían los datos nuevos reales.
    
    Args:
        baseline_df: DataFrame con datos baseline
        drift_percentage: Porcentaje de la muestra para simular drift
    """
    print("\n" + "="*80)
    print("SIMULANDO DATOS ACTUALES")
    print("="*80)
    
    # Tomar una muestra de los datos
    sample_size = int(len(baseline_df) * drift_percentage)
    current_df = baseline_df.sample(n=sample_size, random_state=123).copy()
    
    print(f"\n✓ Datos actuales simulados: {current_df.shape[0]} muestras")
    print(f"  (Usando {drift_percentage*100}% del baseline como simulación)")
    
    return current_df


def calculate_psi(expected, actual, bins=10):
    """
    Calcula el Population Stability Index (PSI)
    
    PSI mide el cambio en la distribución de una variable.
    - PSI < 0.1: Sin cambio significativo
    - 0.1 <= PSI < 0.25: Cambio moderado
    - PSI >= 0.25: Cambio significativo
    """
    # Limpiar NaN
    expected = expected[~np.isnan(expected)]
    actual = actual[~np.isnan(actual)]
    
    if len(expected) == 0 or len(actual) == 0:
        return 0.0
    
    # Crear bins basados en los cuantiles del baseline
    breakpoints = np.quantile(expected, np.linspace(0, 1, bins + 1))
    breakpoints = np.unique(breakpoints)
    
    if len(breakpoints) < 2:
        return 0.0
    
    # Contar observaciones en cada bin
    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]
    
    # Convertir a porcentajes (con suavizado)
    expected_percents = (expected_counts + 1) / (len(expected) + len(breakpoints) - 1)
    actual_percents = (actual_counts + 1) / (len(actual) + len(breakpoints) - 1)
    
    # Calcular PSI
    psi = np.sum((actual_percents - expected_percents) * np.log(actual_percents / expected_percents))
    
    return psi


def calculate_ks_statistic(reference, current):
    """
    Calcula el test de Kolmogorov-Smirnov
    
    Mide la máxima diferencia entre las distribuciones acumuladas.
    - p-value < 0.05: Las distribuciones son significativamente diferentes
    """
    reference = reference[~np.isnan(reference)]
    current = current[~np.isnan(current)]
    
    if len(reference) == 0 or len(current) == 0:
        return 0.0, 1.0
    
    statistic, p_value = ks_2samp(reference, current)
    
    return statistic, p_value


def calculate_jensen_shannon(reference, current, bins=30):
    """
    Calcula la divergencia de Jensen-Shannon
    
    Mide la similitud entre dos distribuciones de probabilidad.
    - JS = 0: Distribuciones idénticas
    - JS = 1: Distribuciones completamente diferentes
    """
    reference = reference[~np.isnan(reference)]
    current = current[~np.isnan(current)]
    
    if len(reference) == 0 or len(current) == 0:
        return 0.0
    
    # Crear histogramas
    min_val = min(reference.min(), current.min())
    max_val = max(reference.max(), current.max())
    bins_edges = np.linspace(min_val, max_val, bins + 1)
    
    ref_hist, _ = np.histogram(reference, bins=bins_edges)
    cur_hist, _ = np.histogram(current, bins=bins_edges)
    
    # Normalizar (con suavizado)
    ref_hist = (ref_hist + 1e-10) / (ref_hist.sum() + 1e-10 * len(ref_hist))
    cur_hist = (cur_hist + 1e-10) / (cur_hist.sum() + 1e-10 * len(cur_hist))
    
    # Calcular divergencia
    js_div = jensenshannon(ref_hist, cur_hist)
    
    return js_div


def calculate_chi_square(reference, current):
    """
    Calcula el test Chi-cuadrado para variables categóricas
    
    Mide si la distribución de categorías ha cambiado.
    - p-value < 0.05: Cambio significativo en la distribución
    """
    # Obtener todas las categorías únicas
    all_categories = list(set(reference) | set(current))
    
    if len(all_categories) <= 1:
        return 0.0, 1.0, 0.0
    
    # Contar frecuencias
    ref_counts = pd.Series(reference).value_counts()
    cur_counts = pd.Series(current).value_counts()
    
    # Crear tabla de contingencia
    contingency_table = pd.DataFrame({
        'reference': [ref_counts.get(cat, 0) for cat in all_categories],
        'current': [cur_counts.get(cat, 0) for cat in all_categories]
    })
    
    # Chi-cuadrado
    try:
        chi2, p_value, dof, expected = chi2_contingency(contingency_table.T)
        
        # Cramér's V (medida del tamaño del efecto)
        n = contingency_table.sum().sum()
        cramers_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
        
        return chi2, p_value, cramers_v
    except:
        return 0.0, 1.0, 0.0


def analyze_drift(baseline_df, current_df, exclude_cols=['Diagnosis']):
    """
    Analiza data drift para todas las variables
    """
    print("\n" + "="*80)
    print("ANÁLISIS DE DATA DRIFT")
    print("="*80)
    
    feature_cols = [col for col in baseline_df.columns if col not in exclude_cols]
    
    # Clasificar columnas
    numeric_cols = baseline_df[feature_cols].select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = baseline_df[feature_cols].select_dtypes(include=['object']).columns.tolist()
    
    drift_results = []
    
    # Analizar variables numéricas
    print(f"\n📊 Analizando {len(numeric_cols)} variables numéricas...")
    for col in numeric_cols:
        ref_data = baseline_df[col].dropna().values
        cur_data = current_df[col].dropna().values
        
        if len(ref_data) > 0 and len(cur_data) > 0:
            # Calcular métricas
            psi = calculate_psi(ref_data, cur_data)
            ks_stat, ks_pval = calculate_ks_statistic(ref_data, cur_data)
            js_div = calculate_jensen_shannon(ref_data, cur_data)
            
            # Determinar nivel de drift
            if psi < 0.1 and ks_pval >= 0.05:
                drift_level = "Sin drift"
            elif psi < 0.25 or (ks_pval < 0.05 and ks_stat < 0.2):
                drift_level = "Drift moderado"
            else:
                drift_level = "Drift significativo"
            
            drift_results.append({
                'feature': col,
                'type': 'numeric',
                'psi': round(psi, 4),
                'ks_statistic': round(ks_stat, 4),
                'ks_pvalue': round(ks_pval, 4),
                'js_divergence': round(js_div, 4),
                'chi2': None,
                'chi2_pvalue': None,
                'cramers_v': None,
                'drift_level': drift_level
            })
    
    # Analizar variables categóricas
    print(f"📝 Analizando {len(categorical_cols)} variables categóricas...")
    for col in categorical_cols:
        ref_data = baseline_df[col].dropna()
        cur_data = current_df[col].dropna()
        
        if len(ref_data) > 0 and len(cur_data) > 0:
            # Calcular Chi-cuadrado
            chi2, p_value, cramers_v = calculate_chi_square(ref_data, cur_data)
            
            # Determinar nivel de drift
            if p_value >= 0.05 and cramers_v < 0.1:
                drift_level = "Sin drift"
            elif p_value < 0.05 and cramers_v < 0.3:
                drift_level = "Drift moderado"
            else:
                drift_level = "Drift significativo"
            
            drift_results.append({
                'feature': col,
                'type': 'categorical',
                'psi': None,
                'ks_statistic': None,
                'ks_pvalue': None,
                'js_divergence': None,
                'chi2': round(chi2, 4),
                'chi2_pvalue': round(p_value, 4),
                'cramers_v': round(cramers_v, 4),
                'drift_level': drift_level
            })
    
    # Crear DataFrame con resultados
    results_df = pd.DataFrame(drift_results)
    
    return results_df


def generate_summary(results_df):
    """Genera resumen del análisis de drift"""
    print("\n" + "="*80)
    print("RESUMEN DE DRIFT")
    print("="*80)
    
    # Contar por nivel de drift
    drift_counts = results_df['drift_level'].value_counts()
    
    print(f"\n📊 Resumen por nivel de drift:")
    for level, count in drift_counts.items():
        pct = (count / len(results_df)) * 100
        print(f"   {level}: {count} features ({pct:.1f}%)")
    
    # Features con drift significativo
    significant_drift = results_df[results_df['drift_level'] == 'Drift significativo']
    
    if len(significant_drift) > 0:
        print(f"\n⚠️  Features con drift significativo:")
        for _, row in significant_drift.iterrows():
            print(f"   - {row['feature']} ({row['type']})")
    else:
        print(f"\n✓ No se detectó drift significativo en ninguna feature")
    
    return drift_counts


def save_monitoring_results(results_df, drift_summary):
    """Guarda los resultados del monitoreo"""
    print("\n" + "="*80)
    print("GUARDANDO RESULTADOS")
    print("="*80)
    
    project_root = Path(__file__).parent.parent.parent
    monitoring_dir = project_root / "monitoring_results"
    monitoring_dir.mkdir(parents=True, exist_ok=True)
    
    # Timestamp para los archivos
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. Guardar resultados detallados en CSV
    results_path = monitoring_dir / f"drift_report_{timestamp}.csv"
    results_df.to_csv(results_path, index=False)
    print(f"\n💾 Resultados detallados guardados en: {results_path}")
    
    # También guardar como drift_report.csv (último reporte)
    latest_path = monitoring_dir / "drift_report.csv"
    results_df.to_csv(latest_path, index=False)
    print(f"💾 Último reporte guardado en: {latest_path}")
    
    # 2. Guardar resumen en JSON
    summary_dict = {
        'timestamp': datetime.now().isoformat(),
        'total_features': len(results_df),
        'drift_summary': {
            level: int(count) for level, count in drift_summary.items()
        },
        'features_with_significant_drift': results_df[
            results_df['drift_level'] == 'Drift significativo'
        ]['feature'].tolist()
    }
    
    summary_path = monitoring_dir / f"drift_summary_{timestamp}.json"
    with open(summary_path, 'w') as f:
        json.dump(summary_dict, f, indent=4)
    print(f"💾 Resumen guardado en: {summary_path}")
    
    # También guardar como drift_summary.json (último resumen)
    latest_summary_path = monitoring_dir / "drift_summary.json"
    with open(latest_summary_path, 'w') as f:
        json.dump(summary_dict, f, indent=4)
    print(f"💾 Último resumen guardado en: {latest_summary_path}")


def main():
    """Función principal del script de monitoreo"""
    print("="*80)
    print("PASO 5: MONITOREO DE DATA DRIFT")
    print("="*80)
    
    # 1. Cargar datos baseline
    baseline_df = load_baseline_data()
    
    # 2. Simular/cargar datos actuales
    # En producción, aquí cargarías datos nuevos reales
    current_df = simulate_current_data(baseline_df, drift_percentage=0.2)
    
    # 3. Analizar drift
    results_df = analyze_drift(baseline_df, current_df)
    
    # 4. Generar resumen
    drift_summary = generate_summary(results_df)
    
    # 5. Guardar resultados
    save_monitoring_results(results_df, drift_summary)
    
    print("\n" + "="*80)
    print("✅ PASO 5 COMPLETADO EXITOSAMENTE")
    print("="*80)
    print(f"\nLos resultados están disponibles para visualización en Streamlit")


if __name__ == "__main__":
    main()
