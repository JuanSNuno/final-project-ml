"""
test_api.py
Script para probar la API de predicción

Ejecuta este script después de iniciar la API con model_deploy.py
"""

import requests
import json

# URL de la API
API_URL = "http://localhost:8000"

def test_health():
    """Prueba el endpoint de salud"""
    print("="*80)
    print("🏥 Probando endpoint /health")
    print("="*80)
    
    response = requests.get(f"{API_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_model_info():
    """Prueba el endpoint de información del modelo"""
    print("="*80)
    print("ℹ️  Probando endpoint /model/info")
    print("="*80)
    
    response = requests.get(f"{API_URL}/model/info")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_predict():
    """Prueba el endpoint de predicción"""
    print("="*80)
    print("🎯 Probando endpoint /predict")
    print("="*80)
    
    # Datos de ejemplo para predicción
    sample_data = {
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
    
    print(f"Datos de entrada:")
    print(json.dumps(sample_data, indent=2))
    print()
    
    response = requests.post(
        f"{API_URL}/predict",
        json=sample_data
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_batch_predict():
    """Prueba el endpoint de predicción en lote"""
    print("="*80)
    print("📊 Probando endpoint /predict/batch")
    print("="*80)
    
    # Múltiples instancias para predicción
    batch_data = {
        "instances": [
            {
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
            },
            {
                "Age": 65.0,
                "Gender": 0,
                "Ethnicity": 1,
                "EducationLevel": 3,
                "BMI": 28.0,
                "Smoking": 1,
                "AlcoholConsumption": 3.0,
                "PhysicalActivity": 8.0,
                "DietQuality": 8.0,
                "SleepQuality": 8.0,
                "FamilyHistoryAlzheimers": 0,
                "CardiovascularDisease": 0,
                "Diabetes": 0,
                "Depression": 0,
                "HeadInjury": 0,
                "Hypertension": 0,
                "SystolicBP": 120,
                "DiastolicBP": 80,
                "CholesterolTotal": 190.0,
                "CholesterolLDL": 110.0,
                "CholesterolHDL": 55.0,
                "CholesterolTriglycerides": 150.0,
                "MMSE": 28.0,
                "FunctionalAssessment": 9.0,
                "MemoryComplaints": 0,
                "BehavioralProblems": 0,
                "ADL": 8.0,
                "Confusion": 0,
                "Disorientation": 0,
                "PersonalityChanges": 0,
                "DifficultyCompletingTasks": 0,
                "Forgetfulness": 0
            }
        ]
    }
    
    print(f"Enviando {len(batch_data['instances'])} instancias...")
    print()
    
    response = requests.post(
        f"{API_URL}/predict/batch",
        json=batch_data
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*80)
    print("  🧪 PRUEBAS DE LA API")
    print("="*80 + "\n")
    
    try:
        # Verificar que la API esté corriendo
        response = requests.get(API_URL)
        print(f"✅ API respondiendo en {API_URL}\n")
    except requests.exceptions.ConnectionError:
        print(f"❌ No se pudo conectar a la API en {API_URL}")
        print("   Por favor, inicia la API primero con: python mlops_pipeline/src/model_deploy.py")
        return
    
    # Ejecutar pruebas
    test_health()
    test_model_info()
    test_predict()
    test_batch_predict()
    
    print("="*80)
    print("  ✅ TODAS LAS PRUEBAS COMPLETADAS")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
