# src/app.py
from flask import Flask, request, jsonify
import pandas as pd 
from src.estadisticas import resumen_estadistico, detectar_outliers_iqr,correlacion_columnas 

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


@app.route('/correlacion', methods=['POST'])
def endpoint_correlacion():
    """
    Recibe JSON con 'df' (lista de diccionarios) y los nombres de 'col1' y 'col2'.
    Ejemplo: {"df": [{"a": 1, "b": 2}, {"a": 2, "b": 4}], "col1": "a", "col2": "b"}
    """
    body = request.get_json(silent=True)
    
    # Validaciones de entrada
    if not body or not all(k in body for k in ("df", "col1", "col2")):
        return jsonify({"error": "Faltan parámetros: 'df', 'col1' y 'col2' son obligatorios."}), 400
    
    try:
        df = pd.DataFrame(body["df"])
        col1, col2 = body["col1"], body["col2"]
        
        if col1 not in df.columns or col2 not in df.columns:
            return jsonify({"error": f"Columnas '{col1}' o '{col2}' no encontradas en los datos."}), 400

        # Tu función integrada
        correlacion = float(df[col1].corr(df[col2]))
        
        return jsonify({"correlacion": correlacion}), 200
    except Exception as exc:
        return jsonify({"error": f"Error al calcular la correlación: {str(exc)}"}), 400


@app.route('/salud', methods=['GET'])
def health_check():
    """Devuelve {"estado": "ok"} con código 200."""
    return jsonify({"estado": "ok"}), 200


if __name__ == '__main__':
    app.run(debug=True)