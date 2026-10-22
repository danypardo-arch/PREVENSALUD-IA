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

    /* OCULTAR MENÚS Y ESPACIOS VACÍOS SUPERIORES DE STREAMLIT */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
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

    /* VENTANA MODAL DE HABEAS DATA */
    .habeas-card {
        background: rgba(11, 25, 44, 0.9) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 210, 255, 0.4);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 0 35px rgba(0, 210, 255, 0.25), inset 0 0 15px rgba(217, 4, 41, 0.1);
        margin-bottom: 20px;
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

    /* CORRECCIÓN VISUAL UPLOADER DE ARCHIVOS */
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: rgba(11, 25, 44, 0.9) !important;
        border: 1px dashed #00D2FF !important;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.15);
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #00D2FF 0%, #0077FF 100%) !important;
        color: #030712 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 6px;
        box-shadow: 0 0 12px rgba(0, 210, 255, 0.4);
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

PLOTLY_CYBER_THEME = ['#00D2FF', '#FF2A54', '#0077FF', '#9B51E0', '#00F5D4', '#FF9F1C']

# ==============================================================================
# 3. MANEJO DE ESTADO PARA HABEAS DATA (CONSENTIMIENTO)
# ==============================================================================
if 'habeas_aceptado' not in st.session_state:
    st.session_state.habeas_aceptado = False

# ==============================================================================
# 4. ENCABEZADO PRINCIPAL (LOGO)
# ==============================================================================
col_izq, col_logo, col_der = st.columns([1, 2, 1])

logo_cargado = False
nombres_posibles = ["Logo.png", "logo.png", "Logo.jpg", "logo.jpg", "Logo.jpeg"]

for nombre in nombres_posibles:
    if os.path.exists(nombre):
        try:
            img = Image.open(nombre)
            col_logo.image(img, use_container_width=True)
            logo_cargado = True
            break
        except Exception:
            pass

if not logo_cargado:
    col_logo.markdown("<h1 class='cyber-title' style='text-align: center;'>PREVENSALUD IA</h1>", unsafe_allow_html=True)
    col_logo.markdown("<p style='color: #00D2FF; font-family: Rajdhani; font-size: 1.2rem; font-weight: 600; text-align: center;'>SISTEMA INTELIGENTE DE ANALÍTICA PREDICTIVA Y HOSPITALARIA</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 5. MODAL DE AVISO DE HABEAS DATA Y CONSENTIMIENTO INFORMADO
# ==============================================================================
if not st.session_state.habeas_aceptado:
    st.markdown('<div class="habeas-card">', unsafe_allow_html=True)
    
    st.markdown("### 🔐 Aviso de Habeas Data y Consentimiento Informado")
    st.markdown("**PrevenSalud IA**")
    
    st.write(
        "Al ingresar y utilizar este aplicativo, usted declara conocer y autorizar de manera expresa, libre e informada "
        "a **PrevenSalud IA** para el tratamiento de los datos suministrados en esta plataforma, de conformidad con la "
        "**Ley 1581 de 2012 (Ley de Protección de Datos Personales)** y el **Decreto 1377 de 2013**."
    )
    
    st.markdown("#### 📋 1. Finalidad del Tratamiento de Datos")
    st.write(
        "Los datos de urgencias hospitalarias e información relacionada ingresados en este aplicativo serán utilizados única y exclusivamente para:\n"
        "- Alimentar y entrenar los modelos de Inteligencia Artificial orientados a la predicción de demanda de servicios de urgencias.\n"
        "- Optimizar la asignación de recursos hospitalarios y mitigar el colapso en el sistema de salud.\n"
        "- Fines estrictamente académicos, de investigación y simulación dentro del marco del curso universitario correspondiente."
    )
    
    st.markdown("#### ⚠️ 2. Tratamiento de Datos Sensibles (Salud)")
    st.write(
        "Tratándose de datos relacionados con la salud, se informa al usuario que el otorgamiento de esta autorización es de carácter facultativo. "
        "PrevenSalud IA garantiza que los datos históricos o en tiempo real serán sometidos a procesos estrictos de **anonimización o seudonimización**, "
        "asegurando que no se pueda identificar la identidad de los pacientes, cumpliendo con la reserva de la historia clínica."
    )
    
    st.markdown("#### 🛠️ 3. Derechos del Titular (Habeas Data)")
    st.write(
        "Como titular de la información, usted tiene derecho a conocer, actualizar, rectificar y solicitar la supresión de sus datos personales, "
        "así como a revocar esta autorización en cualquier momento. Al ser un prototipo académico, puede ejercer estos derechos enviando una solicitud interna al administrador del proyecto."
    )
    
    st.markdown("---")
    st.markdown("##### 🛑 Confirmación de Términos y Autorización Obligatoria")
    
    check_terminos = st.checkbox(
        "Acepto de manera expresa los Términos y Condiciones y el Aviso de Privacidad de Habeas Data. (Obligatorio)"
    )
    check_sensibles = st.checkbox(
        "Autorizo explícitamente el tratamiento de mis datos de salud (datos sensibles) bajo parámetros de estricta anonimización con fines de predicción académica. (Obligatorio)"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 INGRESAR AL APLICATIVO", type="primary"):
        if check_terminos and check_sensibles:
            st.session_state.habeas_aceptado = True
            st.rerun()
        else:
            st.error("⚠️ Debe aceptar ambas casillas obligatorias para ingresar al aplicativo.")
            
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()  # Detiene la ejecución para que no cargue el resto del contenido hasta aceptar

# ==============================================================================
# 6. BARRA LATERAL (SIDEBAR) - SOLO VISIBLE TRAS ACEPTAR HABEAS DATA
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
# 7. ESTRUCTURA DE PESTAÑAS FUTURISTAS (SOLO VISIBLE TRAS ACEPTAR HABEAS DATA)
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
