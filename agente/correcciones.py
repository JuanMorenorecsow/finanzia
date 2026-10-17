import csv
import os
import unicodedata
from datetime import datetime
from difflib import SequenceMatcher

RUTA_CORRECCIONES = "datos/correcciones.csv"
ENCABEZADOS = ["fecha_hora", "descripcion", "categoria"]
SIMILITUD_MINIMA = 0.8


def normalizar(texto):
    """Minúsculas, sin tildes y sin espacios repetidos, para comparar descripciones."""
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return " ".join(texto.split())


def guardar_correccion(descripcion, categoria, ruta=RUTA_CORRECCIONES):
    """Guarda que el usuario corrigió la categoría de esta descripción."""
    existe = os.path.exists(ruta) and os.path.getsize(ruta) > 0
    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if not existe:
            escritor.writerow(ENCABEZADOS)
        escritor.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), normalizar(descripcion), categoria])


def cargar_correcciones(ruta=RUTA_CORRECCIONES):
    """Devuelve las correcciones guardadas, de la más antigua a la más reciente."""
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        return []
    with open(ruta, "r", newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def buscar_correccion(descripcion, correcciones):
    """Categoría que el usuario dio a una descripción igual o muy parecida, o None.

    Si hay varias, gana la más reciente, porque los hábitos cambian.
    """
    texto = normalizar(descripcion)
    for c in reversed(correcciones):
        if SequenceMatcher(None, texto, c["descripcion"]).ratio() >= SIMILITUD_MINIMA:
            return c["categoria"]
    return None
