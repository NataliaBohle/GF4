# Reorganizado para incluir el nuevo sistema de navegación con fichas técnicas
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("data_proyectos_10porpais.csv")

df = load_data()

# Mapeo para nombre en mapa
df["Nombre País"] = df["País"].map({
    "🇨🇱 Chile": "Chile",
    "🇵🇪 Perú": "Peru",
    "🇦🇷 Argentina": "Argentina",
    "🇵🇾 Paraguay": "Paraguay",
    "🇺🇾 Uruguay": "Uruguay",
    "🇧🇷 Brasil": "Brazil",
    "🇨🇴 Colombia": "Colombia",
    "🇰🇷 Costa Rica": "Costa Rica",
    "🇪🇨 Ecuador": "Ecuador",
    "🇲🇽 México": "Mexico"
})

# --- SIDEBAR ---
st.sidebar.title("📚 Navegación")
seccion = st.sidebar.radio("Selecciona vista:", ["Dashboard", "Ficha Técnica"])

if seccion == "Dashboard":
    st.sidebar.markdown("### Filtros")
    paises = st.sidebar.multiselect("🌎 País", df["País"].unique())
    tipos = st.sidebar.multiselect("⚡ Tipo de Proyecto", df["Tipo de Proyecto"].unique())
    rango_ingreso = st.sidebar.slider("🗕️ Año de Ingreso", int(df["Año Ingreso Evaluación"].min()), int(df["Año Ingreso Evaluación"].max()), (2015, 2023))
    rango_aprobacion = st.sidebar.slider("🗕️ Año de Aprobación", int(df["Año Aprobación Proyecto"].min()), int(df["Año Aprobación Proyecto"].max()), (2016, 2024))

    # Filtro
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

elif seccion == "Ficha Técnica":
    pais_ficha = st.sidebar.selectbox("📄 Elige un país", [
        "Chile", "Perú", "Argentina", "Paraguay", "Uruguay",
        "Brasil", "Colombia", "Costa Rica", "Ecuador", "México"
    ])

# --- PÁGINA PRINCIPAL ---
if seccion == "Dashboard":
    st.title("🌎 Transición Energética Justa en América Latina y el Caribe")
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
    st.subheader("Grupo Focal 4. REDALSEIA 2025")
    
    st.markdown("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus sodales mi non enim facilisis, 
    vitae lacinia lorem euismod. In volutpat porta sapien, condimentum consectetur ante varius in. Cras ac nulla 
    sed nibh sodales pharetra. Quisque ultrices porttitor ex et lacinia. Nulla tempus metus sed bibendum tincidunt. 
    Aliquam lacinia scelerisque facilisis. Vivamus vulputate molestie velit, nec blandit est vehicula a. Ut bibendum 
    augue ut dui sollicitudin, tristique luctus ipsum mollis. Vivamus nec tellus nisi. Quisque sed rutrum quam. 
    Proin sit amet tristique lacus. Mauris aliquet molestie velit id egestas. Donec sed lectus eget mauris varius 
    sodales. Cras dui lacus, pulvinar id.
    """)
    
    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
    
    
    st.markdown(" ")  # o st.text(" ")
    # KPIs
    st.subheader("🔢 Indicadores Principales*")
    st.markdown("""
    * Estos indicadores no son representativos de la totalidad de proyectos de cada país. Corresponden a los
    proyectos enviados por cada país para realizar el panel de datos y el análisis objetivo del grupo focal.
    """)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Proyectos", len(df_filtrado))
    col2.metric("Capacidad Total (MW)", round(df_filtrado["Energía Generada (MW)"].sum(), 1))
    col3.metric("Prom. Energía por Proyecto", round(df_filtrado["Energía Generada (MW)"].mean(), 1))
    
    
    # MAPA COMPLETO LATAM
    st.subheader("🗺️ Generación Total por País (MW)")
    # Lista completa de países latinoamericanos
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
        st.markdown("### Tipos de Proyecto (con íconos)")
    
        # Contar y mapear íconos
        tipo_counts = df_filtrado["Tipo de Proyecto"].value_counts().reset_index()
        tipo_counts.columns = ["Tipo", "Cantidad"]
    
        iconos = {
            "Solar": "Solar ☀️",
            "Eólico": "Eólica 🌀",
            "Mini Hidroeléctrica": "Mini Hidro💧",
            "Hidrógeno verde": "H2V🧪",
            "Biomasa": "Biomasa🌿"
        }
    
        tipo_counts["Ícono"] = tipo_counts["Tipo"].map(iconos)
    
        # Gráfico de barras horizontales
        fig_barh = px.bar(
            tipo_counts.sort_values("Cantidad"),
            x="Cantidad",
            y="Ícono",
            orientation="h",
            labels={"Cantidad": "Cantidad de proyectos", "Ícono": "Tipo"},
            title="Cantidad de proyectos por tipo"
        )
    
        st.plotly_chart(fig_barh, use_container_width=True)
    
    
    
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
        df_mit = mit.value_counts()
        fig3a = px.bar(
            x=df_mit.index,
            y=df_mit.values,
            labels={"x": "Medida", "y": "Frecuencia"},
            title="Medidas de Mitigación"
        )
        st.plotly_chart(fig3a, use_container_width=True)
    
        st.markdown("#### ♻️ Medidas de Compensación")
        comp = df_filtrado["Medidas de Compensación"].str.split(", ").explode()
        df_comp = comp.value_counts()
        fig3b = px.bar(
            x=df_comp.index,
            y=df_comp.values,
            labels={"x": "Medida", "y": "Frecuencia"},
            title="Medidas de Compensación"
        )
        st.plotly_chart(fig3b, use_container_width=True)
    
        st.markdown("#### 🧱 Medidas de Reparación")
        rep = df_filtrado["Medidas de Reparación"].str.split(", ").explode()
        df_rep = rep.value_counts()
        fig3c = px.bar(
            x=df_rep.index,
            y=df_rep.values,
            labels={"x": "Medida", "y": "Frecuencia"},
            title="Medidas de Reparación"
        )
        st.plotly_chart(fig3c, use_container_width=True)
    
    # GRÁFICO DE LÍNEAS POR AÑO
    st.subheader("📈 Evolución Anual de Energía Generada por Proyectos")
    
    df_linea = df_filtrado.copy()
    
    # Agrupar energía por año de ingreso y aprobación
    energia_ingreso = df_linea.groupby("Año Ingreso Evaluación")["Energía Generada (MW)"].sum().reset_index()
    energia_aprobacion = df_linea.groupby("Año Aprobación Proyecto")["Energía Generada (MW)"].sum().reset_index()
    
    energia_ingreso["Tipo"] = "Ingreso"
    energia_aprobacion["Tipo"] = "Aprobación"
    energia_ingreso = energia_ingreso.rename(columns={"Año Ingreso Evaluación": "Año"})
    energia_aprobacion = energia_aprobacion.rename(columns={"Año Aprobación Proyecto": "Año"})
    
    # Combinar ambos
    df_tendencia = pd.concat([energia_ingreso, energia_aprobacion])
    
    fig_linea = px.line(
        df_tendencia,
        x="Año",
        y="Energía Generada (MW)",
        color="Tipo",
        markers=True,
        labels={"Energía Generada (MW)": "MW generados"},
        title="Energía generada por año de ingreso y aprobación"
    )
    
    st.plotly_chart(fig_linea, use_container_width=True)
    
    st.subheader("📊 Tiempo entre ingreso y aprobación")
    
    df_scatter = df_filtrado.copy()
    df_scatter["Años entre ingreso y aprobación"] = df_scatter["Año Aprobación Proyecto"] - df_scatter["Año Ingreso Evaluación"]
    
    fig_scatter = px.scatter(
        df_scatter,
        x="Año Ingreso Evaluación",
        y="Años entre ingreso y aprobación",
        color="Tipo de Proyecto",
        size="Energía Generada (MW)",
        hover_name="Proyecto",
        title="Retraso en aprobación por año de ingreso"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    #tipo/pais
    # Paleta más armónica por tipo
    color_map = {
        "Solar": "#F4D06F",        # amarillo suave
        "Eólico": "#90BEDE",       # celeste claro
        "Mini Hidroeléctrica": "#B5EAD7",  # verde agua
        "Hidrógeno Verde": "#FFDAC1",      # salmón suave
        "Biomasa": "#C7CEEA"       # lavanda claro
    }
    
    fig_treemap = px.treemap(
        df_filtrado,
        path=["País", "Tipo de Proyecto"],
        values="Energía Generada (MW)",
        color="Tipo de Proyecto",
        color_discrete_map=color_map,
        title="Participación de tipos de proyecto por país (en MW)"
    )
    st.plotly_chart(fig_treemap, use_container_width=True)
    
    
    st.subheader("🔥 Impactos Ambientales por Tipo de Proyecto (Heatmap)")
    
    # Separar múltiples impactos
    df_heat = df_filtrado.copy()
    df_heat = df_heat.assign(Impactos=df_heat["Impactos Ambientales"].str.split(", "))
    df_heat = df_heat.explode("Impactos")
    df_heat["Impactos"] = df_heat["Impactos"].str.strip()
    
    # Agrupar
    tabla_heat = df_heat.groupby(["Tipo de Proyecto", "Impactos"]).size().reset_index(name="Frecuencia")
    
    # Solo mostrar los 10 impactos más comunes para claridad
    top_impactos = tabla_heat.groupby("Impactos")["Frecuencia"].sum().nlargest(10).index
    tabla_heat = tabla_heat[tabla_heat["Impactos"].isin(top_impactos)]
    
    # Gráfico
    fig_heat = px.density_heatmap(
        tabla_heat,
        x="Impactos",
        y="Tipo de Proyecto",
        z="Frecuencia",
        color_continuous_scale="YlOrBr",
        title="Top 10 Impactos Ambientales por Tipo de Proyecto"
    )
    fig_heat.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig_heat, use_container_width=True)
    
    
    # TABLA DETALLE
    st.subheader("📋 Detalle de Proyectos")
    st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
elif seccion == "Ficha Técnica":
    if pais_ficha == "Chile":
        st.title("🇨🇱 Ficha Técnica - Chile")
        st.subheader("Perfil Energético")
        st.markdown("""
        - **Matriz renovable:** 62% (2023)
        - **Capacidad solar:** 6.000 MW
        - **Capacidad eólica:** 4.000 MW
        - **Proyectos H2V en curso:** 7
        - **Desafíos:** escasez hídrica en zonas críticas, conexión SIC/SING
        """)
        st.subheader("Principales Proyectos")
        st.markdown("""
        - Parque Solar Atacama (250 MW)
        - Parque Eólico Llanos del Viento (180 MW)
        - Proyecto H2 Magallanes (60 MW electrólisis)
        """)
    else:
        st.title(f"Ficha Técnica - {pais_ficha}")
        st.info("Esta ficha técnica está en construcción. Pronto estará disponible.")
