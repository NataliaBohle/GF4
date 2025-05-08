import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("data_proyectos_10porpais.csv")

df = load_data()

# Mapear nombres de países para el mapa
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

# Filtros
st.sidebar.title("Filtros")
paises = st.sidebar.multiselect("🌎 País", df["País"].unique())
tipos = st.sidebar.multiselect("⚡ Tipo de Proyecto", df["Tipo de Proyecto"].unique())
rango_ingreso = st.sidebar.slider("📅 Año de Ingreso", int(df["Año Ingreso Evaluación"].min()), int(df["Año Ingreso Evaluación"].max()), (2015, 2023))
rango_aprobacion = st.sidebar.slider("📅 Año de Aprobación", int(df["Año Aprobación Proyecto"].min()), int(df["Año Aprobación Proyecto"].max()), (2016, 2024))

# Aplicar filtros
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

# Título y banderas
st.title("🌎 Plataforma de datos. Grupo Focal 4. Transición Energética Justa en REDLASEIA")
st.markdown("""
<div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
  <img src="https://flagcdn.com/w40/cl.png" title="Chile" width="30">
  <img src="https://flagcdn.com/w40/pe.png" title="Perú" width="30">
  <img src="https://flagcdn.com/w40/ar.png" title="Argentina" width="30">
  <img src="https://flagcdn.com/w40/py.png" title="Paraguay" width="30">
  <img src="https://flagcdn.com/w40/uy.png" title="Uruguay" width="30">
  <img src="https://flagcdn.com/w40/br.png" title="Brasil" width="30">
  <img src="https://flagcdn.com/w40/co.png" title="Colombia" width="30">
  <img src="https://flagcdn.com/w40/cr.png" title="Costa Rica" width="30">
  <img src="https://flagcdn.com/w40/ec.png" title="Ecuador" width="30">
  <img src="https://flagcdn.com/w40/mx.png" title="México" width="30">
</div>
""", unsafe_allow_html=True)

# KPIs
st.subheader("🔢 Indicadores Principales")
col1, col2, col3 = st.columns(3)
col1.metric("Total Proyectos", len(df_filtrado))
col2.metric("Capacidad Total (MW)", round(df_filtrado["Energía Generada (MW)"].sum(), 1))
col3.metric("Prom. Energía por Proyecto", round(df_filtrado["Energía Generada (MW)"].mean(), 1))

# Mapa coroplético LATAM
st.subheader("🗺️ Generación Total por País (MW)")
latam_paises = [
    "Argentina", "Belize", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica",
    "Cuba", "Dominican Republic", "Ecuador", "El Salvador", "Guatemala", "Honduras",
    "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Uruguay", "Venezuela",
    "Puerto Rico", "Haiti", "Jamaica", "Trinidad and Tobago", "Guyana", "Suriname",
    "French Guiana"
]
df_base = pd.DataFrame({"Nombre País": latam_paises})
df_map = df_base.merge(
    df_filtrado.groupby("Nombre País")["Energía Generada (MW)"].sum().reset_index(),
    on="Nombre País", how="left"
)
fig_map = px.choropleth(
    df_map,
    locations="Nombre País",
    locationmode="country names",
    color="Energía Generada (MW)",
    hover_name="Nombre País",
    color_continuous_scale="Viridis",
    title="Generación Total de Energía por País (MW)",
    scope="world"  # mostrar todo el mundo
)
fig_map.update_geos(
    fitbounds="locations",
    visible=False,
    lataxis_range=[-60, 33],  # restringe a LATAM
    lonaxis_range=[-120, -30]
)
fig_map.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
st.plotly_chart(fig_map, use_container_width=True)

# Gráficos
st.subheader("📊 Análisis de Proyectos")
tab1, tab2, tab3 = st.tabs(["Tipo de Proyecto", "Impactos Ambientales", "Medidas Aplicadas"])

with tab1:
    fig1 = px.histogram(df_filtrado, x="Tipo de Proyecto", color="Tipo de Proyecto", title="Distribución por tipo")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    all_impactos = df_filtrado["Impactos Ambientales"].str.split(", ").explode()
    df_impactos = all_impactos.value_counts().reset_index()
    df_impactos.columns = ["Impacto", "Frecuencia"]
    fig2 = px.histogram(df_impactos, x="Impacto", y="Frecuencia",
                        labels={"Impacto": "Impacto Ambiental", "Frecuencia": "Cantidad"},
                        title="Impactos Ambientales más Frecuentes")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown("#### 🛡️ Medidas de Mitigación")
    mit = df_filtrado["Medidas de Mitigación"].str.split(", ").explode()
    fig3a = px.histogram(mit.value_counts().reset_index(),
                         x="index", y="count", labels={"index": "Medida", "count": "Frecuencia"})
    st.plotly_chart(fig3a, use_container_width=True)

    st.markdown("#### ♻️ Medidas de Compensación")
    comp = df_filtrado["Medidas de Compensación"].str.split(", ").explode()
    fig3b = px.histogram(comp.value_counts().reset_index(),
                         x="index", y="count", labels={"index": "Medida", "count": "Frecuencia"})
    st.plotly_chart(fig3b, use_container_width=True)

    st.markdown("#### 🧱 Medidas de Reparación")
    rep = df_filtrado["Medidas de Reparación"].str.split(", ").explode()
    fig3c = px.histogram(rep.value_counts().reset_index(),
                         x="index", y="count", labels={"index": "Medida", "count": "Frecuencia"})
    st.plotly_chart(fig3c, use_container_width=True)

# Tabla final
st.subheader("📋 Detalle de Proyectos")
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
