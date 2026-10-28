"""Genera el dataset de gastos de FinanzIA a partir de frases_base.py.

Uso (desde la carpeta principal del proyecto):
    python datos/generador/generar_dataset.py

Sale:
    datos/dataset_gastos.csv       gastos etiquetados con las 11 categorías
    datos/ingresos_sinteticos.csv  ingresos de 3 perfiles × 3 meses

Cada frase base produce entre 1 y 3 descripciones (variantes), escritas como las escribiría
un usuario: tal cual, con muletillas ("Me gasté en"), con el medio de pago, informal (sin
tildes, abreviada) o con un error de digitación. Todas las variantes de una frase comparten
frase_base, para dividir entrenamiento / validación / prueba sin que una frase quede en dos lados.
La semilla es fija: el resultado sale igual cada vez.
"""
import csv
import random
import re
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from frases_base import FRASES

SEMILLA = 42
rng = random.Random(SEMILLA)
RAIZ = Path(__file__).resolve().parents[2]


def normalizar(t: str) -> str:
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return " ".join(re.sub(r"[^a-z0-9ñ ]", " ", t).split())


# Las frases de pruebas/etiquetados.csv se dejan por fuera: ese archivo es una evaluación
# independiente y el modelo no puede haberlas visto.
with open(RAIZ / "pruebas" / "etiquetados.csv", encoding="utf-8") as f:
    EXCLUIDAS = {normalizar(fila["descripcion"]) for fila in csv.DictReader(f)}

# ---------------------------------------------------------------- variantes
MULETILLAS = ["Me gasté en", "Pagué", "Gasto:", "Pago de"]
PAGOS = ["por Nequi", "con Daviplata", "en efectivo", "con tarjeta débito", "por PSE"]
ABREVIATURAS = {"para": "pa", "que": "q", "por": "x", "universidad": "U", "transmilenio": "transmi",
                "celular": "cel", "cumpleaños": "cumple", "mensualidad": "mensualida", "con": "cn",
                "administración": "admin", "de": "d"}


def sin_tildes(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def informal(t):
    palabras = [ABREVIATURAS.get(w.lower(), w) if rng.random() < 0.7 else w for w in t.split()]
    return sin_tildes(" ".join(palabras)).lower()


def con_error(t):
    """Un error de digitación realista en una palabra larga."""
    palabras = t.split()
    largas = [i for i, w in enumerate(palabras) if len(w) >= 5 and w.isalpha()]
    if not largas:
        return None
    i = rng.choice(largas)
    w = palabras[i]
    tipo = rng.choice(["quitar", "cambiar", "fonetico"])
    if tipo == "quitar":
        j = rng.randrange(1, len(w) - 1)
        w = w[:j] + w[j + 1:]
    elif tipo == "cambiar":
        j = rng.randrange(1, len(w) - 2)
        w = w[:j] + w[j + 1] + w[j] + w[j + 2:]
    else:
        pares = [("z", "s"), ("ll", "y"), ("v", "b"), ("b", "v"), ("c", "s"), ("ción", "cion"), ("h", "")]
        candidatos = [(a, b) for a, b in pares if a in w.lower()]
        if not candidatos:
            return None
        a, b = rng.choice(candidatos)
        w = w.lower().replace(a, b, 1)
    palabras[i] = w
    return " ".join(palabras).lower()


def variantes(texto: str):
    """Devuelve [(descripcion, tipo_variante, es_informal)]."""
    base_informal = texto == texto.lower()  # las frases en minúscula ya son jerga o abreviaciones
    out = [(texto, "original", base_informal)]
    opciones = ["muletilla", "pago", "informal", "error", "muletilla_pago"]
    for tipo in rng.sample(opciones, k=rng.choice([0, 1, 1, 2])):
        if tipo == "muletilla":
            d = f"{rng.choice(MULETILLAS)} {texto[0].lower() + texto[1:]}"
        elif tipo == "pago":
            d = f"{texto} {rng.choice(PAGOS)}"
        elif tipo == "muletilla_pago":
            d = f"{rng.choice(MULETILLAS)} {texto[0].lower() + texto[1:]} {rng.choice(PAGOS)}"
        elif tipo == "informal":
            d = informal(texto)
        else:
            d = con_error(texto)
        if d and normalizar(d) not in {normalizar(x[0]) for x in out} | EXCLUIDAS:
            out.append((d, tipo, base_informal or tipo in ("informal", "error")))
    return out


# ---------------------------------------------------------------- montos y fechas
INICIO = datetime(2026, 5, 1)
DIAS = (datetime(2026, 10, 26) - INICIO).days


def monto(minimo, maximo):
    v = rng.uniform(minimo, maximo) * 1000
    paso = 100 if v < 20_000 else 500 if v < 200_000 else 1000
    return int(round(v / paso) * paso)


def fecha():
    d = INICIO + timedelta(days=rng.randrange(DIAS), hours=rng.randint(6, 22), minutes=rng.randrange(60))
    return d.strftime("%Y-%m-%d %H:%M")


# ---------------------------------------------------------------- construcción
filas, excluidas = [], 0
for cat, bloque in FRASES.items():
    bases = []
    for linea in bloque.strip().splitlines():
        texto, mn, mx = [x.strip() for x in linea.split(";")]
        if normalizar(texto) in EXCLUIDAS:
            excluidas += 1
            continue
        bases.append((texto, float(mn), float(mx)))
    # División 70/15/15 por frase base dentro de cada categoría (sin fuga y estratificada)
    orden = list(range(len(bases)))
    rng.shuffle(orden)
    n_val = round(len(bases) * 0.15)
    n_pru = round(len(bases) * 0.15)
    conjunto = {}
    for pos, i in enumerate(orden):
        conjunto[i] = "prueba" if pos < n_pru else "validacion" if pos < n_pru + n_val else "entrenamiento"
    for i, (texto, mn, mx) in enumerate(bases):
        for desc, tipo, es_inf in variantes(texto):
            filas.append({
                "fecha_hora": fecha(), "monto": monto(mn, mx), "tipo_movimiento": "Gasto",
                "descripcion_libre": desc, "frase_base": normalizar(texto), "categoria": cat,
                "variante": tipo, "informal": es_inf, "fuente": "generado", "etiquetador": "IA",
                "revisor": "", "categoria_revisor": "", "conjunto": conjunto[i],
            })

df = pd.DataFrame(filas).sample(frac=1, random_state=SEMILLA).reset_index(drop=True)
df.insert(0, "id", range(1, len(df) + 1))
df.to_csv(RAIZ / "datos" / "dataset_gastos.csv", index=False, encoding="utf-8")

# ---------------------------------------------------------------- ingresos sintéticos
# Tres formas de recibir dinero, como en el perfil de la app: diario, quincenal y por proyectos.
ing = []
for y, m in [(2026, 8), (2026, 9), (2026, 10)]:
    # Diario: ventas de un puesto, 24 días al mes, con días buenos y malos (±40 %)
    for dia in sorted(rng.sample(range(1, 29), 24)):
        ing.append(("diario", y, m, dia, "Ventas del día", round(75_000 * rng.uniform(0.6, 1.4), -3)))
    # Quincenal: dos pagos fijos
    for dia in (15, 28):
        ing.append(("quincenal", y, m, dia, "Pago de la quincena", 900_000))
    # Por proyectos (freelance): un pago grande algunos meses y meses casi en cero
    if (y, m) != (2026, 9):
        ing.append(("por_proyectos", y, m, rng.randint(1, 28), "Pago del proyecto de un cliente",
                    round(rng.uniform(3.0, 5.0) * 1e6, -3)))
    else:
        ing.append(("por_proyectos", y, m, 15, "Anticipo pequeño de un cliente nuevo", 300_000))
ingresos = pd.DataFrame(ing, columns=["perfil", "anio", "mes", "dia", "descripcion", "monto"])
ingresos["fecha"] = pd.to_datetime(dict(year=ingresos.anio, month=ingresos.mes, day=ingresos.dia)).dt.date
ingresos = ingresos[["perfil", "fecha", "descripcion", "monto"]].sort_values(["perfil", "fecha"])
ingresos["monto"] = ingresos["monto"].astype(int)
ingresos.to_csv(RAIZ / "datos" / "ingresos_sinteticos.csv", index=False, encoding="utf-8")

print(f"{len(df)} gastos · {df.frase_base.nunique()} frases base · {len(ingresos)} ingresos "
      f"· {excluidas} frases base excluidas por estar en pruebas/etiquetados.csv")
