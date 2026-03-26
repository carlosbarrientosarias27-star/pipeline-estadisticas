# tests/test_estadisticas.py
import pytest
import numpy as np
import pandas as pd
from src.estadisticas import (
    resumen_estadistico,
    detectar_outliers_iqr,
    analizar_dataframe,
    correlacion_columnas,
)

# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def datos_normales():
    return [2, 4, 4, 4, 5, 5, 7, 7]


@pytest.fixture
def datos_con_outlier():
    return [1, 2, 3, 4, 5, 100]


@pytest.fixture
def df_numerico():
    return pd.DataFrame({"edad": [20, 25, 30, 35, 40], "salario": [1000, 2000, 3000, 4000, 5000]})


@pytest.fixture
def df_mixto():
    return pd.DataFrame({"nombre": ["Ana", "Luis", "Marta"], "edad": [30, 25, 28]})


# ──────────────────────────────────────────────
# resumen_estadistico
# ──────────────────────────────────────────────

class TestResumenEstadistico:
    def test_valores_correctos(self, datos_normales):
        res = resumen_estadistico(datos_normales)
        np.testing.assert_almost_equal(res["media"], 4.75, decimal=5)
        np.testing.assert_almost_equal(res["mediana"], 4.5, decimal=5)
        assert res["minimo"] == 2.0
        assert res["maximo"] == 7.0
        assert "percentil_25" in res
        assert "percentil_75" in res

    def test_devuelve_todas_las_claves(self, datos_normales):
        res = resumen_estadistico(datos_normales)
        claves_esperadas = {"media", "mediana", "desv_tipica", "minimo", "maximo",
                            "percentil_25", "percentil_75"}
        assert claves_esperadas == set(res.keys())

    def test_lista_vacia_lanza_valueerror(self):
        with pytest.raises(ValueError, match="vacía"):
            resumen_estadistico([])

    def test_string_en_lista_lanza_valueerror(self):
        with pytest.raises(ValueError):
            resumen_estadistico([1, 2, "tres"])

    def test_un_elemento(self):
        res = resumen_estadistico([42])
        assert res["media"] == 42.0
        assert res["minimo"] == 42.0
        assert res["maximo"] == 42.0

    def test_enteros_y_floats(self):
        res = resumen_estadistico([1, 2.5, 3])
        np.testing.assert_almost_equal(res["media"], 2.1666, decimal=3)


# ──────────────────────────────────────────────
# detectar_outliers_iqr
# ──────────────────────────────────────────────

class TestDetectarOutliersIQR:
    def test_detecta_outlier_alto(self, datos_con_outlier):
        outliers = detectar_outliers_iqr(datos_con_outlier)
        assert 100 in outliers

    def test_sin_outliers_devuelve_lista_vacia(self, datos_normales):
        outliers = detectar_outliers_iqr(datos_normales)
        assert outliers == []

    def test_outlier_negativo(self):
        datos = [-100, 1, 2, 3, 4, 5]
        outliers = detectar_outliers_iqr(datos)
        assert -100 in outliers

    def test_devuelve_lista(self, datos_con_outlier):
        resultado = detectar_outliers_iqr(datos_con_outlier)
        assert isinstance(resultado, list)


# ──────────────────────────────────────────────
# analizar_dataframe
# ──────────────────────────────────────────────

class TestAnalizarDataframe:
    def test_columna_correcta(self, df_numerico):
        res = analizar_dataframe(df_numerico, "edad")
        np.testing.assert_almost_equal(res["media"], 30.0, decimal=5)

    def test_columna_inexistente_lanza_keyerror(self, df_numerico):
        with pytest.raises(KeyError):
            analizar_dataframe(df_numerico, "altura")

    def test_columna_no_numerica_lanza_typeerror(self, df_mixto):
        with pytest.raises(TypeError):
            analizar_dataframe(df_mixto, "nombre")


# ──────────────────────────────────────────────
# correlacion_columnas
# ──────────────────────────────────────────────

class TestCorrelacionColumnas:
    def test_correlacion_perfecta_positiva(self):
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 10]})
        corr = correlacion_columnas(df, "x", "y")
        np.testing.assert_almost_equal(corr, 1.0, decimal=5)

    def test_correlacion_perfecta_negativa(self):
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [10, 8, 6, 4, 2]})
        corr = correlacion_columnas(df, "x", "y")
        np.testing.assert_almost_equal(corr, -1.0, decimal=5)

    def test_correlacion_baja(self):
        # datos con baja correlación lineal
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 1, 4, 3, 3]})
        corr = correlacion_columnas(df, "x", "y")
        assert abs(corr) < 0.9   # no correlación perfecta

    def test_devuelve_float(self, df_numerico):
        corr = correlacion_columnas(df_numerico, "edad", "salario")
        assert isinstance(corr, float)