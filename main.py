import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)

df6 = pd.read_csv("datasets/Internet_Accesos-por-tecnologia.csv")
df11 = pd.read_csv("datasets/Internet_Penetracion.csv")

df6 = df6.dropna()
df11 = df11.drop(columns=["Unnamed: 4", "Unnamed: 5", "Unnamed: 6"])
df11["Accesos por cada 100 hogares"] = df11["Accesos por cada 100 hogares"].str.replace(',', '.').astype(float)

st.title("Conexiones de Internet en Provincias de Argentina")

provincia = st.selectbox("Selecciona una provincia:", df6["Provincia"].unique())

filtro6 = df6[df6["Provincia"] == provincia].iloc[::-1]

fig, ax = plt.subplots(figsize=(12, 6))

conexiones = ["ADSL", "Cablemodem", "Fibra óptica", "Wireless", "Otros"]
for conexion in conexiones:
    ax.plot(
        [f"Año {a}, Trim {t}" for a, t in zip(filtro6["Año"], filtro6["Trimestre"])],
        filtro6[conexion],
        marker="o",
        linestyle="-",
        label=conexion
    )

ax.set_xlabel("Trimestre")
ax.set_ylabel("Cantidad de Conexiones")
ax.set_title(f"Conexiones en {provincia} a lo largo del tiempo")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.grid(True)

plt.legend()

st.pyplot(fig)

st.title(f"Accesos cada 100 hogares")

año = st.selectbox("Selecciona el Año", df11["Año"].unique())
trimestre = st.selectbox("Selecciona el Trimestre", df11["Trimestre"].unique())

df_trimestre_ano = df11[(df11["Año"] == año) & (df11["Trimestre"] == trimestre)]
df_trimestre_ano = df_trimestre_ano.sort_values(by="Accesos por cada 100 hogares", ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="Provincia", y="Accesos por cada 100 hogares", data=df_trimestre_ano, ax=ax)
ax.set_xlabel("Provincia")
ax.set_ylabel("Accesos por cada 100 hogares")
ax.set_title(f"Accesos en el Trimestre {trimestre}, {año}")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.grid(axis="y")

st.pyplot(fig)


st.title("Aumento del Acceso a Internet por cada 100 hogares")

provincias = df11["Provincia"].unique()
provincia_seleccionada = st.selectbox("Selecciona una provincia", provincias)

df_filtrado = df11[df11["Provincia"] == provincia_seleccionada]

trimestre = st.slider("Trimestre", 1, 4, 1)
trimestres = list(range(1, trimestre + 1))

acceso_base = df_filtrado[df_filtrado["Trimestre"].isin(trimestres)]["Accesos por cada 100 hogares"].values[0]

aumento = 2.0
acceso_actual = acceso_base + (trimestre - 1) * (aumento / 100) * acceso_base
nuevo_acceso = acceso_base + (trimestre * (aumento / 100)) * acceso_base

plt.figure(figsize=(8, 6))
plt.bar(["Acceso Base", f"Trimestre {trimestre}"], [acceso_base, nuevo_acceso], color=["blue", "green"])
plt.xlabel("Categorías")
plt.ylabel("Acceso por cada 100 hogares")
plt.title(f"Acceso a Internet en el Trimestre {trimestre} en {provincia_seleccionada}")
plt.xticks(rotation=0)

st.pyplot()