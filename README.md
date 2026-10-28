# FinanzIA

Agente de finanzas personales para personas con ingresos variables. Clasifica cada gasto en una de 11 categorías, calcula el presupuesto disponible y avisa cuando se pasa un tope.

## Cómo correrlo

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Cómo funciona el agente

| Parte | Qué hace | Tipo |
| --- | --- | --- |
| `agente/knn.py` | Clasifica el gasto comparándolo con los ejemplos más parecidos del dataset (KNN, similitud coseno sobre pedacitos de 3 y 4 letras, K = 5) | IA (aprendizaje supervisado) |
| `agente/correcciones.py` | Si el usuario ya corrigió un gasto igual o muy parecido, se usa su corrección antes que el KNN | Aprendizaje con el uso |
| `agente/presupuesto.py` | Disponible = base del mes − obligaciones fijas − meta de ahorro − gastado | Cálculo |
| `agente/alertas.py` | Avisa cuando una categoría pasa el 80 % o el 100 % de su tope | Reglas |
| `agente/categorizador.py` | Une todo: corrección → KNN → duda. Las palabras clave quedan como línea base para comparar | |

Si ningún ejemplo se parece al menos un 25 % al gasto escrito, el agente no adivina: dice que no está seguro y pide revisar la categoría.

## Dataset

`datos/dataset_gastos.csv`: 1.245 gastos, 663 frases base distintas, mínimo 51 por categoría. Se genera con `python datos/generador/generar_dataset.py` (semilla fija) a partir de las frases escritas en `datos/generador/frases_base.py`.

| Columna | Para qué sirve |
| --- | --- |
| `descripcion_libre` | El texto que lee el KNN |
| `categoria` | La respuesta correcta |
| `frase_base` | Agrupa las variantes de una misma frase, para que ninguna quede a la vez en entrenamiento y en prueba |
| `conjunto` | `entrenamiento` (70 %), `validacion` (15 %) o `prueba` (15 %). La app nunca usa `prueba` |
| `variante` / `informal` | Cómo se escribió (con muletilla, medio de pago, abreviada o con errores) |
| `fuente` | `generado` por ahora; los gastos reales del equipo entran como `real` |
| `etiquetador` / `revisor` / `categoria_revisor` | Para la revisión del equipo y la kappa de Cohen |

`datos/ingresos_sinteticos.csv`: ingresos de 3 perfiles (diario, quincenal y por proyectos) durante 3 meses, para probar el presupuesto en meses buenos y malos.

Las frases de `pruebas/etiquetados.csv` se excluyen del dataset, para que ese archivo siga siendo una evaluación independiente.

## Evaluación

```bash
python pruebas/calidad_dataset.py        # criterios de calidad del dataset
python pruebas/evaluar.py                # KNN vs palabras clave
python pruebas/evaluar_correcciones.py   # efecto de las correcciones del usuario
```

| Evaluación | Palabras clave | KNN |
| --- | --- | --- |
| Conjunto de prueba del dataset (181 gastos que el modelo nunca vio) | F1 macro 0,38 | **F1 macro 0,58** |
| `pruebas/etiquetados.csv` (60 gastos escritos por el equipo) | F1 macro 0,75 | F1 macro 0,75 |

## Pendiente

- Revisar el dataset: que un integrante revise las etiquetas y que dos personas etiqueten las mismas 100 frases para calcular la kappa (meta ≥ 0,80).
- Agregar unos 100 gastos reales con `fuente = real` para comparar con datos de verdad.
