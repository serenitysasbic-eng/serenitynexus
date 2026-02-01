# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime

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
        label, .stMarkdown p, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { 
            color: white !important; font-weight: 500; 
        }
        [data-testid="stSidebar"] { background-color: rgba(10, 20, 8, 0.9) !important; backdrop-filter: blur(10px); }
        h1, h2, h3 { color: #9BC63B !important; text-shadow: 2px 2px 4px #000; }
        .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #9BC63B; border-radius: 8px; width: 100%; font-weight: bold; }
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; }
        .cam-grid { background: #000; border: 1px solid #2E7D32; height: 80px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #ff0000; border-radius: 5px; }
        .ley-box { background: rgba(0, 0, 0, 0.7); border: 2px dashed #9BC63B; padding: 25px; border-radius: 15px; color: white; }
        .certificate-box { background: white; color: #050a04; padding: 40px; border: 10px double #D4AF37; text-align: center; max-width: 650px; margin: auto; }
        .logo-container { background: white; padding: 8px; border-radius: 5px; display: inline-block; margin: 3px; }
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
    "SUSCRIPCIONES", "DONACIONES Y CERTIFICADO PERSONAS", "LOGÍSTICA AEROLÍNEAS", "UBICACIÓN"
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

# 2. LOS 6 PUNTOS FARO (8 CÁMARAS + 4 MICROS)
elif menu == "6 PUNTOS FARO":
    st.title("🛰️ Monitoreo Perimetral - 6 Nodos")
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
    m[1].markdown("<div class='metric-card'><h3>Salud</h3><h1>94%</h1></div>", unsafe_allow_html=True)
    m[2].markdown("<div class='metric-card'><h3>Alertas</h3><h1>12</h1></div>", unsafe_allow_html=True)
    m[3].markdown("<div class='metric-card'><h3>Área</h3><h1>86 ha</h1></div>", unsafe_allow_html=True)

# 4. GESTIÓN LEY 2173 (CON GENERADOR DE CERTIFICADO EMPRESARIAL)
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Cumplimiento Ley 2173 de 2021")
    st.markdown("<p style='color:white;'>Gestión de 'Áreas de Vida' y Certificación Corporativa.</p>", unsafe_allow_html=True)
    
    col_config, col_cert = st.columns([1, 1.2])
    
    with col_config:
        nombre_empresa = st.text_input("Nombre de la Empresa Aliada")
        nit_empresa = st.text_input("NIT de la Empresa")
        arboles = st.number_input("Número de Árboles Sembrados", min_value=1, value=50)
        uploaded_logo = st.file_uploader("Suba el Logo de la Empresa para el Certificado", type=["png", "jpg"])
        
        if st.button("🌟 GENERAR CERTIFICADO CORPORATIVO"):
            st.session_state.cert_corp = True
            st.balloons()

    if st.session_state.get('cert_corp', False):
        with col_cert:
            st.markdown(f"""
                <div class="certificate-box">
                    <div style="text-align:right; font-size:0.7rem;">SH-BIC-2173-{random.randint(1000,9999)}</div>
                    <h2 style="color:#2E7D32;">SERENITY HUB S.A.S. BIC</h2>
                    <p>Reconoce a:</p>
                    <h3 style="text-transform:uppercase; color:#000;">{nombre_empresa}</h3>
                    <p>NIT: {nit_empresa}</p>
                    <hr>
                    <p>Por su compromiso con la <b>Ley 2173 de 2021</b> mediante la siembra y mantenimiento de:</p>
                    <h2 style="color:#2E7D32;">{arboles} ÁRBOLES NATIVOS</h2>
                    <p>En el Área de Vida Protegida: <b>KBA Bosque San Antonio</b></p>
                    <div style="margin-top:20px;">
                        {"<img src='data:image/png;base64,...' width='100'>" if uploaded_logo else "<i>Logo Empresa Aliada</i>"}
                    </div>
                    <p style="font-size:0.8rem; margin-top:20px;">Verificado por Sistema Nexus IA | {datetime.now().strftime('%d/%m/%Y')}</p>
                </div>
            """, unsafe_allow_html=True)

# 5. SUSCRIPCIONES (RESTAURADO)
elif menu == "SUSCRIPCIONES":
    st.title("💳 Planes de Apoyo")
    p = st.columns(3)
    p[0].markdown("<div class='faro-card'><h3>Plan Semilla</h3><h2>$5 USD</h2></div>", unsafe_allow_html=True)
    p[1].markdown("<div class='faro-card'><h3>Plan Guardián</h3><h2>$25 USD</h2></div>", unsafe_allow_html=True)
    p[2].markdown("<div class='faro-card' style='border-color:#D4AF37;'><h3>Plan Halcón</h3><h2>$200 USD</h2></div>", unsafe_allow_html=True)

# 6. DONACIONES Y CERTIFICADO PERSONAS
elif menu == "DONACIONES Y CERTIFICADO PERSONAS":
    st.title("🌳 Certificado para Personas Naturales")
    n_p = st.text_input("Nombre"); m_p = st.number_input("Monto USD", min_value=1)
    if st.button("GENERAR"):
        st.markdown(f"<div class='certificate-box'><h2>CERTIFICADO</h2><p>{n_p}</p><p>${m_p} USD</p></div>", unsafe_allow_html=True)

# 7. LOGÍSTICA AEROLÍNEAS (LOGOS RESTAURADOS)
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Conectividad Global")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Europa / Asia")
        st.markdown("<div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/4/44/Iberia_Logo.svg' width='80'></div> <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Lufthansa_Logo_2018.svg' width='80'></div>", unsafe_allow_html=True)
    with c2:
        st.subheader("América")
        st.markdown("<div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Avianca_logo.svg' width='80'></div> <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/c/c2/Copa_Airlines_logo.svg' width='80'></div>", unsafe_allow_html=True)

# 8. UBICACIÓN
elif menu == "UBICACIÓN":
    st.title("📍 Ubicación")
    st.write("Dagua y Felidia, Valle del Cauca.")
    st.map(pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]}))
































