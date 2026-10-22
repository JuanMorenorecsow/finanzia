import streamlit as st
from agente.alertas import gasto_por_categoria, revisar_topes
from agente.categorizador import CATEGORIAS, categorizar
from agente.correcciones import cargar_correcciones, guardar_correccion
from agente.presupuesto import cargar_perfil, calcular_presupuesto_disponible, guardar_perfil
from agente.registro import guardar_movimiento, cargar_movimientos, corregir_categoria, movimientos_del_mes

st.set_page_config(page_title="FinanzIA")


def pesos(valor):
    """Formato colombiano: $1.000.000"""
    return "$" + f"{valor:,.0f}".replace(",", ".")


st.title("FinanzIA")

perfil = cargar_perfil()

# --- Pantalla 1: perfil de ingresos ---
if "fuentes_ingreso" not in perfil:
    st.subheader("Configuremos tu perfil")
    st.write("¿Cómo recibes tu dinero? Puedes elegir más de una opción.")
    st.write("Marca todas las que apliquen:")

    tipos = []
    if st.checkbox("Mensual"):
        tipos.append("Mensual")
    if st.checkbox("Quincenal"):
        tipos.append("Quincenal")
    if st.checkbox("Diario"):
        tipos.append("Diario")

    fuentes = []
    total_mensual = 0

    if "Mensual" in tipos:
        mensual = st.number_input("¿Cuánto recibes al mes?", min_value=0, step=50000)
        fuentes.append({"tipo": "mensual", "monto": mensual})
        total_mensual += mensual

    if "Quincenal" in tipos:
        quincena = st.number_input("¿Cuánto recibes cada quincena?", min_value=0, step=50000)
        fuentes.append({"tipo": "quincenal", "monto": quincena})
        total_mensual += quincena * 2

    if "Diario" in tipos:
        por_dia = st.number_input("¿Cuánto ganas en un día normal?", min_value=0, step=5000)
        dias = st.number_input("¿Cuántos días trabajas al mes?", min_value=1, max_value=31, value=24)
        fuentes.append({"tipo": "diario", "monto": por_dia, "dias_al_mes": dias})
        total_mensual += por_dia * dias

    st.write(f"Ingreso mensual estimado: **{pesos(total_mensual)}**")

    if st.button("Guardar perfil"):
        if not tipos or total_mensual <= 0:
            st.warning("Elige al menos un tipo de ingreso e indica un monto mayor a 0.")
        else:
            perfil["fuentes_ingreso"] = fuentes
            perfil["tipo_ingreso"] = " y ".join(t.lower() for t in tipos)
            perfil["ingreso_estimado_mensual"] = total_mensual
            guardar_perfil(perfil)
            st.rerun()

    st.stop()

# --- Pantalla 2: cuánto dinero quiere administrar ---
if "monto_a_administrar" not in perfil:
    st.subheader("¿Cuánto vas a administrar?")
    st.write(f"Tu ingreso mensual estimado es **{pesos(perfil['ingreso_estimado_mensual'])}**.")

    monto_admin = st.number_input(
        "¿Cuánto dinero quieres administrar con FinanzIA? "
        "(puedes poner el disponible total o el monto que quieras administrar)",
        min_value=0,
        step=50000,
        value=int(perfil["ingreso_estimado_mensual"]),
    )

    if st.button("Empezar"):
        if monto_admin <= 0:
            st.warning("Escribe un monto mayor a 0.")
        else:
            perfil["monto_a_administrar"] = monto_admin
            guardar_perfil(perfil)
            st.rerun()

    st.stop()

# --- Barra lateral: cambiar la configuración ---
with st.sidebar:
    st.write(f"Administrando: **{pesos(perfil['monto_a_administrar'])}**")

    if st.button("Cambiar monto a administrar"):
        perfil.pop("monto_a_administrar", None)
        guardar_perfil(perfil)
        st.rerun()

    if st.button("Cambiar mi perfil de ingresos"):
        for clave in ["fuentes_ingreso", "tipo_ingreso", "ingreso_estimado_mensual", "monto_a_administrar"]:
            perfil.pop(clave, None)
        guardar_perfil(perfil)
        st.rerun()

# --- Aviso de la acción anterior (sobrevive al rerun) ---
if "aviso" in st.session_state:
    st.success(st.session_state.pop("aviso"))

# --- Datos del mes ---
movimientos = cargar_movimientos()
del_mes = movimientos_del_mes(movimientos)
p = calcular_presupuesto_disponible(perfil, del_mes)

col1, col2 = st.columns(2)
col1.metric("Disponible", pesos(p["disponible"]))
col2.metric("Gastado", pesos(p["gastado"]))
st.caption(f"Disponible = base {pesos(p['ingreso'])} - obligaciones {pesos(p['obligaciones'])} "
           f"- ahorro {pesos(p['ahorro'])} - gastado {pesos(p['gastado'])}")

tab_ingresos, tab_gastos, tab_ahorro = st.tabs(["Ingresos", "Gastos", "Ahorro"])

# --- Pestaña Ingresos ---
with tab_ingresos:
    st.subheader("Registrar un ingreso")
    with st.form("form_ingreso", clear_on_submit=True):
        monto_ing = st.number_input("Monto", min_value=0, step=5000, key="monto_ing")
        desc_ing = st.text_input("Descripción corta (ej: ventas del día)", key="desc_ing")
        enviar_ing = st.form_submit_button("Guardar ingreso")

    if enviar_ing:
        if monto_ing > 0 and desc_ing.strip() != "":
            guardar_movimiento("ingreso", monto_ing, desc_ing.strip(), "")
            st.session_state["aviso"] = "Ingreso guardado"
            st.rerun()
        else:
            st.warning("Escribe un monto mayor a 0 y una descripción.")

    ingresos = [m for m in del_mes if m["tipo"] == "ingreso"]
    total_ingresos = sum(float(m["monto"]) for m in ingresos)
    st.metric("Ingresos registrados este mes", pesos(total_ingresos))

    if ingresos:
        st.dataframe(ingresos)
    else:
        st.info("Todavía no has registrado ingresos.")

    st.caption("Por ahora los ingresos registrados no cambian el Disponible: "
               "se calcula con el monto que elegiste administrar.")

# --- Pestaña Gastos ---
with tab_gastos:
    st.subheader("Registrar un gasto")
    with st.form("form_gasto", clear_on_submit=True):
        monto_gas = st.number_input("Monto", min_value=0, step=1000, key="monto_gas")
        desc_gas = st.text_input("Descripción corta (ej: empanadas, pasajes)", key="desc_gas")
        enviar_gas = st.form_submit_button("Guardar gasto")

    if enviar_gas:
        if monto_gas > 0 and desc_gas.strip() != "":
            categoria, origen = categorizar(desc_gas.strip(), cargar_correcciones())
            guardar_movimiento("gasto", monto_gas, desc_gas.strip(), categoria)
            fuente = "por una corrección tuya anterior" if origen == "corrección" else "por palabras clave"
            st.session_state["aviso"] = (f"Gasto guardado. Categoría: {categoria} ({fuente}). "
                                         "Si no es, corrígela más abajo.")
            st.rerun()
        else:
            st.warning("Escribe un monto mayor a 0 y una descripción.")

    st.subheader("Alertas")
    alertas = revisar_topes(perfil, del_mes) if perfil.get("topes") else []
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
    else:
        st.info("Todavía no hay gastos para graficar.")

    st.subheader("Corregir una categoría")
    ultimos = [(i, m) for i, m in enumerate(movimientos) if m["tipo"] == "gasto"][::-1][:20]
    if ultimos:
        elegido = st.selectbox(
            "Gasto",
            ultimos,
            format_func=lambda x: f"{x[1]['fecha_hora'][:16]} - {x[1]['descripcion']} - "
                                  f"{pesos(float(x[1]['monto']))} - {x[1]['categoria']}",
        )
        nueva = st.selectbox("Categoría correcta", CATEGORIAS)
        if st.button("Corregir"):
            indice, mov = elegido
            corregir_categoria(indice, nueva)
            guardar_correccion(mov["descripcion"], nueva)
            st.session_state["aviso"] = (f"Listo. La próxima vez que escribas algo como "
                                         f"'{mov['descripcion']}', lo pondré en {nueva}.")
            st.rerun()
    else:
        st.info("Todavía no hay gastos para corregir.")

    st.subheader("Gastos registrados")
    gastos = [m for m in movimientos if m["tipo"] == "gasto"]
    if gastos:
        st.dataframe(gastos)
    else:
        st.info("Todavía no has registrado gastos.")

# --- Pestaña Ahorro ---
with tab_ahorro:
    st.subheader("Tu meta de ahorro mensual")
    meta = perfil.get("meta_ahorro_mensual", 0)
    st.metric("Meta actual", pesos(meta))

    nueva_meta = st.number_input(
        "Cambiar mi meta de ahorro mensual",
        min_value=0,
        step=10000,
        value=int(meta),
    )
    if st.button("Guardar meta"):
        perfil["meta_ahorro_mensual"] = nueva_meta
        guardar_perfil(perfil)
        st.session_state["aviso"] = "Meta de ahorro actualizada"
        st.rerun()

    st.caption("La meta de ahorro se descuenta de tu presupuesto disponible.")