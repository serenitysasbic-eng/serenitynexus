# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime

# CONFIGURACIÓN DE IDENTIDAD
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌳", layout="wide")

# --- DISEÑO VISUAL UNIFICADO (CSS) ---
st.markdown("""
    <style>
        .stApp { background-color: #050a04; color: #e8f5e9; font-family: 'Montserrat', sans-serif; }
        h1, h2, h3 { color: #9BC63B; font-family: 'Merriweather', serif; }
        .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #9BC63B; border-radius: 8px; width: 100%; }
        .stButton>button:hover { background-color: #9BC63B; color: black; box-shadow: 0 0 15px #9BC63B; }
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.5); text-align: center; }
        .cam-grid { background: #000; border: 1px solid #2E7D32; height: 100px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #ff0000; border-radius: 5px; }
        .mic-bar { background: rgba(155, 198, 59, 0.2); border: 1px solid #2E7D32; padding: 5px; border-radius: 5px; text-align: center; font-size: 12px; }
        .pago-contenedor { background: white; padding: 20px; border-radius: 10px; text-align: center; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- SEGURIDAD ---
if "auth" not in st.session_state:
    st.markdown("<h1 style='text-align:center;'>SISTEMA NEXUS | SERENITY</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        clave = st.text_input("PASSWORD ADMIN", type="password")
        if st.button("INGRESAR"):
            if clave == "Serenity2026":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- NAVEGACIÓN LATERAL ---
menu = st.sidebar.radio("CENTRO DE CONTROL", [
    "INICIO", 
    "6 PUNTOS FARO", 
    "SUSCRIPCIONES", 
    "DONACIONES Y CERTIFICADO", 
    "LOGÍSTICA AEROLÍNEAS", 
    "UBICACIÓN"
])

# 1. INICIO
if menu == "INICIO":
    st.markdown("<h1 style='text-align:center; font-size:4rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; color:#9BC63B;'>SISTEMA REGENERATIVO BIOMÉTRICO</p>", unsafe_allow_html=True)
    st.components.v1.html("""
        <audio id="audio" src="sonido_bosque.m4a" loop></audio>
        <div style="text-align:center; margin-top:20px;">
            <button onclick="document.getElementById('audio').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:15px; border-radius:5px; cursor:pointer; font-weight:bold;">🔊 ACTIVAR CANAL AUDITIVO HACIENDA</button>
        </div>
    """, height=100)

# 2. LOS 6 PUNTOS FARO (VIGILANCIA COMPLETA)
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
        
        st.subheader("8 Cámaras de Seguridad (Streaming)")
        cam_cols = st.columns(4)
        for j in range(8):
            with cam_cols[j % 4]:
                st.markdown(f"<div class='cam-grid'>CAM {j+1}<br>● LIVE</div>", unsafe_allow_html=True)
        
        st.subheader("4 Micrófonos Bioacústicos")
        mic_cols = st.columns(4)
        for k in range(4):
            with mic_cols[k]:
                st.markdown(f"<div class='mic-bar'>MIC {k+1}<br><span style='color:#9BC63B;'>|||||||||| {random.randint(30,95)}%</span></div>", unsafe_allow_html=True)

# 3. SUSCRIPCIONES (PLANES Y PAGOS)
elif menu == "SUSCRIPCIONES":
    st.title("💳 Planes de Apoyo Regenerativo")
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("<div style='border:1px solid #9BC63B; padding:20px; border-radius:10px;'><h3>Plan Semilla</h3><h2>$5 USD</h2><p>1 Punto Faro/1 mes</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Semilla")
    with p2:
        st.markdown("<div style='border:1px solid #9BC63B; padding:20px; border-radius:10px;'><h3>Plan Guardián</h3><h2>$25 USD</h2><p>6 Puntos Faro/1 mes</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Guardián")
    with p3:
        st.markdown("<div style='border:1px solid #D4AF37; padding:20px; border-radius:10px;'><h3>Plan Halcon</h3><h2>$200 USD</h2><p>6 Puntos Faro/6 meses</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Heroe")
    
    st.markdown("""
        <div class="pago-contenedor">
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg" width="100"> &nbsp;&nbsp;&nbsp;
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/ba/Stripe_Logo%2C_revised_2016.svg" width="100"> &nbsp;&nbsp;&nbsp;
            <img src="https://www.payulatam.com/co/wp-content/uploads/sites/2/2017/08/logo-payu.png" width="80">
        </div>
    """, unsafe_allow_html=True)

# 4. DONACIONES Y CERTIFICADO
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("🌳 Generador de Impacto")
    colA, colB = st.columns(2)
    with colA:
        st.subheader("Donación Voluntaria")
        nombre_d = st.text_input("Nombre del Donante")
        monto_d = st.number_input("Monto (USD)", min_value=1)
        if st.button("PROCESAR Y GENERAR CERTIFICADO"):
            st.balloons()
            st.session_state.ver_cert = True
    
    if "ver_cert" in st.session_state:
        with colB:
            st.markdown(f"""
                <div style="background:white; color:#050a04; padding:30px; border:8px double #D4AF37; text-align:center; font-family:serif;">
                    <h1 style="color:#2E7D32;">CERTIFICADO DE GUARDIÁN</h1>
                    <p>Serenity SAS BIC certifica que:</p>
                    <h2 style="color:black;">{nombre_d}</h2>
                    <p>Ha contribuido con <b>{monto_d} USD</b></p>
                    <p>a la regeneración del KBA San Antonio.</p>
                    <hr>
                    <small>{datetime.now().strftime('%d/%m/%Y')} - Cali, Colombia</small>
                </div>
            """, unsafe_allow_html=True)

# 5. LOGÍSTICA AEROLÍNEAS
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Rutas Globales a Colombia")
    st.info("Conexiones directas para visitantes internacionales de Serenity.")
    c_a1, c_a2 = st.columns(2)
    with c_a1:
        st.subheader("Europa y Asia")
        st.write("- **Iberia/Air Europa:** Madrid")
        st.write("- **Lufthansa:** Frankfurt")
        st.write("- **Air France/KLM:** París/Ámsterdam")
        st.write("- **Turkish Airlines:** Estambul")
    with c_a2:
        st.subheader("Norte y Sur América")
        st.write("- **American/Delta/United:** USA")
        st.write("- **Avianca/LATAM:** Cono Sur y Caribe")

# 6. UBICACIÓN
elif menu == "UBICACIÓN":
    st.title("📍 Ubicación Hacienda Serenity")
    st.write("KBA San Antonio, Valle del Cauca, Colombia.")
    st.map(pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]}))













