import streamlit as st
from agente.alertas import gasto_por_categoria, revisar_topes
from agente.categorizador import categorizar_por_reglas
from agente.presupuesto import cargar_perfil, calcular_presupuesto_disponible
from agente.registro import guardar_movimiento, cargar_movimientos, total_gastado

st.title("FinanzIA")

perfil = cargar_perfil()

# --- Formulario para registrar un movimiento ---
st.subheader("Registrar movimiento")

tipo = st.radio("Tipo", ["gasto", "ingreso"], horizontal=True)
monto = st.number_input("Monto", min_value=0, step=1000)
descripcion = st.text_input("Descripción corta (ej: empanadas, pasajes)")

if st.button("Guardar"):
    if monto > 0 and descripcion.strip() != "":
        categoria = categorizar_por_reglas(descripcion.strip()) if tipo == "gasto" else ""
        guardar_movimiento(tipo, monto, descripcion.strip(), categoria)
        st.success(f"Movimiento guardado. Categoría: {categoria or 'no aplica (ingreso)'}")
    else:
        st.warning("Escribe un monto mayor a 0 y una descripción.")

# --- Presupuesto disponible ---
movimientos = cargar_movimientos()
gastado = total_gastado(movimientos)
disponible = calcular_presupuesto_disponible(perfil, gastado)

st.subheader("Tu situación este mes")
col1, col2 = st.columns(2)
col1.metric("Gastado", f"${gastado:,.0f}")
col2.metric("Disponible", f"${disponible:,.0f}")

# --- Alertas y gasto por categoría ---
st.subheader("Alertas")
alertas = revisar_topes(perfil, movimientos)
if alertas:
    for nivel, mensaje in alertas:
        if nivel == "error":
            st.error(mensaje)
        else:
            st.warning(mensaje)
else:
    st.success("Vas bien, no hay alertas.")

st.subheader("Gasto por categoría")
totales = gasto_por_categoria(movimientos)
if totales:
    st.bar_chart(totales)

# --- Historial ---
st.subheader("Movimientos registrados")
if movimientos:
    st.dataframe(movimientos)
else:
    st.info("Todavía no has registrado movimientos.")