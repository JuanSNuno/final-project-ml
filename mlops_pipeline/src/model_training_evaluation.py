"""
model_training_evaluation.py
Paso 3 del Pipeline MLOps: Entrenamiento y Evaluación de Modelos

Este script carga los datos transformados, entrena múltiples modelos,
los evalua y guarda el mejor modelo basado en métricas de performance.
"""

import pandas as pd
import numpy as np
import json
import joblib
import time
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)


def load_processed_data():
    """Carga los datasets procesados del paso anterior"""
    print("="*80)
    print("CARGANDO DATOS PROCESADOS")
    print("="*80)
    
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data" / "processed"
    
    required_files = {
        'X_train': data_dir / "X_train.csv",
        'X_test': data_dir / "X_test.csv",
        'y_train': data_dir / "y_train.csv",
        'y_test': data_dir / "y_test.csv"
    }
    
    # Verificar que existan todos los archivos
    missing_files = [name for name, path in required_files.items() if not path.exists()]
    if missing_files:
        raise FileNotFoundError(
            f"Faltan archivos de datos procesados: {missing_files}\n"
            "Por favor, ejecuta primero ft_engineering.py"
        )
    
    # Cargar datos
    X_train = pd.read_csv(required_files['X_train'])
    X_test = pd.read_csv(required_files['X_test'])
    y_train = pd.read_csv(required_files['y_train'])['Diagnosis']
    y_test = pd.read_csv(required_files['y_test'])['Diagnosis']
    
    print(f"\n✓ Datos cargados exitosamente:")
    print(f"   X_train: {X_train.shape}")
    print(f"   X_test: {X_test.shape}")
    print(f"   y_train: {y_train.shape}")
    print(f"   y_test: {y_test.shape}")
    
    return X_train, X_test, y_train, y_test


def get_models_to_train():
    """
    Define los modelos a entrenar y evaluar.
    Incluye varios algoritmos supervisados para comparación.
    """
    models = {
        'Logistic Regression': LogisticRegression(
            max_iter=1000,
            random_state=42,
            n_jobs=-1
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        ),
        'Decision Tree': DecisionTreeClassifier(
            max_depth=10,
            random_state=42
        ),
        'KNN': KNeighborsClassifier(
            n_neighbors=5,
            n_jobs=-1
        ),
        'SVM': SVC(
            kernel='rbf',
            probability=True,
            random_state=42
        )
    }
    
    return models


def evaluate_model(model, X_train, X_test, y_train, y_test):
    """
    Evalúa un modelo en los conjuntos de entrenamiento y evaluación.
    Retorna métricas completas de performance.
    """
    # Predicciones
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Probabilidades (si el modelo las soporta)
    try:
        y_test_proba = model.predict_proba(X_test)
        if y_test_proba.shape[1] == 2:  # Clasificación binaria
            y_test_proba = y_test_proba[:, 1]
        else:
            y_test_proba = None
    except AttributeError:
        y_test_proba = None
    
    # Métricas de entrenamiento
    train_accuracy = accuracy_score(y_train, y_train_pred)
    
    # Métricas de evaluación
    test_accuracy = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_test_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_test_pred, average='weighted', zero_division=0)
    
    # ROC-AUC (si hay probabilidades y es clasificación binaria)
    try:
        if y_test_proba is not None and len(np.unique(y_test)) == 2:
            roc_auc = roc_auc_score(y_test, y_test_proba)
        else:
            roc_auc = None
    except:
        roc_auc = None
    
    # Overfitting score (diferencia train-test)
    overfitting = train_accuracy - test_accuracy
    
    metrics = {
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'overfitting': overfitting
    }
    
    return metrics, y_test_pred


def train_and_evaluate_models(models, X_train, X_test, y_train, y_test):
    """
    Entrena y evalúa todos los modelos.
    Retorna un DataFrame con resultados y los modelos entrenados.
    """
    print("\n" + "="*80)
    print("ENTRENAMIENTO Y EVALUACIÓN DE MODELOS")
    print("="*80)
    
    results = []
    trained_models = {}
    predictions = {}
    
    for model_name, model in models.items():
        print(f"\n📚 Entrenando {model_name}...")
        
        # Medir tiempo de entrenamiento
        start_time = time.time()
        model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        print(f"   ✓ Entrenamiento completado en {training_time:.2f} segundos")
        
        # Evaluar modelo
        print(f"   📊 Evaluando modelo...")
        metrics, y_pred = evaluate_model(model, X_train, X_test, y_train, y_test)
        
        # Guardar resultados
        result = {
            'Modelo': model_name,
            'Train Accuracy': round(metrics['train_accuracy'], 4),
            'Test Accuracy': round(metrics['test_accuracy'], 4),
            'Precision': round(metrics['precision'], 4),
            'Recall': round(metrics['recall'], 4),
            'F1-Score': round(metrics['f1_score'], 4),
            'ROC-AUC': round(metrics['roc_auc'], 4) if metrics['roc_auc'] else None,
            'Overfitting': round(metrics['overfitting'], 4),
            'Training Time (s)': round(training_time, 2)
        }
        
        results.append(result)
        trained_models[model_name] = model
        predictions[model_name] = y_pred
        
        print(f"   ✓ Test Accuracy: {result['Test Accuracy']:.4f}")
        print(f"   ✓ F1-Score: {result['F1-Score']:.4f}")
    
    # Crear DataFrame con resultados
    results_df = pd.DataFrame(results)
    
    return results_df, trained_models, predictions


def select_best_model(results_df, trained_models):
    """
    Selecciona el mejor modelo basado en:
    1. Performance (F1-Score primario, Accuracy secundario)
    2. Bajo overfitting
    3. Balance entre métricas
    """
    print("\n" + "="*80)
    print("SELECCIÓN DEL MEJOR MODELO")
    print("="*80)
    
    print("\n📊 Resultados de todos los modelos:")
    print(results_df.to_string(index=False))
    
    # Criterios de selección
    # 1. F1-Score como métrica principal
    # 2. Si hay empate, usar accuracy
    # 3. Preferir modelos con menor overfitting
    
    # Ordenar por F1-Score (descendente) y Overfitting (ascendente)
    results_sorted = results_df.sort_values(
        by=['F1-Score', 'Test Accuracy', 'Overfitting'],
        ascending=[False, False, True]
    )
    
    best_row = results_sorted.iloc[0]
    best_model_name = best_row['Modelo']
    best_model = trained_models[best_model_name]
    
    print(f"\n🏆 MEJOR MODELO: {best_model_name}")
    print(f"   Test Accuracy: {best_row['Test Accuracy']:.4f}")
    print(f"   F1-Score: {best_row['F1-Score']:.4f}")
    print(f"   Precision: {best_row['Precision']:.4f}")
    print(f"   Recall: {best_row['Recall']:.4f}")
    if best_row['ROC-AUC'] is not None:
        print(f"   ROC-AUC: {best_row['ROC-AUC']:.4f}")
    print(f"   Overfitting: {best_row['Overfitting']:.4f}")
    print(f"   Tiempo de entrenamiento: {best_row['Training Time (s)']:.2f}s")
    
    return best_model_name, best_model, results_sorted


def save_results_and_model(best_model_name, best_model, results_df):
    """Guarda el mejor modelo y los resultados de evaluación"""
    print("\n" + "="*80)
    print("GUARDANDO ARTEFACTOS")
    print("="*80)
    
    project_root = Path(__file__).parent.parent.parent
    artifacts_dir = project_root / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Guardar el mejor modelo
    model_path = artifacts_dir / "best_model.joblib"
    joblib.dump(best_model, model_path)
    print(f"\n💾 Mejor modelo guardado en: {model_path}")
    print(f"   Modelo: {best_model_name}")
    
    # 2. Guardar metadata del modelo
    metadata = {
        'model_name': best_model_name,
        'model_type': type(best_model).__name__,
        'training_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    metadata_path = artifacts_dir / "model_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"💾 Metadata guardada en: {metadata_path}")
    
    # 3. Guardar resultados de todos los modelos
    results_path = artifacts_dir / "model_evaluation_results.csv"
    results_df.to_csv(results_path, index=False)
    print(f"💾 Resultados de evaluación guardados en: {results_path}")


def generate_comparison_plot(results_df):
    """Genera un gráfico comparativo de los modelos"""
    project_root = Path(__file__).parent.parent.parent
    artifacts_dir = project_root / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    # Preparar datos para el gráfico
    metrics_to_plot = ['Test Accuracy', 'Precision', 'Recall', 'F1-Score']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(results_df))
    width = 0.2
    
    for i, metric in enumerate(metrics_to_plot):
        offset = width * (i - len(metrics_to_plot)/2 + 0.5)
        ax.bar(x + offset, results_df[metric], width, label=metric)
    
    ax.set_xlabel('Modelos')
    ax.set_ylabel('Score')
    ax.set_title('Comparación de Modelos - Métricas de Evaluación')
    ax.set_xticks(x)
    ax.set_xticklabels(results_df['Modelo'], rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plot_path = artifacts_dir / "model_comparison.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"📊 Gráfico comparativo guardado en: {plot_path}")
    plt.close()


def main():
    """Función principal del script de entrenamiento y evaluación"""
    print("="*80)
    print("PASO 3: ENTRENAMIENTO Y EVALUACIÓN DE MODELOS")
    print("="*80)
    
    # 1. Cargar datos procesados
    X_train, X_test, y_train, y_test = load_processed_data()
    
    # 2. Obtener modelos a entrenar
    models = get_models_to_train()
    print(f"\n📚 Modelos a entrenar: {len(models)}")
    for model_name in models.keys():
        print(f"   - {model_name}")
    
    # 3. Entrenar y evaluar modelos
    results_df, trained_models, predictions = train_and_evaluate_models(
        models, X_train, X_test, y_train, y_test
    )
    
    # 4. Seleccionar el mejor modelo
    best_model_name, best_model, results_sorted = select_best_model(
        results_df, trained_models
    )
    
    # 5. Guardar resultados y modelo
    save_results_and_model(best_model_name, best_model, results_sorted)
    
    # 6. Generar gráfico comparativo
    generate_comparison_plot(results_sorted)
    
    print("\n" + "="*80)
    print("✅ PASO 3 COMPLETADO EXITOSAMENTE")
    print("="*80)
    print(f"\nSiguiente paso: Ejecutar model_deploy.py para desplegar el modelo")


if __name__ == "__main__":
    main()
