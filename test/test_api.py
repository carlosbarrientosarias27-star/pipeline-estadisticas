# tests/test_api.py
import json
import pytest
from src.app import app


@pytest.fixture
def cliente():
    """Crea cliente de test de Flask."""
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


# ──────────────────────────────────────────────
# /salud
# ──────────────────────────────────────────────

def test_health_ok(cliente):
    resp = cliente.get('/salud')
    assert resp.status_code == 200
    assert resp.get_json()['estado'] == 'ok'


# ──────────────────────────────────────────────
# /estadisticas
# ──────────────────────────────────────────────

class TestEndpointEstadisticas:
    def test_datos_validos_devuelve_200(self, cliente):
        payload = {"datos": [4, 7, 13, 2, 1, 9, 15, 3, 8, 6]}
        resp = cliente.post(
            '/estadisticas',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert "media" in data
        assert "mediana" in data
        assert "desv_tipica" in data
        assert "minimo" in data
        assert "maximo" in data

    def test_media_correcta(self, cliente):
        payload = {"datos": [2, 4, 6, 8, 10]}
        resp = cliente.post(
            '/estadisticas',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = resp.get_json()
        assert data['media'] == pytest.approx(6.0, rel=1e-5)

    def test_sin_campo_datos_devuelve_400(self, cliente):
        resp = cliente.post(
            '/estadisticas',
            data=json.dumps({"otro": 123}),
            content_type='application/json'
        )
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_lista_vacia_devuelve_400(self, cliente):
        payload = {"datos": []}
        resp = cliente.post(
            '/estadisticas',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert resp.status_code == 400

    def test_no_numericos_devuelve_400(self, cliente):
        payload = {"datos": [1, 2, "tres"]}
        resp = cliente.post(
            '/estadisticas',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert resp.status_code == 400

    def test_body_vacio_devuelve_400(self, cliente):
        resp = cliente.post(
            '/estadisticas',
            data="",
            content_type='application/json'
        )
        assert resp.status_code == 400


# ──────────────────────────────────────────────
# /outliers
# ──────────────────────────────────────────────

class TestEndpointOutliers:
    def test_detecta_outlier_alto(self, cliente):
        payload = {"datos": [1, 2, 3, 4, 5, 100]}
        resp = cliente.post(
            '/outliers',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert "outliers" in data
        assert 100 in data["outliers"]

    def test_sin_outliers_lista_vacia(self, cliente):
        payload = {"datos": [2, 4, 4, 4, 5, 5, 7, 7]}
        resp = cliente.post(
            '/outliers',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert resp.status_code == 200
        assert resp.get_json()["outliers"] == []

    def test_sin_campo_datos_devuelve_400(self, cliente):
        resp = cliente.post(
            '/outliers',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert resp.status_code == 400

    def test_lista_vacia_devuelve_400(self, cliente):
        payload = {"datos": []}
        resp = cliente.post(
            '/outliers',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert resp.status_code == 400