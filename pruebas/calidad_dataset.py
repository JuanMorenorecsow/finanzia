"""Revisa los criterios de calidad de datos/dataset_gastos.csv.

Uso (desde la carpeta principal):  python pruebas/calidad_dataset.py
Correr antes de entrenar: si un criterio no cumple su meta, se corrige el dataset primero.
"""
import sys
import os

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agente.categorizador import CATEGORIAS  # noqa: E402

df = pd.read_csv("datos/dataset_gastos.csv", keep_default_na=False)
OBLIGATORIOS = ["fecha_hora", "monto", "tipo_movimiento", "descripcion_libre", "frase_base",
                "categoria", "fuente", "conjunto"]
resultados = []


def criterio(numero, nombre, valor, cumple, meta):
    resultados.append(cumple)
    print(f"{numero:>2}. {nombre:<38} {valor:<28} meta: {meta:<10} {'CUMPLE' if cumple else 'NO CUMPLE'}")


completas = (df[OBLIGATORIOS] != "").all(axis=1).mean()
criterio(1, "Completitud", f"{completas:.0%}", completas == 1, "100 %")
validas = df.categoria.isin(CATEGORIAS).mean()
criterio(2, "Categorías válidas", f"{validas:.0%}", validas == 1, "100 %")
repetidas = df.duplicated(["descripcion_libre", "categoria"]).sum()
criterio(3, "Filas repetidas", repetidas, repetidas == 0, "0")
por_cat = df.groupby("categoria").frase_base.nunique()
criterio(4, "Frases base por categoría (mínimo)", por_cat.min(), por_cat.min() >= 50, "≥ 50")
conteo = df.categoria.value_counts()
balance = conteo.max() / conteo.min()
criterio(5, "Balance (mayor / menor)", f"{balance:.2f}", balance <= 3, "≤ 3")
bases = df.groupby("conjunto").frase_base.apply(set)
fuga = len(bases["entrenamiento"] & bases["prueba"]) + len(bases["entrenamiento"] & bases["validacion"]) \
    + len(bases["validacion"] & bases["prueba"])
criterio(6, "Frases base en dos conjuntos", fuga, fuga == 0, "0")

doble = df[df.categoria_revisor != ""]
if len(doble) >= 30:
    from sklearn.metrics import cohen_kappa_score
    kappa = cohen_kappa_score(doble.categoria, doble.categoria_revisor)
    criterio(7, "Kappa entre dos etiquetadores", f"{kappa:.2f} ({len(doble)} frases)", kappa >= 0.8, "≥ 0,80")
else:
    print(f" 7. {'Kappa entre dos etiquetadores':<38} {'pendiente: faltan frases':<28} meta: ≥ 0,80     PENDIENTE")

informal = df.informal.astype(str).eq("True").mean()
criterio(8, "Frases informales (errores, jerga)", f"{informal:.1%}", informal >= 0.2, "≥ 20 %")
montos = pd.to_numeric(df.monto, errors="coerce")
fechas = pd.to_datetime(df.fecha_hora, errors="coerce")
criterio(9, "Montos y fechas válidos", f"{(montos > 0).mean():.0%} / {fechas.notna().mean():.0%}",
         (montos > 0).all() and fechas.notna().all(), "100 %")

reales = df[df.fuente == "real"]
estado = f"{len(reales)} gastos reales" if len(reales) else "pendiente: sin gastos reales"
print(f"10. {'Representatividad (gastos reales)':<38} {estado:<28} meta: ≈ 100    {'PENDIENTE' if len(reales) < 100 else 'CUMPLE'}")
privados = df.descripcion_libre.str.contains(r"\d{7,}|@|\b3\d{9}\b", regex=True).sum()
criterio(11, "Posibles datos personales", privados, privados == 0, "0")

print(f"\nCumple {sum(resultados)} de {len(resultados)} criterios automáticos.")
