import json


def cargar_perfil(ruta="datos/perfil.json"):
    """Lee el perfil del usuario desde el archivo JSON."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def calcular_presupuesto_disponible(perfil, total_gastado):
    """Calcula cuánto le queda disponible al usuario en el periodo."""
    ingreso = perfil["ingreso_estimado_mensual"]
    obligaciones = sum(o["monto"] for o in perfil["obligaciones_fijas"])
    ahorro = perfil["meta_ahorro_mensual"]

    return ingreso - obligaciones - ahorro - total_gastado