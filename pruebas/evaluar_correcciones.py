import csv
import sys
import os

# Permite importar el paquete "agente" desde la carpeta principal
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.metrics import f1_score
from agente.categorizador import categorizar, categorizar_por_reglas
from agente.correcciones import normalizar
from agente.knn import modelo

# Separación fija: dentro de cada categoría, los ejemplos en posición par son de APRENDIZAJE
# (simulan correcciones del usuario) y los impares son de EVALUACIÓN. Nunca se mezclan.
with open("pruebas/etiquetados.csv", "r", newline="", encoding="utf-8") as archivo:
    filas = list(csv.DictReader(archivo))

posicion = {}
aprendizaje, evaluacion = [], []
for f in filas:
    n = posicion.get(f["categoria"], 0)
    posicion[f["categoria"]] = n + 1
    (aprendizaje if n % 2 == 0 else evaluacion).append(f)

# El usuario corrige los ejemplos de aprendizaje que el KNN clasifica mal
correcciones = [{"descripcion": normalizar(f["descripcion"]), "categoria": f["categoria"]}
                for f in aprendizaje if modelo().predecir(f["descripcion"])["categoria"] != f["categoria"]]

reales = [f["categoria"] for f in evaluacion]
solo_reglas = [categorizar_por_reglas(f["descripcion"]) for f in evaluacion]
solo_knn = [modelo().predecir(f["descripcion"])["categoria"] for f in evaluacion]
con_correcciones = [categorizar(f["descripcion"], correcciones)[0] for f in evaluacion]

print(f"Aprendizaje: {len(aprendizaje)} ejemplos ({len(correcciones)} correcciones) | Evaluación: {len(evaluacion)} ejemplos")
print(f"F1 macro solo palabras clave: {f1_score(reales, solo_reglas, average='macro', zero_division=0):.2f}")
print(f"F1 macro solo KNN:            {f1_score(reales, solo_knn, average='macro', zero_division=0):.2f}")
print(f"F1 macro KNN + correcciones:  {f1_score(reales, con_correcciones, average='macro', zero_division=0):.2f}")
print()
print("Ejemplos de evaluación que cambiaron gracias a una corrección:")
for f, a, b in zip(evaluacion, solo_knn, con_correcciones):
    if a != b:
        print(f"  '{f['descripcion']}': {a} -> {b} (real: {f['categoria']})")
