import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==============================================================================
st.set_page_config(
    page_title="PrevenSalud IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado para tarjetas y métricas
st.markdown("""
    <style>
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #1E3A8A;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Header principal
st.title("🏥 PREVENSALUD IA")
st.caption("Plataforma Inteligente de Analítica Predictiva y Gestión Operativa Hospitalaria")

# ==============================================================================
# 2. CARGA Y LIMPIEZA DE DATOS
# ==============================================================================
@st.cache_data
def cargar_datos_disco():
    try:
        return pd.read_excel("PrevenSalud IA Dataset.xlsx")
    except Exception:
        return None

df_raw = cargar_datos_disco()

# --- BARRA LATERAL (SIDEBAR ENRIQUECIDO) ---
st.sidebar.header("⚙️ Configuración y Filtros")

# Carga manual opcional desde la barra lateral
archivo_subido = st.sidebar.file_uploader("📁 Actualizar/Cargar Dataset (Excel)", type=["xlsx"])

if archivo_subido is not None:
    df = pd.read_excel(archivo_subido)
elif df_raw is not None:
    df = df_raw.copy()
else:
    st.info("👋 **Bienvenido a PrevenSalud IA**")
    st.warning("Cargue un archivo Excel mediante el panel izquierdo para comenzar.")
    st.stop()

# Limpieza de nombres de columnas
df.columns = df.columns.str.strip()

# Convertir columnas numéricas clave
for col_num in ['Edad', 'Días estancia', 'Dias estancia']:
    if col_num in df.columns:
        df[col_num] = pd.to_numeric(df[col_num], errors='coerce')

# Procesamiento de fechas
col_fecha = None
for col in df.columns:
    if col.lower() in ['f. ingreso', 'ingreso', 'fecha']:
        col_fecha = col
        break

if col_fecha:
    df['Fecha_Procesada'] = pd.to_datetime(df[col_fecha], errors='coerce')
    df['Mes'] = df['Fecha_Procesada'].dt.month_name()

# --- FILTROS DINÁMICOS EN SIDEBAR ---
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros de Segmentación")

# Filtro 1: Servicio
if 'Servicio actual' in df.columns:
    servicios = ["Todos"] + sorted(list(df['Servicio actual'].dropna().unique()))
    serv_sel = st.sidebar.selectbox("Filtrar por Servicio", servicios)
    if serv_sel != "Todos":
        df = df[df['Servicio actual'] == serv_sel]

# Filtro 2: Aseguradora
if 'Aseguradora' in df.columns:
    aseguradoras = ["Todas"] + sorted(list(df['Aseguradora'].dropna().unique()))
    aseg_sel = st.sidebar.selectbox("Filtrar por Aseguradora", aseguradoras)
    if aseg_sel != "Todas":
        df = df[df['Aseguradora'] == aseg_sel]

# Informador de registros tras filtrar
st.sidebar.markdown("---")
st.sidebar.metric("Registros Filtrados", len(df))

# ==============================================================================
# 3. ESTRUCTURA DE PESTAÑAS INTERACTIVAS
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Tablero Control (KPIs)", 
    "🔮 Simulador Predictivo IA", 
    "🏥 Gestión de Capacidad y Servicios", 
    "📁 Base de Datos Consolidada"
])

# ------------------------------------------------------------------------------
# PESTAÑA 1: DASHBOARD DE CONTROL
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("📈 Resumen Ejecutivo y Capacidades Operativas")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pacientes Activos/Registrados", f"{len(df):,}")
    
    col_estancia = 'Días estancia' if 'Días estancia' in df.columns else ('Dias estancia' if 'Dias estancia' in df.columns else None)
    if col_estancia and df[col_estancia].notna().any():
        col2.metric("Promedio Días Estancia", f"{df[col_estancia].mean():.1f} días")
    else:
        col2.metric("Promedio Días Estancia", "N/A")
        
    if 'Edad' in df.columns and df['Edad'].notna().any():
        col3.metric("Promedio Edad Pacientes", f"{df['Edad'].mean():.1f} años")
    else:
        col3.metric("Promedio Edad Pacientes", "N/A")
        
    if 'Servicio actual' in df.columns:
        col4.metric("Servicios Activos Muestreados", f"{df['Servicio actual'].nunique()}")
    else:
        col4.metric("Servicios Activos", "N/A")
        
    st.markdown("---")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        if 'Diagnóstico actual' in df.columns:
            st.markdown("**Top 10 Diagnósticos de Mayor Frecuencia**")
            top_diag = df['Diagnóstico actual'].value_counts().head(10).reset_index()
            top_diag.columns = ['Diagnóstico', 'Cantidad']
            fig_diag = px.bar(top_diag, x='Cantidad', y='Diagnóstico', orientation='h', color='Cantidad', color_continuous_scale='Blues')
            st.plotly_chart(fig_diag, use_container_width=True)
            
    with col_g2:
        if 'Servicio actual' in df.columns:
            st.markdown("**Distribución Porcentual por Servicio Hospitalario**")
            serv_dist = df['Servicio actual'].value_counts().reset_index()
            serv_dist.columns = ['Servicio', 'Cantidad']
            fig_serv = px.pie(serv_dist, names='Servicio', values='Cantidad', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_serv, use_container_width=True)

# ------------------------------------------------------------------------------
# PESTAÑA 2: SIMULADOR PREDICTIVO DE DEMANDA (IA)
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("🔮 Estimación de Afluencia e Índice de Ocupación por IA")
    st.write("Ajuste los parámetros operativos para simular el comportamiento de demanda proyectado:")
    
    c_sim1, c_sim2, c_sim3 = st.columns(3)
    
    with c_sim1:
        medicos_input = st.number_input("Médicos Programados en Turno", min_value=1, max_value=50, value=6)
        enfermeros_input = st.number_input("Enfermeros/Asistentes", min_value=1, max_value=80, value=12)
        
    with c_sim2:
        camas_totales = st.number_input("Camas Totales en Area", min_value=10, max_value=300, value=50)
        camas_ocupadas = st.number_input("Camas Ocupadas Actules", min_value=0, max_value=300, value=35)
        
    with c_sim3:
        jornada = st.selectbox("Turno Operativo", ["Mañana", "Tarde", "Noche"])
        clima = st.selectbox("Condición Climatológica", ["Normal", "Lluvia Moderada", "Lluvia Intensa"])

    if st.button("🚀 Calcular Proyección y Riesgo de Saturación", type="primary"):
        # Cálculo de simulación basada en reglas heurísticas / ponderaciones
        factor_jornada = 1.3 if jornada == "Noche" else (1.1 if jornada == "Tarde" else 1.0)
        factor_clima = 1.25 if clima == "Lluvia Intensa" else (1.1 if clima == "Lluvia Moderada" else 1.0)
        
        estimacion_llegadas = int((medicos_input * 2.5 + enfermeros_input * 1.2) * factor_jornada * factor_clima)
        ocupacion_proyectada = min(100.0, ((camas_ocupadas + (estimacion_llegadas * 0.4)) / camas_totales) * 100)
        
        st.markdown("---")
        st.markdown("### Resultados del Modelo de Simulación")
        
        res1, res2 = st.columns(2)
        
        with res1:
            st.metric("Estimación de Pacientes Esperados (Próx. Turno)", f"{estimacion_llegadas} pacientes")
            st.metric("Ocupación Proyectada de Camas", f"{ocupacion_proyectada:.1f}%")
            
        with res2:
            if ocupacion_proyectada < 75:
                st.success("🟢 **NIVEL DE RIESGO: BAJO**\n\nCapacidad holgada. Flujo operativo dentro de parámetros normales.")
            elif ocupacion_proyectada < 90:
                st.warning("🟡 **NIVEL DE RIESGO: MODERADO**\n\nAlta ocupación. Se sugiere agilizar procesos de alta y traslado.")
            else:
                st.error("🔴 **NIVEL DE RIESGO: CRÍTICO / SATURACIÓN**\n\nRiesgo alto de sobrecupo. Activar protocolo de contingencia hospitalario.")

# ------------------------------------------------------------------------------
# PESTAÑA 3: GESTIÓN DE CAPACIDAD Y SERVICIOS
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("🏥 Análisis Operativo de Aseguradoras y Especialidades")
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        if 'Aseguradora' in df.columns:
            st.markdown("**Pacientes por Aseguradora / Convenio EPS**")
            aseg_dist = df['Aseguradora'].value_counts().head(10).reset_index()
            aseg_dist.columns = ['Aseguradora', 'Pacientes']
            fig_aseg = px.bar(aseg_dist, x='Pacientes', y='Aseguradora', orientation='h', color='Pacientes', color_continuous_scale='Viridis')
            st.plotly_chart(fig_aseg, use_container_width=True)
            
    with col_s2:
        if 'Especialidad' in df.columns:
            st.markdown("**Distribución por Especialidad Médica**")
            esp_dist = df['Especialidad'].value_counts().head(10).reset_index()
            esp_dist.columns = ['Especialidad', 'Pacientes']
            fig_esp = px.pie(esp_dist, names='Especialidad', values='Pacientes', color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_esp, use_container_width=True)

# ------------------------------------------------------------------------------
# PESTAÑA 4: EXPLORADOR DE DATOS Y DESCARGA
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("📁 Registros Hospitalarios Filtrados")
    st.write("A continuación se presentan los registros activos según los filtros seleccionados en la barra lateral:")
    st.dataframe(df, use_container_width=True)