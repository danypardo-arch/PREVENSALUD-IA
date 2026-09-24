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
# 2. ENCABEZADO CON LOGO CENTRADO Y AJUSTADO
# ==============================================================================
# Usamos proporciones de columnas para centrar el logo y darle un tamaño elegante
col_izq, col_logo, col_der = st.columns([1.2, 2.6, 1.2])

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
    st.title("🏥 PREVENSALUD IA")
    st.markdown("<p style='text-align: center; color: gray;'>Plataforma Inteligente de Analítica Predictiva y Gestión Operativa Hospitalaria</p>", unsafe_allow_html=True)

st.markdown("---")

# ==============================================================================
# 3. BARRA LATERAL (CONFIGURACIÓN Y FILTROS)
# ==============================================================================
st.sidebar.header("⚙️ Configuración y Filtros")
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
# PESTAÑA 2: SIMULADOR PREDICTIVO IA CON RANGO DE FECHAS
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("🔮 Estimación, Análisis de Período y Predicción Futura (IA)")
    st.write("Defina un **Rango de Fechas** para evaluar la información histórica real y proyectar la demanda del período futuro.")
    
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
        
        st.markdown("---")
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

        if st.button("🚀 Ejecutar Análisis de Período y Proyección IA", type="primary"):
            st.markdown("---")
            
            if not es_futuro:
                st.markdown(f"### 📋 Análisis Histórico en Tiempo Real ({fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')})")
                
                if col_fecha and 'Fecha_Solo_Dia' in df_base.columns:
                    df_rango = df_base[(df_base['Fecha_Solo_Dia'] >= fecha_inicio) & (df_base['Fecha_Solo_Dia'] <= fecha_fin)]
                    ingresos_reales = len(df_rango)
                    
                    r1, r2, r3, r4 = st.columns(4)
                    r1.metric("Ingresos Totales en Período", f"{ingresos_reales} pacientes")
                    r2.metric("Duración Evaluada", f"{dias_periodo} días")
                    
                    if col_estancia and ingresos_reales > 0:
                        r3.metric("Promedio Estancia Registrada", f"{df_rango[col_estancia].mean():.1f} días")
                    else:
                        r3.metric("Promedio Estancia Registrada", "N/A")
                        
                    promedio_diario = round(ingresos_reales / dias_periodo, 1) if dias_periodo > 0 else 0
                    r4.metric("Promedio Ingresos/Día", f"{promedio_diario} pac/día")
                    
                    if ingresos_reales > 0:
                        st.markdown("**Tendencia de Atenciones en el Período Seleccionado:**")
                        df_trend = df_rango.groupby('Fecha_Solo_Dia').size().reset_index(name='Atenciones')
                        fig_line = px.line(df_trend, x='Fecha_Solo_Dia', y='Atenciones', markers=True, title="Flujo Diario de Pacientes")
                        st.plotly_chart(fig_line, use_container_width=True)
                        
                        st.dataframe(df_rango, use_container_width=True)
                    else:
                        st.warning(f"No se registraron atenciones entre el {fecha_inicio.strftime('%d/%m/%Y')} y el {fecha_fin.strftime('%d/%m/%Y')}.")
                else:
                    st.warning("No se detectó una columna de fecha válida en el archivo.")
            
            # PROYECCIÓN PREDICTIVA A FUTURO
            st.markdown(f"### 🔮 Proyección Predictiva IA para el Siguiente Período ({dias_periodo} días)")
            
            factor_jornada = 1.3 if jornada == "Noche" else (1.1 if jornada == "Tarde" else 1.0)
            factor_clima = 1.4 if clima == "Pico Epidemiológico / Pandemia" else (1.25 if clima == "Lluvia Intensa" else (1.1 if clima == "Lluvia Moderada" else 1.0))
            
            estimacion_diaria = int((medicos_input * 2.8 + enfermeros_input * 1.3) * factor_jornada * factor_clima)
            estimacion_total_periodo = estimacion_diaria * dias_periodo
            ocupacion_proyectada = min(100.0, ((camas_ocupadas + (estimacion_diaria * 0.45)) / camas_totales) * 100)
            
            p1, p2, p3 = st.columns(3)
            p1.metric(f"Afluencia Proyectada ({dias_periodo} días)", f"{estimacion_total_periodo:,} pacientes")
            p2.metric("Ocupación Promedio de Camas", f"{ocupacion_proyectada:.1f}%")
            p3.metric("Demanda Diaria Estimada", f"~{estimacion_diaria} pac/día")
            
            if ocupacion_proyectada < 75:
                st.success("🟢 **RIESGO BAJO:** Capacidad óptima para el período evaluado.")
            elif ocupacion_proyectada < 90:
                st.warning("🟡 **RIESGO MODERADO:** Se recomienda reforzar personal en turnos pico y agilizar altas.")
            else:
                st.error("🔴 **RIESGO CRÍTICO / SOBRECAPACIDAD:** Alto riesgo de saturación hospitalaria en el período proyectado.")

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
