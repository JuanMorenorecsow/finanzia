import glob
import pandas as pd

ruta = glob.glob("datos/emicron/**/*.csv", recursive=True)[0]
df = pd.read_csv(ruta, sep=None, engine="python", encoding="latin-1")

columnas = ["GASTOS_MES", "COSTOS_MES_ANTERIOR", "CONSUMO_INTERMEDIO"]
print("Filas totales:", len(df))
print()
for c in columnas:
    positivos = df[df[c] > 0][c]
    print(c)
    print("  con valor mayor a 0:", len(positivos))
    print("  mediana (pesos):", f"{positivos.median():,.0f}")
    print("  percentil 25 y 75:", f"{positivos.quantile(0.25):,.0f}", "y", f"{positivos.quantile(0.75):,.0f}")
    print()