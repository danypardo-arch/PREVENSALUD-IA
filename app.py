import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from PIL import Image
import os

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="PrevenSalud IA | Future Health Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. ESTILOS CSS FUTURISTAS Y NEÓN (GLASSMORPHISM)
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Rajdhani:wght@500;600;700&display=swap');
    
    /* CONFIGURACIÓN GENERAL / FONDO ESPACIAL TECNOLÓGICO */
    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
        color: #E2E8F0;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d1f38 0%, #030712 70%);
        background-attachment: fixed;
    }

    /* ENCABEZADO Y CONTENEDOR DEL LOGO (GLASSMORPHISM NEÓN) */
    .tech-header-container {
        background: rgba(11, 25, 44, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-radius: 16px;
        padding: 25px 10px 15px 10px;
        text-align: center;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.15), inset 0 0 15px rgba(217, 4, 41, 0.05);
        margin-bottom: 25px;
    }

    /* TITULOS FUTURISTAS */
    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #FFFFFF !important;
    }
    
    .cyber-title {
        background: linear-gradient(90deg, #FFFFFF 0%, #00D2FF 50%, #FF2A54 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.2rem;
        text-shadow: 0 0 20px rgba(0, 210, 255, 0.5);
    }

    /* BARRA LATERAL FUTURISTA */
    section[data-testid="stSidebar"] {
        background-color: #050C1A !important;
        border-right: 1px solid rgba(0, 210, 255, 0.2);
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {
        color: #00D2FF !important;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
    }

    /* UPLOADER DE ARCHIVOS Y SELECTBOXES SIDEBAR */
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: rgba(13, 31, 56, 0.7) !important;
        border: 1px dashed #00D2FF !important;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.2);
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #00D2FF 0%, #0077FF 100%) !important;
        color: #030712 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 6px;
        box-shadow: 0 0 12px rgba(0, 210, 255, 0.5);
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #0B192C !important;
        color: #FFFFFF !important;
        border: 1px solid #00D2FF !important;
        border-radius: 8px;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #FFFFFF !important;
    }

    /* METRICAS SIDEBAR */
    section[data-testid="stSidebar"] div[data-testid="stMetric"] {
        background: rgba(11, 25, 44, 0.8) !important;
        border: 1px solid #FF2A54 !important;
        border-left: 5px solid #FF2A54 !important;
        box-shadow: 0 0 15px rgba(255, 42, 84, 0.3);
    }

    /* TARJETAS DE MÉTRICAS (KPIs PRINCIPALES) */
    div[data-testid="stMetric"] {
        background: rgba(11, 25, 44, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-left: 5px solid #00D2FF;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4), 0 0 15px rgba(0, 210, 255, 0.15);
        transition: all 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 210, 255, 0.3), 0 0 20px rgba(0, 210, 255, 0.4);
        border-color: #00D2FF;
    }
    
    div[data-testid="stMetricLabel"] {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        color: #94A3B8 !important;
        font-size: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #00D2FF !important;
        font-weight: 800;
        font-size: 1.8rem !important;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }

    /* PESTAÑAS FUTURISTAS (TABS) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(5, 12, 26, 0.8);
        padding: 10px 12px;
        border-radius: 14px;
        border: 1px solid rgba(0, 210, 255, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: rgba(11, 25, 44, 0.6);
        border-radius: 8px;
        color: #94A3B8 !important;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        border: 1px solid transparent;
        padding: 0px 22px;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #00D2FF !important;
        border-color: rgba(0, 210, 255, 0.4);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF2A54 0%, #B80021 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #FF2A54 !important;
        box-shadow: 0 0 20px rgba(255, 42, 84, 0.6);
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
    }

    /* BOTÓN FUTURISTA */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #FF2A54 0%, #00D2FF 100%);
        color: #FFFFFF;
        font-family: 'Orbitron', sans-serif;
        font-weight: 800;
        letter-spacing: 1.5px;
        border-radius: 10px;
        border: none;
        padding: 12px 28px;
        box-shadow: 0 0 20px rgba(255, 42, 84, 0.4);
        transition: all 0.3s ease;
    }
    
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.8);
        transform: scale(1.02);
    }

    /* ESTILIZACIÓN DE TABLAS */
    div[data-testid="stDataFrame"] {
        background: rgba(11, 25, 44, 0.6);
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Paleta Neón Plotly alineada con el Logo
PLOTLY_CYBER_THEME = ['#00D2FF', '#FF2A54', '#0077FF', '#9B51E0', '#00F5D4', '#FF9F1C']

# ==============================================================================
# 3. ENCABEZADO TECH CON LOGO Y LUZ NEÓN
# ==============================================================================
st.markdown('<div class="tech-header-container">', unsafe_allow_html=True)
col_izq, col_logo, col_der = st.columns([1, 2, 1])

logo_cargado = False
nombres_posibles = ["Logo.png", "logo.png", "Logo.jpg", "logo.jpg", "Logo.jpeg"]

for nombre in nombres_posibles:
    if os.path.exists(nombre):
        try:
            img = Image.open(nombre)
            col_logo.image(img, width=420)
            logo_cargado = True
            break
        except Exception:
            pass

if not logo_cargado:
    col_logo.markdown("<h1 class='cyber-title'>PREVENSALUD IA</h1>", unsafe_allow_html=True)
    col_logo.markdown("<p style='color: #00D2FF; font-family: Rajdhani; font-size: 1.2rem; font-weight: 600;'>SISTEMA INTELIGENTE DE ANALÍTICA PREDICTIVA Y HOSPITALARIA</p>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4. BARRA LATERAL (SIDEBAR)
# ==============================================================================
st.sidebar.markdown("### ⚙️ CENTRO DE CONTROL")
archivo_subido = st.sidebar.file_uploader("📂 Cargar Base de Datos (.xlsx)", type=["xlsx"])

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
    st.warning("Cargue un archivo Excel para habilitar los módulos.")
    st.stop()

df_base.columns = df_base.columns.str.strip()

for col_num in ['Edad', 'Días estancia', 'Dias estancia']:
    if col_num in df_base.columns:
        df_base[col_num] = pd.to_numeric(df_base[col_num], errors='coerce')

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

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ FILTROS DE RED")

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
st.sidebar.metric("REGISTROS ACTIVOS", f"{len(df):,}")

# ==============================================================================
# 5. ESTRUCTURA DE PESTAÑAS FUTURISTAS
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 PANEL KPIs", 
    "🔮 MOTOR PREDICTIVO IA", 
    "🏥 CAPACIDAD & RED", 
    "🌐 BASE DE DATOS"
])

# ------------------------------------------------------------------------------
# PESTAÑA 1: DASHBOARD CONTROL (NEÓN)
# ------------------------------------------------------------------------------
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⚡ METRICAS DE OPERACIÓN EN TIEMPO REAL")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("PACIENTES REGISTRADOS", f"{len(df):,}")
    
    col_estancia = 'Días estancia' if 'Días estancia' in df.columns else ('Dias estancia' if 'Dias estancia' in df.columns else None)
    if col_estancia and df[col_estancia].notna().any():
        col2.metric("PROMEDIO ESTANCIA", f"{df[col_estancia].mean():.1f} días")
    else:
        col2.metric("PROMEDIO ESTANCIA", "N/A")
        
    if 'Edad' in df.columns and df['Edad'].notna().any():
        col3.metric("EDAD PROMEDIO", f"{df['Edad'].mean():.1f} años")
    else:
        col3.metric("EDAD PROMEDIO", "N/A")
        
    if 'Servicio actual' in df.columns:
        col4.metric("SERVICIOS ACTIVOS", f"{df['Servicio actual'].nunique()}")
    else:
        col4.metric("SERVICIOS ACTIVOS", "N/A")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if 'Diagnóstico actual' in df.columns:
            st.markdown("##### 🩺 TOP DIAGNÓSTICOS PREVALENTES")
            top_diag = df['Diagnóstico actual'].value_counts().head(10).reset_index()
            top_diag.columns = ['Diagnóstico', 'Cantidad']
            
            fig_diag = px.bar(
                top_diag, x='Cantidad', y='Diagnóstico', orientation='h',
                color_discrete_sequence=['#00D2FF']
            )
            fig_diag.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#E2E8F0", family="Rajdhani"),
                margin=dict(l=0, r=10, t=10, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(0, 210, 255, 0.15)'),
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_diag, use_container_width=True)
            
    with col_g2:
        if 'Servicio actual' in df.columns:
            st.markdown("##### 🏥 DISTRIBUCIÓN POR SERVICIO")
            serv_dist = df['Servicio actual'].value_counts().reset_index()
            serv_dist.columns = ['Servicio', 'Cantidad']
            
            fig_serv = px.pie(
                serv_dist, names='Servicio', values='Cantidad', hole=0.6,
                color_discrete_sequence=PLOTLY_CYBER_THEME
            )
            fig_serv.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#E2E8F0", family="Rajdhani"),
                margin=dict(l=0, r=0, t=10, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_serv, use_container_width=True)

# ------------------------------------------------------------------------------
# PESTAÑA 2: MOTOR PREDICTIVO IA
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🤖 ALGORITMO PREDICTIVO DE DEMANDA Y OCUPACIÓN")
    
    c_f1, c_f2 = st.columns(2)
    
    hoy = date.today()
    fecha_min = date(2015, 1, 1)
    fecha_max = date(2035, 12, 31)
    
    with c_f1:
        fecha_inicio = st.date_input("FECHA INICIO EVALUACIÓN", value=date(2026, 1, 1), min_value=fecha_min, max_value=fecha_max)
    with c_f2:
        fecha_fin = st.date_input("FECHA FIN EVALUACIÓN", value=date(2026, 6, 30), min_value=fecha_min, max_value=fecha_max)
        
    dias_periodo = (fecha_fin - fecha_inicio).days + 1
    
    if fecha_inicio > fecha_fin:
        st.error("⚠️ La Fecha Inicial no puede ser posterior a la Fecha Final.")
    else:
        es_futuro = fecha_inicio > hoy
        
        st.markdown("<hr style='border-color: rgba(0, 210, 255, 0.2);'>", unsafe_allow_html=True)
        st.markdown("##### ⚙️ PARÁMETROS OPERATIVOS DE RED")
        c_sim1, c_sim2, c_sim3 = st.columns(3)
        
        with c_sim1:
            medicos_input = st.number_input("Médicos por Turno", min_value=1, max_value=50, value=6)
            enfermeros_input = st.number_input("Enfermeros/Asistentes por Turno", min_value=1, max_value=80, value=12)
            
        with c_sim2:
            camas_totales = st.number_input("Camas Totales", min_value=10, max_value=300, value=50)
            camas_ocupadas = st.number_input("Camas Ocupadas Base", min_value=0, max_value=300, value=35)
            
        with c_sim3:
            jornada = st.selectbox("Turno Operativo", ["Mañana", "Tarde", "Noche"])
            clima = st.selectbox("Escenario de Contingencia", ["Normal", "Lluvia Moderada", "Lluvia Intensa", "Pico Epidemiológico / Pandemia"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 EJECUTAR SIMULACIÓN IA", type="primary"):
            st.markdown("<hr style='border-color: rgba(0, 210, 255, 0.2);'>", unsafe_allow_html=True)
            
            if not es_futuro:
                st.markdown(f"#### 📋 HISTÓRICO DE AFLUENCIA ({fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')})")
                
                if col_fecha and 'Fecha_Solo_Dia' in df_base.columns:
                    df_rango = df_base[(df_base['Fecha_Solo_Dia'] >= fecha_inicio) & (df_base['Fecha_Solo_Dia'] <= fecha_fin)]
                    ingresos_reales = len(df_rango)
                    
                    r1, r2, r3, r4 = st.columns(4)
                    r1.metric("INGRESOS REALES", f"{ingresos_reales} pac.")
                    r2.metric("DÍAS EVALUADOS", f"{dias_periodo} días")
                    
                    if col_estancia and ingresos_reales > 0:
                        r3.metric("PROM. ESTANCIA", f"{df_rango[col_estancia].mean():.1f} días")
                    else:
                        r3.metric("PROM. ESTANCIA", "N/A")
                        
                    promedio_diario = round(ingresos_reales / dias_periodo, 1) if dias_periodo > 0 else 0
                    r4.metric("INGRESOS/DÍA", f"{promedio_diario} pac/día")
                    
                    if ingresos_reales > 0:
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("##### 📉 TENDENCIA DE AFLUENCIA DÍA A DÍA")
                        df_trend = df_rango.groupby('Fecha_Solo_Dia').size().reset_index(name='Atenciones')
                        
                        fig_line = px.line(df_trend, x='Fecha_Solo_Dia', y='Atenciones', markers=True, color_discrete_sequence=['#00D2FF'])
                        fig_line.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color="#E2E8F0", family="Rajdhani"),
                            xaxis=dict(showgrid=True, gridcolor='rgba(0, 210, 255, 0.15)'),
                            yaxis=dict(showgrid=True, gridcolor='rgba(0, 210, 255, 0.15)')
                        )
                        st.plotly_chart(fig_line, use_container_width=True)
            
            # ESTIMACIÓN IA
            st.markdown(f"#### 🔮 ESTIMACIÓN MODELO PREDICTIVO ({dias_periodo} DÍAS)")
            
            factor_jornada = 1.3 if jornada == "Noche" else (1.1 if jornada == "Tarde" else 1.0)
            factor_clima = 1.4 if clima == "Pico Epidemiológico / Pandemia" else (1.25 if clima == "Lluvia Intensa" else (1.1 if clima == "Lluvia Moderada" else 1.0))
            
            estimacion_diaria = int((medicos_input * 2.8 + enfermeros_input * 1.3) * factor_jornada * factor_clima)
            estimacion_total_periodo = estimacion_diaria * dias_periodo
            ocupacion_proyectada = min(100.0, ((camas_ocupadas + (estimacion_diaria * 0.45)) / camas_totales) * 100)
            
            p1, p2, p3 = st.columns(3)
            p1.metric(f"DEMANDA PROYECTADA", f"{estimacion_total_periodo:,} pac.")
            p2.metric("OCUPACIÓN CAMAS ESPERADA", f"{ocupacion_proyectada:.1f}%")
            p3.metric("PROMEDIO DIARIO IA", f"~{estimacion_diaria} pac/día")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if ocupacion_proyectada < 75:
                st.success("🟢 **ESTADO VERDE / RIESGO BAJO:** Capacidad holgada para cubrir la demanda esperada.")
            elif ocupacion_proyectada < 90:
                st.warning("🟡 **ALERTA AMARILLA / RIESGO MODERADO:** Se recomienda agilizar altas médicas para liberar giros de cama.")
            else:
                st.error("🔴 **ALERTA ROJA / SOBRECAPACIDAD:** Alto riesgo de saturación en red. Activar protocolo de contingencia.")

# ------------------------------------------------------------------------------
# PESTAÑA 3: CAPACIDAD Y SERVICIOS
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🌐 ANÁLISIS DE COBERTURA Y ASEGURADORAS")
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        if 'Aseguradora' in df.columns:
            st.markdown("##### 💳 DEMANDA POR ASEGURADORA / EPS")
            aseg_dist = df['Aseguradora'].value_counts().head(10).reset_index()
            aseg_dist.columns = ['Aseguradora', 'Pacientes']
            
            fig_aseg = px.bar(
                aseg_dist, x='Pacientes', y='Aseguradora', orientation='h',
                color_discrete_sequence=['#FF2A54']
            )
            fig_aseg.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#E2E8F0", family="Rajdhani"),
                margin=dict(l=0, r=10, t=10, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(255, 42, 84, 0.15)'),
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_aseg, use_container_width=True)
            
    with col_s2:
        if 'Especialidad' in df.columns:
            st.markdown("##### 🩺 ATENCIONES POR ESPECIALIDAD")
            esp_dist = df['Especialidad'].value_counts().head(10).reset_index()
            esp_dist.columns = ['Especialidad', 'Pacientes']
            
            fig_esp = px.pie(
                esp_dist, names='Especialidad', values='Pacientes',
                color_discrete_sequence=PLOTLY_CYBER_THEME
            )
            fig_esp.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#E2E8F0", family="Rajdhani"),
                margin=dict(l=0, r=0, t=10, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_esp, use_container_width=True)

# ------------------------------------------------------------------------------
# PESTAÑA 4: BASE DE DATOS
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🌐 EXPLORADOR DE DATOS MATRICIAL")
    st.dataframe(df, use_container_width=True)
