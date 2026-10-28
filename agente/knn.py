"""Clasificador KNN de gastos.

Cómo decide:
  1. Limpia el texto (minúsculas, sin tildes, sin montos, sin medio de pago, sin palabras vacías).
  2. Lo parte en pedacitos de 3 y 4 letras y los pesa con TF-IDF (los pedacitos raros pesan más).
  3. Lo compara con todos los ejemplos del dataset usando similitud coseno.
  4. Votan los K ejemplos más parecidos; cada voto pesa según su similitud.
  5. Si ni el más parecido llega a UMBRAL_DUDA, el agente avisa que no está seguro.

Los pedacitos de letras hacen que "almuerso" o "transmi" se sigan pareciendo a "almuerzo" y
"transmilenio", algo que una lista de palabras clave no logra.
"""
import csv
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

RUTA_DATASET = Path(__file__).resolve().parent.parent / "datos" / "dataset_gastos.csv"
K = 5              # elegido con el conjunto de validación (ver pruebas/evaluar.py)
UMBRAL_DUDA = 0.25  # si el ejemplo más parecido está por debajo, el agente pide confirmar

PALABRAS_VACIAS = set(
    "hoy por pse con nequi en efectivo daviplata compre me gaste pague pago gasto "
    "de la el los las y a al del para un una mi mis lo que se le".split()
)
# El medio de pago no dice en qué se gastó: se quita la frase completa ("con tarjeta débito").
# La palabra "tarjeta" sola sí se conserva, porque indica deudas ("cuota de la tarjeta").
MEDIO_DE_PAGO = re.compile(r"\b(por|con|en|cn|x)\s+(nequi|daviplata|pse|efectivo|tarjeta(\s+(debito|credito))?)\b")


def limpiar(texto):
    """Minúsculas, sin tildes, sin montos, sin medio de pago y sin palabras vacías."""
    t = unicodedata.normalize("NFD", texto.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = MEDIO_DE_PAGO.sub(" ", t)
    t = re.sub(r"\$?\s?\d[\d.,]*\s?(k|mil|lucas)?\b", " ", t)
    t = re.sub(r"[^a-zñ ]", " ", t)
    return " ".join(w for w in t.split() if w not in PALABRAS_VACIAS)


def cargar_ejemplos(conjuntos=("entrenamiento", "validacion"), ruta=RUTA_DATASET):
    """Ejemplos (descripción, categoría) del dataset. La app NUNCA usa el conjunto de prueba."""
    with open(ruta, "r", newline="", encoding="utf-8") as archivo:
        return [(f["descripcion_libre"], f["categoria"]) for f in csv.DictReader(archivo)
                if f["conjunto"] in conjuntos]


class ClasificadorKNN:
    def __init__(self, ejemplos, k=K):
        self.textos = [t for t, _ in ejemplos]
        self.categorias = [c for _, c in ejemplos]
        self.k = k
        self.vectorizador = TfidfVectorizer(preprocessor=limpiar, analyzer="char_wb", ngram_range=(3, 4))
        self.matriz = self.vectorizador.fit_transform(self.textos)

    def predecir(self, descripcion):
        """Devuelve {categoria, duda, similitud, vecinos}, con los vecinos que votaron."""
        sims = cosine_similarity(self.vectorizador.transform([descripcion]), self.matriz).ravel()
        mejores = sims.argsort()[::-1][:self.k]
        votos = {}
        for i in mejores:
            votos[self.categorias[i]] = votos.get(self.categorias[i], 0) + sims[i]
        return {
            "categoria": max(votos, key=votos.get),
            "duda": bool(sims[mejores[0]] < UMBRAL_DUDA),
            "similitud": float(sims[mejores[0]]),
            "vecinos": [(self.textos[i], self.categorias[i], float(sims[i])) for i in mejores],
        }


@lru_cache(maxsize=1)
def modelo():
    """El clasificador de la app, entrenado una sola vez con entrenamiento + validación."""
    return ClasificadorKNN(cargar_ejemplos())
