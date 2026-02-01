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
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; }
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
    "INICIO", "6 PUNTOS FARO", "DASHBOARD ESTADÍSTICO IA", "GESTIÓN LEY 2173 (EMPRESAS)",
    "SUSCRIPCIONES", "DONACIONES Y CERTIFICADO", "LOGÍSTICA AEROLÍNEAS", "UBICACIÓN"
])

# 1. INICIO (CON AUDIO)
if menu == "INICIO":
    st.markdown("<h1 style='text-align:center; font-size:4rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold;'>SISTEMA REGENERATIVO BIOMÉTRICO KBA</p>", unsafe_allow_html=True)
    st.components.v1.html("""
        <audio id="audio_nature" src="https://www.soundjay.com/nature/sounds/forest-birds-01.mp3" loop></audio>
        <div style="text-align:center; margin-top:30px;">
            <button onclick="document.getElementById('audio_nature').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:20px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:16px;">🔊 ACTIVAR SONIDO AMBIENTAL KBA</button>
        </div>
    """, height=150)

# 2. LOS 6 PUNTOS FARO
elif menu == "6 PUNTOS FARO":
    st.title("🛰️ Monitoreo Perimetral")
    faros = ["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara"]
    f_cols = st.columns(3)
    for i, f in enumerate(faros):
        with f_cols[i % 3]:
            st.markdown(f"<div class='faro-card'><h3>FARO {f.upper()}</h3></div>", unsafe_allow_html=True)
            if st.button(f"INGRESAR A FARO {f}"): st.session_state.f_activo = f

    if "f_activo" in st.session_state:
        st.divider()
        st.header(f"📡 TRANSMISIÓN ACTIVA: FARO {st.session_state.f_activo.upper()}")
        cam_cols = st.columns(4)
        for j in range(8):
            with cam_cols[j % 4]: st.markdown(f"<div class='cam-grid'>CAM {j+1}<br>● LIVE</div>", unsafe_allow_html=True)
        st.subheader("Monitoreo Bioacústico")
        mic_cols = st.columns(4)
        for k in range(4):
            with mic_cols[k]: st.markdown(f"<div style='background:rgba(155,198,59,0.2); border:1px solid #2E7D32; padding:10px; border-radius:5px; text-align:center;'><b>MIC {k+1}</b><br><span style='color:#9BC63B;'>||||| {random.randint(40,90)}%</span></div>", unsafe_allow_html=True)

# 3. DASHBOARD ESTADÍSTICO IA
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("📊 Análisis de Inteligencia Biológica")
    m = st.columns(4)
    m[0].markdown("<div class='metric-card'><h3>Especies</h3><h1>1,248</h1></div>", unsafe_allow_html=True)
    m[1].markdown("<div class='metric-card'><h3>Salud Bosque</h3><h1>94%</h1></div>", unsafe_allow_html=True)
    m[2].markdown("<div class='metric-card'><h3>Alertas IA</h3><h1>12</h1></div>", unsafe_allow_html=True)
    m[3].markdown("<div class='metric-card'><h3>Área Protegida</h3><h1>86 ha</h1></div>", unsafe_allow_html=True)
    st.bar_chart(pd.DataFrame({'Detecciones': [120, 450, 300, 80, 45, 110]}, index=["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara"]))

# 4. GESTIÓN LEY 2173 (CON BOTÓN DE DESCARGA)
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Cumplimiento Ley 2173 de 2021")
    c1, c2 = st.columns(2)
    with c1: nit = st.text_input("Ingrese NIT de la Empresa")
    with c2: logo_emp = st.file_uploader("Suba su Logo Corporativo", type=["png", "jpg"])
    if nit:
        st.markdown(f"""
            <div class='ley-box'>
                <h3>ESTADO CORPORATIVO: ACTIVO (NIT {nit})</h3>
                <p>🌳 150 Árboles Monitoreados por IA</p>
                <hr>
                <p>Este registro cumple con los requerimientos de ÁREAS DE VIDA.</p>
            </div>
        """, unsafe_allow_html=True)
        st.download_button("⬇️ DESCARGAR CERTIFICADO TÉCNICO LEY 2173", data="Reporte Técnico Serenity...", file_name=f"Certificado_Ley2173_{nit}.txt")

# 5. SUSCRIPCIONES
elif menu == "SUSCRIPCIONES":
    st.title("💳 Planes de Apoyo")
    p1, p2, p3 = st.columns(3)
    with p1: 
        st.markdown("<div class='faro-card'><h3>Plan Semilla</h3><h2>$5 USD</h2><p>1 Faro / 1 Mes</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Semilla")
    with p2: 
        st.markdown("<div class='faro-card'><h3>Plan Guardián</h3><h2>$25 USD</h2><p>6 Faros / 1 Mes</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Guardián")
    with p3: 
        st.markdown("<div class='faro-card' style='border-color:#D4AF37;'><h3>Plan Halcón</h3><h2>$200 USD</h2><p>6 Faros / 6 Meses</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Halcón")

# 6. DONACIONES Y CERTIFICADO (DIPLOMA BLANCO Y VERDE)
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("🌳 Generador de Diploma de Donación")
    colA, colB = st.columns([1, 1.2])
    with colA:
        nombre_d = st.text_input("Nombre del Donante")
        monto_d = st.number_input("Monto Donado USD", min_value=1)
        if st.button("✨ GENERAR DIPLOMA"): st.session_state.v_cert = True; st.balloons()
    
    if st.session_state.get('v_cert', False):
        with colB:
            folio = datetime.now().strftime("SH-%Y%H%M")
            st.markdown(f"""
                <div class="diploma-box">
                    <h1>CERTIFICADO DE DONACIÓN</h1>
                    <p style="font-size:1.2rem;">Otorgado con profunda gratitud a:</p>
                    <h2 style="font-size:2.2rem; border-bottom: 2px solid black; padding-bottom:10px;">{nombre_d}</h2>
                    <p style="font-size:1.1rem; margin-top:20px;">Por su valiosa contribución de <b>${monto_d} USD</b></p>
                    <p>Destinados a la protección y monitoreo de la biodiversidad en el Bosque San Antonio.</p>
                    <h3 style="margin-top:30px;">SERENITY HUB S.A.S. BIC</h3>
                    <p style="font-size:0.8rem;">Folio: {folio} | Fecha: {datetime.now().strftime('%d/%m/%Y')}</p>
                    <p style="font-size:10px; margin-top:15px; color:#888 !important;">VERIFICADO POR SISTEMA NEXUS IA</p>
                </div>
            """, unsafe_allow_html=True)

# 7. LOGÍSTICA AEROLÍNEAS (NOMBRES + LOGOS)
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Rutas Globales")
    c_a, c_b = st.columns(2)
    with c_a:
        st.subheader("Europa y Asia")
        st.markdown("<div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/4/44/Iberia_Logo.svg' width='80'></div> <b>Iberia</b><br><div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Lufthansa_Logo_2018.svg' width='80'></div> <b>Lufthansa</b><br><div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/en/c/c7/Air_France_Logo.svg' width='80'></div> <b>Air France</b>", unsafe_allow_html=True)
    with c_b:
        st.subheader("América")
        st.markdown("<div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Avianca_logo.svg' width='80'></div> <b>Avianca</b><br><div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/0/00/American_Airlines_logo_2013.svg' width='80'></div> <b>American Airlines</b><br><div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/c/c2/Copa_Airlines_logo.svg' width='80'></div> <b>Copa Airlines</b>", unsafe_allow_html=True)

# 8. UBICACIÓN
elif menu == "UBICACIÓN":
    st.title("📍 Ubicación Hacienda Serenity")
    st.write("Dagua y Felidia, Valle del Cauca, Colombia.")
    st.map(pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]}))


































