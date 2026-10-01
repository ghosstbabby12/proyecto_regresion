"""
Genera dashboard.html: un panel interactivo autocontenido con los datos de
data/*.csv y los resultados de resultados/resultados.json.

Ejecutar (después de entrenar_modelos.py):
    python generar_dashboard.py
Luego abra dashboard.html en el navegador, o con la app Flask: http://127.0.0.1:5000/dashboard
"""
import csv
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
UNIDADES = {"dolar": "pesos", "glucosa": "mg/dL", "energia": "kWh"}
CLAVES_RES = ["titulo", "ecuacion", "intercepto", "coeficientes", "metricas", "variable_mayor_impacto"]


def numero(texto):
    """Convierte a número con 6 cifras significativas (enteros se mantienen enteros)."""
    v = float(texto)
    return int(v) if v.is_integer() else float(f"{v:.6g}")


def main():
    with open(os.path.join(BASE, "resultados", "resultados.json"), encoding="utf-8") as f:
        resultados = json.load(f)

    datos = {}
    for clave, unidad in UNIDADES.items():
        with open(os.path.join(BASE, "data", f"{clave}_data.csv"), encoding="utf-8") as f:
            lector = csv.reader(f)
            cabecera = next(lector)
            filas = [[numero(x) for x in fila] for fila in lector if fila]
        datos[clave] = {
            "target": cabecera[-1],
            "features": cabecera[:-1],
            "unidad": unidad,
            "cols": {c: [fila[i] for fila in filas] for i, c in enumerate(cabecera)},
            "res": {k: resultados[clave][k] for k in CLAVES_RES},
        }

    with open(os.path.join(BASE, "templates", "dashboard_base.html"), encoding="utf-8") as f:
        plantilla = f.read()
    cuerpo = plantilla.replace("__DATOS__", json.dumps(datos, ensure_ascii=False, separators=(",", ":")))

    salida = os.path.join(BASE, "dashboard.html")
    with open(salida, "w", encoding="utf-8") as f:
        f.write('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                '</head>\n<body>\n' + cuerpo + "\n</body>\n</html>\n")
    print(f"Dashboard generado: {salida} ({os.path.getsize(salida) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
