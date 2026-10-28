from agente.correcciones import buscar_correccion
from agente.knn import modelo

# Las 11 categorías del documento (sección 2).
# Las palabras clave ya no deciden en la app: quedan como LÍNEA BASE para comparar con el KNN
# (pruebas/evaluar.py). El orden importa: gana la primera categoría que tenga una palabra clave
# en la descripción, por eso las de negocio van primero ("pollo para vender" es mercancía, no
# comida). Las palabras salen de los ejemplos de la definición de cada categoría, NUNCA del
# conjunto de evaluación (pruebas/etiquetados.csv).
PALABRAS_CLAVE = {
    "Mercancía e insumos": ["para vender", "revender", "mercancía", "mercancia", "inventario", "proveedor",
                            "insumos", "materia prima", "surtido"],
    "Otros gastos del negocio": ["bolsas", "flete", "alquiler carrito", "pipeta", "hielo", "servilletas",
                                 "permiso", "puesto"],
    "Alimentación en casa": ["mercado", "tienda", "arroz", "huevos"],
    "Comidas fuera de casa": ["empanada", "almuerzo", "desayuno", "comida", "pan", "arepa", "jugo", "café",
                              "cafe", "gaseosa", "pollo", "corrientazo", "tinto", "domicilio"],
    "Transporte": ["pasaje", "bus", "taxi", "gasolina", "metro", "transmilenio", "uber", "parqueadero",
                   "peaje", "mototaxi", "sitp"],
    "Vivienda y servicios": ["arriendo", "recibo", "recarga", "plan de datos", "internet"],
    "Salud": ["droguería", "drogueria", "acetaminofén", "acetaminofen", "cita médica", "pastillas"],
    "Educación": ["colegio", "útiles", "utiles", "fotocopias", "matrícula", "matricula"],
    "Deudas y créditos": ["cuota", "gota a gota", "abono", "préstamo", "prestamo"],
    "Personal, hogar y ocio": ["ropa", "zapatos", "champú", "champu", "jabón", "jabon", "peluquería",
                               "peluqueria", "cine", "cerveza", "camiseta"],
}
CATEGORIAS = list(PALABRAS_CLAVE) + ["Otros"]


def categorizar_por_reglas(descripcion):
    """Asigna una categoría buscando palabras clave en la descripción (línea base)."""
    texto = descripcion.lower()
    for categoria, palabras in PALABRAS_CLAVE.items():
        for palabra in palabras:
            if palabra in texto:
                return categoria
    return "Otros"


def categorizar(descripcion, correcciones):
    """Primero mira las correcciones del usuario; si no hay una parecida, decide el KNN.

    Devuelve (categoria, origen), donde origen es:
      "corrección"  el usuario ya había corregido una descripción igual o muy parecida
      "knn"         votaron los ejemplos más parecidos del dataset
      "duda"        ningún ejemplo se parece lo suficiente: es la mejor apuesta, pero hay que revisarla
    """
    categoria = buscar_correccion(descripcion, correcciones)
    if categoria:
        return categoria, "corrección"
    resultado = modelo().predecir(descripcion)
    return resultado["categoria"], "duda" if resultado["duda"] else "knn"
