PALABRAS_CLAVE = {
    "Alimentación": ["empanada", "almuerzo", "desayuno", "comida", "mercado",
                     "pan", "arepa", "jugo", "café", "cafe", "gaseosa", "pollo"],
    "Transporte": ["pasaje", "bus", "taxi", "gasolina", "metro",
                   "transmilenio", "uber", "parqueadero", "peaje"],
    "Mercancía": ["mercancía", "mercancia", "inventario", "proveedor",
                  "insumos", "materia prima", "bolsas"],
}


def categorizar_por_reglas(descripcion):
    """Asigna una categoría buscando palabras clave en la descripción."""
    texto = descripcion.lower()
    for categoria, palabras in PALABRAS_CLAVE.items():
        for palabra in palabras:
            if palabra in texto:
                return categoria
    return "Otros"