# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime

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
        h1, h2, h3 { color: #9BC63B; font-family: 'Merriweather', serif; text-shadow: 2px 2px 4px #000; }
        .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #9BC63B; border-radius: 8px; width: 100%; font-weight: bold; }
        .stButton>button:hover { background-color: #9BC63B; color: black; box-shadow: 0 0 15px #9BC63B; }
        .metric-card { background: rgba(0,0,0,0.6); padding: 20px; border-radius: 10px; border: 1px solid #9BC63B; text-align: center; backdrop-filter: blur(5px); }
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; }
        .cam-grid { background: #000; border: 1px solid #2E7D32; height: 100px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #ff0000; border-radius: 5px; }
        [data-testid="stSidebar"] { background-color: rgba(10, 20, 8, 0.9) !important; backdrop-filter: blur(10px); }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: white !important; font-weight: 500; }
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
try: st.sidebar.image("logo_serenity.png", use_container_width=True)
except: st.sidebar.markdown("### 🌳 Serenity Nexus")

menu = st.sidebar.radio("CENTRO DE CONTROL", [
    "INICIO", "6 PUNTOS FARO", "DASHBOARD ESTADÍSTICO IA", "SUSCRIPCIONES", "DONACIONES Y CERTIFICADO", "LOGÍSTICA AEROLÍNEAS", "UBICACIÓN"
])

# 1. INICIO
if menu == "INICIO":
    st.markdown("<h1 style='text-align:center; font-size:4rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold;'>SISTEMA REGENERATIVO BIOMÉTRICO</p>", unsafe_allow_html=True)
    st.components.v1.html("""
        <audio id="audio" src="sonido_bosque.m4a" loop></audio>
        <div style="text-align:center; margin-top:20px;">
            <button onclick="document.getElementById('audio').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:15px; border-radius:5px; cursor:pointer; font-weight:bold;">🔊 ACTIVAR CANAL AUDITIVO HACIENDA</button>
        </div>
    """, height=100)

# 2. LOS 6 PUNTOS FARO
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
            with mic_cols[k]: st.markdown(f"<div style='background:rgba(155,198,59,0.2); border:1px solid #2E7D32; padding:5px; border-radius:5px; text-align:center;'>MIC {k+1}<br><span style='color:#9BC63B;'>|||||||||| {random.randint(30,95)}%</span></div>", unsafe_allow_html=True)

# 3. NEW: DASHBOARD ESTADÍSTICO IA
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("📊 Análisis de Inteligencia Biológica")
    st.write("Datos procesados en tiempo real por los servidores Nexus en el KBA San Antonio.")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown("<div class='metric-card'><h3>Especies Identificadas</h3><h1 style='color:#9BC63B;'>1,248</h1></div>", unsafe_allow_html=True)
    with m2: st.markdown("<div class='metric-card'><h3>Índice Salud Bosque</h3><h1 style='color:#9BC63B;'>94%</h1></div>", unsafe_allow_html=True)
    with m3: st.markdown("<div class='metric-card'><h3>Alertas de Fauna</h3><h1 style='color:#9BC63B;'>12</h1><p>Últimas 24h</p></div>", unsafe_allow_html=True)
    with m4: st.markdown("<div class='metric-card'><h3>Área Protegida</h3><h1 style='color:#9BC63B;'>86 ha</h1></div>", unsafe_allow_html=True)
    
    st.divider()
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Actividad por Punto Faro (24h)")
        chart_data = pd.DataFrame({
            'Faro': ["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara"],
            'Detecciones': [120, 450, 300, 80, 45, 110]
        })
        st.bar_chart(chart_data.set_index('Faro'))
    with col_chart2:
        st.subheader("Últimos Avistamientos IA")
        st.table([
            {"Hora": "11:20 AM", "Especie": "Tangara Multicolor", "Faro": "Colibrí", "Confianza": "98%"},
            {"Hora": "10:45 AM", "Especie": "Pava Caucana", "Faro": "Halcón", "Confianza": "95%"},
            {"Hora": "09:12 AM", "Especie": "Tigrillo (Leopardus)", "Faro": "Tigrillo", "Confianza": "92%"},
            {"Hora": "07:30 AM", "Especie": "Olinguito", "Faro": "Rana", "Confianza": "89%"}
        ])

# 4. SUSCRIPCIONES
elif menu == "SUSCRIPCIONES":
    st.title("💳 Planes de Apoyo Regenerativo")
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("<div class='faro-card'><h3>Plan Semilla</h3><h2>$5 USD</h2><p>1 Punto Faro/1 mes</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Semilla")
    with p2:
        st.markdown("<div class='faro-card'><h3>Plan Guardián</h3><h2>$25 USD</h2><p>6 Puntos Faro/1 mes</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Guardián")
    with p3:
        st.markdown("<div class='faro-card' style='border-color:#D4AF37;'><h3>Plan Halcon</h3><h2>$200 USD</h2><p>6 Puntos Faro/6 meses</p></div>", unsafe_allow_html=True)
        st.button("Suscribirse Heroe")
    st.markdown("<div style='background:white; padding:20px; border-radius:10px; text-align:center; margin-top:20px;'><img src='https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg' width='100'> &nbsp;&nbsp; <img src='https://upload.wikimedia.org/wikipedia/commons/b/ba/Stripe_Logo%2C_revised_2016.svg' width='100'> &nbsp;&nbsp; <img src='https://www.payulatam.com/co/wp-content/uploads/sites/2/2017/08/logo-payu.png' width='80'></div>", unsafe_allow_html=True)

# 5. DONACIONES Y CERTIFICADO
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("🌳 Generador de Impacto")
    colA, colB = st.columns(2)
    with colA:
        nombre_d = st.text_input("Nombre del Donante"); monto_d = st.number_input("Monto (USD)", min_value=1)
        if st.button("PROCESAR Y GENERAR CERTIFICADO"): st.balloons(); st.session_state.ver_cert = True
    if "ver_cert" in st.session_state:
        with colB: st.markdown(f"<div style='background:white; color:#050a04; padding:30px; border:8px double #D4AF37; text-align:center; font-family:serif;'><h1>CERTIFICADO</h1><p>Serenity SAS BIC certifica que <b>{nombre_d}</b> ha contribuido con {monto_d} USD.</p><hr><small>{datetime.now().strftime('%d/%m/%Y')}</small></div>", unsafe_allow_html=True)

# 6. LOGÍSTICA AEROLÍNEAS
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Conectividad Global")
    st.write("- **Europa/Asia:** Iberia, Lufthansa, KLM, Turkish.")
    st.write("- **América:** American, Delta, United, Avianca.")

# 7. UBICACIÓN
elif menu == "UBICACIÓN":
    st.title("📍 Ubicación")
    st.map(pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]}))





















