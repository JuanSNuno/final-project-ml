"""
Aplicación Streamlit para Monitoreo de Data Drift
Panel interactivo de visualización para métricas de monitoreo de modelos ML
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
from scipy import stats
from scipy.spatial.distance import jensenshannon
from scipy.stats import ks_2samp, chi2_contingency

# Configuración de la página
st.set_page_config(
    page_title="Monitoreo de Data Drift",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Título principal
st.title("🎯 Sistema de Monitoreo de Data Drift")
st.markdown("---")

# ==============================================================================
# FUNCIONES DE CÁLCULO DE DRIFT
# ==============================================================================

@st.cache_data
def calculate_psi(expected, actual, bins=10):
    """Calcular Population Stability Index (PSI)"""
    expected = expected[~np.isnan(expected)]
    actual = actual[~np.isnan(actual)]
    
    breakpoints = np.quantile(expected, np.linspace(0, 1, bins + 1))
    breakpoints = np.unique(breakpoints)
    
    if len(breakpoints) < 2:
        return 0.0
    
    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]
    
    expected_percents = (expected_counts + 1) / (len(expected) + len(breakpoints) - 1)
    actual_percents = (actual_counts + 1) / (len(actual) + len(breakpoints) - 1)
    
    psi = np.sum((actual_percents - expected_percents) * np.log(actual_percents / expected_percents))
    
    return psi


def calculate_ks_statistic(reference, current):
    """Calcular Kolmogorov-Smirnov test"""
    reference = reference[~np.isnan(reference)]
    current = current[~np.isnan(current)]
    return ks_2samp(reference, current)


def calculate_jensen_shannon(reference, current, bins=30):
    """Calcular Jensen-Shannon divergence"""
    reference = reference[~np.isnan(reference)]
    current = current[~np.isnan(current)]
    
    min_val = min(reference.min(), current.min())
    max_val = max(reference.max(), current.max())
    bins_edges = np.linspace(min_val, max_val, bins + 1)
    
    ref_hist, _ = np.histogram(reference, bins=bins_edges)
    cur_hist, _ = np.histogram(current, bins=bins_edges)
    
    ref_hist = (ref_hist + 1e-10) / (ref_hist.sum() + 1e-10 * len(ref_hist))
    cur_hist = (cur_hist + 1e-10) / (cur_hist.sum() + 1e-10 * len(cur_hist))
    
    js_div = jensenshannon(ref_hist, cur_hist)
    
    return js_div


def calculate_chi_square(reference, current):
    """Calcular test Chi-cuadrado para variables categóricas"""
    all_categories = list(set(reference) | set(current))
    
    ref_counts = pd.Series(reference).value_counts()
    cur_counts = pd.Series(current).value_counts()
    
    contingency_table = pd.DataFrame({
        'reference': [ref_counts.get(cat, 0) for cat in all_categories],
        'current': [cur_counts.get(cat, 0) for cat in all_categories]
    })
    
    chi2, p_value, dof, expected = chi2_contingency(contingency_table.T)
    
    n = contingency_table.sum().sum()
    cramers_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
    
    return chi2, p_value, cramers_v


# ==============================================================================
# CARGA DE DATOS
# ==============================================================================

@st.cache_data
def load_data():
    """Cargar y preparar datos"""
    config_path = "../../config.json"
    data_path = None
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            data_path = config.get('data_path', 'alzheimers_disease_data.csv')
    else:
        data_path = "../../alzheimers_disease_data.csv"
    
    df_full = pd.read_csv(data_path)
    
    # Simular datos históricos y actuales
    split_point = int(len(df_full) * 0.8)
    df_reference = df_full.iloc[:split_point].copy()
    df_current = df_full.iloc[split_point:].copy()
    
    return df_reference, df_current, df_full


# ==============================================================================
# ANÁLISIS DE DRIFT
# ==============================================================================

@st.cache_data
def analyze_drift(df_reference, df_current, exclude_cols=['PatientID', 'DoctorInCharge']):
    """Calcular métricas de drift para todas las variables"""
    feature_cols = [col for col in df_reference.columns if col not in exclude_cols]
    
    numeric_cols = df_reference[feature_cols].select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df_reference[feature_cols].select_dtypes(include=['object']).columns.tolist()
    
    drift_results = []
    
    # Analizar variables numéricas
    for col in numeric_cols:
        ref_data = df_reference[col].dropna().values
        cur_data = df_current[col].dropna().values
        
        if len(ref_data) > 0 and len(cur_data) > 0:
            psi = calculate_psi(ref_data, cur_data)
            ks_stat, ks_pval = calculate_ks_statistic(ref_data, cur_data)
            js_div = calculate_jensen_shannon(ref_data, cur_data)
            
            if psi < 0.1:
                alert = "✅ OK"
            elif psi < 0.2:
                alert = "⚠️ MODERADO"
            else:
                alert = "🚨 CRÍTICO"
            
            drift_results.append({
                'Variable': col,
                'Tipo': 'Numérica',
                'PSI': round(psi, 4),
                'KS_Statistic': round(ks_stat, 4),
                'KS_PValue': round(ks_pval, 4),
                'JS_Divergence': round(js_div, 4),
                'Chi2': None,
                'Chi2_PValue': None,
                'Cramers_V': None,
                'Alerta': alert
            })
    
    # Analizar variables categóricas
    for col in categorical_cols:
        ref_data = df_reference[col].dropna().values
        cur_data = df_current[col].dropna().values
        
        if len(ref_data) > 0 and len(cur_data) > 0:
            chi2, chi2_pval, cramers_v = calculate_chi_square(ref_data, cur_data)
            
            if cramers_v < 0.1:
                alert = "✅ OK"
            elif cramers_v < 0.3:
                alert = "⚠️ MODERADO"
            else:
                alert = "🚨 CRÍTICO"
            
            drift_results.append({
                'Variable': col,
                'Tipo': 'Categórica',
                'PSI': None,
                'KS_Statistic': None,
                'KS_PValue': None,
                'JS_Divergence': None,
                'Chi2': round(chi2, 4),
                'Chi2_PValue': round(chi2_pval, 4),
                'Cramers_V': round(cramers_v, 4),
                'Alerta': alert
            })
    
    return pd.DataFrame(drift_results)


# ==============================================================================
# INTERFAZ PRINCIPAL
# ==============================================================================

# Cargar datos
with st.spinner('Cargando datos...'):
    df_reference, df_current, df_full = load_data()
    drift_df = analyze_drift(df_reference, df_current)

# Sidebar - Controles
st.sidebar.header("⚙️ Configuración")
st.sidebar.markdown("---")

# Filtros
st.sidebar.subheader("Filtros")
alert_filter = st.sidebar.multiselect(
    "Nivel de Alerta:",
    options=["✅ OK", "⚠️ MODERADO", "🚨 CRÍTICO"],
    default=["✅ OK", "⚠️ MODERADO", "🚨 CRÍTICO"]
)

type_filter = st.sidebar.multiselect(
    "Tipo de Variable:",
    options=["Numérica", "Categórica"],
    default=["Numérica", "Categórica"]
)

# Aplicar filtros
drift_filtered = drift_df[
    (drift_df['Alerta'].isin(alert_filter)) & 
    (drift_df['Tipo'].isin(type_filter))
]

# Información del dataset
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Información del Dataset")
st.sidebar.metric("Total de Variables", len(drift_df))
st.sidebar.metric("Datos de Referencia", len(df_reference))
st.sidebar.metric("Datos Actuales", len(df_current))

# ==============================================================================
# MÉTRICAS PRINCIPALES
# ==============================================================================

st.header("📊 Resumen Ejecutivo")

col1, col2, col3, col4 = st.columns(4)

critical_vars = drift_df[drift_df['Alerta'] == "🚨 CRÍTICO"]
moderate_vars = drift_df[drift_df['Alerta'] == "⚠️ MODERADO"]
ok_vars = drift_df[drift_df['Alerta'] == "✅ OK"]

with col1:
    st.metric(
        label="Variables Totales",
        value=len(drift_df),
        delta=None
    )

with col2:
    st.metric(
        label="🚨 Críticas",
        value=len(critical_vars),
        delta=f"{len(critical_vars)/len(drift_df)*100:.1f}%",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="⚠️ Moderadas",
        value=len(moderate_vars),
        delta=f"{len(moderate_vars)/len(drift_df)*100:.1f}%",
        delta_color="off"
    )

with col4:
    st.metric(
        label="✅ OK",
        value=len(ok_vars),
        delta=f"{len(ok_vars)/len(drift_df)*100:.1f}%",
        delta_color="normal"
    )

st.markdown("---")

# ==============================================================================
# VISUALIZACIONES
# ==============================================================================

# Tabs para organizar visualizaciones
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard General", 
    "📈 Distribuciones", 
    "📋 Tabla Detallada",
    "💡 Recomendaciones"
])

# TAB 1: Dashboard General
with tab1:
    st.subheader("Estado General del Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de dona
        fig, ax = plt.subplots(figsize=(8, 6))
        sizes = [len(ok_vars), len(moderate_vars), len(critical_vars)]
        labels = ['OK', 'Moderado', 'Crítico']
        colors = ['#2ecc71', '#f39c12', '#e74c3c']
        explode = (0.05, 0.05, 0.1)
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
               explode=explode, startangle=90, textprops={'fontweight': 'bold', 'fontsize': 12})
        ax.set_title('Distribución de Alertas', fontsize=14, fontweight='bold', pad=20)
        st.pyplot(fig)
    
    with col2:
        # Top variables con mayor drift
        fig, ax = plt.subplots(figsize=(8, 6))
        top_drift = drift_df[drift_df['Tipo'] == 'Numérica'].nlargest(10, 'PSI')
        
        if len(top_drift) > 0:
            colors_bars = ['#e74c3c' if x >= 0.2 else '#f39c12' if x >= 0.1 else '#2ecc71' 
                          for x in top_drift['PSI']]
            ax.barh(top_drift['Variable'], top_drift['PSI'], color=colors_bars, alpha=0.8)
            ax.axvline(x=0.1, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Umbral Moderado')
            ax.axvline(x=0.2, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Umbral Crítico')
            ax.set_xlabel('PSI', fontweight='bold', fontsize=11)
            ax.set_title('Top 10 Variables con Mayor Drift (PSI)', fontsize=14, fontweight='bold', pad=20)
            ax.legend()
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
        st.pyplot(fig)
    
    # Evolución temporal simulada
    st.subheader("Evolución Temporal del Drift")
    
    fig, ax = plt.subplots(figsize=(14, 5))
    time_points = pd.date_range(end=datetime.now(), periods=20, freq='D')
    psi_mean = drift_df[drift_df['Tipo'] == 'Numérica']['PSI'].mean()
    drift_timeline = [psi_mean * (0.8 + 0.4 * np.random.random()) for _ in range(20)]
    
    ax.plot(time_points, drift_timeline, marker='o', linewidth=2, markersize=6, color='#3498db', label='PSI Promedio')
    ax.axhline(y=0.1, color='orange', linestyle='--', linewidth=2, label='Umbral Moderado', alpha=0.7)
    ax.axhline(y=0.2, color='red', linestyle='--', linewidth=2, label='Umbral Crítico', alpha=0.7)
    ax.fill_between(time_points, 0, 0.1, color='green', alpha=0.1)
    ax.fill_between(time_points, 0.1, 0.2, color='orange', alpha=0.1)
    ax.fill_between(time_points, 0.2, max(drift_timeline + [0.25]), color='red', alpha=0.1)
    
    ax.set_xlabel('Fecha', fontweight='bold', fontsize=11)
    ax.set_ylabel('PSI Promedio', fontweight='bold', fontsize=11)
    ax.set_title('Evolución del Drift en los Últimos 20 Días', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left')
    ax.grid(alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# TAB 2: Distribuciones
with tab2:
    st.subheader("Comparación de Distribuciones")
    
    # Seleccionar variable
    vars_list = drift_filtered['Variable'].tolist()
    
    if len(vars_list) > 0:
        selected_var = st.selectbox("Seleccione una variable:", vars_list)
        
        var_info = drift_filtered[drift_filtered['Variable'] == selected_var].iloc[0]
        
        # Mostrar métricas de la variable
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tipo", var_info['Tipo'])
        with col2:
            st.metric("Alerta", var_info['Alerta'])
        
        if var_info['Tipo'] == 'Numérica':
            with col3:
                st.metric("PSI", f"{var_info['PSI']:.4f}")
            with col4:
                st.metric("JS Divergence", f"{var_info['JS_Divergence']:.4f}")
            
            # Gráfico de distribución
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            ref_data = df_reference[selected_var].dropna()
            cur_data = df_current[selected_var].dropna()
            
            # Histogramas
            axes[0].hist(ref_data, bins=30, alpha=0.6, label='Referencia', color='blue', density=True)
            axes[0].hist(cur_data, bins=30, alpha=0.6, label='Actual', color='red', density=True)
            axes[0].set_xlabel(selected_var, fontweight='bold')
            axes[0].set_ylabel('Densidad', fontweight='bold')
            axes[0].set_title(f'Distribución: {selected_var}', fontsize=12, fontweight='bold')
            axes[0].legend()
            axes[0].grid(alpha=0.3)
            
            # Boxplots
            data_to_plot = [ref_data, cur_data]
            axes[1].boxplot(data_to_plot, labels=['Referencia', 'Actual'])
            axes[1].set_ylabel(selected_var, fontweight='bold')
            axes[1].set_title(f'Boxplot: {selected_var}', fontsize=12, fontweight='bold')
            axes[1].grid(alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Estadísticas
            st.subheader("Estadísticas Descriptivas")
            stats_df = pd.DataFrame({
                'Métrica': ['Media', 'Mediana', 'Desv. Estándar', 'Mínimo', 'Máximo'],
                'Referencia': [
                    f"{ref_data.mean():.2f}",
                    f"{ref_data.median():.2f}",
                    f"{ref_data.std():.2f}",
                    f"{ref_data.min():.2f}",
                    f"{ref_data.max():.2f}"
                ],
                'Actual': [
                    f"{cur_data.mean():.2f}",
                    f"{cur_data.median():.2f}",
                    f"{cur_data.std():.2f}",
                    f"{cur_data.min():.2f}",
                    f"{cur_data.max():.2f}"
                ]
            })
            st.dataframe(stats_df, use_container_width=True)
        
        else:  # Categórica
            with col3:
                st.metric("Chi2", f"{var_info['Chi2']:.4f}")
            with col4:
                st.metric("Cramér's V", f"{var_info['Cramers_V']:.4f}")
            
            # Gráfico de barras
            fig, ax = plt.subplots(figsize=(12, 6))
            
            ref_data = df_reference[selected_var].value_counts(normalize=True)
            cur_data = df_current[selected_var].value_counts(normalize=True)
            
            all_cats = list(set(ref_data.index) | set(cur_data.index))
            x = np.arange(len(all_cats))
            width = 0.35
            
            ref_vals = [ref_data.get(cat, 0) for cat in all_cats]
            cur_vals = [cur_data.get(cat, 0) for cat in all_cats]
            
            ax.bar(x - width/2, ref_vals, width, label='Referencia', alpha=0.8, color='blue')
            ax.bar(x + width/2, cur_vals, width, label='Actual', alpha=0.8, color='red')
            
            ax.set_xlabel('Categorías', fontweight='bold')
            ax.set_ylabel('Frecuencia Relativa', fontweight='bold')
            ax.set_title(f'Distribución: {selected_var}', fontsize=12, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(all_cats, rotation=45, ha='right')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
    else:
        st.info("No hay variables que cumplan con los filtros seleccionados.")

# TAB 3: Tabla Detallada
with tab3:
    st.subheader("Tabla Detallada de Métricas")
    
    # Mostrar tabla filtrada
    st.dataframe(
        drift_filtered.style.applymap(
            lambda x: 'background-color: #ffcccc' if x == "🚨 CRÍTICO" else 
                     ('background-color: #fff4cc' if x == "⚠️ MODERADO" else ''),
            subset=['Alerta']
        ),
        use_container_width=True,
        height=400
    )
    
    # Opción de descarga
    csv = drift_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte CSV",
        data=csv,
        file_name=f'drift_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
        mime='text/csv',
    )

# TAB 4: Recomendaciones
with tab4:
    st.subheader("💡 Recomendaciones Automatizadas")
    
    # Calcular métricas de riesgo
    total_vars = len(drift_df)
    risk_score = (len(critical_vars) * 3 + len(moderate_vars) * 1)
    max_risk = total_vars * 3
    risk_percentage = (risk_score / max_risk) * 100
    
    # Mostrar nivel de riesgo
    if risk_percentage < 10:
        st.success("🟢 **NIVEL DE RIESGO: BAJO**")
        st.write("El sistema está operando dentro de parámetros normales.")
    elif risk_percentage < 30:
        st.warning("🟡 **NIVEL DE RIESGO: MEDIO**")
        st.write("Se detectaron cambios moderados que requieren atención.")
    else:
        st.error("🔴 **NIVEL DE RIESGO: ALTO**")
        st.write("Se requiere acción inmediata - considerar reentrenamiento del modelo.")
    
    st.metric("Score de Riesgo", f"{risk_score}/{max_risk}", f"{risk_percentage:.1f}%")
    
    st.markdown("---")
    
    # Recomendaciones específicas
    if len(critical_vars) > 0:
        st.error("### 🚨 ACCIÓN INMEDIATA REQUERIDA")
        st.write("**Variables con drift crítico:**")
        for _, row in critical_vars.head(10).iterrows():
            st.write(f"- **{row['Variable']}** ({row['Tipo']})")
        
        st.write("\n**Acciones recomendadas:**")
        st.write("1. ✅ Investigar causas del drift en estas variables")
        st.write("2. ✅ Validar calidad de datos actuales")
        st.write("3. ✅ Considerar reentrenamiento del modelo")
        st.write("4. ✅ Revisar pipeline de preprocesamiento")
    
    if len(moderate_vars) > 0:
        st.warning("### ⚠️ MONITOREO CONTINUO")
        st.write("**Variables con drift moderado:**")
        for _, row in moderate_vars.head(10).iterrows():
            st.write(f"- **{row['Variable']}** ({row['Tipo']})")
        
        st.write("\n**Acciones recomendadas:**")
        st.write("1. 📊 Aumentar frecuencia de monitoreo")
        st.write("2. 📊 Establecer alertas tempranas")
        st.write("3. 📊 Documentar cambios observados")
    
    if len(critical_vars) == 0 and len(moderate_vars) == 0:
        st.success("### ✅ ESTADO ÓPTIMO")
        st.write("Todas las variables están dentro de umbrales aceptables.")
        st.write("Mantener frecuencia de monitoreo actual.")
    
    st.markdown("---")
    
    # Periodicidad recomendada
    st.subheader("📅 Periodicidad de Monitoreo Recomendada")
    
    if risk_percentage >= 30:
        st.error("**🔴 Monitoreo DIARIO** - Revisión cada 3 días")
    elif risk_percentage >= 10:
        st.warning("**🟡 Monitoreo SEMANAL** - Revisión cada 2 semanas")
    else:
        st.success("**🟢 Monitoreo QUINCENAL** - Revisión mensual")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Sistema de Monitoreo de Data Drift v1.0 | Desarrollado para MLOps Pipeline</p>
    </div>
    """,
    unsafe_allow_html=True
)
