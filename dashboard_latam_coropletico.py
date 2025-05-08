
import streamlit as st
import pandas as pd
import plotly as pl
import plotly.express as px

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("data_proyectos_10porpais.csv")

df = load_data()

# Agregar nombre estándar del país para mapas
df["Nombre País"] = df["País"].map({
    "🇨🇱 Chile": "Chile",
    "🇵🇪 Perú": "Peru",
    "🇦🇷 Argentina": "Argentina",
    "🇵🇾 Paraguay": "Paraguay",
    "🇺🇾 Uruguay": "Uruguay",
    "🇧🇷 Brasil": "Brazil",
    "🇨🇴 Colombia": "Colombia",
    "🇨🇷 Costa Rica": "Costa Rica",
    "🇪🇨 Ecuador": "Ecuador",
    "🇲🇽 México": "Mexico"
})

# SIDEBAR
st.sidebar.title("Filtros")
paises = st.sidebar.multiselect("🌎 País", df["País"].unique())
tipos = st.sidebar.multiselect("⚡ Tipo de Proyecto", df["Tipo de Proyecto"].unique())
rango_ingreso = st.sidebar.slider("📅 Año de Ingreso", int(df["Año Ingreso Evaluación"].min()), int(df["Año Ingreso Evaluación"].max()), (2015, 2023))
rango_aprobacion = st.sidebar.slider("📅 Año de Aprobación", int(df["Año Aprobación Proyecto"].min()), int(df["Año Aprobación Proyecto"].max()), (2016, 2024))

# Filtrado de datos
df_filtrado = df.copy()
if paises:
    df_filtrado = df_filtrado[df_filtrado["País"].isin(paises)]
if tipos:
    df_filtrado = df_filtrado[df_filtrado["Tipo de Proyecto"].isin(tipos)]

df_filtrado = df_filtrado[
    (df_filtrado["Año Ingreso Evaluación"] >= rango_ingreso[0]) & 
    (df_filtrado["Año Ingreso Evaluación"] <= rango_ingreso[1]) & 
    (df_filtrado["Año Aprobación Proyecto"] >= rango_aprobacion[0]) & 
    (df_filtrado["Año Aprobación Proyecto"] <= rango_aprobacion[1])
]

# TÍTULO PRINCIPAL
st.title("🌎 Dashboard de Proyectos de Transición Energética en LATAM")

# KPIs
st.subheader("🔢 Indicadores Principales")
col1, col2, col3 = st.columns(3)
col1.metric("Total Proyectos", len(df_filtrado))
col2.metric("Capacidad Total (MW)", round(df_filtrado["Energía Generada (MW)"].sum(), 1))
col3.metric("Prom. Energía por Proyecto", round(df_filtrado["Energía Generada (MW)"].mean(), 1))

# MAPA COROPLÉTICO
st.subheader("🗺️ Generación Total por País (MW)")
df_summary = df_filtrado.groupby("Nombre País")["Energía Generada (MW)"].sum().reset_index()
fig_map = px.choropleth(
    df_summary,
    locations="Nombre País",
    locationmode="country names",
    color="Energía Generada (MW)",
    hover_name="Nombre País",
    color_continuous_scale="Viridis",
    title="Generación Total de Energía por País (MW)",
    scope="south america"
)
fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# GRÁFICOS
st.subheader("📊 Análisis de Proyectos")
tab1, tab2, tab3 = st.tabs(["Tipo de Proyecto", "Impactos Ambientales", "Medidas Aplicadas"])

with tab1:
    fig1 = px.histogram(df_filtrado, x="Tipo de Proyecto", color="Tipo de Proyecto", title="Distribución por tipo")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    all_impactos = df_filtrado["Impactos Ambientales"].str.split(", ").explode()
    df_impactos = all_impactos.value_counts().reset_index()
    df_impactos.columns = ["Impacto", "Frecuencia"]

    fig2 = px.histogram(df_impactos,
                        x="Impacto", y="Frecuencia",
                        labels={"Impacto": "Impacto Ambiental", "Frecuencia": "Cantidad"},
                        title="Impactos Ambientales más Frecuentes")
    st.plotly_chart(fig2, use_container_width=True)


with tab3:
    medidas = pd.concat([
        df_filtrado["Medidas de Mitigación"].str.split(", ").explode(),
        df_filtrado["Medidas de Compensación"].str.split(", ").explode(),
        df_filtrado["Medidas de Reparación"].str.split(", ").explode()
    ])
    fig3 = px.histogram(medidas.value_counts().reset_index(),
                        x="index", y="count", labels={"index": "Medida", "count": "Frecuencia"},
                        title="Medidas Ambientales aplicadas")
    st.plotly_chart(fig3, use_container_width=True)

# DETALLE DE PROYECTOS
st.subheader("📋 Detalle de Proyectos")
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
