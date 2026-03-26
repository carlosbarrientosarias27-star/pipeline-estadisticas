# 📊 Pipeline Estadísticas

Pipeline modular en Python para procesamiento, análisis estadístico y visualización de datos, con API REST integrada y suite de tests automatizados.

---

# 📁 Estructura del Proyecto

```
PIPELINE-ESTADISTICAS/
│
├── data/
│   └── dataset.csv          # Dataset principal de entrada
│
├── src/
│   ├── app.py               # Punto de entrada y API REST
│   ├── estadisticas.py      # Módulo de cálculo estadístico
│   └── graficos.py          # Módulo de generación de gráficos
│
├── tests/
│   ├── test_api.py          # Tests de la API
│   ├── test_estadisticas.py # Tests del módulo estadístico
│   └── test_graficos.py     # Tests del módulo de gráficos
│
├── conftest.py              # Configuración global de pytest
├── pytest.ini               # Configuración de pytest
├── requirements.txt         # Dependencias del proyecto
└── README.md
```

---

# 🚀 Instalación

## Prerrequisitos

- Python 3.8+
- pip

## Pasos

1. **Clona el repositorio:**

```bash
git clone https://github.com/tu-usuario/pipeline-estadisticas.git
cd pipeline-estadisticas
```

2. **Crea y activa un entorno virtual:**

```bash
python -m venv venv

# En Linux/macOS
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

3. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

---

# ▶️ Uso

## Iniciar la API

```bash
python src/app.py
```

La API estará disponible en `http://localhost:5000` (o el puerto configurado).

## Ejecutar el pipeline completo

```bash
python src/app.py --input data/dataset.csv
```

---

# 🔌 Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/estadisticas` | Devuelve estadísticas descriptivas del dataset |
| `GET` | `/api/graficos` | Genera y devuelve los gráficos disponibles |
| `POST` | `/api/upload` | Sube un nuevo dataset para procesar |

---

# 📐 Módulos

## `estadisticas.py`

Contiene las funciones de análisis estadístico:

- Media, mediana y moda
- Desviación estándar y varianza
- Correlaciones entre variables
- Detección de valores atípicos (outliers)

## `graficos.py`

Encargado de la visualización de datos:

- Histogramas de distribución
- Diagramas de dispersión (scatter plots)
- Boxplots por categoría
- Heatmaps de correlación

## `app.py`

Punto de entrada del proyecto. Orquesta el pipeline y expone los resultados a través de la API REST.

---

# 🧪 Tests

Ejecuta todos los tests con:

```bash
pytest
```

Para ver el informe de cobertura:

```bash
pytest --cov=src tests/
```

Para ejecutar solo un módulo de tests:

```bash
pytest tests/test_estadisticas.py -v
```

---

# 📦 Dependencias

Las dependencias principales se encuentran en `requirements.txt`. Entre ellas:

- `pandas` — manipulación y análisis de datos
- `numpy` — operaciones numéricas
- `matplotlib` / `seaborn` — visualización
- `flask` / `fastapi` — API REST
- `pytest` — framework de testing

---

# 🤝 Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Haz commit de tus cambios: `git commit -m 'Add: nueva funcionalidad'`
4. Sube la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

# 📄 Licencia

Este proyecto está licenciado bajo los términos del archivo [LICENSE](LICENSE MIT).
