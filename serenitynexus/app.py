# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime
from PIL import Image
import base64

# CONFIGURACIÓN DE IDENTIDAD
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌳", layout="wide")

# --- DISEÑO VISUAL Y ESTILOS (CSS) ---
st.markdown("""
    <style>
        .stApp { 
            background-image: linear-gradient(rgba(5, 10, 4, 0.7), rgba(5, 10, 4, 0.8)), 
            url('https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1920&q=80');
            background-size: cover; background-position: center; background-attachment: fixed;
            color: #e8f5e9; font-family: 'Montserrat', sans-serif; 
        }
        
        /* TEXTOS BLANCOS GENERALES */
        label, .stMarkdown p, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { 
            color: white !important; font-weight: 500; 
        }
        [data-testid="stSidebar"] { background-color: rgba(10, 20, 8, 0.9) !important; backdrop-filter: blur(10px); }
        h1, h2, h3 { color: #9BC63B !important; text-shadow: 2px 2px 4px #000; }
        
        /* BOTONES */
        .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #9BC63B; border-radius: 8px; width: 100%; font-weight: bold; }
        
        /* TARJETAS Y CUADROS */
        .metric-card { background: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; border: 1px solid #9BC63B; text-align: center; }
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; height: 100%; }
        
        /* FARO GEMINI ESPECIAL */
        .faro-gemini { border: 2px solid #4285F4; padding: 15px; border-radius: 10px; background: rgba(66, 133, 244, 0.2); text-align: center; box-shadow: 0 0 15px #4285F4; }
        
        .cam-grid { background: #000; border: 1px solid #2E7D32; height: 80px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #ff0000; border-radius: 5px; }
        
        /* DIPLOMA BLANCO (ESTILO DONACIÓN) */
        .diploma-box { 
            background: white !important; 
            color: black !important; 
            padding: 40px; 
            border: 15px double #2E7D32; 
            text-align: center; 
            max-width: 700px; 
            margin: auto;
            box-shadow: 0 0 30px rgba(0,0,0,0.5);
        }
        .diploma-box h1 { color: #2E7D32 !important; text-shadow: none !important; margin-bottom: 5px; }
        .diploma-box p, .diploma-box h2, .diploma-box h3 { color: black !important; text-shadow: none !important; }

        /* LOGOS AEROLÍNEAS */
        .logo-container { background: white; padding: 8px; border-radius: 5px; display: inline-block; margin: 3px; vertical-align: middle; }
    </style>
""", unsafe_allow_html=True)

# --- SEGURIDAD ---
if "auth" not in st.session_state:
    st.markdown("<div style='text-align:center; padding-top: 50px;'><h1>SISTEMA NEXUS | SERENITY</h1></div>", unsafe_allow_html=True)
    col_sec = st.columns([1,1,1])
    with col_sec[1]:
        clave = st.text_input("PASSWORD ADMIN", type="password")
        if st.button("INGRESAR"):
            if clave == "Serenity2026":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- NAVEGACIÓN ---
menu = st.sidebar.radio("CENTRO DE CONTROL", [
    "INICIO", "RED DE FAROS (7 NODOS)", "DASHBOARD ESTADÍSTICO IA", "GESTIÓN LEY 2173 (EMPRESAS)",
    "SUSCRIPCIONES", "DONACIONES Y CERTIFICADO", "LOGÍSTICA AEROLÍNEAS", "UBICACIÓN"
])

# 1. INICIO (CON AUDIO EARTH)
if menu == "INICIO":
    st.markdown("<h1 style='text-align:center; font-size:4rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold;'>SISTEMA REGENERATIVO BIOMÉTRICO KBA</p>", unsafe_allow_html=True)
    st.components.v1.html("""
        <audio id="audio_earth" src="sonido_Earth.mp3" loop></audio>
        <div style="text-align:center; margin-top:30px;">
            <button onclick="document.getElementById('audio_earth').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:20px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:16px;">🔊 ACTIVAR SONIDO GLOBAL EARTH</button>
        </div>
    """, height=150)

# 2. RED DE FAROS (AHORA SON 7 CON GEMINI)
elif menu == "RED DE FAROS (7 NODOS)":
    st.title("🛰️ Monitoreo Perimetral - Red Neural")
    
    # Fila 1: Faros Físicos
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown("<div class='faro-card'><h3>FARO HALCÓN</h3></div>", unsafe_allow_html=True); st.button("Conectar Halcón")
    with c2: st.markdown("<div class='faro-card'><h3>FARO COLIBRÍ</h3></div>", unsafe_allow_html=True); st.button("Conectar Colibrí")
    with c3: st.markdown("<div class='faro-card'><h3>FARO RANA</h3></div>", unsafe_allow_html=True); st.button("Conectar Rana")
    
    # Fila 2: Faros Físicos
    st.write("")
    c4, c5, c6 = st.columns(3)
    with c4: st.markdown("<div class='faro-card'><h3>FARO VENADO</h3></div>", unsafe_allow_html=True); st.button("Conectar Venado")
    with c5: st.markdown("<div class='faro-card'><h3>FARO TIGRILLO</h3></div>", unsafe_allow_html=True); st.button("Conectar Tigrillo")
    with c6: st.markdown("<div class='faro-card'><h3>FARO CAPIBARA</h3></div>", unsafe_allow_html=True); st.button("Conectar Capibara")

    # Fila 3: FARO GEMINI (Central de Inteligencia)
    st.write("---")
    st.markdown("<h3 style='text-align:center; color:#4285F4;'>NODO CENTRAL DE INTELIGENCIA</h3>", unsafe_allow_html=True)
    col_gemini = st.columns([1,2,1])
    with col_gemini[1]:
        st.markdown("<div class='faro-gemini'><h3>✨ FARO GEMINI ✨</h3><p>Procesamiento Neural & Protección de Datos</p></div>", unsafe_allow_html=True)
        if st.button("ACCEDER AL NÚCLEO GEMINI"): st.session_state.f_activo = "GEMINI"

    if "f_activo" in st.session_state:
        st.divider()
        color_titulo = "#4285F4" if st.session_state.f_activo == "GEMINI" else "#9BC63B"
        st.markdown(f"<h2 style='color:{color_titulo};'>📡 TRANSMISIÓN EN VIVO: {st.session_state.f_activo}</h2>", unsafe_allow_html=True)
        
        c_cols = st.columns(4)
        for j in range(8):
            label = "IA-ANALYSIS" if st.session_state.f_activo == "GEMINI" else "LIVE"
            with c_cols[j % 4]: st.markdown(f"<div class='cam-grid'>CAM {j+1}<br>● {label}</div>", unsafe_allow_html=True)
        
        st.subheader("Análisis Bioacústico")
        m_cols = st.columns(4)
        for k in range(4):
            val = random.randint(85,99) if st.session_state.f_activo == "GEMINI" else random.randint(40,90)
            with m_cols[k]: st.markdown(f"<div style='background:rgba(155,198,59,0.2); border:1px solid #2E7D32; padding:10px; border-radius:5px; text-align:center;'><b>MIC {k+1}</b><br><span style='color:#9BC63B;'>||||| {val}%</span></div>", unsafe_allow_html=True)

# 3. DASHBOARD ESTADÍSTICO IA
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("📊 Análisis de Inteligencia Biológica")
    m = st.columns(4)
    m[0].markdown("<div class='metric-card'><h3>Especies</h3><h1>1,248</h1></div>", unsafe_allow_html=True)
    m[1].markdown("<div class='metric-card'><h3>Salud Bosque</h3><h1>94%</h1></div>", unsafe_allow_html=True)
    m[2].markdown("<div class='metric-card'><h3>Alertas IA</h3><h1>12</h1></div>", unsafe_allow_html=True)
    m[3].markdown("<div class='metric-card'><h3>Área Protegida</h3><h1>87 ha</h1></div>", unsafe_allow_html=True) # Sumé la hectárea Gemini
    st.divider()
    st.subheader("Detecciones por Punto Faro (24h)")
    st.bar_chart(pd.DataFrame({'Detecciones': [120, 450, 300, 80, 45, 110, 950]}, index=["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara", "GEMINI (Global)"]))

# 4. GESTIÓN LEY 2173
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Cumplimiento Ley 2173 de 2021")
    c1, c2 = st.columns(2)
    with c1: nit = st.text_input("Ingrese NIT de la Empresa")
    with c2: logo_emp = st.file_uploader("Suba Logo Corporativo", type=["png", "jpg"])
    if nit:
        st.markdown(f"<div class='metric-card' style='text-align:left;'><h3>EMPRESA ACTIVA: NIT {nit}</h3><p>🌳 150 Árboles Monitoreados</p></div>", unsafe_allow_html=True)
        st.download_button("⬇️ DESCARGAR CERTIFICADO LEY 2173", data=f"Reporte NIT {nit}", file_name=f"Certificado_Ley2173.txt")

# 5. SUSCRIPCIONES
elif menu == "SUSCRIPCIONES":
    st.title("💳 Planes de Apoyo Regenerativo")
    p1, p2, p3 = st.columns(3)
    with p1: 
        st.markdown("<div class='faro-card'><h3>Plan Semilla</h3><h2>$5 USD</h2><p>1 Faro / 1 Mes</p></div>", unsafe_allow_html=True)
        if st.button("SUSCRIBIRSE SEMILLA"): st.success("Redirigiendo...")
    with p2: 
        st.markdown("<div class='faro-card'><h3>Plan Guardián</h3><h2>$25 USD</h2><p>6 Faros / 1 Mes</p></div>", unsafe_allow_html=True)
        if st.button("SUSCRIBIRSE GUARDIÁN"): st.success("Redirigiendo...")
    with p3: 
        st.markdown("<div class='faro-card' style='border-color:#D4AF37;'><h3>Plan Halcón</h3><h2>$200 USD</h2><p>6 Faros / 6 Meses</p></div>", unsafe_allow_html=True)
        if st.button("SUSCRIBIRSE HALCÓN"): st.success("Redirigiendo...")

# 6. DONACIONES Y CERTIFICADO
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("🌳 Generador de Diploma")
    cA, cB = st.columns([1, 1.2])
    with cA:
        nombre_d = st.text_input("Nombre Completo")
        monto_d = st.number_input("Monto Donación (USD)", min_value=1)
        if st.button("✨ GENERAR DIPLOMA"): st.session_state.v_cert = True; st.balloons()
    if st.session_state.get('v_cert', False):
        with cB:
            st.markdown(f"""
                <div class="diploma-box">
                    <h1>CERTIFICADO DE DONACIÓN</h1>
                    <p>Otorgado con gratitud a:</p>
                    <h2 style="font-size:2rem; border-bottom: 2px solid black;">{nombre_d}</h2>
                    <p>Por su contribución de <b>${monto_d} USD</b></p>
                    <p>Protección y Monitoreo Biométrico - Bosque San Antonio</p>
                    <hr>
                    <h3 style="margin:0;">SERENITY S.A.S. BIC</h3>
                    <p style="font-size:0.7rem;">Folio: SH-{random.randint(1000,9999)} | {datetime.now().strftime('%d/%m/%Y')}</p>
                </div>
            """, unsafe_allow_html=True)

# 7. LOGÍSTICA AEROLÍNEAS
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Rutas Globales")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Europa / Asia")
        st.markdown("""
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/4/44/Iberia_Logo.svg' width='80'></div> <b>Iberia</b><br>
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Lufthansa_Logo_2018.svg' width='80'></div> <b>Lufthansa</b><br>
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/en/c/c7/Air_France_Logo.svg' width='80'></div> <b>Air France</b><br>
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/c/c3/Turkish_Airlines_logo_2019.svg' width='80'></div> <b>Turkish Airlines</b>
        """, unsafe_allow_html=True)
    with col2:
        st.subheader("América")
        st.markdown("""
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Avianca_logo.svg' width='80'></div> <b>Avianca</b><br>
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/0/00/American_Airlines_logo_2013.svg' width='80'></div> <b>American Airlines</b><br>
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/c/c2/Copa_Airlines_logo.svg' width='80'></div> <b>Copa Airlines</b>
        """, unsafe_allow_html=True)

# 8. UBICACIÓN
elif menu == "UBICACIÓN":
    st.title("📍 Ubicación Hacienda Serenity")
    st.write("Dagua y Felidia, Valle del Cauca, Colombia.")
    st.map(pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]}))






































