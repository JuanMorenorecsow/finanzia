import json


def cargar_perfil(ruta="datos/perfil.json"):
    """Lee el perfil del usuario desde el archivo JSON."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def es_pago_de_obligacion(movimiento, perfil):
    """True si el gasto es el pago de una obligación fija del perfil (p. ej. "pago arriendo")."""
    texto = movimiento["descripcion"].lower()
    return any(o["nombre"].lower() in texto for o in perfil["obligaciones_fijas"])


def ingreso_del_mes(perfil, movimientos_mes):
    """Con ingreso diario se usa lo que realmente ha entrado en el mes; con ingreso fijo, el estimado."""
    if perfil["tipo_ingreso"] == "diario":
        return sum(float(m["monto"]) for m in movimientos_mes if m["tipo"] == "ingreso")
    return perfil["ingreso_estimado_mensual"]


def calcular_presupuesto_disponible(perfil, movimientos_mes):
    """Presupuesto Disponible Real del mes. Es un cálculo con una fórmula fija, no una predicción:

    ingreso del mes − obligaciones fijas − meta de ahorro − lo ya gastado

    Los pagos de obligaciones fijas no se suman a "lo ya gastado" porque ya están descontados.
    """
    ingreso = ingreso_del_mes(perfil, movimientos_mes)
    obligaciones = sum(o["monto"] for o in perfil["obligaciones_fijas"])
    ahorro = perfil["meta_ahorro_mensual"]
    gastado = sum(float(m["monto"]) for m in movimientos_mes
                  if m["tipo"] == "gasto" and not es_pago_de_obligacion(m, perfil))
    return {"ingreso": ingreso, "obligaciones": obligaciones, "ahorro": ahorro, "gastado": gastado,
            "disponible": ingreso - obligaciones - ahorro - gastado}
