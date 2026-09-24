import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
from PIL import Image
import os

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==============================================================================
st.set_page_config(
    page_title="PrevenSalud IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado
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

# ==============================================================================
# 2. BARRA LATERAL (LOGO, CARGA Y FILTROS)
# ==============================================================================

# Intentar cargar el logo buscando variantes comunes de nombre
logo_encontrado = False
for nombre_logo in ["logo.png", "logo.jpg", "logo.jpeg", "LOGO.PNG"]:
    if os.path.exists(nombre_logo):
        try:
            imagen_logo = Image.open(nombre_logo)
            st.sidebar.image(imagen_logo, use_container_width=True)
            logo_encontrado = True
            break
        except Exception:
            pass

if not logo_encontrado:
    st.sidebar.title("🏥 PrevenSalud IA")

st.sidebar.header("⚙️ Configuración y Filtros")

# Carga manual opcional de dataset
archivo_subido = st.sidebar.file_uploader("📁 Actualizar Dataset (Excel)", type=["xlsx"])

@st.cache_data
def cargar_datos_disco():
    try:
        return pd.read_excel("PrevenSalud IA Dataset.xlsx")
    except Exception:
        return None

df_raw = cargar_datos_disco()

if archivo_subido is not None:
    df_base = pd.read_excel(archivo_subido)
elif df_raw is not None:
    df_base = df_raw.copy()
else:
    st.info("👋 **Bienvenido a PrevenSalud IA**")
    st.warning("Cargue un archivo Excel para habilitar las funciones.")
    st.stop()

# Limpieza básica
df_base.columns = df_base.columns.str.strip()

for col_num in ['Edad', 'Días estancia', 'Dias estancia']:
    if col_num in df_base.columns:
        df_base[col_num] = pd.to_numeric(df_base[col_num], errors='coerce')

# Procesamiento de fechas robusto
col_fecha = None
columnas_posibles_fecha = ['f. ingreso', 'ingreso', 'fecha', 'f. nacimiento', 'fecha ingreso']

for col in df_base.columns:
    if col.lower().strip() in columnas_posibles_fecha:
        col_fecha = col
        break

if col_fecha:
    # Convertir a datetime y extraer solo la parte de fecha (sin hora)
    df_base['Fecha_Procesada'] = pd.to_datetime(df_base[col_fecha], errors='coerce')
    df_base['Fecha_Solo_Dia'] = df_base['Fecha_Procesada'].dt.date

# Copia de trabajo para aplicar filtros dinámicos
df = df_base.copy()

# --- FILTROS DE SEGMENTACIÓN EN BARRA LATERAL ---
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros Operativos")

if 'Servicio actual' in df.columns:
    servicios = ["Todos"] + sorted(list(df['Servicio actual'].dropna().unique()))
    serv_sel = st.sidebar.selectbox("Servicio Hospitalario", servicios)
    if serv_sel != "Todos":
        df = df[df['Servicio actual'] == serv_sel]

if 'Aseguradora' in df.columns:
    aseguradoras = ["Todas"] + sorted(list(df['Aseguradora'].dropna().unique()))
    aseg_sel = st.sidebar.selectbox("Aseguradora / EPS", aseguradoras)
    if aseg_sel != "Todas":
        df = df[df['Aseguradora'] == aseg_sel]

st.sidebar.markdown("---")
st.sidebar.metric("Registros Filtrados", len(df))

# Header principal
st.title("🏥 PREVENSALUD IA")
st.caption("Plataforma Inteligente de Analítica Predictiva y Gestión Operativa Hospitalaria")

# ==============================================================================
# 3. ESTRUCTURA DE PESTAÑAS
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
# PESTAÑA 2: SIMULADOR PREDICTIVO DE DEMANDA CON ANÁLISIS TEMPORAL
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("🔮 Estimación y Simulación de Demanda (IA)")
    st.write("Seleccione la fecha de consulta para realizar un **análisis histórico** o proyectar la **demanda futura** con parámetros operativos.")
    
    # Obtener fecha por defecto razonable basada en el dataset si existe
    fecha_defecto = date.today()
    if col_fecha and 'Fecha_Solo_Dia' in df_base.columns:
        fechas_validas = df_base['Fecha_Solo_Dia'].dropna()
        if not fechas_validas.empty:
            fecha_defecto = fechas_validas.iloc[0] # Usa la primera fecha del dataset como ejemplo inicial

    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        fecha_evaluar = st.date_input("Fecha a Evaluar", value=fecha_defecto)
    
    hoy = date.today()
    es_futuro = fecha_evaluar > hoy
    
    with col_f2:
        if es_futuro:
            st.info(f"📅 **Modo Proyección Futura (IA):** Evaluando fecha posterior a hoy ({fecha_evaluar.strftime('%d/%m/%Y')}).")
        else:
            st.success(f"📊 **Modo Análisis Histórico:** Evaluando registros pasados o del día actual ({fecha_evaluar.strftime('%d/%m/%Y')}).")
            
    st.markdown("---")
    
    st.markdown("##### ⚙️ Parámetros de Personal y Capacidad")
    c_sim1, c_sim2, c_sim3 = st.columns(3)
    
    with c_sim1:
        medicos_input = st.number_input("Médicos Programados en Turno", min_value=1, max_value=50, value=6)
        enfermeros_input = st.number_input("Enfermeros/Asistentes", min_value=1, max_value=80, value=12)
        
    with c_sim2:
        camas_totales = st.number_input("Camas Totales Disponibles", min_value=10, max_value=300, value=50)
        camas_ocupadas = st.number_input("Camas Ocupadas Actuales", min_value=0, max_value=300, value=35)
        
    with c_sim3:
        jornada = st.selectbox("Turno Operativo", ["Mañana", "Tarde", "Noche"])
        clima = st.selectbox("Condición Climatológica / Externa", ["Normal", "Lluvia Moderada", "Lluvia Intensa", "Pico Epidemiológico"])

    if st.button("🚀 Procesar Evaluación Temporal y Predicción", type="primary"):
        st.markdown("---")
        
        # SI LA FECHA ES PASADA O HOY: Muestra comparación con datos reales del dataset BASE
        if not es_futuro:
            st.markdown(f"### 📋 Evaluación Histórica para {fecha_evaluar.strftime('%d/%m/%Y')}")
            
            if col_fecha and 'Fecha_Solo_Dia' in df_base.columns:
                df_fecha_filtro = df_base[df_base['Fecha_Solo_Dia'] == fecha_evaluar]
                ingresos_reales = len(df_fecha_filtro)
                
                r1, r2, r3 = st.columns(3)
                r1.metric("Ingresos Reales Registrados", f"{ingresos_reales} pacientes")
                
                if col_estancia and ingresos_reales > 0:
                    r2.metric("Promedio Estancia Registrada", f"{df_fecha_filtro[col_estancia].mean():.1f} días")
                else:
                    r2.metric("Promedio Estancia Registrada", "N/A")
                    
                capacidad_cobertura = (ingresos_reales / (medicos_input * 4)) * 100 if medicos_input > 0 else 0
                r3.metric("Rendimiento Personal Programado", f"{capacidad_cobertura:.1f}%")
                
                if ingresos_reales > 0:
                    st.dataframe(df_fecha_filtro, use_container_width=True)
                else:
                    st.warning(f"No se registraron atenciones con la fecha exacta {fecha_evaluar.strftime('%d/%m/%Y')}. Comprueba en el 'Explorador de Datos' el formato de fechas de tu archivo.")
            else:
                st.warning("No se detectó una columna de fecha en el Excel subido.")
                
        # SI LA FECHA ES FUTURA: Muestra Proyección y Algoritmo Predictivo
        else:
            st.markdown(f"### 🔮 Proyección Predictiva para {fecha_evaluar.strftime('%d/%m/%Y')}")
            
            factor_jornada = 1.3 if jornada == "Noche" else (1.1 if jornada == "Tarde" else 1.0)
            factor_clima = 1.35 if clima == "Pico Epidemiológico" else (1.25 if clima == "Lluvia Intensa" else (1.1 if clima == "Lluvia Moderada" else 1.0))
            
            estimacion_llegadas = int((medicos_input * 2.8 + enfermeros_input * 1.3) * factor_jornada * factor_clima)
            ocupacion_proyectada = min(100.0, ((camas_ocupadas + (estimacion_llegadas * 0.45)) / camas_totales) * 100)
            
            p1, p2, p3 = st.columns(3)
            p1.metric("Afluencia Estimada (Pacientes)", f"{estimacion_llegadas} pacientes")
            p2.metric("Ocupación Proyectada de Camas", f"{ocupacion_proyectada:.1f}%")
            p3.metric("Relación Paciente/Médico Proyectada", f"{round(estimacion_llegadas / medicos_input, 1)}:1")
            
            if ocupacion_proyectada < 75:
                st.success("🟢 **NIVEL DE RIESGO: BAJO**\n\nCapacidad operativamente adecuada para responder a la demanda proyectada.")
            elif ocupacion_proyectada < 90:
                st.warning("🟡 **NIVEL DE RIESGO: MODERADO**\n\nAlta demanda prevista. Se sugiere optimizar tiempos de alta y preparar personal de reserva.")
            else:
                st.error("🔴 **NIVEL DE RIESGO: CRÍTICO / SATURACIÓN**\n\nAlerta de sobrecapacidad. Activar planes de contingencia para la fecha indicada.")

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
# PESTAÑA 4: EXPLORADOR DE DATOS
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("📁 Registros Hospitalarios Filtrados")
    st.write("Consulta detallada de la base de datos:")
    st.dataframe(df, use_container_width=True)
