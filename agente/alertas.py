def gasto_por_categoria(movimientos):
    """Suma lo gastado en cada categoría."""
    totales = {}
    for m in movimientos:
        if m["tipo"] == "gasto":
            categoria = m["categoria"] or "Otros"
            totales[categoria] = totales.get(categoria, 0) + float(m["monto"])
    return totales


def revisar_topes(perfil, movimientos):
    """Devuelve una lista de alertas por topes superados o casi superados."""
    alertas = []
    totales = gasto_por_categoria(movimientos)

    for categoria, tope in perfil["topes"].items():
        gastado = totales.get(categoria, 0)
        if gastado > tope:
            exceso = gastado - tope
            alertas.append(("error", f"Superaste el tope de {categoria} por ${exceso:,.0f}."))
        elif gastado >= tope * 0.8:
            alertas.append(("warning", f"Vas en el {gastado / tope:.0%} del tope de {categoria}."))

    return alertas