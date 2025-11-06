"""
data_processing.py
Paso 1 del Pipeline MLOps: Carga y limpieza de datos

Este script carga los datos crudos desde el CSV, realiza limpieza básica
y guarda el dataset limpio para el siguiente paso del pipeline.
"""

import pandas as pd
import numpy as np
import json
import os
from pathlib import Path


def load_config():
    """Carga la configuración del proyecto desde config.json"""
    config_path = Path(__file__).parent.parent.parent / "config.json"
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        return {
            "data_path": "alzheimers_disease_data.csv",
            "training": {"test_size": 0.2, "random_state": 42}
        }


def load_raw_data(config):
    """Carga el dataset crudo desde CSV"""
    project_root = Path(__file__).parent.parent.parent
    data_path = project_root / config.get('data_path', 'alzheimers_disease_data.csv')
    
    if not data_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {data_path}")
    
    print(f"✓ Cargando datos desde: {data_path}")
    df = pd.read_csv(data_path)
    print(f"  Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
    
    return df


def clean_data(df):
    """
    Realiza limpieza básica del dataset:
    - Elimina duplicados
    - Maneja valores faltantes
    - Corrige tipos de datos
    - Elimina columnas innecesarias para el modelo
    """
    print("\n" + "="*80)
    print("LIMPIEZA DE DATOS")
    print("="*80)
    
    # Crear copia para no modificar el original
    df_clean = df.copy()
    
    # 1. Eliminar duplicados
    n_duplicates = df_clean.duplicated().sum()
    if n_duplicates > 0:
        df_clean = df_clean.drop_duplicates()
        print(f"✓ Eliminados {n_duplicates} registros duplicados")
    else:
        print("✓ No se encontraron duplicados")
    
    # 2. Información sobre valores faltantes
    missing_info = df_clean.isnull().sum()
    if missing_info.sum() > 0:
        print(f"\n📊 Valores faltantes detectados:")
        for col, count in missing_info[missing_info > 0].items():
            pct = (count / len(df_clean)) * 100
            print(f"   {col}: {count} ({pct:.2f}%)")
        print(f"   (Se manejarán en la etapa de feature engineering)")
    else:
        print("\n✓ No hay valores faltantes")
    
    # 3. Verificar y corregir tipos de datos
    print(f"\n📋 Tipos de datos:")
    numeric_cols = df_clean.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df_clean.select_dtypes(include=['object']).columns.tolist()
    print(f"   Numéricas: {len(numeric_cols)} columnas")
    print(f"   Categóricas: {len(categorical_cols)} columnas")
    
    # 4. Eliminar columnas de identificación que no son features
    # (PatientID y DoctorInCharge son identificadores, no features)
    # Nota: Diagnosis es el target y se mantiene
    id_columns = ['PatientID', 'DoctorInCharge']
    existing_id_cols = [col for col in id_columns if col in df_clean.columns]
    
    if existing_id_cols:
        df_clean = df_clean.drop(columns=existing_id_cols)
        print(f"\n✓ Eliminadas columnas de identificación: {existing_id_cols}")
    
    print(f"\n✅ Limpieza completada")
    print(f"   Dimensiones finales: {df_clean.shape[0]} filas × {df_clean.shape[1]} columnas")
    
    return df_clean


def save_cleaned_data(df, output_path):
    """Guarda el dataset limpio en el directorio de datos procesados"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"\n💾 Dataset limpio guardado en: {output_path}")


def main():
    """Función principal del script de procesamiento de datos"""
    print("="*80)
    print("PASO 1: PROCESAMIENTO DE DATOS")
    print("="*80)
    
    # 1. Cargar configuración
    config = load_config()
    
    # 2. Cargar datos crudos
    df_raw = load_raw_data(config)
    
    # 3. Limpiar datos
    df_clean = clean_data(df_raw)
    
    # 4. Guardar datos limpios
    project_root = Path(__file__).parent.parent.parent
    output_path = project_root / "data" / "processed" / "cleaned_data.csv"
    save_cleaned_data(df_clean, output_path)
    
    print("\n" + "="*80)
    print("✅ PASO 1 COMPLETADO EXITOSAMENTE")
    print("="*80)
    print(f"\nSiguiente paso: Ejecutar ft_engineering.py")


if __name__ == "__main__":
    main()
