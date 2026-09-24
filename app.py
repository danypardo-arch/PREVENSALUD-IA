import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
from PIL import Image
import os

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS PROFESIONALES
# ==============================================================================
st.set_page_config(
    page_title="PrevenSalud IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilos CSS avanzados
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: #1E293B;
    }
    
    .stApp {
        background-color: #F1F5F9;
    }

    /* BARRA LATERAL (SIDEBAR) */
    section[data-testid="stSidebar"] {
        background-color: #0A2540 !important;
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    /* Corrección de legibilidad en inputs y selectboxes de la barra lateral */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] div[role="button"] {
        background-color: #FFFFFF !important;
        color: #0A2540 !important;
        border-radius: 6px;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #0A2540 !important;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    /* TARJETAS DE MÉTRICAS (KPIs) */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-left: 5px solid #1E6091;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }
    
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #475569 !important;
        font-size: 0.88rem !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #0A2540 !important;
        font-weight: 700;
        font-size: 1.65rem !important;
    }

    /* DISEÑO RESALTADO DE PESTAÑAS (TABS) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #0A2540;
        padding: 8px 10px;
        border-radius: 10px;
        box-shadow: 0 3px 8px rgba(10, 37, 64, 0.15);
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        background-color: transparent;
        border-radius: 6px;
        color: #CBD5E1 !important;
        font-weight: 600;
        font-size: 0.9rem;
        border: none;
        padding: 0px 18px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #D90429 !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 6px rgba(217, 4, 41, 0.3);
    }

    /* BOTONES PRIMARIOS */
    div.stButton > button[kind="primary"] {
        background-color: #D90429;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        box-shadow: 0 2px 6px rgba(217, 4, 41, 0.25);
    }
    
    div.stButton > button[kind="primary"]:hover {
        background-color: #B80021;
    }

    /* ENCABEZADOS Y CONTENEDORES */
    h1, h2, h3, h4 {
        color: #0A2540;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Paleta cromática para gráficos Plotly
COLOR_PALETTE = ['#0A2540', '#1E6091', '#2A9D8F', '#E76F51', '#D90429', '#457B9D', '#A8DADC']

# ==============================================================================
# 2. ENCABEZADO CON LOGO CENTRADO
# ==============================================================================
col_izq, col_logo, col_der = st.columns([1, 2, 1])

logo_cargado = False
nombres_posibles = ["Logo.png", "logo.png", "Logo.jpg", "logo.jpg", "Logo.jpeg"]

for nombre in nombres_posibles:
    if os.path.exists(nombre):
        try:
            img = Image.open(nombre)
            col_logo.image(img, width=400)
            logo_cargado = True
            break
        except Exception:
            pass

if not logo_cargado:
    st.markdown("<h1 style='text-align: center; color: #0A2540;'>🏥 PREVENSALUD IA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B; font-weight: 500;'>Plataforma Inteligente de Analítica Predictiva y Gestión Operativa Hospitalaria</p>", unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 10px; margin-bottom: 25px; border-color: #CBD5E1;'>", unsafe_allow_html=True)

# ==============================================================================
# 3. BARRA LATERAL (CONFIGURACIÓN Y FILTROS)
# ==============================================================================
st.sidebar.markdown("### ⚙️ Configuración")
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

# Limpieza básica de columnas
df_base.columns = df_base.columns.str.strip()

for col_num in ['Edad', 'Días estancia', 'Dias estancia']:
    if col_num in df_base.columns:
        df_base[col_num] = pd.to_numeric(df_base[col_num], errors='coerce')

# Procesamiento de fechas
col_fecha = None
columnas_posibles_fecha = ['f. ingreso', 'ingreso', 'fecha', 'f. nacimiento', 'fecha ingreso']

for col in df_base.columns:
    if col.lower().strip() in columnas_posibles_fecha:
        col_fecha = col
        break

if col_fecha:
    df_base['Fecha_Procesada'] = pd.to_datetime(df_base[col_fecha], errors='coerce')
    df_base['Fecha_Solo_Dia'] = df_base['Fecha_Procesada'].dt.date

df = df_base.copy()

# Filtros dinámicos laterales
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filtros Operativos")

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
st.sidebar.metric("Registros Filtrados", f"{len(df):,}")

# ==============================================================================
# 4. ESTRUCTURA DE PESTAÑAS
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
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📈 Resumen Ejecutivo y Capacidades Operativas")
    st.markdown("<p style='color: #475569;'>Vista panorámica del comportamiento operativo e indicadores clave del centro médico.</p>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pacientes Activos", f"{len(df):,}")
    
    col_estancia = 'Días estancia' if 'Días estancia' in df.columns else ('Dias estancia' if 'Dias estancia' in df.columns else None)
    if col_estancia and df[col_estancia].notna().any():
        col2.metric("Promedio Estancia", f"{df[col_estancia].mean():.1f} días")
    else:
        col2.metric("Promedio Estancia", "N/A")
        
    if 'Edad' in df.columns and df['Edad'].notna().any():
        col3.metric("Promedio Edad", f"{df['Edad'].mean():.1f} años")
    else:
        col3.metric("Promedio Edad", "N/A")
        
    if 'Servicio actual' in df.columns:
        col4.metric("Servicios Activos", f"{df['Servicio actual'].nunique()}")
    else:
        col4.metric("Servicios Activos", "N/A")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if 'Diagnóstico actual' in df.columns:
            st.markdown("##### 🩺 Top 10 Diagnósticos Frecuentes")
            top_diag = df['Diagnóstico actual'].value_counts().head(10).reset_index()
            top_diag.columns = ['Diagnóstico', 'Cantidad']
            
            fig_diag = px.bar(
                top_diag, x='Cantidad', y='Diagnóstico', orientation='h',
                color_discrete_sequence=['#1E6091']
            )
            fig_diag.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=10, t=10, b=0),
                xaxis=dict(showgrid=True, gridcolor='#CBD5E1'),
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_diag, use_container_width=True)
            
    with col_g2:
        if 'Servicio actual' in df.columns:
            st.markdown("##### 🏥 Distribución por Servicio")
            serv_dist = df['Servicio actual'].value_counts().reset_index()
            serv_dist.columns = ['Servicio', 'Cantidad']
            
            fig_serv = px.pie(
                serv_dist, names='Servicio', values='Cantidad', hole=0.5,
                color_discrete_sequence=COLOR_PALETTE
            )
            fig_serv.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_serv, use_container_width=True)

# ------------------------------------------------------------------------------
# PESTAÑA 2: SIMULADOR PREDICTIVO IA
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔮 Estimación, Análisis de Período y Predicción Futura (IA)")
    st.markdown("<p style='color: #475569;'>Seleccione el rango de fechas para evaluar métricas históricas y proyectar la demanda esperada.</p>", unsafe_allow_html=True)
    
    c_f1, c_f2 = st.columns(2)
    
    hoy = date.today()
    fecha_min = date(2015, 1, 1)
    fecha_max = date(2035, 12, 31)
    
    with c_f1:
        fecha_inicio = st.date_input("Fecha Inicial del Período", value=date(2026, 1, 1), min_value=fecha_min, max_value=fecha_max)
    with c_f2:
        fecha_fin = st.date_input("Fecha Final del Período", value=date(2026, 6, 30), min_value=fecha_min, max_value=fecha_max)
        
    dias_periodo = (fecha_fin - fecha_inicio).days + 1
    
    if fecha_inicio > fecha_fin:
        st.error("⚠️ La Fecha Inicial no puede ser posterior a la Fecha Final.")
    else:
        es_futuro = fecha_inicio > hoy
        
        st.markdown("<hr style='margin: 15px 0; border-color: #CBD5E1;'>", unsafe_allow_html=True)
        st.markdown("##### ⚙️ Parámetros de Capacidad Operativa y Contingencia")
        c_sim1, c_sim2, c_sim3 = st.columns(3)
        
        with c_sim1:
            medicos_input = st.number_input("Médicos Programados por Turno", min_value=1, max_value=50, value=6)
            enfermeros_input = st.number_input("Enfermeros/Asistentes por Turno", min_value=1, max_value=80, value=12)
            
        with c_sim2:
            camas_totales = st.number_input("Camas Totales Disponibles", min_value=10, max_value=300, value=50)
            camas_ocupadas = st.number_input("Camas Ocupadas Promedio", min_value=0, max_value=300, value=35)
            
        with c_sim3:
            jornada = st.selectbox("Turno Operativo Predominante", ["Mañana", "Tarde", "Noche"])
            clima = st.selectbox("Escenario Epidemiológico/Climático", ["Normal", "Lluvia Moderada", "Lluvia Intensa", "Pico Epidemiológico / Pandemia"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Ejecutar Proyección IA", type="primary"):
            st.markdown("<hr style='margin: 20px 0; border-color: #CBD5E1;'>", unsafe_allow_html=True)
            
            if not es_futuro:
                st.markdown(f"#### 📋 Análisis Histórico ({fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')})")
                
                if col_fecha and 'Fecha_Solo_Dia' in df_base.columns:
                    df_rango = df_base[(df_base['Fecha_Solo_Dia'] >= fecha_inicio) & (df_base['Fecha_Solo_Dia'] <= fecha_fin)]
                    ingresos_reales = len(df_rango)
                    
                    r1, r2, r3, r4 = st.columns(4)
                    r1.metric("Ingresos Totales", f"{ingresos_reales} pac.")
                    r2.metric("Días Evaluados", f"{dias_periodo} días")
                    
                    if col_estancia and ingresos_reales > 0:
                        r3.metric("Prom. Estancia", f"{df_rango[col_estancia].mean():.1f} días")
                    else:
                        r3.metric("Prom. Estancia", "N/A")
                        
                    promedio_diario = round(ingresos_reales / dias_periodo, 1) if dias_periodo > 0 else 0
                    r4.metric("Promedio Ingresos/Día", f"{promedio_diario} pac/día")
                    
                    if ingresos_reales > 0:
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("##### 📉 Flujo Diario Histórico de Pacientes")
                        df_trend = df_rango.groupby('Fecha_Solo_Dia').size().reset_index(name='Atenciones')
                        
                        fig_line = px.line(df_trend, x='Fecha_Solo_Dia', y='Atenciones', markers=True, color_discrete_sequence=['#1E6091'])
                        fig_line.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(showgrid=True, gridcolor='#CBD5E1'),
                            yaxis=dict(showgrid=True, gridcolor='#CBD5E1')
                        )
                        st.plotly_chart(fig_line, use_container_width=True)
                    else:
                        st.warning(f"No se registraron atenciones entre el {fecha_inicio.strftime('%d/%m/%Y')} y el {fecha_fin.strftime('%d/%m/%Y')}.")
            
            # PROYECCIÓN PREDICTIVA
            st.markdown(f"#### 🔮 Proyección Predictiva IA ({dias_periodo} días proyectados)")
            
            factor_jornada = 1.3 if jornada == "Noche" else (1.1 if jornada == "Tarde" else 1.0)
            factor_clima = 1.4 if clima == "Pico Epidemiológico / Pandemia" else (1.25 if clima == "Lluvia Intensa" else (1.1 if clima == "Lluvia Moderada" else 1.0))
            
            estimacion_diaria = int((medicos_input * 2.8 + enfermeros_input * 1.3) * factor_jornada * factor_clima)
            estimacion_total_periodo = estimacion_diaria * dias_periodo
            ocupacion_proyectada = min(100.0, ((camas_ocupadas + (estimacion_diaria * 0.45)) / camas_totales) * 100)
            
            p1, p2, p3 = st.columns(3)
            p1.metric(f"Afluencia Estimada", f"{estimacion_total_periodo:,} pac.")
            p2.metric("Ocupación Proyectada Camas", f"{ocupacion_proyectada:.1f}%")
            p3.metric("Demanda Diaria Estimada", f"~{estimacion_diaria} pac/día")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if ocupacion_proyectada < 75:
                st.success("🟢 **RIESGO BAJO:** Capacidad operativa suficiente para la demanda proyectada.")
            elif ocupacion_proyectada < 90:
                st.warning("🟡 **RIESGO MODERADO:** Se aconseja agilizar las altas médicas y reforzar personal.")
            else:
                st.error("🔴 **RIESGO ALTO / SOBRECAPACIDAD:** Alto riesgo de saturación hospitalaria en el período.")

# ------------------------------------------------------------------------------
# PESTAÑA 3: GESTIÓN DE CAPACIDAD Y SERVICIOS
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏥 Análisis Operativo de Aseguradoras y Especialidades")
    st.markdown("<p style='color: #475569;'>Distribución por pagadores/convenios e indicadores de especialidades.</p>", unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        if 'Aseguradora' in df.columns:
            st.markdown("##### 💳 Pacientes por Aseguradora / EPS")
            aseg_dist = df['Aseguradora'].value_counts().head(10).reset_index()
            aseg_dist.columns = ['Aseguradora', 'Pacientes']
            
            fig_aseg = px.bar(
                aseg_dist, x='Pacientes', y='Aseguradora', orientation='h',
                color_discrete_sequence=['#0A2540']
            )
            fig_aseg.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=10, t=10, b=0),
                xaxis=dict(showgrid=True, gridcolor='#CBD5E1'),
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_aseg, use_container_width=True)
            
    with col_s2:
        if 'Especialidad' in df.columns:
            st.markdown("##### 🩺 Atenciones por Especialidad")
            esp_dist = df['Especialidad'].value_counts().head(10).reset_index()
            esp_dist.columns = ['Especialidad', 'Pacientes']
            
            fig_esp = px.pie(
                esp_dist, names='Especialidad', values='Pacientes',
                color_discrete_sequence=COLOR_PALETTE
            )
            fig_esp.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_esp, use_container_width=True)

# ------------------------------------------------------------------------------
# PESTAÑA 4: EXPLORADOR DE DATOS
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📁 Registros Hospitalarios Consolidados")
    st.markdown("<p style='color: #475569;'>Tabla interactiva con los datos detallados actualmente filtrados.</p>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
