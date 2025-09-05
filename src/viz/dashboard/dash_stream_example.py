import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

ruta = (
    "/Users/gara/Desktop/Estadistica_II/grupo-4/src/data/csv/rendimientos_diarios.csv"
)

st.title("Dashboard de ejemplo")

df = pd.read_csv(ruta, sep=";")
df_sin_fecha = df.loc[:, df.columns != "Date"]
##### TABLAS DE DATOS
st.subheader("Tabla de Rendimientos")
st.dataframe(df_sin_fecha)
#####


##### GRAFICAR
st.subheader("Gráfico de rendimientos")
empresa = st.selectbox("Selecciona uns empresa:", df_sin_fecha.columns.tolist())

fig, ax = plt.subplots()

ax.hist(df[empresa], bins=50, color="navy", edgecolor="black")
ax.set_title(f"Rendimientos Diarios de {empresa}")
ax.set_xlabel("Rendimientos diarios")
ax.set_ylabel("Frecuencia")
# ax.set_xlim(-0.2, 0.2)   # Eje X entre 0 y 10
# ax.set_ylim(0, 120)  # Eje Y entre 0 y 100

st.pyplot(fig)
######


###### PARA CREACIÓN DE FILTROS
# st.subheader("Filtro")
# mes = st.selectbox("Selecciona un mes:", df["Mes"])
# ventas_mes = df[df["Mes"] == mes]["Ventas"].values[0]
# st.write(f"🔎 Ventas en {mes}: **{ventas_mes}**")
######
