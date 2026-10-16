import csv
import os
from datetime import datetime

RUTA_MOVIMIENTOS = "datos/movimientos.csv"
ENCABEZADOS = ["fecha_hora", "tipo", "monto", "descripcion", "categoria"]


def guardar_movimiento(tipo, monto, descripcion, categoria="", ruta=RUTA_MOVIMIENTOS):
    """Agrega un movimiento (ingreso o gasto) al archivo CSV."""
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    existe = os.path.exists(ruta) and os.path.getsize(ruta) > 0

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if not existe:
            escritor.writerow(ENCABEZADOS)
        escritor.writerow([fecha_hora, tipo, monto, descripcion, categoria])


def cargar_movimientos(ruta=RUTA_MOVIMIENTOS):
    """Devuelve la lista de movimientos guardados."""
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        return []
    with open(ruta, "r", newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def total_gastado(movimientos):
    """Suma todos los gastos."""
    return sum(float(m["monto"]) for m in movimientos if m["tipo"] == "gasto")