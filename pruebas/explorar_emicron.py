import glob
import pandas as pd

archivos = glob.glob("datos/emicron/**/*.csv", recursive=True)
print("Archivos CSV encontrados:", archivos)

for ruta in archivos:
    df = None
    for sep in [";", ","]:
        try:
            df = pd.read_csv(ruta, sep=sep, encoding="latin-1", low_memory=False)
            if df.shape[1] > 1:
                break
        except Exception:
            continue
    print("\n====", ruta)
    print("Filas:", len(df), "| Columnas:", df.shape[1])
    print(list(df.columns))
    print(df.head(3).to_string())