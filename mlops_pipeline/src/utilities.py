"""
utilities.py
Módulo de utilidades compartidas para reducir código duplicado
"""

from pathlib import Path
import json
from typing import Dict, Any


def load_config(config_name: str = "config.json") -> Dict[str, Any]:
    """Carga archivo de configuración JSON"""
    config_path = Path(__file__).parent.parent / config_name
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    
    return {}


def get_project_root() -> Path:
    """Obtiene la raíz del proyecto"""
    return Path(__file__).parent.parent.parent


def get_data_dir(subdir: str = "") -> Path:
    """Obtiene directorio de datos"""
    root = get_project_root()
    data_dir = root / "mlops_pipeline" / "data" / subdir
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_artifacts_dir() -> Path:
    """Obtiene directorio de artefactos"""
    root = get_project_root()
    artifacts = root / "mlops_pipeline" / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    return artifacts


def validate_dataframe(df, required_columns: list) -> bool:
    """Valida que un dataframe tenga las columnas requeridas"""
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {missing}")
    return True


def save_results(data: Dict[str, Any], filename: str, directory: str = "artifacts") -> Path:
    """Guarda resultados en JSON"""
    output_dir = get_project_root() / "mlops_pipeline" / directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / filename
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return output_file
