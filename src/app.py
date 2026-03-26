# src/app.py
from flask import Flask, request, jsonify
from src.estadisticas import resumen_estadistico, detectar_outliers_iqr

app = Flask(__name__)


@app.route('/estadisticas', methods=['POST'])
def endpoint_estadisticas():
    """Recibe JSON {"datos": [1,2,3,...]} y devuelve el resumen estadístico.
    400 si datos está vacío o ausente.
    400 si contiene valores no numéricos.
    """
    body = request.get_json(silent=True)
    if not body or "datos" not in body:
        return jsonify({"error": "El campo 'datos' es obligatorio."}), 400

    datos = body["datos"]
    if not isinstance(datos, list) or len(datos) == 0:
        return jsonify({"error": "El campo 'datos' debe ser una lista no vacía."}), 400

    try:
        resultado = resumen_estadistico(datos)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(resultado), 200


@app.route('/outliers', methods=['POST'])
def endpoint_outliers():
    """Recibe JSON {"datos": [...]} y devuelve {"outliers": [...]}."""
    body = request.get_json(silent=True)
    if not body or "datos" not in body:
        return jsonify({"error": "El campo 'datos' es obligatorio."}), 400

    datos = body["datos"]
    if not isinstance(datos, list) or len(datos) == 0:
        return jsonify({"error": "El campo 'datos' debe ser una lista no vacía."}), 400

    try:
        outliers = detectar_outliers_iqr(datos)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"outliers": outliers}), 200


@app.route('/salud', methods=['GET'])
def health_check():
    """Devuelve {"estado": "ok"} con código 200."""
    return jsonify({"estado": "ok"}), 200


if __name__ == '__main__':
    app.run(debug=True)