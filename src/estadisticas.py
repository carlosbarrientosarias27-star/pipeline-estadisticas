# src/estadisticas.py
import numpy as np
import pandas as pd
from typing import Union


def resumen_estadistico(datos: list) -> dict:
    """Recibe lista de números y devuelve dict con estadísticas.
    Maneja n=1 devolviendo desv_tipica=0.0 sin warnings.
    """
    if not datos:
        raise ValueError("La lista no puede estar vacía.")

    # Validación de tipos
    for i, v in enumerate(datos):
        if not isinstance(v, (int, float)):
            raise ValueError(f"El elemento en posición {i} ('{v}') no es numérico.")

    arr = np.array(datos, dtype=float)
    n = len(arr)

    # Evitamos RuntimeWarning: Degrees of freedom <= 0
    desv = float(np.std(arr, ddof=1)) if n > 1 else 0.0

    return {
        "media": float(np.mean(arr)),
        "mediana": float(np.median(arr)),
        "desv_tipica": desv,
        "minimo": float(np.min(arr)),
        "maximo": float(np.max(arr)),
        "percentil_25": float(np.percentile(arr, 25)),
        "percentil_75": float(np.percentile(arr, 75)),
    }

def detectar_outliers_iqr(datos: list) -> list:
    """Devuelve lista con los valores outliers usando el método IQR.
    Un valor es outlier si está fuera de [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
    Usa numpy. Devuelve lista vacía si no hay outliers.
    """
    arr = np.array(datos, dtype=float)
    q1 = np.percentile(arr, 25)
    q3 = np.percentile(arr, 75)
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    outliers = arr[(arr < limite_inferior) | (arr > limite_superior)]
    return outliers.tolist()


def analizar_dataframe(df: pd.DataFrame, columna: str) -> dict:
    """Aplica resumen_estadistico a una columna de un DataFrame.
    Lanza KeyError si la columna no existe.
    Lanza TypeError si la columna no es numérica.
    """
    if columna not in df.columns:
        raise KeyError(f"La columna '{columna}' no existe en el DataFrame.")

    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise TypeError(f"La columna '{columna}' no es numérica.")

    return resumen_estadistico(df[columna].dropna().tolist())


def correlacion_columnas(df: pd.DataFrame, col1: str, col2: str) -> float:
    """Calcula el coeficiente de correlación de Pearson entre dos columnas."""
    return float(df[col1].corr(df[col2]))