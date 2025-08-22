import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título
st.title("📊 Dashboard de Ventas")

# Datos de ejemplo
data = {
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo"],
    "Ventas": [120, 150, 90, 200, 170]
}
df = pd.DataFrame(data)

# Mostrar tabla
st.subheader("Tabla de ventas")
st.dataframe(df)

# Gráfico
st.subheader("Gráfico de ventas")
fig, ax = plt.subplots()
ax.plot(df["Mes"], df["Ventas"], marker="o")
st.pyplot(fig)

# Filtro
st.subheader("Filtro")
mes = st.selectbox("Selecciona un mes:", df["Mes"])
ventas_mes = df[df["Mes"] == mes]["Ventas"].values[0]
st.write(f"🔎 Ventas en {mes}: **{ventas_mes}**")