import csv
import sys
import os

# Permite importar el paquete "agente" desde la carpeta principal
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.metrics import f1_score, accuracy_score, classification_report
from agente.categorizador import categorizar_por_reglas

with open("pruebas/etiquetados.csv", "r", newline="", encoding="utf-8") as archivo:
    filas = list(csv.DictReader(archivo))

reales = [f["categoria"] for f in filas]
predichas = [categorizar_por_reglas(f["descripcion"]) for f in filas]

print(f"Ejemplos evaluados: {len(filas)}")
print(f"Exactitud: {accuracy_score(reales, predichas):.2f}")
print(f"F1 macro: {f1_score(reales, predichas, average='macro', zero_division=0):.2f}")
print()
print("Detalle por categoría:")
print(classification_report(reales, predichas, zero_division=0))

print("Errores:")
for f, p in zip(filas, predichas):
    if f["categoria"] != p:
        print(f"  '{f['descripcion']}': real = {f['categoria']}, predicha = {p}")