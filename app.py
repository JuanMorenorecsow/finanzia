import streamlit as st
from agente.alertas import gasto_por_categoria, revisar_topes
from agente.categorizador import CATEGORIAS, categorizar
from agente.correcciones import cargar_correcciones, guardar_correccion
from agente.presupuesto import cargar_perfil, calcular_presupuesto_disponible
from agente.registro import guardar_movimiento, cargar_movimientos, corregir_categoria, movimientos_del_mes

st.title("FinanzIA")

perfil = cargar_perfil()

# --- Formulario para registrar un movimiento (percepción) ---
st.subheader("Registrar movimiento")

tipo = st.radio("Tipo", ["gasto", "ingreso"], horizontal=True)
monto = st.number_input("Monto", min_value=0, step=1000)
descripcion = st.text_input("Descripción corta (ej: empanadas, pasajes)")

if st.button("Guardar"):
    if monto > 0 and descripcion.strip() != "":
        categoria, origen = "", ""
        if tipo == "gasto":
            # Decisión: se clasifica el gasto (los ingresos no se clasifican)
            categoria, origen = categorizar(descripcion.strip(), cargar_correcciones())
        guardar_movimiento(tipo, monto, descripcion.strip(), categoria)
        if categoria:
            fuente = "por una corrección tuya anterior" if origen == "corrección" else "por palabras clave"
            st.success(f"Movimiento guardado. Categoría: {categoria} ({fuente}). Si no es, corrígela abajo.")
        else:
            st.success("Movimiento guardado. Categoría: no aplica (ingreso)")
    else:
        st.warning("Escribe un monto mayor a 0 y una descripción.")

# --- Presupuesto disponible (se calcula, no se clasifica) ---
movimientos = cargar_movimientos()
del_mes = movimientos_del_mes(movimientos)
p = calcular_presupuesto_disponible(perfil, del_mes)

st.subheader("Tu situación este mes")
col1, col2 = st.columns(2)
col1.metric("Gastado", f"${p['gastado']:,.0f}")
col2.metric("Disponible", f"${p['disponible']:,.0f}")
st.caption(f"Disponible = ingreso ${p['ingreso']:,.0f} − obligaciones ${p['obligaciones']:,.0f} "
           f"− ahorro ${p['ahorro']:,.0f} − gastado ${p['gastado']:,.0f}")

# --- Alertas y gasto por categoría ---
st.subheader("Alertas")
alertas = revisar_topes(perfil, del_mes)
if alertas:
    for nivel, mensaje in alertas:
        if nivel == "error":
            st.error(mensaje)
        else:
            st.warning(mensaje)
else:
    st.success("Vas bien, no hay alertas.")

st.subheader("Gasto por categoría")
totales = gasto_por_categoria(del_mes)
if totales:
    st.bar_chart(totales)

# --- Corregir una categoría (aprendizaje) ---
st.subheader("Corregir una categoría")
gastos = [(i, m) for i, m in enumerate(movimientos) if m["tipo"] == "gasto"][::-1][:20]
if gastos:
    elegido = st.selectbox("Gasto", gastos, format_func=lambda x: f"{x[1]['fecha_hora'][:16]} · {x[1]['descripcion']} · "
                                                                  f"${float(x[1]['monto']):,.0f} · {x[1]['categoria']}")
    nueva = st.selectbox("Categoría correcta", CATEGORIAS)
    if st.button("Corregir"):
        indice, mov = elegido
        corregir_categoria(indice, nueva)
        guardar_correccion(mov["descripcion"], nueva)
        st.success(f"Listo. La próxima vez que escribas algo como “{mov['descripcion']}”, lo pondré en {nueva}.")
        st.rerun()
else:
    st.info("Todavía no hay gastos para corregir.")

# --- Historial ---
st.subheader("Movimientos registrados")
if movimientos:
    st.dataframe(movimientos)
else:
    st.info("Todavía no has registrado movimientos.")
