"""
model_deploy.py
Paso 4 del Pipeline MLOps: Despliegue del Modelo como API

Este script crea una API REST usando FastAPI que:
1. Carga el preprocessor y el modelo entrenado
2. Expone un endpoint /predict para hacer predicciones
3. Recibe datos crudos en JSON y retorna predicciones
"""

import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn


# ==============================================================================
# CONFIGURACIÓN Y CARGA DE ARTEFACTOS
# ==============================================================================

# Definir rutas de artefactos
PROJECT_ROOT = Path(__file__).parent.parent.parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
PREPROCESSOR_PATH = ARTIFACTS_DIR / "preprocessor.joblib"
MODEL_PATH = ARTIFACTS_DIR / "best_model.joblib"
METADATA_PATH = ARTIFACTS_DIR / "model_metadata.json"

# Cargar artefactos al inicio
try:
    print("🔄 Cargando artefactos del modelo...")
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)
    
    if METADATA_PATH.exists():
        with open(METADATA_PATH, 'r') as f:
            model_metadata = json.load(f)
    else:
        model_metadata = {"model_name": "Unknown"}
    
    print(f"✅ Preprocessor cargado desde: {PREPROCESSOR_PATH}")
    print(f"✅ Modelo cargado desde: {MODEL_PATH}")
    print(f"✅ Modelo: {model_metadata.get('model_name', 'Unknown')}")
except FileNotFoundError as e:
    print(f"❌ Error: No se encontraron los artefactos necesarios.")
    print(f"   Por favor, ejecuta primero todo el pipeline (data_processing.py, ft_engineering.py, model_training_evaluation.py)")
    raise


# ==============================================================================
# DEFINICIÓN DE LA API
# ==============================================================================

app = FastAPI(
    title="Alzheimer's Disease Prediction API",
    description="API para predicción de Alzheimer usando modelos de ML",
    version="1.0.0"
)


# ==============================================================================
# MODELOS DE DATOS (PYDANTIC)
# ==============================================================================

class PredictionInput(BaseModel):
    """
    Modelo de entrada para predicciones.
    Define los campos esperados en la solicitud JSON.
    """
    Age: float = Field(..., description="Edad del paciente")
    Gender: int = Field(..., description="Género (0=Femenino, 1=Masculino)")
    Ethnicity: int = Field(..., description="Etnicidad")
    EducationLevel: int = Field(..., description="Nivel educativo")
    BMI: float = Field(..., description="Índice de masa corporal")
    Smoking: int = Field(..., description="Fumador (0=No, 1=Sí)")
    AlcoholConsumption: float = Field(..., description="Consumo de alcohol")
    PhysicalActivity: float = Field(..., description="Actividad física")
    DietQuality: float = Field(..., description="Calidad de la dieta")
    SleepQuality: float = Field(..., description="Calidad del sueño")
    FamilyHistoryAlzheimers: int = Field(..., description="Historia familiar (0=No, 1=Sí)")
    CardiovascularDisease: int = Field(..., description="Enfermedad cardiovascular (0=No, 1=Sí)")
    Diabetes: int = Field(..., description="Diabetes (0=No, 1=Sí)")
    Depression: int = Field(..., description="Depresión (0=No, 1=Sí)")
    HeadInjury: int = Field(..., description="Lesión en la cabeza (0=No, 1=Sí)")
    Hypertension: int = Field(..., description="Hipertensión (0=No, 1=Sí)")
    SystolicBP: int = Field(..., description="Presión arterial sistólica")
    DiastolicBP: int = Field(..., description="Presión arterial diastólica")
    CholesterolTotal: float = Field(..., description="Colesterol total")
    CholesterolLDL: float = Field(..., description="Colesterol LDL")
    CholesterolHDL: float = Field(..., description="Colesterol HDL")
    CholesterolTriglycerides: float = Field(..., description="Triglicéridos")
    MMSE: float = Field(..., description="Mini-Mental State Examination")
    FunctionalAssessment: float = Field(..., description="Evaluación funcional")
    MemoryComplaints: int = Field(..., description="Quejas de memoria (0=No, 1=Sí)")
    BehavioralProblems: int = Field(..., description="Problemas de comportamiento (0=No, 1=Sí)")
    ADL: float = Field(..., description="Activities of Daily Living")
    Confusion: int = Field(..., description="Confusión (0=No, 1=Sí)")
    Disorientation: int = Field(..., description="Desorientación (0=No, 1=Sí)")
    PersonalityChanges: int = Field(..., description="Cambios de personalidad (0=No, 1=Sí)")
    DifficultyCompletingTasks: int = Field(..., description="Dificultad completando tareas (0=No, 1=Sí)")
    Forgetfulness: int = Field(..., description="Olvido (0=No, 1=Sí)")
    
    class Config:
        schema_extra = {
            "example": {
                "Age": 75.0,
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
        }


class PredictionOutput(BaseModel):
    """Modelo de salida para predicciones"""
    prediction: int = Field(..., description="Clase predicha (0 o 1)")
    probability: float = Field(..., description="Probabilidad de la predicción")
    model_name: str = Field(..., description="Nombre del modelo utilizado")


class BatchPredictionInput(BaseModel):
    """Modelo para predicciones en lote"""
    instances: List[PredictionInput] = Field(..., description="Lista de instancias a predecir")


# ==============================================================================
# FUNCIONES AUXILIARES
# ==============================================================================

def preprocess_input(input_data: PredictionInput) -> np.ndarray:
    """
    Convierte los datos de entrada JSON a un DataFrame
    y aplica las transformaciones del preprocessor
    """
    # Convertir a diccionario y luego a DataFrame
    data_dict = input_data.dict()
    df = pd.DataFrame([data_dict])
    
    # Aplicar transformaciones
    X_transformed = preprocessor.transform(df)
    
    return X_transformed


def make_prediction(X_transformed: np.ndarray) -> tuple:
    """
    Realiza la predicción usando el modelo cargado
    Retorna: (predicción, probabilidad)
    """
    # Predicción
    prediction = model.predict(X_transformed)[0]
    
    # Probabilidad (si el modelo la soporta)
    try:
        probabilities = model.predict_proba(X_transformed)[0]
        # Tomar la probabilidad de la clase predicha
        probability = float(probabilities[prediction])
    except AttributeError:
        # Si el modelo no soporta probabilidades, usar un placeholder
        probability = 1.0
    
    return int(prediction), probability


# ==============================================================================
# ENDPOINTS DE LA API
# ==============================================================================

@app.get("/")
def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Alzheimer's Disease Prediction API",
        "version": "1.0.0",
        "model": model_metadata.get('model_name', 'Unknown'),
        "endpoints": {
            "/": "Información de la API",
            "/health": "Estado de salud de la API",
            "/predict": "Realizar una predicción (POST)",
            "/predict/batch": "Realizar predicciones en lote (POST)",
            "/model/info": "Información del modelo"
        }
    }


@app.get("/health")
def health_check():
    """Endpoint para verificar el estado de salud de la API"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "preprocessor_loaded": preprocessor is not None
    }


@app.get("/model/info")
def model_info():
    """Endpoint para obtener información del modelo"""
    return {
        "model_metadata": model_metadata,
        "model_type": type(model).__name__,
        "preprocessor_type": type(preprocessor).__name__
    }


@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    """
    Endpoint principal para realizar predicciones.
    
    Recibe datos crudos en JSON, aplica transformaciones
    y retorna la predicción del modelo.
    """
    try:
        # 1. Preprocesar entrada
        X_transformed = preprocess_input(input_data)
        
        # 2. Realizar predicción
        prediction, probability = make_prediction(X_transformed)
        
        # 3. Preparar respuesta
        response = PredictionOutput(
            prediction=prediction,
            probability=probability,
            model_name=model_metadata.get('model_name', 'Unknown')
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al realizar la predicción: {str(e)}"
        )


@app.post("/predict/batch")
def predict_batch(input_data: BatchPredictionInput):
    """
    Endpoint para realizar predicciones en lote.
    Recibe múltiples instancias y retorna predicciones para todas.
    """
    try:
        predictions = []
        
        for instance in input_data.instances:
            # Preprocesar y predecir
            X_transformed = preprocess_input(instance)
            prediction, probability = make_prediction(X_transformed)
            
            predictions.append({
                "prediction": int(prediction),
                "probability": float(probability)
            })
        
        return {
            "predictions": predictions,
            "count": len(predictions),
            "model_name": model_metadata.get('model_name', 'Unknown')
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al realizar las predicciones: {str(e)}"
        )


# ==============================================================================
# FUNCIÓN PRINCIPAL
# ==============================================================================

def main():
    """Inicia el servidor de la API"""
    print("="*80)
    print("INICIANDO API DE PREDICCIÓN")
    print("="*80)
    print(f"\n📡 Modelo: {model_metadata.get('model_name', 'Unknown')}")
    print(f"📡 Servidor: http://localhost:8000")
    print(f"📄 Documentación: http://localhost:8000/docs")
    print(f"📄 Redoc: http://localhost:8000/redoc")
    print("\nPresiona CTRL+C para detener el servidor\n")
    
    # Iniciar servidor
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
