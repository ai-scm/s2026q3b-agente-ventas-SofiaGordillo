import streamlit as st
import pandas as pd

from app.graph import ask_sales_agent
from app.visualizations import create_chart
from app.exports import export_csv, export_excel


st.set_page_config(
    page_title="Sales AI Agent",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sales AI Agent")
st.subheader("Asistente inteligente para el análisis de ventas")

st.markdown(
    """
    Realiza preguntas sobre las ventas utilizando lenguaje natural.
    El agente consultará los datos de MySQL mediante Amazon Bedrock,
    LangGraph y MCP.
    """
)

if "resultado" not in st.session_state:
    st.session_state.resultado = None

with st.form("formulario_pregunta"):
    pregunta = st.text_input(
        "¿Qué deseas saber sobre las ventas?",
        placeholder="Ej.: ¿Cuáles son los productos más vendidos en Medellín?",
    )

    consultar = st.form_submit_button(
        "Consultar ventas",
        type="primary",
    )

if consultar:
    if not pregunta.strip():
        st.warning("Escribe una pregunta antes de consultar.")
    else:
        with st.spinner("Analizando la pregunta y consultando las ventas..."):
            try:
                st.session_state.resultado = ask_sales_agent(
                    pregunta.strip()
                )
            except Exception:
                st.session_state.resultado = {
                    "response": (
                        "No fue posible completar la consulta. "
                        "Verifica la conexión con AWS y MySQL."
                    ),
                    "results": [],
                    "sql": "",
                    "error": "Error al procesar la consulta.",
                }

resultado = st.session_state.resultado

if resultado:
    st.divider()
    st.header("Resultados")

    if resultado.get("error"):
        st.error(resultado["response"])

    else:
        st.success(resultado["response"])

        filas = resultado.get("results", [])

        if filas:
            df = pd.DataFrame(filas)

            # Convertir columnas numéricas recibidas como texto.
            for columna in df.columns:
                convertido = pd.to_numeric(
                    df[columna],
                    errors="coerce",
                )

                if convertido.notna().all():
                    df[columna] = convertido

            st.subheader("Datos encontrados")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            # Gráfico interactivo.
            grafico = create_chart(df)

            if grafico is not None:
                st.subheader("Visualización interactiva")
                st.plotly_chart(
                    grafico,
                    use_container_width=True,
                )
            else:
                st.info(
                    "No hay suficientes columnas categóricas y numéricas "
                    "para generar un gráfico."
                )

            # Exportaciones.
            st.subheader("Descargar resultados")

            col_csv, col_excel = st.columns(2)

            with col_csv:
                st.download_button(
                    label="Descargar CSV",
                    data=export_csv(df),
                    file_name="resultados_ventas.csv",
                    mime="text/csv",
                )

            with col_excel:
                st.download_button(
                    label="Descargar Excel",
                    data=export_excel(df),
                    file_name="resultados_ventas.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                )

        else:
            st.info(
                "La consulta no devolvió registros para mostrar."
            )

        with st.expander("Ver consulta SQL generada"):
            st.code(
                resultado.get("sql", "No se generó SQL."),
                language="sql",
            )