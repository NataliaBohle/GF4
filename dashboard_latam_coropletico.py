
import streamlit as st
import pandas as pd
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

# Filtrado
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

# TÍTULO Y BANDERAS
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

# MAPA COMPLETO LATAM
st.subheader("🗺️ Generación Total por País (MW)")
# Lista completa de países latinoamericanos
latam_paises = [
    "Argentina", "Belize", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica",
    "Cuba", "Dominican Republic", "Ecuador", "El Salvador", "Guatemala", "Honduras",
    "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Uruguay", "Venezuela",
    "Puerto Rico", "Haiti", "Jamaica", "Trinidad and Tobago", "Guyana", "Suriname",
    "French Guiana"
]

# Preparar DataFrame de mapa
df_base = pd.DataFrame({"Nombre País": latam_paises})
df_map = df_base.merge(
    df_filtrado.groupby("Nombre País")["Energía Generada (MW)"].sum().reset_index(),
    on="Nombre País", how="left"
)

# Hover info
df_map["info"] = df_map["Energía Generada (MW)"].apply(
    lambda x: "País no participa de REDLASEIA" if pd.isna(x) else f"{x:.1f} MW"
)

# Colorear gris sin datos
df_map["Energía Generada (MW)"] = df_map["Energía Generada (MW)"].fillna(0)

# Mapa
fig_map = px.choropleth(
    df_map,
    locations="Nombre País",
    locationmode="country names",
    color="Energía Generada (MW)",
    hover_name="Nombre País",
    hover_data={"info": True, "Energía Generada (MW)": False, "Nombre País": False},
    color_continuous_scale=[
        (0.0, "#d3d3d3"),
        (0.00001, "#440154"),
        (0.5, "#21908C"),
        (1.0, "#FDE725")
    ],
    range_color=(0.00001, df_map["Energía Generada (MW)"].max()),
    title="Generación Total de Energía por País (MW)",
    scope="world"
)

fig_map.update_geos(
    fitbounds="locations",
    visible=False,
    lataxis_range=[-60, 33],
    lonaxis_range=[-120, -30]
)
fig_map.update_traces(marker_line_color="black", marker_line_width=0.5)

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
    fig2 = px.histogram(df_impactos, x="Impacto", y="Frecuencia",
                        labels={"Impacto": "Impacto Ambiental", "Frecuencia": "Cantidad"},
                        title="Impactos Ambientales más Frecuentes")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown("#### 🛡️ Medidas de Mitigación")
    mit = df_filtrado["Medidas de Mitigación"].str.split(", ").explode()
    df_mit = mit.value_counts().reset_index()
    df_mit.columns = ["Medida", "Frecuencia"]
    st.dataframe(df_mit, use_container_width=True)

    st.markdown("#### ♻️ Medidas de Compensación")
    comp = df_filtrado["Medidas de Compensacióntest"].str.split(", ").explode()
    df_comp = comp.value_counts().reset_index()
    df_comp.columns = ["Medida", "Frecuencia"]
    st.dataframe(df_comp, use_container_width=True)

    st.markdown("#### 🧱 Medidas de Reparación")
    rep = df_filtrado["Medidas de Reparación"].str.split(", ").explode()
    df_rep = rep.value_counts().reset_index()
    df_rep.columns = ["Medida", "Frecuencia"]
    st.dataframe(df_rep, use_container_width=True)

# TABLA DETALLE
st.subheader("📋 Detalle de Proyectos")
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
