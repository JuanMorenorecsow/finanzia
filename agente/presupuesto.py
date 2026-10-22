import json
import os

RUTA_PERFIL = "datos/perfil.json"


def cargar_perfil(ruta=RUTA_PERFIL):
    """Lee el perfil del usuario. Si el archivo no existe o está dañado, devuelve un perfil vacío."""
    if os.path.exists(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except Exception:
            return {}
    return {}


def guardar_perfil(perfil, ruta=RUTA_PERFIL):
    """Guarda o actualiza el perfil del usuario en el archivo JSON."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(perfil, archivo, ensure_ascii=False, indent=4)


def es_pago_de_obligacion(movimiento, perfil):
    """True si el gasto es el pago de una obligación fija del perfil (p. ej. 'pago arriendo')."""
    texto = movimiento.get("descripcion", "").lower()
    obligaciones = perfil.get("obligaciones_fijas", [])
    return any(o.get("nombre", "").lower() in texto for o in obligaciones)


def ingreso_del_mes(perfil, movimientos_mes):
    """Base del mes. Si el usuario eligió cuánto administrar, se usa ese monto.
    Si no, con ingreso diario se usa lo que realmente ha entrado; con ingreso fijo, el estimado."""
    if perfil.get("monto_a_administrar"):
        return perfil["monto_a_administrar"]
    if perfil.get("tipo_ingreso") == "diario":
        return sum(float(m["monto"]) for m in movimientos_mes if m.get("tipo") == "ingreso")
    return perfil.get("ingreso_estimado_mensual", 0)


def calcular_presupuesto_disponible(perfil, movimientos_mes):
    """Presupuesto Disponible Real del mes: una fórmula fija, no una predicción.

    base del mes - obligaciones fijas - meta de ahorro - lo ya gastado
    Los pagos de obligaciones fijas no se suman a lo gastado porque ya están descontados.
    """
    ingreso = ingreso_del_mes(perfil, movimientos_mes)
    obligaciones = sum(o.get("monto", 0) for o in perfil.get("obligaciones_fijas", []))
    ahorro = perfil.get("meta_ahorro_mensual", 0)
    gastado = sum(
        float(m["monto"])
        for m in movimientos_mes
        if m.get("tipo") == "gasto" and not es_pago_de_obligacion(m, perfil)
    )

    return {
        "ingreso": ingreso,
        "obligaciones": obligaciones,
        "ahorro": ahorro,
        "gastado": gastado,
        "disponible": ingreso - obligaciones - ahorro - gastado,
    }