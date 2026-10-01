# Regresión lineal múltiple – CRISP-DM (Dólar, Glucosa, Energía)

## Estructura
```
proyecto_regresion/
├── data/                    # dolar_data.csv, glucosa_data.csv, energia_data.csv
├── entrenar_modelos.py      # Fases CRISP-DM: comprensión, preparación, modelado, evaluación, exportación
├── app.py                   # Interfaz web Flask (selección de ejercicio + predicción)
├── templates/index.html     # Página de la interfaz
├── modelos/                 # modelo_dolar.joblib, modelo_glucosa.joblib, modelo_energia.joblib
├── graficas/                # dispersión, correlación, real vs. predicho, importancia
├── resultados/              # resultados.json y resumen.md (métricas e interpretación)
├── resultados_consola.txt   # salida completa del entrenamiento
└── requirements.txt
```

## Cómo ejecutar
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python entrenar_modelos.py   # entrena, evalúa, grafica y exporta los 3 modelos
python generar_dashboard.py  # genera dashboard.html con los datos y resultados
python app.py                # abre http://127.0.0.1:5000 (dashboard en /dashboard)
```

## Despliegue en Render
El archivo `render.yaml` define el servicio web (gunicorn `app:app`, Python 3.13).
En Render: **New → Blueprint**, conectar este repositorio de GitHub y confirmar.
Las versiones de `requirements.txt` están fijadas porque los modelos `.joblib`
se guardaron con scikit-learn 1.9.1 y deben cargarse con la misma versión.

## Guardar y cargar un modelo (joblib)
```python
import joblib, pandas as pd
paquete = joblib.load("modelos/modelo_glucosa.joblib")
X = pd.DataFrame([{"Edad": 45, "IMC": 27, "Actividad_Fisica": 3}])
print(paquete["modelo"].predict(X))      # -> nivel de glucosa estimado
```
Cada `.joblib` guarda un diccionario con el modelo entrenado, el orden de las
variables, la unidad, las métricas, los coeficientes y los rangos de los datos.
Con `pickle` sería equivalente: `pickle.dump(obj, open("m.pkl","wb"))` y
`pickle.load(open("m.pkl","rb"))`; joblib es más eficiente con arreglos de NumPy.

## API (opcional)
`POST /api/predecir/<dolar|glucosa|energia>` con JSON, por ejemplo:
`{"Temperatura": 30, "Hora": 18, "Dia_Semana": 3}`
