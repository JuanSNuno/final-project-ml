"""
prediction_ui.py
Interfaz profesional de usuario para predicciones de Alzheimer

UI/UX moderna y responsiva con Streamlit para consultar predicciones
del modelo de forma visual e intuitiva.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
from typing import Dict, Any

# ==============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==============================================================================

st.set_page_config(
    page_title="Alzheimer Prediction - AI System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Sistema de Predicción de Alzheimer basado en ML"
    }
)

# CSS personalizado para mayor profesionalismo
st.markdown("""
    <style>
    /* Variables de color */
    :root {
        --primary-color: #0066cc;
        --secondary-color: #00d4ff;
        --success-color: #00cc44;
        --warning-color: #ff9900;
        --danger-color: #ff3333;
        --dark-bg: #0a0e27;
        --light-bg: #f5f7fa;
    }
    
    /* Estilos generales */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Cards personalizadas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .prediction-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
    }
    
    .prediction-medium {
        background: linear-gradient(135deg, #ffd93d 0%, #ffb700 100%);
        color: white;
    }
    
    .prediction-low {
        background: linear-gradient(135deg, #6bcf7f 0%, #4fa95c 100%);
        color: white;
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(90deg, #0066cc, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    h2 {
        color: #0066cc;
        border-bottom: 3px solid #00d4ff;
        padding-bottom: 10px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f5f7fa;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# CONFIGURACIÓN Y CONSTANTES
# ==============================================================================

# URL de la API - se puede configurar por variable de entorno
API_URL = "http://localhost:8000"

# Características y descripción
FEATURE_DESCRIPTIONS = {
    "Age": "Edad del paciente (años)",
    "Gender": "Género (0=Femenino, 1=Masculino)",
    "Ethnicity": "Etnicidad",
    "EducationLevel": "Nivel educativo (0-4)",
    "BMI": "Índice de masa corporal",
    "Smoking": "Fumador (0=No, 1=Sí)",
    "AlcoholConsumption": "Consumo de alcohol (unidades/semana)",
    "PhysicalActivity": "Actividad física (horas/semana)",
    "DietQuality": "Calidad de la dieta (0-10)",
    "SleepQuality": "Calidad del sueño (0-10)",
    "FamilyHistoryAlzheimers": "Historia familiar (0=No, 1=Sí)",
    "CardiovascularDisease": "Enfermedad cardiovascular (0=No, 1=Sí)",
    "Diabetes": "Diabetes (0=No, 1=Sí)",
    "Depression": "Depresión (0=No, 1=Sí)",
    "HeadInjury": "Lesión en la cabeza (0=No, 1=Sí)",
    "Hypertension": "Hipertensión (0=No, 1=Sí)",
    "SystolicBP": "Presión arterial sistólica (mmHg)",
    "DiastolicBP": "Presión arterial diastólica (mmHg)",
    "CholesterolTotal": "Colesterol total (mg/dL)",
    "CholesterolLDL": "Colesterol LDL (mg/dL)",
    "CholesterolHDL": "Colesterol HDL (mg/dL)",
    "CholesterolTriglycerides": "Triglicéridos (mg/dL)",
    "MMSE": "Mini-Mental State Examination (0-30)",
    "FunctionalAssessment": "Evaluación funcional (0-10)",
    "MemoryComplaints": "Quejas de memoria (0=No, 1=Sí)",
    "BehavioralProblems": "Problemas de comportamiento (0=No, 1=Sí)",
    "ADL": "Activities of Daily Living (0-10)",
    "Confusion": "Confusión (0=No, 1=Sí)",
    "Disorientation": "Desorientación (0=No, 1=Sí)",
    "PersonalityChanges": "Cambios de personalidad (0=No, 1=Sí)",
    "DifficultyCompletingTasks": "Dificultad completando tareas (0=No, 1=Sí)",
    "Forgetfulness": "Olvido (0=No, 1=Sí)"
}

# Valores por defecto
DEFAULT_VALUES = {
    "Age": 70.0,
    "Gender": 1,
    "Ethnicity": 0,
    "EducationLevel": 2,
    "BMI": 25.5,
    "Smoking": 0,
    "AlcoholConsumption": 5.0,
    "PhysicalActivity": 6.5,
    "DietQuality": 7.0,
    "SleepQuality": 7.5,
    "FamilyHistoryAlzheimers": 1,
    "CardiovascularDisease": 0,
    "Diabetes": 0,
    "Depression": 0,
    "HeadInjury": 0,
    "Hypertension": 1,
    "SystolicBP": 140,
    "DiastolicBP": 85,
    "CholesterolTotal": 220.0,
    "CholesterolLDL": 130.0,
    "CholesterolHDL": 45.0,
    "CholesterolTriglycerides": 180.0,
    "MMSE": 24.0,
    "FunctionalAssessment": 7.5,
    "MemoryComplaints": 1,
    "BehavioralProblems": 0,
    "ADL": 5.5,
    "Confusion": 0,
    "Disorientation": 0,
    "PersonalityChanges": 0,
    "DifficultyCompletingTasks": 1,
    "Forgetfulness": 1
}

# ==============================================================================
# FUNCIONES AUXILIARES
# ==============================================================================

@st.cache_resource
def check_api_health():
    """Verifica si la API está disponible"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_model_info():
    """Obtiene información del modelo"""
    try:
        response = requests.get(f"{API_URL}/model/info", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def predict_single(patient_data: Dict) -> Dict[str, Any]:
    """Realiza una predicción individual"""
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=patient_data,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error de API: {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"error": "No se puede conectar a la API"}
    except Exception as e:
        return {"error": str(e)}

def get_risk_color(probability: float) -> str:
    """Retorna color basado en probabilidad"""
    if probability >= 0.7:
        return "#ff3333"  # Rojo - Alto riesgo
    elif probability >= 0.4:
        return "#ff9900"  # Naranja - Riesgo moderado
    else:
        return "#00cc44"  # Verde - Bajo riesgo

def get_risk_label(probability: float) -> str:
    """Retorna etiqueta de riesgo"""
    if probability >= 0.7:
        return "🔴 ALTO RIESGO"
    elif probability >= 0.4:
        return "🟡 RIESGO MODERADO"
    else:
        return "🟢 BAJO RIESGO"

# ==============================================================================
# HEADER
# ==============================================================================

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3050/3050159.png", width=80)

with col2:
    st.title("🧠 Alzheimer Prediction System")
    st.markdown("### Sistema Inteligente de Predicción de Alzheimer")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    <p>Utiliza Machine Learning avanzado para evaluar el riesgo de Alzheimer</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# VERIFICACIÓN DE CONEXIÓN A LA API
# ==============================================================================

api_available = check_api_health()

if not api_available:
    st.error("""
    ❌ **API no disponible**
    
    La API no está respondiendo en `{API_URL}`
    
    Por favor:
    1. Asegúrate de que el servidor de API está ejecutándose
    2. Desde otra terminal, ejecuta: `python mlops_pipeline/src/scripts/model_deploy.py`
    3. O si usas Docker: `docker run -p 8000:8000 alzheimer-api`
    
    Luego recarga esta página.
    """.format(API_URL=API_URL))
    st.stop()

# Mostrar estado de la API
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Estado de la API", "🟢 Conectada", delta="Online")

with col2:
    model_info = get_model_info()
    if model_info:
        model_name = model_info.get("model_metadata", {}).get("model_name", "Unknown")
        st.metric("Modelo", model_name)

with col3:
    st.metric("Timestamp", datetime.now().strftime("%H:%M:%S"))

st.markdown("---")

# ==============================================================================
# INTERFAZ PRINCIPAL
# ==============================================================================

# Crear pestañas
tab1, tab2, tab3 = st.tabs([
    "📋 Predicción Individual",
    "📊 Predicción por Lote",
    "ℹ️ Información del Sistema"
])

# ==============================================================================
# TAB 1: PREDICCIÓN INDIVIDUAL
# ==============================================================================

with tab1:
    st.header("Predicción Individual")
    
    # Crear dos columnas para el formulario
    col_form, col_preview = st.columns([2, 1])
    
    with col_form:
        st.subheader("Datos del Paciente")
        
        # Crear secciones organizadas
        with st.expander("📊 Información General", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input(
                    FEATURE_DESCRIPTIONS["Age"],
                    min_value=18.0, max_value=120.0, value=DEFAULT_VALUES["Age"],
                    step=1.0, key="age"
                )
                gender = st.radio(
                    FEATURE_DESCRIPTIONS["Gender"],
                    options=[0, 1], format_func=lambda x: "Femenino" if x == 0 else "Masculino",
                    key="gender"
                )
            
            with col2:
                bmi = st.number_input(
                    FEATURE_DESCRIPTIONS["BMI"],
                    min_value=10.0, max_value=60.0, value=DEFAULT_VALUES["BMI"],
                    step=0.1, key="bmi"
                )
                education = st.number_input(
                    FEATURE_DESCRIPTIONS["EducationLevel"],
                    min_value=0, max_value=4, value=DEFAULT_VALUES["EducationLevel"],
                    step=1, key="education"
                )
        
        with st.expander("❤️ Factores de Riesgo Médicos", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                smoking = st.checkbox(
                    "Fumador",
                    value=bool(DEFAULT_VALUES["Smoking"]),
                    key="smoking"
                )
                diabetes = st.checkbox(
                    "Diabetes",
                    value=bool(DEFAULT_VALUES["Diabetes"]),
                    key="diabetes"
                )
                heart_disease = st.checkbox(
                    "Enfermedad Cardiovascular",
                    value=bool(DEFAULT_VALUES["CardiovascularDisease"]),
                    key="heart"
                )
            
            with col2:
                hypertension = st.checkbox(
                    "Hipertensión",
                    value=bool(DEFAULT_VALUES["Hypertension"]),
                    key="hypertension"
                )
                depression = st.checkbox(
                    "Depresión",
                    value=bool(DEFAULT_VALUES["Depression"]),
                    key="depression"
                )
                head_injury = st.checkbox(
                    "Antecedente de Lesión en Cabeza",
                    value=bool(DEFAULT_VALUES["HeadInjury"]),
                    key="head_injury"
                )
            
            with col3:
                family_history = st.checkbox(
                    "Historia Familiar de Alzheimer",
                    value=bool(DEFAULT_VALUES["FamilyHistoryAlzheimers"]),
                    key="family_history"
                )
        
        with st.expander("🧬 Indicadores Cognitivos", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                mmse = st.slider(
                    FEATURE_DESCRIPTIONS["MMSE"],
                    min_value=0, max_value=30, value=int(DEFAULT_VALUES["MMSE"]),
                    step=1, key="mmse"
                )
                memory_complaints = st.checkbox(
                    "Quejas de Memoria",
                    value=bool(DEFAULT_VALUES["MemoryComplaints"]),
                    key="memory"
                )
                confusion = st.checkbox(
                    "Confusión",
                    value=bool(DEFAULT_VALUES["Confusion"]),
                    key="confusion"
                )
            
            with col2:
                adl = st.slider(
                    FEATURE_DESCRIPTIONS["ADL"],
                    min_value=0.0, max_value=10.0, value=DEFAULT_VALUES["ADL"],
                    step=0.5, key="adl"
                )
                disorientation = st.checkbox(
                    "Desorientación",
                    value=bool(DEFAULT_VALUES["Disorientation"]),
                    key="disorientation"
                )
                personality_changes = st.checkbox(
                    "Cambios de Personalidad",
                    value=bool(DEFAULT_VALUES["PersonalityChanges"]),
                    key="personality"
                )
        
        with st.expander("💊 Valores de Laboratorio", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                systolic = st.number_input(
                    FEATURE_DESCRIPTIONS["SystolicBP"],
                    min_value=60, max_value=250, value=DEFAULT_VALUES["SystolicBP"],
                    step=1, key="systolic"
                )
                diastolic = st.number_input(
                    FEATURE_DESCRIPTIONS["DiastolicBP"],
                    min_value=40, max_value=150, value=DEFAULT_VALUES["DiastolicBP"],
                    step=1, key="diastolic"
                )
                total_chol = st.number_input(
                    FEATURE_DESCRIPTIONS["CholesterolTotal"],
                    min_value=100.0, max_value=400.0, value=DEFAULT_VALUES["CholesterolTotal"],
                    step=1.0, key="total_chol"
                )
            
            with col2:
                ldl = st.number_input(
                    FEATURE_DESCRIPTIONS["CholesterolLDL"],
                    min_value=50.0, max_value=300.0, value=DEFAULT_VALUES["CholesterolLDL"],
                    step=1.0, key="ldl"
                )
                hdl = st.number_input(
                    FEATURE_DESCRIPTIONS["CholesterolHDL"],
                    min_value=20.0, max_value=150.0, value=DEFAULT_VALUES["CholesterolHDL"],
                    step=1.0, key="hdl"
                )
                triglycerides = st.number_input(
                    FEATURE_DESCRIPTIONS["CholesterolTriglycerides"],
                    min_value=50.0, max_value=500.0, value=DEFAULT_VALUES["CholesterolTriglycerides"],
                    step=1.0, key="triglycerides"
                )
        
        with st.expander("🏃 Estilos de Vida", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                alcohol = st.slider(
                    FEATURE_DESCRIPTIONS["AlcoholConsumption"],
                    min_value=0.0, max_value=20.0, value=DEFAULT_VALUES["AlcoholConsumption"],
                    step=0.5, key="alcohol"
                )
                diet_quality = st.slider(
                    FEATURE_DESCRIPTIONS["DietQuality"],
                    min_value=0.0, max_value=10.0, value=DEFAULT_VALUES["DietQuality"],
                    step=0.5, key="diet"
                )
            
            with col2:
                physical_activity = st.slider(
                    FEATURE_DESCRIPTIONS["PhysicalActivity"],
                    min_value=0.0, max_value=24.0, value=DEFAULT_VALUES["PhysicalActivity"],
                    step=0.5, key="activity"
                )
                sleep_quality = st.slider(
                    FEATURE_DESCRIPTIONS["SleepQuality"],
                    min_value=0.0, max_value=10.0, value=DEFAULT_VALUES["SleepQuality"],
                    step=0.5, key="sleep"
                )
        
        with st.expander("📋 Otros Síntomas", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                behavioral = st.checkbox(
                    "Problemas de Comportamiento",
                    value=bool(DEFAULT_VALUES["BehavioralProblems"]),
                    key="behavioral"
                )
                functional = st.slider(
                    FEATURE_DESCRIPTIONS["FunctionalAssessment"],
                    min_value=0.0, max_value=10.0, value=DEFAULT_VALUES["FunctionalAssessment"],
                    step=0.5, key="functional"
                )
            
            with col2:
                difficulty = st.checkbox(
                    "Dificultad Completando Tareas",
                    value=bool(DEFAULT_VALUES["DifficultyCompletingTasks"]),
                    key="difficulty"
                )
                forgetfulness = st.checkbox(
                    "Olvido",
                    value=bool(DEFAULT_VALUES["Forgetfulness"]),
                    key="forgetfulness"
                )
        
        # Botón de predicción
        st.markdown("---")
        predict_button = st.button(
            "🔮 Realizar Predicción",
            key="predict_button",
            use_container_width=True,
            type="primary"
        )
    
    with col_preview:
        st.subheader("Resumen del Paciente")
        st.markdown(f"""
        **Edad:** {age:.0f} años  
        **Género:** {'M' if gender else 'F'}  
        **BMI:** {bmi:.1f}
        
        **Riesgos Detectados:**
        - Diabetes: {'✓' if diabetes else '✗'}
        - Hipertensión: {'✓' if hypertension else '✗'}
        - Enfermedad Cardíaca: {'✓' if heart_disease else '✗'}
        - Depresión: {'✓' if depression else '✗'}
        - Hist. Familiar: {'✓' if family_history else '✗'}
        
        **Cognitivos:**
        - MMSE: {mmse}/30
        - ADL: {adl:.1f}/10
        - Memoria: {'Quejas' if memory_complaints else 'Normal'}
        """)
    
    # Realizar predicción
    if predict_button:
        with st.spinner("🔄 Procesando predicción..."):
            patient_data = {
                "Age": age,
                "Gender": gender,
                "Ethnicity": DEFAULT_VALUES["Ethnicity"],
                "EducationLevel": education,
                "BMI": bmi,
                "Smoking": int(smoking),
                "AlcoholConsumption": alcohol,
                "PhysicalActivity": physical_activity,
                "DietQuality": diet_quality,
                "SleepQuality": sleep_quality,
                "FamilyHistoryAlzheimers": int(family_history),
                "CardiovascularDisease": int(heart_disease),
                "Diabetes": int(diabetes),
                "Depression": int(depression),
                "HeadInjury": int(head_injury),
                "Hypertension": int(hypertension),
                "SystolicBP": systolic,
                "DiastolicBP": diastolic,
                "CholesterolTotal": total_chol,
                "CholesterolLDL": ldl,
                "CholesterolHDL": hdl,
                "CholesterolTriglycerides": triglycerides,
                "MMSE": mmse,
                "FunctionalAssessment": functional,
                "MemoryComplaints": int(memory_complaints),
                "BehavioralProblems": int(behavioral),
                "ADL": adl,
                "Confusion": int(confusion),
                "Disorientation": int(disorientation),
                "PersonalityChanges": int(personality_changes),
                "DifficultyCompletingTasks": int(difficulty),
                "Forgetfulness": int(forgetfulness)
            }
            
            result = predict_single(patient_data)
        
        if "error" in result:
            st.error(f"❌ Error: {result['error']}")
        else:
            prediction = result.get("prediction", 0)
            probability = result.get("probability", 0.0)
            model_name = result.get("model_name", "Unknown")
            
            # Mostrar resultado
            st.markdown("---")
            st.subheader("Resultado de la Predicción")
            
            # Crear visualizaciones
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                # Gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=probability * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Probabilidad de Alzheimer (%)"},
                    delta={'reference': 50},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': get_risk_color(probability)},
                        'steps': [
                            {'range': [0, 40], 'color': "#e8f5e9"},
                            {'range': [40, 70], 'color': "#fff3e0"},
                            {'range': [70, 100], 'color': "#ffebee"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Resultado en cards
            st.markdown("---")
            
            result_col1, result_col2 = st.columns(2)
            
            with result_col1:
                st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, {get_risk_color(probability)} 0%, {get_risk_color(probability)}dd 100%);
                    padding: 30px;
                    border-radius: 15px;
                    color: white;
                    text-align: center;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                '>
                    <h2 style='color: white; margin: 0;'>{get_risk_label(probability)}</h2>
                    <h1 style='color: white; margin: 10px 0;'>{probability*100:.1f}%</h1>
                    <p style='color: white; margin: 0;'>Probabilidad de Alzheimer</p>
                </div>
                """, unsafe_allow_html=True)
            
            with result_col2:
                st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px;
                    border-radius: 15px;
                    color: white;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                '>
                    <h3 style='color: white; margin-top: 0;'>📊 Detalles</h3>
                    <p><b>Modelo:</b> {model_name}</p>
                    <p><b>Clasificación:</b> {"Positivo (Riesgo)" if prediction == 1 else "Negativo (Sin Riesgo)"}</p>
                    <p><b>Timestamp:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Recomendaciones
            st.markdown("---")
            st.subheader("📋 Recomendaciones")
            
            recommendations = []
            
            if probability >= 0.7:
                recommendations.append("🔴 **Riesgo Alto:** Se recomienda consulta urgente con especialista")
                recommendations.append("- Realizar pruebas neuropsicológicas completas")
                recommendations.append("- Considerar resonancia magnética (MRI)")
                recommendations.append("- Evaluación cognitiva detallada")
            elif probability >= 0.4:
                recommendations.append("🟡 **Riesgo Moderado:** Se recomienda seguimiento regular")
                recommendations.append("- Control cada 6 meses")
                recommendations.append("- Pruebas cognitivas periódicas")
                recommendations.append("- Estilo de vida saludable")
            else:
                recommendations.append("🟢 **Bajo Riesgo:** Mantener hábitos saludables")
                recommendations.append("- Continuar actividades cognitivas")
                recommendations.append("- Ejercicio físico regular")
                recommendations.append("- Control médico anual")
            
            for rec in recommendations:
                st.markdown(rec)
            
            # Guardar resultado en sesión
            if "predictions_history" not in st.session_state:
                st.session_state.predictions_history = []
            
            st.session_state.predictions_history.append({
                "timestamp": datetime.now(),
                "age": age,
                "probability": probability,
                "prediction": prediction,
                "model": model_name
            })

# ==============================================================================
# TAB 2: PREDICCIÓN POR LOTE
# ==============================================================================

with tab2:
    st.header("Predicción por Lote (Batch)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Opción 1: Cargar archivo CSV")
        uploaded_file = st.file_uploader(
            "Selecciona un archivo CSV",
            type="csv",
            help="El archivo debe tener las mismas columnas que las características del modelo"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✓ Archivo cargado: {uploaded_file.name}")
                st.dataframe(df.head(), use_container_width=True)
                
                if st.button("🔮 Predecir Lote", use_container_width=True, type="primary"):
                    # Convertir a lista de diccionarios
                    records = df.to_dict(orient='records')
                    
                    with st.spinner(f"Procesando {len(records)} registros..."):
                        predictions = []
                        progress_bar = st.progress(0)
                        
                        for idx, record in enumerate(records):
                            result = predict_single(record)
                            if "error" not in result:
                                predictions.append({
                                    **record,
                                    "prediction": result.get("prediction"),
                                    "probability": result.get("probability")
                                })
                            progress_bar.progress((idx + 1) / len(records))
                    
                    # Mostrar resultados
                    st.subheader("Resultados")
                    results_df = pd.DataFrame(predictions)
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Descargar resultados
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Descargar Resultados (CSV)",
                        data=csv,
                        file_name=f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                    # Estadísticas
                    st.subheader("Estadísticas del Lote")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Total Procesados",
                            len(predictions)
                        )
                    
                    with col2:
                        positives = sum(1 for p in predictions if p["prediction"] == 1)
                        st.metric(
                            "Casos Positivos",
                            positives
                        )
                    
                    with col3:
                        avg_prob = sum(p["probability"] for p in predictions) / len(predictions)
                        st.metric(
                            "Probabilidad Promedio",
                            f"{avg_prob*100:.1f}%"
                        )
                    
                    # Gráfico de distribución
                    fig = px.histogram(
                        results_df,
                        x="probability",
                        nbins=20,
                        title="Distribución de Probabilidades",
                        labels={"probability": "Probabilidad", "count": "Cantidad"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ Error al procesar archivo: {e}")
    
    with col2:
        st.markdown("### Opción 2: Datos Manuales")
        
        st.info("""
        📋 **Instrucciones:**
        1. Descarga la plantilla
        2. Completa los datos de los pacientes
        3. Sube el archivo CSV
        4. Obtén predicciones para todo el lote
        """)
        
        # Template
        template_data = {k: [DEFAULT_VALUES[k]] for k in DEFAULT_VALUES.keys()}
        template_df = pd.DataFrame(template_data)
        
        csv_template = template_df.to_csv(index=False)
        st.download_button(
            label="📄 Descargar Plantilla CSV",
            data=csv_template,
            file_name="template_pacientes.csv",
            mime="text/csv",
            use_container_width=True
        )

# ==============================================================================
# TAB 3: INFORMACIÓN DEL SISTEMA
# ==============================================================================

with tab3:
    st.header("Información del Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Información de la API")
        
        if model_info:
            st.json(model_info)
        else:
            st.warning("No se pudo obtener información del modelo")
    
    with col2:
        st.subheader("🔧 Configuración")
        
        st.markdown(f"""
        **URL de la API:** `{API_URL}`  
        **Estado:** {'🟢 Online' if api_available else '🔴 Offline'}  
        **Última Actualización:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)
        
        if "predictions_history" in st.session_state and len(st.session_state.predictions_history) > 0:
            st.subheader("📈 Historial de Predicciones")
            
            history_df = pd.DataFrame(st.session_state.predictions_history)
            st.dataframe(history_df, use_container_width=True)
            
            # Gráfico de histórico
            fig = px.line(
                history_df,
                x="timestamp",
                y="probability",
                markers=True,
                title="Histórico de Predicciones",
                labels={"timestamp": "Hora", "probability": "Probabilidad"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📚 Características del Sistema")
    
    features = """
    ✅ **Predicción Individual:** Evaluación de pacientes individuales  
    ✅ **Predicción por Lote:** Procesamiento de múltiples pacientes  
    ✅ **Interfaz Intuitiva:** Diseño profesional y fácil de usar  
    ✅ **Recomendaciones:** Sugerencias basadas en riesgo  
    ✅ **Exportación:** Descarga de resultados en CSV  
    ✅ **Historial:** Registro de predicciones realizadas  
    ✅ **Visualizaciones:** Gráficos interactivos  
    """
    
    st.markdown(features)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
    <p>🧠 Sistema de Predicción de Alzheimer | Desarrollado con Machine Learning</p>
    <p>Versión 1.0 | Noviembre 2025</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# FOOTER
# ==============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; font-size: 12px; padding: 20px;'>
<p>⚠️ Este sistema es una herramienta de apoyo diagnóstico y no reemplaza la evaluación médica profesional</p>
<p>Consulte siempre con un especialista para un diagnóstico definitivo</p>
</div>
""", unsafe_allow_html=True)
