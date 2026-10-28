"""Compara el KNN con la línea base de palabras clave.

Uso (desde la carpeta principal):  python pruebas/evaluar.py

1. Elige K con el conjunto de VALIDACIÓN del dataset.
2. Mide una sola vez en el conjunto de PRUEBA del dataset (frases que el modelo nunca vio).
3. Mide también en pruebas/etiquetados.csv, escrito por el equipo y que el dataset no contiene.
"""
import csv
import sys
import os

# Permite importar el paquete "agente" desde la carpeta principal
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.metrics import f1_score, accuracy_score, classification_report
from agente.categorizador import categorizar_por_reglas
from agente.knn import ClasificadorKNN, cargar_ejemplos


def f1(reales, predichas):
    return f1_score(reales, predichas, average="macro", zero_division=0)


entrenamiento = cargar_ejemplos(("entrenamiento",))
validacion = cargar_ejemplos(("validacion",))
prueba = cargar_ejemplos(("prueba",))
print(f"Dataset: {len(entrenamiento)} entrenamiento | {len(validacion)} validación | {len(prueba)} prueba")

# --- 1. Elegir K con validación ---
# Con menos de 200 ejemplos de validación, diferencias menores a 0,03 son ruido: entre las K
# que quedan a esa distancia de la mejor, se elige la más grande porque es más estable.
print("\n1. Elegir K (F1 macro en validación)")
resultados = {}
for k in [1, 3, 5, 7, 9]:
    modelo = ClasificadorKNN(entrenamiento, k)
    resultados[k] = f1([c for _, c in validacion], [modelo.predecir(t)["categoria"] for t, _ in validacion])
    print(f"   K={k}: {resultados[k]:.3f}")
mejor = max(resultados.values())
k_elegida = max(k for k, v in resultados.items() if v >= mejor - 0.03)
print(f"   K elegida: {k_elegida}")

# --- 2. Prueba del dataset (una sola vez) ---
modelo = ClasificadorKNN(entrenamiento, k_elegida)
reales = [c for _, c in prueba]
pred_knn = [modelo.predecir(t)["categoria"] for t, _ in prueba]
pred_reglas = [categorizar_por_reglas(t) for t, _ in prueba]
print("\n2. Conjunto de prueba del dataset")
print(f"   Palabras clave: F1 macro {f1(reales, pred_reglas):.2f} | exactitud {accuracy_score(reales, pred_reglas):.2f}")
print(f"   KNN:            F1 macro {f1(reales, pred_knn):.2f} | exactitud {accuracy_score(reales, pred_knn):.2f}")
print("\n   Detalle del KNN por categoría:")
print(classification_report(reales, pred_knn, zero_division=0))

# --- 3. Ejemplos escritos por el equipo ---
with open("pruebas/etiquetados.csv", "r", newline="", encoding="utf-8") as archivo:
    filas = list(csv.DictReader(archivo))
modelo = ClasificadorKNN(entrenamiento + validacion, k_elegida)  # igual que en la app
reales = [f["categoria"] for f in filas]
pred_reglas = [categorizar_por_reglas(f["descripcion"]) for f in filas]
pred_knn = [modelo.predecir(f["descripcion"])["categoria"] for f in filas]
print(f"3. pruebas/etiquetados.csv ({len(filas)} ejemplos del equipo)")
print(f"   Palabras clave: F1 macro {f1(reales, pred_reglas):.2f} | exactitud {accuracy_score(reales, pred_reglas):.2f}")
print(f"   KNN:            F1 macro {f1(reales, pred_knn):.2f} | exactitud {accuracy_score(reales, pred_knn):.2f}")

print("\n   Errores del KNN:")
for f, p in zip(filas, pred_knn):
    if f["categoria"] != p:
        print(f"     '{f['descripcion']}': real = {f['categoria']}, predicha = {p}")
