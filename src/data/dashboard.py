# dashboard_streamlit.py
import streamlit as st
import matplotlib.pyplot as plt
from datetime import date

# Importar clases desde los módulos
from var_cvar import var_cvar
import io

# -------------------------------------------------------------------
# Configuración general de la app
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Financiero - VaR & CVaR",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Dashboard de Análisis Financiero")
st.markdown(
    "Este panel permite analizar rendimientos, pruebas de normalidad y el cálculo del VaR y CVaR para activos seleccionados."
)

# -------------------------------------------------------------------
# Entradas de usuario
# -------------------------------------------------------------------
st.sidebar.header("Configuración del análisis")

empresas = st.sidebar.text_input(
    "Ingrese los símbolos (separados por comas)", "BND,TSLA,AAPL,MSFT,GOOG,SPY,BTC-USD"
).split(",")

empresas = [e.strip().upper() for e in empresas if e.strip() != ""]

fecha_inicio = st.sidebar.date_input("Fecha de inicio AA/MM/DD", date(2022, 1, 1))
fecha_fin = st.sidebar.date_input("Fecha de fin AA/MM/DD", date.today())


# alpha = st.sidebar.slider("Nivel de significancia (α)", 0.0, 0.50, 0.001)
conf = st.sidebar.slider("Nivel de confianza para VaR/CVaR", 0.9, 0.99, 0.05)


# Inicialización de objetos

try:
    st.info("Descargando datos con `yfinance`...")
    modelo = var_cvar(empresas, str(fecha_inicio), str(fecha_fin), alpha=0.0, conf=conf)
    st.success("Datos descargados correctamente")
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# -------------------------------------------------------------------
# Selección de empresa y análisis
# -------------------------------------------------------------------
empresa = st.selectbox("Seleccione una empresa:", empresas)
analisis = st.radio(
    "Seleccione el tipo de análisis:",
    ["Visualizar datos", "Test de Normalidad", "VaR y CVaR (Normal)"],
)

# -------------------------------------------------------------------
# Visualizaciones según selección
# -------------------------------------------------------------------
if analisis == "Visualizar datos":
    st.subheader(f"Rendimientos de {empresa}")
    try:
        modelo.graficar_rendimientos(empresa)
        st.pyplot(plt.gcf())
    except Exception as e:
        st.error(f"No fue posible generar la gráfica: {e}")

elif analisis == "Test de Normalidad":
    st.subheader(f"Prueba de Normalidad - {empresa}")
    try:
        modelo.normalidad(empresa, graficar=True)
        st.pyplot(plt.gcf())
    except Exception as e:
        st.error(f"No fue posible generar la gráfica: {e}")

elif analisis == "VaR y CVaR (Normal)":
    st.subheader(f"Cálculo de VaR y CVaR - {empresa}")
    try:
        resultados = modelo.var_cvar_normal(empresa, graficar=True)
        st.pyplot(plt.gcf())
        # st.markdown(f"**VaR ({conf*100:.1f}%):** {resultados['VaR']:.4f}")
        st.latex(f"VaR({conf * 100:.1f}\%) = {resultados['VaR']:.4f}")
        # st.markdown(f"**CVaR ({conf*100:.1f}%):** {resultados['CVaR']:.4f}")
        st.latex(f"CVaR ({conf * 100:.1f}\%)= {resultados['CVaR']:.4f}")
    except Exception as e:
        st.error(f"No fue posible calcular VaR/CVaR: {e}")

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    st.download_button(
        label="Descargar Gráfico",
        data=buffer,
        file_name=f"{empresa}_{analisis}.png",
        mime="image/png",
    )


# -------------------------------------------------------------------
# Pie de página
# -------------------------------------------------------------------
st.markdown("---")
