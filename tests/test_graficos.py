# tests/test_graficos.py
import os
import pytest
import tempfile
from src.graficos import histograma, boxplot_comparativo


@pytest.fixture
def datos_a():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@pytest.fixture
def datos_b():
    return [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]


class TestHistograma:
    def test_genera_archivo(self, datos_a):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            ruta = tmp.name
        try:
            histograma(datos_a, "Test Histograma", ruta)
            assert os.path.exists(ruta)
            assert os.path.getsize(ruta) > 0
        finally:
            os.unlink(ruta)

    def test_titulo_personalizado(self, datos_a):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            ruta = tmp.name
        try:
            histograma(datos_a, "Mi Título Especial", ruta)
            assert os.path.exists(ruta)
        finally:
            os.unlink(ruta)


class TestBoxplotComparativo:
    def test_genera_archivo(self, datos_a, datos_b):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            ruta = tmp.name
        try:
            boxplot_comparativo(datos_a, datos_b, ["Serie A", "Serie B"], ruta)
            assert os.path.exists(ruta)
            assert os.path.getsize(ruta) > 0
        finally:
            os.unlink(ruta)

    def test_etiquetas_personalizadas(self, datos_a, datos_b):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            ruta = tmp.name
        try:
            boxplot_comparativo(datos_a, datos_b, ["Control", "Experimento"], ruta)
            assert os.path.exists(ruta)
        finally:
            os.unlink(ruta)