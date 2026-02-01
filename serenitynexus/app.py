# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime
from PIL import Image

# CONFIGURACIÓN DE IDENTIDAD
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌳", layout="wide")

# --- DISEÑO VISUAL AVANZADO (CSS) ---
st.markdown("""
    <style>
        .stApp { 
            background-image: linear-gradient(rgba(5, 10, 4, 0.7), rgba(5, 10, 4, 0.8)), 
            url('https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1920&q=80');
            background-size: cover; background-position: center; background-attachment: fixed;
            color: #e8f5e9; font-family: 'Montserrat', sans-serif; 
        }
        
        /* TEXTOS BLANCOS Y ETIQUETAS */
        label, .stMarkdown p, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { 
            color: white !important; 
            font-weight: 500; 
        }
        [data-testid="stSidebar"] { background-color: rgba(10, 20, 8, 0.9) !important; backdrop-filter: blur(10px); }

        h1, h2, h3 { color: #9BC63B !important; font-family: 'Merriweather', serif; text-shadow: 2px 2px 4px #000; }
        
        /* BOTONES */
        .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #9BC63B; border-radius: 8px; width: 100%; font-weight: bold; }
        .stButton>button:hover { background-color: #9BC63B; color: black; box-shadow: 0 0 15px #9BC63B; }
        
        /* CONTENEDORES */
        .metric-card { background: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; border: 1px solid #9BC63B; text-align: center; }
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; }
        .cam-grid { background: #000; border: 1px solid #2E7D32; height: 80px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #ff0000; border-radius: 5px; }
        .ley-box { background: rgba(0, 0, 0, 0.7); border: 2px dashed #9BC63B; padding: 25px; border-radius: 15px; color: white; }
        
        /* CERTIFICADO PREMIUM */
        .certificate-box { 
            background: white; color: #050a04; padding: 40px; border: 10px double #D4AF37; 
            text-align: center; box-shadow: 0 0 30px rgba(0,0,0,0.8); max-width: 700px; margin: auto; 
        }
        .qr-code { background: #eee; padding: 10px; border: 1px solid #ccc; width: 80px; margin: 10px auto; font-size: 8px; }
        .logo-container { background: white; padding: 8px; border-radius: 5px; display: inline-block; margin: 3px; }
    </style>
""", unsafe_allow_html=True)

# --- SEGURIDAD ---
if "auth" not in st.session_state:
    st.markdown("<div style='text-align:center; padding-top: 50px;'>", unsafe_allow_html=True)
    try: st.image("logo_serenity.png", width=250)
    except: st.markdown("<h1>SISTEMA NEXUS | SERENITY</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
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

# 1. INICIO
if menu == "INICIO":
    st.markdown("<h1 style='text-align:center; font-size:4rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold;'>SISTEMA REGENERATIVO BIOMÉTRICO KBA</p>", unsafe_allow_html=True)
    st.components.v1.html("""
        <audio id="audio_nature" src="https://www.soundjay.com/nature/sounds/forest-birds-01.mp3" loop></audio>
        <div style="text-align:center; margin-top:30px;">
            <button onclick="document.getElementById('audio_nature').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:20px; border-radius:10px; cursor:pointer; font-weight:bold;">🔊 ACTIVAR SONIDO AMBIENTAL</button>
        </div>
    """, height=130)

# 2. LOS 6 PUNTOS FARO (ESTRUCTURA COMPLETA)
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
        st.header(f"📡 TRANSMISIÓN: FARO {st.session_state.f_activo.upper()}")
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
    st.bar_chart(pd.DataFrame({'Detecciones': [120, 450, 300, 80, 45, 110]}, index=["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara"]))

# 4. GESTIÓN LEY 2173 (EMPRESAS)
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Cumplimiento Ley 2173 de 2021")
    st.markdown("<p style='color:white;'>Gestión de 'Áreas de Vida' para el sector corporativo BIC.</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: nit = st.text_input("Ingrese NIT de la Empresa")
    with c2: uploaded_logo = st.file_uploader("Logo Empresa", type=["png", "jpg"])
    if nit:
        st.markdown("<div class='ley-box'>", unsafe_allow_html=True)
        if uploaded_logo: st.image(uploaded_logo, width=120)
        st.markdown(f"<h3>ESTADO: ACTIVO (NIT {nit})</h3><p>🌳 150 Árboles en Monitoreo</p></div>", unsafe_allow_html=True)

# 6. DONACIONES Y CERTIFICADO (RESTAURADO + QR + FOLIO)
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("🌳 Certificación Oficial Serenity Hub")
    colA, colB = st.columns([1, 1.2])
    with colA:
        nombre_d = st.text_input("Nombre del Donante")
        monto_d = st.number_input("Monto (USD)", min_value=1)
        if st.button("✨ GENERAR CERTIFICADO"): 
            st.session_state.ver_cert = True
            st.balloons()
    if st.session_state.get('ver_cert', False):
        folio = datetime.now().strftime("SH-2026-%H%M%S")
        with colB:
            st.markdown(f"""
                <div class="certificate-box">
                    <h1 style="color:#2E7D32; margin:0;">CERTIFICADO DE IMPACTO</h1>
                    <p style="color:#D4AF37; font-weight:bold; letter-spacing:2px;">GUARDIÁN DEL BOSQUE KBA</p>
                    <p>Serenity Hub S.A.S. BIC certifica que:</p>
                    <h2 style="text-transform:uppercase; color:#000; border-bottom: 2px solid #eee;">{nombre_d}</h2>
                    <p>Ha realizado una donación de <b>${monto_d} USD</b></p>
                    <p>Para la regeneración y protección biométrica de San Antonio.</p>
                    <hr>
                    <h3 style="margin:0;">SERENITY HUB S.A.S. BIC</h3>
                    <p style="font-size:0.8rem; color:#666;">Folio: {folio} | Fecha: {datetime.now().strftime('%d/%m/%Y')}</p>
                    <div class="qr-code">SCAN PARA VERIFICAR<br><br><b>[ QR VALID ]</b></div>
                </div>
            """, unsafe_allow_html=True)

# 7. LOGÍSTICA AEROLÍNEAS (COMPLETA)
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Rutas Globales a Serenity")
    st.markdown("<p style='color:white;'>Conectividad internacional vía Cali (CLO).</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Europa / Asia")
        st.markdown("<div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/4/44/Iberia_Logo.svg' width='70'></div><div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Lufthansa_Logo_2018.svg' width='70'></div>", unsafe_allow_html=True)
        st.write("- Iberia (Madrid)\n- Lufthansa (Frankfurt)\n- Turkish (Estambul)")
    with c2:
        st.subheader("América")
        st.markdown("<div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Avianca_logo.svg' width='70'></div><div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/c/c2/Copa_Airlines_logo.svg' width='70'></div>", unsafe_allow_html=True)
        st.write("- Avianca / Latam\n- Copa (Hub Panamá)\n- American / United")

# 5. SUSCRIPCIONES (INTEGRADA) / 8. UBICACIÓN
elif menu == "SUSCRIPCIONES":
    st.title("💳 Planes")
    st.columns(3)[1].markdown("<div class='faro-card'><h3>PLAN GUARDIÁN</h3><h1>$25 USD</h1></div>", unsafe_allow_html=True)
elif menu == "UBICACIÓN":
    st.title("📍 Ubicación")
    st.map(pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]}))






























