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
        
        /* TEXTO BLANCO EN SIDEBAR Y LABELS */
        [data-testid="stSidebar"] { background-color: rgba(10, 20, 8, 0.9) !important; backdrop-filter: blur(10px); }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, label, .stMarkdown p { 
            color: white !important; 
            font-weight: 500; 
        }

        h1, h2, h3 { color: #9BC63B !important; font-family: 'Merriweather', serif; text-shadow: 2px 2px 4px #000; }
        
        /* BOTONES */
        .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #9BC63B; border-radius: 8px; width: 100%; font-weight: bold; }
        .stButton>button:hover { background-color: #9BC63B; color: black; box-shadow: 0 0 15px #9BC63B; }
        
        /* TARJETAS Y CUADROS */
        .metric-card { background: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; border: 1px solid #9BC63B; text-align: center; backdrop-filter: blur(5px); }
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; }
        .cam-grid { background: #000; border: 1px solid #2E7D32; height: 100px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #ff0000; border-radius: 5px; }
        
        /* CAJA LEY 2173 */
        .ley-box { background: rgba(0, 0, 0, 0.7); border: 2px dashed #9BC63B; padding: 25px; border-radius: 15px; color: white; }
        .ley-box h3, .ley-box b, .ley-box p { color: white !important; }

        /* CONTENEDOR LOGOS AEROLÍNEAS */
        .logo-container { background: white; padding: 10px; border-radius: 8px; display: inline-block; margin: 5px; text-align: center; }
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
    "INICIO", "6 PUNTOS FARO", "DASHBOARD ESTADÍSTICO IA", "GESTIÓN LEY 2173 (EMPRESAS)",
    "SUSCRIPCIONES", "DONACIONES Y CERTIFICADO", "LOGÍSTICA AEROLÍNEAS", "UBICACIÓN"
])

# 1. INICIO
if menu == "INICIO":
    st.markdown("<h1 style='text-align:center; font-size:4rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold;'>SISTEMA REGENERATIVO BIOMÉTRICO</p>", unsafe_allow_html=True)
    st.components.v1.html("""
        <audio id="audio_nature" src="https://www.soundjay.com/nature/sounds/forest-birds-01.mp3" loop></audio>
        <div style="text-align:center; margin-top:30px;">
            <button onclick="document.getElementById('audio_nature').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:15px; border-radius:5px; cursor:pointer; font-weight:bold; font-size:16px;">🔊 ACTIVAR SONIDO AMBIENTAL KBA</button>
        </div>
    """, height=130)

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
            with mic_cols[k]: 
                st.markdown(f"<div style='background:rgba(155,198,59,0.2); border:1px solid #2E7D32; padding:15px; border-radius:5px; text-align:center;'><b>MIC {k+1}</b><br><span style='color:#9BC63B;'>|||||||||| {random.randint(30,95)}%</span></div>", unsafe_allow_html=True)

# 3. DASHBOARD ESTADÍSTICO IA
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("📊 Análisis de Inteligencia Biológica")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown("<div class='metric-card'><h3>Especies Identificadas</h3><h1 style='color:#9BC63B;'>1,248</h1></div>", unsafe_allow_html=True)
    with m2: st.markdown("<div class='metric-card'><h3>Índice Salud Bosque</h3><h1 style='color:#9BC63B;'>94%</h1></div>", unsafe_allow_html=True)
    with m3: st.markdown("<div class='metric-card'><h3>Alertas de Fauna</h3><h1 style='color:#9BC63B;'>12</h1></div>", unsafe_allow_html=True)
    with m4: st.markdown("<div class='metric-card'><h3>Área Protegida</h3><h1 style='color:#9BC63B;'>86 ha</h1></div>", unsafe_allow_html=True)
    
    st.divider()
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("Actividad por Nodo (24h)")
        st.bar_chart(pd.DataFrame({'Faro': ["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara"], 'Detecciones': [120, 450, 300, 80, 45, 110]}).set_index('Faro'))
    with c2:
        st.subheader("🛰️ ÚLTIMOS AVISTAMIENTOS IA")
        avistamientos = [{"h": "11:20 AM", "e": "Tangara Multicolor", "f": "Colibrí", "c": "98%"}, {"h": "10:45 AM", "e": "Pava Caucana", "f": "Halcón", "c": "95%"}, {"h": "09:12 AM", "e": "Tigrillo (Leopardus)", "f": "Tigrillo", "c": "92%"}]
        for a in avistamientos:
            st.markdown(f"<div class='avistamiento-row'><span style='color:#9BC63B; font-weight:bold;'>{a['e']}</span> detectado en <b>Faro {a['f']}</b> | {a['h']}</div>", unsafe_allow_html=True)

# 4. GESTIÓN LEY 2173 (EMPRESAS)
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Cumplimiento Ley 2173 de 2021")
    st.markdown("<p style='color:white; font-size:1.1rem;'>Gestión de 'Áreas de Vida' con transparencia total para el sector corporativo.</p>", unsafe_allow_html=True)
    
    c_l1, c_l2 = st.columns(2)
    with c_l1: nit = st.text_input("Ingrese NIT de la Empresa")
    with c_l2: uploaded_logo = st.file_uploader("Suba su Logo Corporativo", type=["png", "jpg"])

    if nit:
        st.markdown("<div class='ley-box'>", unsafe_allow_html=True)
        if uploaded_logo: st.image(uploaded_logo, width=150)
        st.markdown(f"""
                <h3>Estado Corporativo: ACTIVO</h3>
                <p><b>Empresa Asociada:</b> Registro Vinculado al NIT {nit}</p>
                <hr style='border-color: rgba(255,255,255,0.2);'>
                <p>🌳 <b>Árboles Sembrados:</b> 150 (Meta 2026 cumplida)</p>
                <p>📡 <b>Monitoreo Biométrico:</b> Activo en Faro Venado</p>
                <p>📉 <b>Supervivencia Garantizada:</b> 98.5% mediante monitoreo IA</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("GENERAR REPORTE"): st.success("Reporte generado con éxito.")

# 5. SUSCRIPCIONES
elif menu == "SUSCRIPCIONES":
    st.title("💳 Planes de Apoyo Regenerativo")
    p1, p2, p3 = st.columns(3)
    with p1: st.markdown("<div class='faro-card'><h3>Plan Semilla</h3><h2>$5 USD</h2><p>1 Punto Faro/1 mes</p></div>", unsafe_allow_html=True); st.button("Suscribirse Semilla")
    with p2: st.markdown("<div class='faro-card'><h3>Plan Guardián</h3><h2>$25 USD</h2><p>6 Puntos Faro/1 mes</p></div>", unsafe_allow_html=True); st.button("Suscribirse Guardián")
    with p3: st.markdown("<div class='faro-card' style='border-color:#D4AF37;'><h3>Plan Halcón</h3><h2>$200 USD</h2><p>6 Puntos Faro/6 meses</p></div>", unsafe_allow_html=True); st.button("Suscribirse Héroe")
    st.markdown("<div style='background:white; padding:20px; border-radius:10px; text-align:center; margin-top:20px;'><img src='https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg' width='100'> &nbsp;&nbsp; <img src='https://upload.wikimedia.org/wikipedia/commons/b/ba/Stripe_Logo%2C_revised_2016.svg' width='100'> &nbsp;&nbsp; <img src='https://www.payulatam.com/co/wp-content/uploads/sites/2/2017/08/logo-payu.png' width='80'></div>", unsafe_allow_html=True)

# 6. DONACIONES Y CERTIFICADO
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("🌳 Generador de Impacto")
    colA, colB = st.columns(2)
    with colA:
        nombre_d = st.text_input("Nombre del Donante"); monto_d = st.number_input("Monto (USD)", min_value=1)
        if st.button("GENERAR CERTIFICADO"): st.balloons(); st.session_state.ver_cert = True
    if "ver_cert" in st.session_state:
        with colB: st.markdown(f"<div style='background:white; color:#050a04; padding:30px; border:8px double #D4AF37; text-align:center;'><h1>CERTIFICADO</h1><p><b>{nombre_d}</b> ha contribuido con {monto_d} USD.</p><hr><small>{datetime.now().strftime('%d/%m/%Y')}</small></div>", unsafe_allow_html=True)

# 7. LOGÍSTICA AEROLÍNEAS
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Rutas Globales a Colombia")
    c_a1, c_a2 = st.columns(2)
    with c_a1:
        st.subheader("Europa y Asia")
        st.markdown("""
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/4/44/Iberia_Logo.svg' width='80'></div>
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Lufthansa_Logo_2018.svg' width='80'></div>
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/en/c/c7/Air_France_Logo.svg' width='80'></div>
        """, unsafe_allow_html=True)
        st.write("- Iberia / Air Europa (Madrid)\n- Lufthansa (Frankfurt)\n- Air France / KLM (París/Ámsterdam)\n- Turkish Airlines (Estambul)")
    with c_a2:
        st.subheader("América")
        st.markdown("""
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Avianca_logo.svg' width='80'></div>
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/0/00/American_Airlines_logo_2013.svg' width='80'></div>
        <div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/c/c2/Copa_Airlines_logo.svg' width='80'></div>
        """, unsafe_allow_html=True)
        st.write("- Avianca / LATAM (Suramérica)\n- American / Delta / United (USA)\n- Copa Airlines (Vía Panamá)")

# 8. UBICACIÓN
elif menu == "UBICACIÓN":
    st.title("📍 Ubicación Hacienda Serenity")
    st.write("Dagua y Felidia, Valle del Cauca, Colombia.")
    st.map(pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]}))





























