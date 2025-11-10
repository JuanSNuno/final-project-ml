"""
ft_engineering.py
Paso 2 del Pipeline MLOps: Feature Engineering

Este script carga el dataset limpio, aplica transformaciones usando ColumnTransformer,
y guarda el preprocessor ajustado junto con los datasets transformados.
"""

import pandas as pd
import numpy as np
import json
import joblib
from pathlib import Path
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split


def load_config():
    """Carga la configuración del proyecto"""
    config_path = Path(__file__).parent.parent.parent / "config.json"
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        return {
            "training": {"test_size": 0.2, "random_state": 42}
        }


def load_cleaned_data():
    """Carga el dataset limpio del paso anterior"""
    project_root = Path(__file__).parent.parent.parent
    data_path = project_root / "data" / "processed" / "cleaned_data.csv"
    
    if not data_path.exists():
        raise FileNotFoundError(
            f"No se encontró el dataset limpio: {data_path}\n"
            "Por favor, ejecuta primero data_processing.py"
        )
    
    print(f"✓ Cargando dataset limpio desde: {data_path}")
    df = pd.read_csv(data_path)
    print(f"  Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
    
    return df


def identify_feature_types(df, target_col='Diagnosis'):
    """
    Identifica y clasifica las columnas en:
    - Numéricas
    - Categóricas nominales
    - Categóricas ordinales
    """
    print("\n" + "="*80)
    print("CLASIFICACIÓN DE CARACTERÍSTICAS")
    print("="*80)
    
    # Separar features del target
    feature_cols = [col for col in df.columns if col != target_col]
    df_features = df[feature_cols]
    
    # Detectar tipos automáticamente
    numeric_features = df_features.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = df_features.select_dtypes(include=['object']).columns.tolist()
    
    # Para este dataset, todas las categóricas son nominales
    # Si hubiera ordinales específicas, se definirían aquí
    ordinal_features = []
    nominal_features = categorical_features
    
    print(f"\n📊 Variables Numéricas ({len(numeric_features)}):")
    if numeric_features:
        for col in numeric_features[:10]:  # Mostrar primeras 10
            print(f"   - {col}")
        if len(numeric_features) > 10:
            print(f"   ... y {len(numeric_features) - 10} más")
    
    print(f"\n📝 Variables Categóricas Nominales ({len(nominal_features)}):")
    if nominal_features:
        for col in nominal_features:
            print(f"   - {col}")
    
    print(f"\n📈 Variables Categóricas Ordinales ({len(ordinal_features)}):")
    if ordinal_features:
        for col in ordinal_features:
            print(f"   - {col}")
    else:
        print("   Ninguna")
    
    return numeric_features, nominal_features, ordinal_features


def create_preprocessor(numeric_features, nominal_features, ordinal_features):
    """
    Crea el ColumnTransformer con pipelines específicos para cada tipo de feature.
    
    Según el documento:
    - Numéricas: SimpleImputer (median) + StandardScaler
    - Nominales: SimpleImputer (most_frequent) + OneHotEncoder
    - Ordinales: SimpleImputer (most_frequent) + OrdinalEncoder
    """
    print("\n" + "="*80)
    print("CONSTRUCCIÓN DE PIPELINES DE PREPROCESAMIENTO")
    print("="*80)
    
    transformers_list = []
    
    # Pipeline para variables numéricas
    if numeric_features:
        numeric_pipeline = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        transformers_list.append(('numeric', numeric_pipeline, numeric_features))
        print(f"\n✓ Pipeline Numérico ({len(numeric_features)} features):")
        print(f"    1. SimpleImputer(strategy='median')")
        print(f"    2. StandardScaler()")
    
    # Pipeline para variables categóricas nominales
    if nominal_features:
        nominal_pipeline = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        transformers_list.append(('nominal', nominal_pipeline, nominal_features))
        print(f"\n✓ Pipeline Categórico Nominal ({len(nominal_features)} features):")
        print(f"    1. SimpleImputer(strategy='most_frequent')")
        print(f"    2. OneHotEncoder(handle_unknown='ignore')")
    
    # Pipeline para variables categóricas ordinales
    if ordinal_features:
        ordinal_pipeline = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('ordinal', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
        ])
        transformers_list.append(('ordinal', ordinal_pipeline, ordinal_features))
        print(f"\n✓ Pipeline Categórico Ordinal ({len(ordinal_features)} features):")
        print(f"    1. SimpleImputer(strategy='most_frequent')")
        print(f"    2. OrdinalEncoder(handle_unknown='use_encoded_value')")
    
    # Crear ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=transformers_list,
        remainder='drop'
    )
    
    print(f"\n✅ ColumnTransformer creado con {len(transformers_list)} transformadores")
    
    return preprocessor


def prepare_train_test_split(df, target_col='Diagnosis', test_size=0.2, random_state=42):
    """Separa features y target, y crea train/test split"""
    print("\n" + "="*80)
    print("SEPARACIÓN DE DATOS")
    print("="*80)
    
    # Separar features y target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    print(f"\n✓ Features (X): {X.shape}")
    print(f"✓ Target (y): {y.shape}")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    
    print(f"\n📊 División train-test ({int((1-test_size)*100)}-{int(test_size*100)}):")
    print(f"   Entrenamiento: {X_train.shape[0]} muestras ({(X_train.shape[0]/len(y)*100):.1f}%)")
    print(f"   Evaluación: {X_test.shape[0]} muestras ({(X_test.shape[0]/len(y)*100):.1f}%)")
    
    # Verificar distribución de clases
    print(f"\n📈 Distribución del target en entrenamiento:")
    train_dist = y_train.value_counts()
    for label, count in train_dist.items():
        print(f"   Clase {label}: {count} ({count/len(y_train)*100:.1f}%)")
    
    print(f"\n📈 Distribución del target en evaluación:")
    test_dist = y_test.value_counts()
    for label, count in test_dist.items():
        print(f"   Clase {label}: {count} ({count/len(y_test)*100:.1f}%)")
    
    return X_train, X_test, y_train, y_test


def fit_transform_data(preprocessor, X_train, X_test):
    """
    Ajusta el preprocessor SOLO con datos de entrenamiento
    y transforma ambos conjuntos
    """
    print("\n" + "="*80)
    print("AJUSTE Y TRANSFORMACIÓN")
    print("="*80)
    
    print("\n📊 Ajustando preprocessor con datos de entrenamiento...")
    preprocessor.fit(X_train)
    print("✓ Preprocessor ajustado")
    
    print("\n🔄 Transformando datos de entrenamiento...")
    X_train_transformed = preprocessor.transform(X_train)
    print(f"✓ Datos de entrenamiento transformados: {X_train_transformed.shape}")
    
    print("\n🔄 Transformando datos de evaluación...")
    X_test_transformed = preprocessor.transform(X_test)
    print(f"✓ Datos de evaluación transformados: {X_test_transformed.shape}")
    
    print(f"\n📈 Características:")
    print(f"   Originales: {X_train.shape[1]}")
    print(f"   Después de transformación: {X_train_transformed.shape[1]}")
    
    return X_train_transformed, X_test_transformed


def save_artifacts(preprocessor, X_train, X_test, y_train, y_test):
    """Guarda el preprocessor y los datasets transformados"""
    print("\n" + "="*80)
    print("GUARDANDO ARTEFACTOS")
    print("="*80)
    
    project_root = Path(__file__).parent.parent.parent
    
    # 1. Guardar preprocessor
    artifacts_dir = project_root / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    preprocessor_path = artifacts_dir / "preprocessor.joblib"
    joblib.dump(preprocessor, preprocessor_path)
    print(f"\n💾 Preprocessor guardado en: {preprocessor_path}")
    
    # 2. Guardar datasets transformados
    data_dir = project_root / "data" / "processed"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Convertir arrays a DataFrames para guardar como CSV
    X_train_df = pd.DataFrame(X_train)
    X_test_df = pd.DataFrame(X_test)
    y_train_df = pd.DataFrame(y_train, columns=['Diagnosis'])
    y_test_df = pd.DataFrame(y_test, columns=['Diagnosis'])
    
    X_train_path = data_dir / "X_train.csv"
    X_test_path = data_dir / "X_test.csv"
    y_train_path = data_dir / "y_train.csv"
    y_test_path = data_dir / "y_test.csv"
    
    X_train_df.to_csv(X_train_path, index=False)
    X_test_df.to_csv(X_test_path, index=False)
    y_train_df.to_csv(y_train_path, index=False)
    y_test_df.to_csv(y_test_path, index=False)
    
    print(f"💾 X_train guardado en: {X_train_path}")
    print(f"💾 X_test guardado en: {X_test_path}")
    print(f"💾 y_train guardado en: {y_train_path}")
    print(f"💾 y_test guardado en: {y_test_path}")


def main():
    """Función principal del script de feature engineering"""
    print("="*80)
    print("PASO 2: FEATURE ENGINEERING")
    print("="*80)
    
    # 1. Cargar configuración
    config = load_config()
    training_config = config.get('training', {})
    test_size = training_config.get('test_size', 0.2)
    random_state = training_config.get('random_state', 42)
    
    # 2. Cargar datos limpios
    df = load_cleaned_data()
    
    # 3. Identificar tipos de features
    numeric_features, nominal_features, ordinal_features = identify_feature_types(df)
    
    # 4. Crear preprocessor
    preprocessor = create_preprocessor(numeric_features, nominal_features, ordinal_features)
    
    # 5. Separar train/test
    X_train, X_test, y_train, y_test = prepare_train_test_split(
        df, test_size=test_size, random_state=random_state
    )
    
    # 6. Ajustar y transformar datos
    X_train_transformed, X_test_transformed = fit_transform_data(
        preprocessor, X_train, X_test
    )
    
    # 7. Guardar artefactos
    save_artifacts(preprocessor, X_train_transformed, X_test_transformed, y_train, y_test)
    
    print("\n" + "="*80)
    print("✅ PASO 2 COMPLETADO EXITOSAMENTE")
    print("="*80)
    print(f"\nSiguiente paso: Ejecutar model_training_evaluation.py")


if __name__ == "__main__":
    main()
