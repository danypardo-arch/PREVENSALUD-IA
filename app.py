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
# 3. ENCABEZADO CON LOGO CENTRADO (SIN CAJAS O BARRAS VACÍAS)
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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 PANEL KPIs", 
    "🔮 MOTOR PREDICTIVO IA", 
    "🏥 CAPACIDAD & RED", 
    "🌐 BASE DE DATOS",
    "⚖️ EVALUACIÓN ÉTICA"
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


# ==============================================================================
# 6. PESTAÑA 5: ⚖️ EVALUACIÓN ÉTICA - IPS SAN GABRIEL
#    (pegar este bloque COMPLETO al final de appF.py)
#    Usa: st, pd, np, px, go, date (ya importados al inicio de appF.py),
#         PLOTLY_CYBER_THEME, df (DataFrame ya filtrado por la barra lateral)
#         y tab5 (definida en st.tabs).
# ==============================================================================
from datetime import timedelta
from io import BytesIO

# ------------------------------------------------------------------------------
# 6.1 CONSTANTES NORMATIVAS Y DE CONFIGURACIÓN
# ------------------------------------------------------------------------------
SECTORES_ET = ["Médico", "Enfermería", "Administración", "Usuarios", "COPACOS", "Bioética", "Otro"]

# Requisitos mínimos de voto/voz por sector (cantidad de integrantes)
# Hospitalario: Res. 13437/1991 (médico, enfermería, 2 COPACOS, usuarios) + administración (propuesta del manual)
REQ_HOSP = {"Médico": 1, "Enfermería": 1, "Administración": 1, "Usuarios": 1, "COPACOS": 2}
# Investigación: SUPUESTO (pautas CIOMS / Res. 8430/1993) -> debe validarlo el especialista en bioética
REQ_INV = {"Médico": 1, "Enfermería": 1, "Bioética": 1, "Usuarios": 1, "COPACOS": 1}

COLS_COMITE = ["Cargo / rol", "Sector que representa", "Departamento", "¿Voz?", "¿Voto?", "¿Declaró conflicto de interés?"]
COLS_SESIONES = ["Fecha", "Comité", "Tema", "Asistentes", "¿Se declararon conflictos?", "Abstenciones", "¿Quórum plural?"]
COLS_PQRS = ["Fecha recepción", "Canal", "Descripción breve (sin datos personales)", "Fecha respuesta", "Satisfacción (1-5)"]
COLS_CAPAC = ["Área", "Personal total", "Capacitados en bioética", "Horas de formación"]

UMBRAL_VERDE = 80
UMBRAL_AMARILLO = 60
UMBRAL_EQUIDAD = 25     # % de desviación sobre el promedio general que activa la alerta
MIN_N_EQUIDAD = 5       # tamaño mínimo de grupo para evaluar equidad (evita ruido estadístico)
PLAZO_PQRS_DIAS_HABILES = 15

NOMBRES_DIM = {
    "composicion": "Composición y cumplimiento normativo",
    "pluralidad": "Pluralidad e imparcialidad",
    "transparencia": "Conflictos de interés y transparencia",
    "pqrs": "PQRS y rendición de cuentas",
    "capacitacion": "Capacitación continua",
    "equidad": "Equidad en servicios",
}
PESOS_DEFECTO = {"composicion": 30, "pluralidad": 20, "transparencia": 15,
                 "pqrs": 15, "capacitacion": 10, "equidad": 10}

NIVELES_PIRAMIDE = [
    "Seguridad clínica (decisiones sin sesgo)",
    "Seguridad jurídica y confianza (Res. 13437)",
    "Afiliación (enfermería, administración y comunidad)",
    "Reconocimiento (reputación y dignidad del paciente)",
    "Autorrealización (excelencia ética y humanización)",
]

ACCIONES_ET = {
    "composicion": [
        ("Reestructurar el comité con enfermería, administración, usuarios y 2 delegados COPACOS, todos con voz y voto",
         "Gerencia / Dirección científica", "30 días"),
        ("Formalizar con acto administrativo la conformación del comité y las actas de elección de representantes",
         "Gerencia y Jurídica", "45 días"),
    ],
    "pluralidad": [
        ("Aprobar normas claras de elección de representantes (medicina, enfermería, administración, usuarios y comunidad) "
         "con criterios de votación sin conflictos de interés", "Comité de Ética + Jurídica", "60 días"),
        ("Crear el comité interdisciplinario y el protocolo de participación para que ningún sector supere el 50 % de los votos",
         "Gerencia", "60 días"),
    ],
    "transparencia": [
        ("Adoptar el formato obligatorio de declaración de conflictos de interés al inicio de cada sesión",
         "Secretaría del Comité", "15 días"),
        ("Cumplir la reunión mensual del comité y registrar actas con abstenciones", "Presidencia del Comité", "30 días"),
    ],
    "pqrs": [
        ("Habilitar buzón físico, formulario virtual y línea de atención; responder por escrito en máx. 15 días hábiles",
         "Atención al usuario", "30 días"),
        ("Realizar reunión trimestral con COPACOS y usuarios y publicar el informe semestral de rendición de cuentas",
         "Gerencia / Comité", "90 días"),
    ],
    "capacitacion": [
        ("Implementar módulos periódicos de formación en dilemas bioéticos, humanización y derechos de los pacientes",
         "Talento humano / Docencia", "90 días"),
    ],
    "equidad": [
        ("Revisar los grupos con estancia atípica (aseguradora, edad, servicio) y ajustar procesos; incluirlos en el tablero de control",
         "Calidad / Comité de Ética", "60 días"),
    ],
}


# ------------------------------------------------------------------------------
# 6.2 DATOS INICIALES DE EJEMPLO (ESCENARIO SANCIONADO Y ESCENARIO CORREGIDO)
# ------------------------------------------------------------------------------
def _fila(cargo, sector, depto, voz, voto, conflicto):
    return {"Cargo / rol": cargo, "Sector que representa": sector, "Departamento": depto,
            "¿Voz?": voz, "¿Voto?": voto, "¿Declaró conflicto de interés?": conflicto}


def comite_hosp_sancionado():
    """Escenario que originó la sanción: solo especialistas del mismo departamento."""
    filas = [_fila(f"Especialista {i} (Cardiología)", "Médico", "Cardiología", True, True, False) for i in range(1, 6)]
    return pd.DataFrame(filas, columns=COLS_COMITE)


def comite_hosp_corregido():
    """Propuesta del manual: estructura plural con voz y voto."""
    return pd.DataFrame([
        _fila("Representante del equipo médico", "Médico", "Medicina interna", True, True, True),
        _fila("Representante de enfermería", "Enfermería", "Enfermería", True, True, True),
        _fila("Representante administrativo", "Administración", "Administración", True, True, True),
        _fila("Representante de usuarios", "Usuarios", "Asociación de usuarios", True, True, True),
        _fila("Delegado COPACOS 1", "COPACOS", "Comunidad (COPACOS 1)", True, True, True),
        _fila("Delegado COPACOS 2", "COPACOS", "Comunidad (COPACOS 2)", True, True, True),
    ], columns=COLS_COMITE)


def comite_inv_sancionado():
    filas = [_fila(f"Investigador {i} (Cardiología)", "Médico", "Cardiología", True, True, False) for i in range(1, 4)]
    return pd.DataFrame(filas, columns=COLS_COMITE)


def comite_inv_corregido():
    return pd.DataFrame([
        _fila("Investigador / médico", "Médico", "Investigación clínica", True, True, True),
        _fila("Representante de enfermería", "Enfermería", "Enfermería", True, True, True),
        _fila("Especialista en bioética", "Bioética", "Bioética", True, True, True),
        _fila("Representante de usuarios", "Usuarios", "Asociación de usuarios", True, True, True),
        _fila("Delegado de la comunidad (COPACOS)", "COPACOS", "Comunidad (COPACOS 1)", True, True, True),
    ], columns=COLS_COMITE)


def sesiones_ejemplo():
    h = date.today()
    return pd.DataFrame([
        {"Fecha": h - timedelta(days=150), "Comité": "Hospitalario", "Tema": "Revisión de caso clínico (ejemplo)",
         "Asistentes": 5, "¿Se declararon conflictos?": False, "Abstenciones": 0, "¿Quórum plural?": False},
        {"Fecha": h - timedelta(days=120), "Comité": "Hospitalario", "Tema": "Autorización de procedimiento (ejemplo)",
         "Asistentes": 5, "¿Se declararon conflictos?": False, "Abstenciones": 0, "¿Quórum plural?": False},
        {"Fecha": h - timedelta(days=60), "Comité": "Hospitalario", "Tema": "Queja de usuario (ejemplo)",
         "Asistentes": 4, "¿Se declararon conflictos?": True, "Abstenciones": 1, "¿Quórum plural?": False},
    ], columns=COLS_SESIONES)


def pqrs_ejemplo():
    h = date.today()
    return pd.DataFrame([
        {"Fecha recepción": h - timedelta(days=90), "Canal": "Buzón", "Descripción breve (sin datos personales)": "Falta de información sobre decisión del comité (ejemplo)",
         "Fecha respuesta": h - timedelta(days=75), "Satisfacción (1-5)": 3},
        {"Fecha recepción": h - timedelta(days=70), "Canal": "Formulario virtual", "Descripción breve (sin datos personales)": "Solicitud de representación comunitaria (ejemplo)",
         "Fecha respuesta": h - timedelta(days=30), "Satisfacción (1-5)": 2},
        {"Fecha recepción": h - timedelta(days=40), "Canal": "Línea de atención", "Descripción breve (sin datos personales)": "Trato digno en hospitalización (ejemplo)",
         "Fecha respuesta": h - timedelta(days=33), "Satisfacción (1-5)": 4},
        {"Fecha recepción": h - timedelta(days=35), "Canal": "Buzón", "Descripción breve (sin datos personales)": "Demora en respuesta del comité (ejemplo)",
         "Fecha respuesta": None, "Satisfacción (1-5)": None},
    ], columns=COLS_PQRS)


def capacitacion_ejemplo():
    return pd.DataFrame([
        {"Área": "Medicina", "Personal total": 40, "Capacitados en bioética": 22, "Horas de formación": 60},
        {"Área": "Enfermería", "Personal total": 60, "Capacitados en bioética": 18, "Horas de formación": 40},
        {"Área": "Administración", "Personal total": 25, "Capacitados en bioética": 5, "Horas de formación": 10},
        {"Área": "Otros", "Personal total": 30, "Capacitados en bioética": 6, "Horas de formación": 12},
    ], columns=COLS_CAPAC)


def iniciar_estado_etica():
    """Carga los datos de ejemplo una sola vez por sesión."""
    if "et_hosp" not in st.session_state:
        st.session_state["et_hosp"] = comite_hosp_sancionado()
    if "et_inv" not in st.session_state:
        st.session_state["et_inv"] = comite_inv_sancionado()
    if "et_ses" not in st.session_state:
        st.session_state["et_ses"] = sesiones_ejemplo()
    if "et_pqrs" not in st.session_state:
        st.session_state["et_pqrs"] = pqrs_ejemplo()
    if "et_cap" not in st.session_state:
        st.session_state["et_cap"] = capacitacion_ejemplo()


# --- Callbacks de botones (se ejecutan antes de dibujar los widgets) ---
def cb_escenario(nombre):
    if nombre == "corregido":
        st.session_state["et_hosp"] = comite_hosp_corregido()
        st.session_state["et_inv"] = comite_inv_corregido()
    else:
        st.session_state["et_hosp"] = comite_hosp_sancionado()
        st.session_state["et_inv"] = comite_inv_sancionado()
    for k in ("et_ed_hosp", "et_ed_inv"):      # reinicia los editores
        st.session_state.pop(k, None)


def cb_limpiar_registros():
    st.session_state["et_ses"] = pd.DataFrame(columns=COLS_SESIONES)
    st.session_state["et_pqrs"] = pd.DataFrame(columns=COLS_PQRS)
    st.session_state.pop("et_ed_pqrs", None)


def cb_borrar_ultima_sesion():
    ses = st.session_state["et_ses"]
    if len(ses) > 0:
        st.session_state["et_ses"] = ses.iloc[:-1].reset_index(drop=True)


# ------------------------------------------------------------------------------
# 6.3 FUNCIONES DE CÁLCULO (sin dependencias de la interfaz)
# ------------------------------------------------------------------------------
def estado_semaforo(valor):
    """Devuelve (emoji, texto) según los umbrales del semáforo."""
    if valor is None:
        return "⚪", "Sin datos"
    if valor >= UMBRAL_VERDE:
        return "🟢", "Cumple"
    if valor >= UMBRAL_AMARILLO:
        return "🟡", "En riesgo"
    return "🔴", "Riesgo de sanción"


def color_semaforo(valor):
    if valor is None:
        return "#64748B"
    if valor >= UMBRAL_VERDE:
        return "#00F5D4"
    if valor >= UMBRAL_AMARILLO:
        return "#FF9F1C"
    return "#FF2A54"


def fmt(valor, sufijo=""):
    return "N/D" if valor is None else f"{valor:.0f}{sufijo}"


def promedio(valores, defecto=None):
    """Promedio ignorando None."""
    v = [x for x in valores if x is not None]
    return float(np.mean(v)) if v else defecto


def promedio_ponderado(pares):
    """pares = [(peso, valor)], ignora los valores None y re-normaliza los pesos."""
    validos = [(p, v) for p, v in pares if v is not None]
    total = sum(p for p, _ in validos)
    if total <= 0:
        return None
    return sum(p * v for p, v in validos) / total


def _limpiar_comite(df_c):
    d = df_c.copy() if df_c is not None else pd.DataFrame(columns=COLS_COMITE)
    for c in COLS_COMITE:
        if c not in d.columns:
            d[c] = None
    d = d.dropna(subset=["Sector que representa"])
    for c in ["¿Voz?", "¿Voto?", "¿Declaró conflicto de interés?"]:
        d[c] = d[c].fillna(False).astype(bool)
    # si no hay departamento, se usa el sector como "departamento"
    d["Departamento"] = d["Departamento"].where(d["Departamento"].notna() & (d["Departamento"].astype(str).str.strip() != ""),
                                                d["Sector que representa"])
    return d


def _concentracion(serie):
    """Devuelve (HHI, categoría dominante, participación dominante 0-1)."""
    if len(serie) == 0:
        return 1.0, None, 1.0
    cuotas = serie.value_counts(normalize=True)
    return float((cuotas ** 2).sum()), cuotas.index[0], float(cuotas.iloc[0])


def calcular_comite(df_c, requisitos):
    """Evalúa composición, pluralidad y declaración de conflictos de un comité."""
    d = _limpiar_comite(df_c)
    k_ref = len(requisitos)

    # 1) Checklist de roles obligatorios (voz y voto)
    detalle = []
    for sector, req in requisitos.items():
        de_sector = d[d["Sector que representa"] == sector]
        efectivo = float((0.5 * de_sector["¿Voz?"].astype(int) + 0.5 * de_sector["¿Voto?"].astype(int)).sum())
        detalle.append({"Sector": sector, "Requerido": req, "Efectivo (voz+voto)": efectivo,
                        "Cumple": efectivo >= req, "Avance": min(efectivo / req, 1.0)})
    cumplimiento = float(np.mean([x["Avance"] for x in detalle]) * 100) if detalle else 0.0

    # 2) Pluralidad: 1 - Herfindahl, normalizada por el máximo esperable con k sectores
    votantes = d[d["¿Voto?"]]
    if len(votantes) == 0:
        pluralidad, dominante, cuota_dom, votos_sector = 0.0, None, 1.0, pd.Series(dtype=int)
    else:
        hhi_s, dom_s, cuota_s = _concentracion(votantes["Sector que representa"])
        hhi_d, dom_d, cuota_d = _concentracion(votantes["Departamento"])
        norm = 1 - 1 / k_ref
        pl_s = min((1 - hhi_s) / norm, 1.0) * 100
        pl_d = min((1 - hhi_d) / norm, 1.0) * 100
        pluralidad = min(pl_s, pl_d)
        if cuota_s >= cuota_d:
            dominante, cuota_dom = f"el sector {dom_s}", cuota_s
        else:
            dominante, cuota_dom = f"el departamento {dom_d}", cuota_d
        votos_sector = votantes["Sector que representa"].value_counts()

    # 3) Integrantes con declaración de conflictos vigente
    pct_decl = float(d["¿Declaró conflicto de interés?"].mean() * 100) if len(d) else 0.0

    return {"detalle": detalle, "cumplimiento": cumplimiento, "pluralidad": pluralidad,
            "dominante": dominante, "cuota_dom": cuota_dom * 100, "votos_sector": votos_sector,
            "pct_decl": pct_decl, "n": len(d), "n_votos": len(votantes)}


def calcular_sesiones(ses):
    """Indicadores de transparencia a partir del registro de sesiones."""
    vacio = {"n": 0, "pct_decl": None, "pct_quorum": None, "abst": 0, "pct_reunion": 0.0, "tendencia": pd.DataFrame()}
    if ses is None or len(ses) == 0:
        return vacio
    d = ses.copy()
    d["Fecha"] = pd.to_datetime(d["Fecha"], errors="coerce")
    d = d.dropna(subset=["Fecha"])
    if d.empty:
        return vacio
    d["Mes"] = d["Fecha"].dt.to_period("M")
    d["decl"] = d["¿Se declararon conflictos?"].fillna(False).astype(bool)
    d["quo"] = d["¿Quórum plural?"].fillna(False).astype(bool)
    d["abst"] = pd.to_numeric(d["Abstenciones"], errors="coerce").fillna(0)

    # Reunión mensual obligatoria (Res. 13437): meses con sesión del comité hospitalario en los últimos 6 meses
    mes_actual = pd.Period(date.today(), "M")
    ultimos = {mes_actual - i for i in range(6)}
    meses_hosp = set(d[d["Comité"] == "Hospitalario"]["Mes"])
    pct_reunion = len(meses_hosp & ultimos) / 6 * 100

    tend = d.groupby("Mes").agg(Sesiones=("Fecha", "count"),
                                pct_decl=("decl", "mean"), pct_quorum=("quo", "mean")).reset_index()
    tend["Mes"] = tend["Mes"].astype(str)
    tend["% con declaración de conflictos"] = tend["pct_decl"] * 100
    tend["% con quórum plural"] = tend["pct_quorum"] * 100

    return {"n": len(d), "pct_decl": float(d["decl"].mean() * 100), "pct_quorum": float(d["quo"].mean() * 100),
            "abst": int((d["abst"] > 0).sum()), "pct_reunion": pct_reunion, "tendencia": tend}


def calcular_pqrs(pq):
    """% respondido en 15 días hábiles, satisfacción y tabla enriquecida."""
    res = {"n": 0, "pct_tiempo": None, "sat": None, "tabla": pd.DataFrame()}
    if pq is None or len(pq) == 0:
        return res
    d = pq.copy()
    d["rec"] = pd.to_datetime(d["Fecha recepción"], errors="coerce")
    d["res"] = pd.to_datetime(d["Fecha respuesta"], errors="coerce")
    d = d.dropna(subset=["rec"]).copy()
    if d.empty:
        return res
    hoy = pd.Timestamp(date.today())
    fin = d["res"].fillna(hoy)
    dias = np.busday_count(d["rec"].values.astype("datetime64[D]"), fin.values.astype("datetime64[D]"))
    d["Días hábiles"] = np.clip(dias, 0, None)   # no se descuentan festivos (supuesto)
    respondida = d["res"].notna()
    en_plazo = respondida & (d["Días hábiles"] <= PLAZO_PQRS_DIAS_HABILES)
    vencida = (~respondida) & (d["Días hábiles"] > PLAZO_PQRS_DIAS_HABILES)
    evaluadas = respondida | vencida          # las pendientes aún en plazo no se evalúan
    d["Estado"] = np.where(en_plazo, "✅ A tiempo",
                  np.where(respondida, "⏰ Tardía", np.where(vencida, "🔴 Vencida sin respuesta", "⏳ Pendiente en plazo")))
    pct = float(en_plazo.sum() / evaluadas.sum() * 100) if evaluadas.sum() > 0 else None
    sat = pd.to_numeric(d["Satisfacción (1-5)"], errors="coerce").dropna()
    return {"n": len(d), "pct_tiempo": pct, "sat": float(sat.mean()) if len(sat) else None,
            "tabla": d[["Fecha recepción", "Canal", "Días hábiles", "Estado"]]}


def calcular_capacitacion(cap):
    if cap is None or len(cap) == 0:
        return {"pct": None, "tabla": pd.DataFrame()}
    d = cap.copy()
    for c in ["Personal total", "Capacitados en bioética", "Horas de formación"]:
        d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0)
    d["% cobertura"] = np.where(d["Personal total"] > 0,
                                np.minimum(d["Capacitados en bioética"] / d["Personal total"], 1) * 100, 0)
    total = d["Personal total"].sum()
    pct = float(min(d["Capacitados en bioética"].sum() / total, 1) * 100) if total > 0 else None
    return {"pct": pct, "tabla": d}


def columna_estancia(d):
    for c in ["Días estancia", "Dias estancia"]:
        if c in d.columns:
            return c
    return None


def calcular_equidad(base):
    """Compara la estancia promedio por aseguradora, grupo de edad y servicio contra el promedio general."""
    col_est = columna_estancia(base) if base is not None else None
    if base is None or base.empty or col_est is None:
        return None, pd.DataFrame(), None
    d = base.copy()
    d[col_est] = pd.to_numeric(d[col_est], errors="coerce")
    d = d.dropna(subset=[col_est])
    if d.empty:
        return None, pd.DataFrame(), None
    media = d[col_est].mean()
    if media == 0 or np.isnan(media):
        return None, pd.DataFrame(), None

    dims = []
    if "Aseguradora" in d.columns:
        dims.append(("Aseguradora", "Aseguradora"))
    if "Edad" in d.columns:
        d["Grupo de edad"] = pd.cut(pd.to_numeric(d["Edad"], errors="coerce"), bins=[-1, 17, 39, 59, 200],
                                    labels=["0-17", "18-39", "40-59", "60+"]).astype(object)
        dims.append(("Grupo de edad", "Grupo de edad"))
    if "Servicio actual" in d.columns:
        dims.append(("Servicio actual", "Servicio"))
    if not dims:
        return None, pd.DataFrame(), media

    tablas = []
    for col, nombre in dims:
        g = d.dropna(subset=[col]).groupby(col)[col_est].agg(["count", "mean"]).reset_index()
        g.columns = ["Grupo", "Volumen de atención", "Estancia promedio (días)"]
        g.insert(0, "Dimensión", nombre)
        g["Grupo"] = g["Grupo"].astype(str)
        tablas.append(g)
    t = pd.concat(tablas, ignore_index=True)
    t["Desviación vs. promedio (%)"] = (t["Estancia promedio (días)"] / media - 1) * 100
    t["Evaluable"] = t["Volumen de atención"] >= MIN_N_EQUIDAD
    t["Alerta"] = t["Evaluable"] & (t["Desviación vs. promedio (%)"].abs() > UMBRAL_EQUIDAD)
    evaluables = int(t["Evaluable"].sum())
    score = float(100 * (1 - t["Alerta"].sum() / evaluables)) if evaluables > 0 else None
    return score, t, media


def calcular_niveles_piramide(ind):
    """Convierte los indicadores en los 5 niveles de la pirámide (0-100)."""
    n1 = promedio_ponderado([(0.6, ind["pluralidad"]), (0.4, ind["transparencia"])]) or 0.0
    n2 = promedio_ponderado([(0.7, ind["composicion"]), (0.3, ind["pct_reunion"])]) or 0.0
    n3 = ind["afiliacion"]
    n4 = promedio_ponderado([(0.6, ind["pct_pqrs"]), (0.4, ind["sat_100"])]) or 0.0
    n5 = promedio([ind["capacitacion"], ind["equidad"], ind["rendicion"]], 0.0)
    return [n1, n2, n3, n4, n5]


def generar_plan_accion(dims):
    """Lista priorizada de acciones según las dimensiones en rojo/amarillo."""
    filas = []
    for clave, valor in dims.items():
        if valor is None or valor >= UMBRAL_VERDE:
            continue
        prioridad = "🔴 Alta" if valor < UMBRAL_AMARILLO else "🟡 Media"
        for accion, resp, plazo in ACCIONES_ET.get(clave, []):
            filas.append({"Prioridad": prioridad, "Dimensión": NOMBRES_DIM[clave], "Puntaje": round(valor),
                          "Acción (según el manual)": accion, "Responsable sugerido": resp, "Plazo": plazo})
    filas.append({"Prioridad": "🟡 Media", "Dimensión": "Validación externa", "Puntaje": None,
                  "Acción (según el manual)": "Someter el manual y la estructura de los comités a validación de un especialista en bioética hospitalaria",
                  "Responsable sugerido": "Gerencia", "Plazo": "30 días"})
    plan = pd.DataFrame(filas)
    orden = {"🔴 Alta": 0, "🟡 Media": 1}
    plan["_o"] = plan["Prioridad"].map(orden)
    return plan.sort_values("_o", kind="stable").drop(columns="_o").reset_index(drop=True)


def construir_excel(hojas):
    """Genera un Excel en memoria con una hoja por sección."""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for nombre, tabla in hojas.items():
            if tabla is None:
                continue
            tabla.to_excel(writer, sheet_name=nombre[:31], index=False)
    return buffer.getvalue()


# ------------------------------------------------------------------------------
# 6.4 FUNCIONES DE DIBUJO (Plotly con el tema neón de la app)
# ------------------------------------------------------------------------------
def _layout_cyber(fig, alto=320, margen=None):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0", family="Rajdhani"), height=alto,
        margin=margen or dict(l=10, r=10, t=30, b=10))
    return fig


def dibujar_gauge(valor):
    v = 0 if valor is None else valor
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=v, number={"suffix": " / 100", "font": {"size": 44}},
        title={"text": "ÍNDICE GLOBAL DE ÉTICA INSTITUCIONAL", "font": {"size": 18}},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": color_semaforo(valor)},
               "bgcolor": "rgba(0,0,0,0)",
               "steps": [{"range": [0, UMBRAL_AMARILLO], "color": "rgba(255,42,84,0.25)"},
                         {"range": [UMBRAL_AMARILLO, UMBRAL_VERDE], "color": "rgba(255,159,28,0.25)"},
                         {"range": [UMBRAL_VERDE, 100], "color": "rgba(0,245,212,0.25)"}]}))
    return _layout_cyber(fig, 300, dict(l=30, r=30, t=60, b=10))


def dibujar_dona(votos_sector):
    fig = px.pie(names=votos_sector.index, values=votos_sector.values, hole=0.6,
                 color_discrete_sequence=PLOTLY_CYBER_THEME)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.25))
    return _layout_cyber(fig, 300, dict(l=0, r=0, t=10, b=0))


def dibujar_piramide(niveles):
    """Pirámide de 5 niveles dibujada con polígonos; nivel 1 en la base."""
    anchos = [10, 8.4, 6.8, 5.2, 3.6, 2.0]
    fig = go.Figure()
    for i, valor in enumerate(niveles):
        w0, w1 = anchos[i] / 2, anchos[i + 1] / 2
        ruta = f"M {-w0},{i} L {w0},{i} L {w1},{i + 1} L {-w1},{i + 1} Z"
        fig.add_shape(type="path", path=ruta, fillcolor=color_semaforo(valor), opacity=0.85,
                      line=dict(color="#0B192C", width=3))
        fig.add_annotation(x=0, y=i + 0.5, text=f"<b>{valor:.0f}</b>", showarrow=False,
                           font=dict(size=20, color="#030712", family="Orbitron"))
        fig.add_annotation(x=5.4, y=i + 0.5, text=f"<b>Nivel {i + 1}</b> · {NIVELES_PIRAMIDE[i]}",
                           showarrow=False, xanchor="left", font=dict(size=14, color="#E2E8F0"))
    fig.update_xaxes(visible=False, range=[-5.5, 24])
    fig.update_yaxes(visible=False, range=[-0.1, 5.1])
    return _layout_cyber(fig, 420, dict(l=0, r=0, t=10, b=0))


# ------------------------------------------------------------------------------
# 6.5 PINTAR LA PESTAÑA
# ------------------------------------------------------------------------------
def render_checklist(res, titulo):
    st.markdown(f"**{titulo}**")
    for x in res["detalle"]:
        icono = "✅" if x["Cumple"] else "❌"
        st.markdown(f"{icono} **{x['Sector']}** — requerido: {x['Requerido']} · con voz y voto: {x['Efectivo (voz+voto)']:.1f}")
    if res["dominante"] is None:
        st.error("🔴 No hay integrantes con voto: el comité no puede decidir.")
    elif res["cuota_dom"] > 50:
        st.error(f"🔴 El comité está dominado por {res['dominante']} ({res['cuota_dom']:.0f} % de los votos).")
    else:
        st.success(f"🟢 Ningún sector ni departamento supera el 50 % de los votos (máx.: {res['cuota_dom']:.0f} %).")


def render_evaluacion_etica(base_df):
    iniciar_estado_etica()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⚖️ EVALUACIÓN DE SERVICIOS ÉTICOS · IPS SAN GABRIEL")
    st.caption("Seguimiento a la pluralidad, imparcialidad y transparencia del Comité de Ética (Res. 13437 de 1991). "
               "Los datos precargados son de EJEMPLO: reemplácelos con los datos reales de la institución.")

    # Contenedor superior: se llena al final, cuando ya se calcularon todos los indicadores
    zona_resumen = st.container()
    st.markdown("---")

    # ---------------- B. COMPOSICIÓN DEL COMITÉ ----------------
    st.markdown("### 🏛️ B. COMPOSICIÓN DEL COMITÉ")
    b1, b2, b3 = st.columns([1, 1, 2])
    b1.button("✅ Cargar escenario corregido", key="et_btn_corr", on_click=cb_escenario, args=("corregido",),
              use_container_width=True)
    b2.button("↩️ Volver al escenario sancionado", key="et_btn_sanc", on_click=cb_escenario, args=("sancionado",),
              use_container_width=True)
    b3.caption("El escenario sancionado reproduce un comité solo de especialistas de un mismo departamento. "
               "El corregido aplica la estructura propuesta en el manual.")

    cfg_comite = {
        "Sector que representa": st.column_config.SelectboxColumn("Sector que representa", options=SECTORES_ET, required=True),
        "¿Voz?": st.column_config.CheckboxColumn("¿Voz?"),
        "¿Voto?": st.column_config.CheckboxColumn("¿Voto?"),
        "¿Declaró conflicto de interés?": st.column_config.CheckboxColumn("¿Declaró conflicto de interés?"),
    }
    tab_h, tab_i = st.tabs(["🏥 Comité de Ética Hospitalaria", "🔬 Comité de Ética de Investigación"])
    with tab_h:
        ed_h = st.data_editor(st.session_state["et_hosp"], num_rows="dynamic", use_container_width=True,
                              column_config=cfg_comite, key="et_ed_hosp")
    with tab_i:
        ed_i = st.data_editor(st.session_state["et_inv"], num_rows="dynamic", use_container_width=True,
                              column_config=cfg_comite, key="et_ed_inv")

    res_h = calcular_comite(ed_h, REQ_HOSP)
    res_i = calcular_comite(ed_i, REQ_INV)

    cc1, cc2 = st.columns(2)
    with cc1:
        render_checklist(res_h, "Checklist · Comité Hospitalario (Res. 13437/1991 + administración del manual)")
        st.caption(f"Cumplimiento: {res_h['cumplimiento']:.0f} % · Pluralidad: {res_h['pluralidad']:.0f}/100")
        if len(res_h["votos_sector"]) > 0:
            st.plotly_chart(dibujar_dona(res_h["votos_sector"]), use_container_width=True, key="et_dona_h")
    with cc2:
        render_checklist(res_i, "Checklist · Comité de Investigación (supuesto CIOMS / Res. 8430, validar con bioética)")
        st.caption(f"Cumplimiento: {res_i['cumplimiento']:.0f} % · Pluralidad: {res_i['pluralidad']:.0f}/100")
        if len(res_i["votos_sector"]) > 0:
            st.plotly_chart(dibujar_dona(res_i["votos_sector"]), use_container_width=True, key="et_dona_i")

    # Se pondera 70 % hospitalario y 30 % investigación (si el de investigación está vacío, solo cuenta el hospitalario)
    p_h, p_i = (0.7, 0.3) if res_i["n"] > 0 else (1.0, 0.0)
    comp_total = res_h["cumplimiento"] * p_h + res_i["cumplimiento"] * p_i
    plur_total = res_h["pluralidad"] * p_h + res_i["pluralidad"] * p_i
    decl_integrantes = res_h["pct_decl"] * p_h + res_i["pct_decl"] * p_i

    st.markdown("---")

    # ---------------- D. CONFLICTOS DE INTERÉS Y TRANSPARENCIA ----------------
    st.markdown("### 🔍 D. CONFLICTOS DE INTERÉS Y TRANSPARENCIA")
    with st.form("et_form_sesion", clear_on_submit=True):
        f1, f2, f3 = st.columns([1, 1, 2])
        f_fecha = f1.date_input("Fecha de la sesión", value=date.today(), key="et_f_fecha")
        f_comite = f2.selectbox("Comité", ["Hospitalario", "Investigación"], key="et_f_comite")
        f_tema = f3.text_input("Tema tratado (sin datos personales de pacientes)", key="et_f_tema")
        g1, g2, g3, g4 = st.columns(4)
        f_asist = g1.number_input("Asistentes", min_value=0, max_value=50, value=6, key="et_f_asist")
        f_abst = g2.number_input("Integrantes que se abstuvieron", min_value=0, max_value=50, value=0, key="et_f_abst")
        f_decl = g3.checkbox("Se declararon conflictos", key="et_f_decl")
        f_quo = g4.checkbox("Hubo quórum plural", key="et_f_quo")
        enviado = st.form_submit_button("➕ Registrar sesión")
    if enviado:
        nueva = pd.DataFrame([{"Fecha": f_fecha, "Comité": f_comite, "Tema": f_tema, "Asistentes": int(f_asist),
                               "¿Se declararon conflictos?": f_decl, "Abstenciones": int(f_abst), "¿Quórum plural?": f_quo}])
        st.session_state["et_ses"] = pd.concat([st.session_state["et_ses"], nueva], ignore_index=True)
        st.success("Sesión registrada.")

    ses = st.session_state["et_ses"]
    r_ses = calcular_sesiones(ses)
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("SESIONES REGISTRADAS", r_ses["n"])
    d2.metric("% CON DECLARACIÓN DE CONFLICTOS", "N/D" if r_ses["pct_decl"] is None else f"{r_ses['pct_decl']:.0f} %")
    d3.metric("% CON QUÓRUM PLURAL", "N/D" if r_ses["pct_quorum"] is None else f"{r_ses['pct_quorum']:.0f} %")
    d4.metric("DECISIONES CON ABSTENCIÓN", r_ses["abst"])
    st.metric("REUNIÓN MENSUAL (ÚLTIMOS 6 MESES, COMITÉ HOSPITALARIO)", f"{r_ses['pct_reunion']:.0f} %",
              help="La Res. 13437 de 1991 indica que el comité debe reunirse como mínimo una vez al mes.")
    if r_ses["n"] > 0:
        t1, t2 = st.columns([3, 2])
        with t1:
            st.dataframe(ses.sort_values("Fecha", ascending=False), use_container_width=True, hide_index=True)
        with t2:
            tend = r_ses["tendencia"]
            if len(tend) > 0:
                fig_t = px.line(tend, x="Mes", y=["% con declaración de conflictos", "% con quórum plural"],
                                markers=True, color_discrete_sequence=PLOTLY_CYBER_THEME)
                fig_t.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.45, title=None),
                                    yaxis=dict(range=[0, 105], title="%", gridcolor="rgba(0, 210, 255, 0.15)"),
                                    xaxis=dict(title=None))
                st.plotly_chart(_layout_cyber(fig_t, 280), use_container_width=True, key="et_tend")
        st.button("🗑️ Eliminar la última sesión registrada", key="et_btn_del_ses", on_click=cb_borrar_ultima_sesion)
    else:
        st.info("Aún no hay sesiones registradas.")

    transp = promedio_ponderado([(0.30, r_ses["pct_decl"]), (0.30, r_ses["pct_quorum"]),
                                 (0.20, r_ses["pct_reunion"]), (0.20, decl_integrantes)])

    st.markdown("---")

    # ---------------- E. BUZÓN ÉTICO / PQRS Y RENDICIÓN DE CUENTAS ----------------
    st.markdown("### 📬 E. BUZÓN ÉTICO, PQRS Y RENDICIÓN DE CUENTAS")
    st.caption("Registre solo información agregada: no escriba nombres ni identificaciones de pacientes (Ley 1581 de 2012).")
    ed_pq = st.data_editor(
        st.session_state["et_pqrs"], num_rows="dynamic", use_container_width=True, key="et_ed_pqrs",
        column_config={
            "Fecha recepción": st.column_config.DateColumn("Fecha recepción"),
            "Canal": st.column_config.SelectboxColumn("Canal", options=["Buzón", "Formulario virtual", "Línea de atención"]),
            "Fecha respuesta": st.column_config.DateColumn("Fecha respuesta"),
            "Satisfacción (1-5)": st.column_config.NumberColumn("Satisfacción (1-5)", min_value=1, max_value=5, step=1),
        })
    r_pq = calcular_pqrs(ed_pq)
    e1, e2, e3 = st.columns(3)
    e1.metric("QUEJAS ÉTICAS RECIBIDAS", r_pq["n"])
    e2.metric(f"% RESPONDIDAS EN {PLAZO_PQRS_DIAS_HABILES} DÍAS HÁBILES",
              "N/D" if r_pq["pct_tiempo"] is None else f"{r_pq['pct_tiempo']:.0f} %")
    e3.metric("SATISFACCIÓN PROMEDIO", "N/D" if r_pq["sat"] is None else f"{r_pq['sat']:.1f} / 5")
    if len(r_pq["tabla"]) > 0:
        with st.expander("Ver estado de cada queja"):
            st.dataframe(r_pq["tabla"], use_container_width=True, hide_index=True)
    st.button("🧹 Limpiar registros de ejemplo (sesiones y quejas)", key="et_btn_limpiar", on_click=cb_limpiar_registros)

    k1, k2 = st.columns(2)
    chk_reunion = k1.checkbox("Reunión trimestral con COPACOS y usuarios realizada", key="et_chk_reunion")
    chk_informe = k2.checkbox("Informe semestral público publicado", key="et_chk_informe")
    rendicion = (50 if chk_reunion else 0) + (50 if chk_informe else 0)

    sat_100 = None if r_pq["sat"] is None else (r_pq["sat"] - 1) / 4 * 100
    pqrs_score = promedio_ponderado([(0.50, r_pq["pct_tiempo"]), (0.20, sat_100), (0.30, rendicion)])

    st.markdown("---")

    # ---------------- F. CAPACITACIÓN CONTINUA ----------------
    st.markdown("### 🎓 F. CAPACITACIÓN CONTINUA")
    ed_cap = st.data_editor(
        st.session_state["et_cap"], use_container_width=True, hide_index=True, key="et_ed_cap", disabled=["Área"],
        column_config={
            "Personal total": st.column_config.NumberColumn(min_value=0, step=1),
            "Capacitados en bioética": st.column_config.NumberColumn(min_value=0, step=1),
            "Horas de formación": st.column_config.NumberColumn(min_value=0, step=1),
        })
    r_cap = calcular_capacitacion(ed_cap)
    if len(r_cap["tabla"]) > 0:
        fig_cap = px.bar(r_cap["tabla"], x="Área", y="% cobertura", text=r_cap["tabla"]["% cobertura"].round(0).astype(int).astype(str) + " %",
                         color_discrete_sequence=PLOTLY_CYBER_THEME)
        fig_cap.update_yaxes(range=[0, 105], gridcolor="rgba(0, 210, 255, 0.15)")
        st.plotly_chart(_layout_cyber(fig_cap, 280), use_container_width=True, key="et_cap_fig")
        st.caption("Cobertura = personal capacitado en dilemas bioéticos, humanización y derechos de los pacientes / personal total.")

    st.markdown("---")

    # ---------------- G. SEÑALES DE EQUIDAD ----------------
    st.markdown("### ⚖️ G. SEÑALES DE EQUIDAD EN LOS SERVICIOS")
    st.caption("Usa la base de datos cargada y respeta los filtros de la barra lateral. Es una SEÑAL para que el comité revise, "
               "no una prueba de discriminación.")
    eq_score, eq_tabla, eq_media = calcular_equidad(base_df)
    if eq_tabla.empty:
        st.warning("No se pudo evaluar la equidad: la base necesita la columna 'Días estancia' y al menos una de: "
                   "'Aseguradora', 'Edad' o 'Servicio actual'. Esta dimensión se excluye del índice global.")
    else:
        st.markdown(f"Estancia promedio general (con los filtros activos): **{eq_media:.1f} días**. "
                    f"Se marca alerta si un grupo (con al menos {MIN_N_EQUIDAD} atenciones) se desvía más de {UMBRAL_EQUIDAD} %.")
        vista = eq_tabla.copy()
        vista["Alerta"] = np.where(vista["Alerta"], "🚨 Revisar", np.where(vista["Evaluable"], "✅ Normal", "ℹ️ Muestra pequeña"))
        vista = vista.drop(columns="Evaluable").round({"Estancia promedio (días)": 1, "Desviación vs. promedio (%)": 1})
        st.dataframe(vista, use_container_width=True, hide_index=True)
        graf = eq_tabla[eq_tabla["Evaluable"]]
        if len(graf) > 0:
            fig_eq = px.bar(graf, x="Desviación vs. promedio (%)", y="Grupo", color="Dimensión", orientation="h",
                            color_discrete_sequence=PLOTLY_CYBER_THEME)
            fig_eq.add_vline(x=UMBRAL_EQUIDAD, line_dash="dash", line_color="#FF2A54")
            fig_eq.add_vline(x=-UMBRAL_EQUIDAD, line_dash="dash", line_color="#FF2A54")
            fig_eq.update_layout(xaxis=dict(gridcolor="rgba(0, 210, 255, 0.15)"),
                                 legend=dict(orientation="h", yanchor="bottom", y=-0.35, title=None))
            st.plotly_chart(_layout_cyber(fig_eq, max(280, 28 * len(graf) + 120)), use_container_width=True, key="et_eq_fig")

    st.markdown("---")

    # ---------------- ENSAMBLE DE INDICADORES ----------------
    dims = {
        "composicion": comp_total,
        "pluralidad": plur_total,
        "transparencia": transp,
        "pqrs": pqrs_score,
        "capacitacion": r_cap["pct"],
        "equidad": eq_score,
    }

    # Afiliación: cuántos sectores de participación (no médicos) tienen representante con voz y voto en el comité hospitalario
    afil = [x["Avance"] for x in res_h["detalle"] if x["Sector"] != "Médico"]
    afiliacion = float(np.mean(afil) * 100) if afil else 0.0
    niveles_auto = calcular_niveles_piramide({
        "pluralidad": plur_total, "transparencia": transp, "composicion": comp_total,
        "pct_reunion": r_ses["pct_reunion"], "afiliacion": afiliacion,
        "pct_pqrs": r_pq["pct_tiempo"], "sat_100": sat_100,
        "capacitacion": r_cap["pct"], "equidad": eq_score, "rendicion": rendicion})

    # ---------------- C. PIRÁMIDE ----------------
    st.markdown("### 🔺 C. PIRÁMIDE DE NECESIDADES ÉTICAS Y DE ATENCIÓN CENTRADA EN EL USUARIO")
    with st.expander("⚙️ Ajustar los niveles manualmente (opcional)"):
        manual = st.checkbox("Usar valores manuales en lugar de los calculados", key="et_pir_manual")
        niveles = []
        for i, nombre in enumerate(NIVELES_PIRAMIDE):
            val = st.slider(f"Nivel {i + 1} · {nombre}", 0, 100, int(round(niveles_auto[i])), key=f"et_pir_{i}_{int(round(niveles_auto[i]))}")
            niveles.append(float(val))
        if not manual:
            niveles = niveles_auto
    st.plotly_chart(dibujar_piramide(niveles), use_container_width=True, key="et_pir_fig")
    primero_debil = next((i for i, v in enumerate(niveles) if v < UMBRAL_VERDE), None)
    if primero_debil is None:
        st.success("🟢 Los cinco niveles están en condición de cumplimiento.")
    else:
        st.error(f"🔴 El primer nivel que falla es el Nivel {primero_debil + 1}: {NIVELES_PIRAMIDE[primero_debil]} "
                 f"({niveles[primero_debil]:.0f}/100). Los niveles superiores dependen de este: corríjalo primero.")

    st.markdown("---")

    # ---------------- H. ÁRBOL DE PROBLEMAS -> INDICADORES ----------------
    st.markdown("### 🌳 H. ÁRBOL DE PROBLEMAS → INDICADORES")
    ige_tmp = promedio_ponderado([(PESOS_DEFECTO[k], v) for k, v in dims.items()])
    filas_arbol = [
        ("Causa", "Incumplimiento de la Resolución 13437 de 1991", "Cumplimiento de la composición del comité", dims["composicion"]),
        ("Causa", "Ausencia de criterios éticos en la toma de decisiones", "Conflictos declarados, quórum plural y reunión mensual", dims["transparencia"]),
        ("Causa", "Débil control y seguimiento a los servicios", "Equidad en servicios y rendición de cuentas", promedio([dims["equidad"], rendicion])),
        ("Efecto", "Sesgo en la toma de decisiones / falta de imparcialidad", "Índice de pluralidad", dims["pluralidad"]),
        ("Efecto", "Riesgo normativo, legal e institucional", "Índice Global de Ética (IGE)", ige_tmp),
        ("Efecto", "Pérdida de confianza de usuarios y comunidad", "PQRS a tiempo y satisfacción", promedio([r_pq["pct_tiempo"], sat_100])),
        ("Efecto", "Deterioro de la calidad y la humanización", "Cobertura de capacitación en bioética", dims["capacitacion"]),
    ]
    arbol = pd.DataFrame([{"Tipo": t, "Causa / efecto del manual": c, "Indicador asociado": i,
                           "Valor": fmt(v, " / 100"), "Estado": " ".join(estado_semaforo(v))} for t, c, i, v in filas_arbol])
    st.dataframe(arbol, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ---------------- A. RESUMEN SUPERIOR (se pinta en el contenedor de arriba) ----------------
    with zona_resumen:
        st.markdown("### 🚦 A. SEMÁFORO GENERAL")
        with st.expander("⚙️ Fórmula del IGE: ajustar pesos (se normalizan para sumar 100 %)"):
            pesos = {}
            cols_p = st.columns(3)
            for idx, (clave, nombre) in enumerate(NOMBRES_DIM.items()):
                pesos[clave] = cols_p[idx % 3].slider(nombre, 0, 100, PESOS_DEFECTO[clave], key=f"et_peso_{clave}")
            suma = sum(pesos.values())
            if suma == 0:
                pesos, suma = dict(PESOS_DEFECTO), 100
                st.warning("Todos los pesos estaban en 0: se usaron los pesos por defecto.")
            elif suma != 100:
                st.warning(f"Los pesos suman {suma} %: se normalizan automáticamente a 100 %.")
            else:
                st.success("Los pesos suman 100 %.")

        ige = promedio_ponderado([(pesos[k], v) for k, v in dims.items()])
        sin_datos = [NOMBRES_DIM[k] for k, v in dims.items() if v is None]

        cg, ck = st.columns([1, 1])
        with cg:
            st.plotly_chart(dibujar_gauge(ige), use_container_width=True, key="et_gauge")
        with ck:
            emoji, texto = estado_semaforo(ige)
            if ige is None:
                st.warning("No hay datos suficientes para calcular el índice.")
            elif ige >= UMBRAL_VERDE:
                st.success(f"{emoji} IGE {ige:.0f}/100 — {texto}: la institución cumple.")
            elif ige >= UMBRAL_AMARILLO:
                st.warning(f"{emoji} IGE {ige:.0f}/100 — {texto}: hay brechas por cerrar.")
            else:
                st.error(f"{emoji} IGE {ige:.0f}/100 — {texto}: alto riesgo de nueva sanción.")
            if sin_datos:
                st.caption("Dimensiones sin datos (excluidas del índice): " + ", ".join(sin_datos))
            m1, m2 = st.columns(2)
            m1.metric("CUMPLIMIENTO DE COMPOSICIÓN", f"{comp_total:.0f} %")
            m2.metric("ÍNDICE DE PLURALIDAD", f"{plur_total:.0f} / 100")
            m3, m4 = st.columns(2)
            m3.metric("% PQRS ÉTICAS A TIEMPO", "N/D" if r_pq["pct_tiempo"] is None else f"{r_pq['pct_tiempo']:.0f} %")
            m4.metric("% PERSONAL CAPACITADO", "N/D" if r_cap["pct"] is None else f"{r_cap['pct']:.0f} %")

        resumen = pd.DataFrame([{"Dimensión": NOMBRES_DIM[k], "Peso (%)": round(pesos[k] / suma * 100, 1),
                                 "Puntaje": None if v is None else round(v, 1), "Estado": " ".join(estado_semaforo(v))}
                                for k, v in dims.items()])
        st.dataframe(resumen, use_container_width=True, hide_index=True)

    # ---------------- I. PLAN DE ACCIÓN Y DESCARGA ----------------
    st.markdown("### 📋 I. PLAN DE ACCIÓN AUTOMÁTICO")
    plan = generar_plan_accion(dims)
    st.dataframe(plan, use_container_width=True, hide_index=True)

    hojas = {
        "Resumen IGE": pd.concat([pd.DataFrame([{"Dimensión": "ÍNDICE GLOBAL (IGE)", "Peso (%)": 100,
                                                "Puntaje": None if ige is None else round(ige, 1),
                                                "Estado": " ".join(estado_semaforo(ige))}]), resumen], ignore_index=True),
        "Comité hospitalario": _limpiar_comite(ed_h),
        "Comité investigación": _limpiar_comite(ed_i),
        "Sesiones": ses,
        "PQRS": ed_pq,
        "Capacitación": r_cap["tabla"],
        "Equidad": eq_tabla.drop(columns="Evaluable") if not eq_tabla.empty else None,
        "Árbol de problemas": arbol,
        "Plan de acción": plan,
    }
    try:
        datos_excel = construir_excel(hojas)
        st.download_button("⬇️ Descargar informe de evaluación ética (Excel)", data=datos_excel,
                           file_name=f"evaluacion_etica_IPS_San_Gabriel_{date.today().isoformat()}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           key="et_descarga_xlsx")
    except Exception:
        st.download_button("⬇️ Descargar plan de acción (CSV)", data=plan.to_csv(index=False).encode("utf-8-sig"),
                           file_name=f"plan_accion_etica_{date.today().isoformat()}.csv", mime="text/csv",
                           key="et_descarga_csv")

    st.markdown("---")
    st.caption("🔒 Esta pestaña trabaja con datos agregados y no debe contener nombres ni identificaciones de pacientes "
               "(Ley 1581 de 2012, habeas data). Esta herramienta apoya el seguimiento, no reemplaza la validación de un "
               "especialista en bioética ni del ente regulador.")


# ------------------------------------------------------------------------------
# PESTAÑA 5: EVALUACIÓN ÉTICA
# ------------------------------------------------------------------------------
with tab5:
    render_evaluacion_etica(df)
