import csv
import os
from datetime import datetime

RUTA_MOVIMIENTOS = "datos/movimientos.csv"
ENCABEZADOS = ["fecha_hora", "tipo", "monto", "descripcion", "categoria", "categoria_propuesta"]


def guardar_movimiento(tipo, monto, descripcion, categoria="", ruta=RUTA_MOVIMIENTOS):
    """Agrega un movimiento (ingreso o gasto) al archivo CSV.

    La categoría que propuso el agente se guarda también en "categoria_propuesta",
    para poder medir después cuántas veces el usuario la corrigió.
    """
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    movimientos = cargar_movimientos(ruta)
    movimientos.append({"fecha_hora": fecha_hora, "tipo": tipo, "monto": monto, "descripcion": descripcion,
                        "categoria": categoria, "categoria_propuesta": categoria})
    _escribir(movimientos, ruta)


def corregir_categoria(indice, categoria, ruta=RUTA_MOVIMIENTOS):
    """Cambia la categoría del movimiento número `indice` (en el orden del archivo)."""
    movimientos = cargar_movimientos(ruta)
    movimientos[indice]["categoria"] = categoria
    _escribir(movimientos, ruta)


def cargar_movimientos(ruta=RUTA_MOVIMIENTOS):
    """Devuelve la lista de movimientos guardados."""
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        return []
    with open(ruta, "r", newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def movimientos_del_mes(movimientos, hoy=None):
    """Solo los movimientos del mes de `hoy` (por defecto, el mes actual)."""
    mes = (hoy or datetime.now()).strftime("%Y-%m")
    return [m for m in movimientos if m["fecha_hora"].startswith(mes)]


def total_gastado(movimientos):
    """Suma todos los gastos."""
    return sum(float(m["monto"]) for m in movimientos if m["tipo"] == "gasto")


def _escribir(movimientos, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADOS)
        escritor.writeheader()
        for m in movimientos:
            # Los archivos viejos no tienen "categoria_propuesta": se toma la categoría que tenían
            escritor.writerow({c: m.get(c) or (m.get("categoria", "") if c == "categoria_propuesta" else "")
                               for c in ENCABEZADOS})
