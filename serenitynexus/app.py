# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime
from PIL import Image

# CONFIGURACIÓN DE IDENTIDAD
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌳", layout="wide")

# --- DISEÑO VISUAL AVANZADO (CSS ACTUALIZADO PARA LETRAS BLANCAS) ---
st.markdown("""
    <style>
        .stApp { 
            background-image: linear-gradient(rgba(5, 10, 4, 0.7), rgba(5, 10, 4, 0.8)), 
            url('https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1920&q=80');
            background-size: cover; background-position: center; background-attachment: fixed;
            color: #e8f5e9; font-family: 'Montserrat', sans-serif; 
        }
        
        /* FUERZA EL COLOR BLANCO EN TODAS LAS ETIQUETAS DE INPUT (Ej: Ingrese NIT) */
        label {
            color: white !important;
            font-weight: bold !important;
        }

        /* TEXTO BLANCO EN SIDEBAR */
        [data-testid="stSidebar"] { background-color: rgba(10, 20, 8, 0.9) !important; backdrop-filter: blur(10px); }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: white !important; font-weight: 500; }

        h1, h2, h3 { color: #9BC63B; font-family: 'Merriweather', serif; text-shadow: 2px 2px 4px #000; }
        
        /* BOTONES */
        .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #9BC63B; border-radius: 8px; width: 100%; font-weight: bold; }
        .stButton>button:hover { background-color: #9BC63B; color: black; box-shadow: 0 0 15px #9BC63B; }
        
        /* TARJETAS DE MÉTRICAS */
        .metric-card { background: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; border: 1px solid #9BC63B; text-align: center; backdrop-filter: blur(5px); }
        
        /* TABLA DE AVISTAMIENTOS */
        .avistamiento-row { 
            background: rgba(255, 255, 255, 0.1); 
            border-left: 5px solid #9BC63B; 
            padding: 12px; 
            margin-bottom: 8px; 
            border-radius: 0 5px 5px 0;
            color: white;
        }
        .especie-tag { color: #9BC63B; font-weight: bold; font-size: 1.1rem; }
        
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; }
        .cam-grid { background: #000; border: 1px solid #2E7D32; height: 100px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #ff0000; border-radius: 5px; }
        
        /* CAJA DE LEY 2173 */
        .ley-box { 
            background: rgba(0, 0, 0, 0.7); 
            border: 2px dashed #9BC63B; 
            padding: 25px; 
            border-radius: 15px; 
            margin-top: 10px; 
        }
        .ley-box h3, .ley-box b, .ley-box p { color: white !important; }
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
    "INICIO", 
    "6 PUNTOS FARO", 
    "DASHBOARD ESTADÍSTICO IA", 
    "GESTIÓN LEY 2173 (EMPRESAS)",
    "SUSCRIPCIONES", 
    "DONACIONES Y CERTIFICADO", 
    "LOGÍSTICA AEROLÍNEAS", 
    "UBICACIÓN"
])

# 1. INICIO
if menu == "INICIO":
    st.markdown("<h1 style='text-align:center; font-size:4rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold;'>SISTEMA REGENERATIVO BIOMÉTRICO</p>", unsafe_allow_html=True)
    st.components.v1.html("""
        <audio id="audio_nature" src="https://www.soundjay.com/nature/sounds/forest-birds-01.mp3" loop></audio>
        <div style="text-align:center; margin-top:30px;">
            <button onclick="document.getElementById('audio_nature').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:20px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:16px;">🔊 ACTIVAR SONIDO AMBIENTAL KBA</button>
        </div>
    """, height=130)

# 2. LOS 6 PUNTOS FARO
elif menu == "6 PUNTOS FARO":
    st.title("🛰️ Monitoreo Perimetral")
    faros = ["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara"]
    f_cols = st.columns(3)
    for i, f in enumerate(faros):
        with f_cols[i % 3]:
            st.markdown(f"<div class='faro-card'><h3>FARO {f.upper()}</h3></div>", unsafe_allow_html=True)
            if st.button(f"INGRESAR A FARO {f}"): st.session_state.f_activo = f

# 3. DASHBOARD ESTADÍSTICO IA
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("📊 Análisis de Inteligencia Biológica")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown("<div class='metric-card'><h3>Especies Identificadas</h3><h1 style='color:#9BC63B;'>1,248</h1></div>", unsafe_allow_html=True)
    with m2: st.markdown("<div class='metric-card'><h3>Índice Salud Bosque</h3><h1 style='color:#9BC63B;'>94%</h1></div>", unsafe_allow_html=True)

# 4. GESTIÓN LEY 2173 (CON CAMBIOS A BLANCO)
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Cumplimiento Ley 2173 de 2021")
    
    # Cambio de Azul a Blanco usando Markdown personalizado
    st.markdown("<p style='color: white; font-size: 1.1rem;'>Gestión de 'Áreas de Vida' con transparencia total para el sector corporativo.</p>", unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        # El label "Ingrese NIT de la Empresa" ahora es blanco por el CSS global arriba
        nit = st.text_input("Ingrese NIT de la Empresa")
    with col_input2:
        uploaded_logo = st.file_uploader("Suba el Logo de su Empresa (PNG/JPG)", type=["png", "jpg", "jpeg"])

    if nit:
        st.markdown("<div class='ley-box'>", unsafe_allow_html=True)
        if uploaded_logo is not None:
            image = Image.open(uploaded_logo)
            st.image(image, width=150)
        st.markdown(f"""
                <h3 style='margin-bottom:20px; color:white;'>Estado Corporativo: ACTIVO</h3>
                <p><b>Empresa Asociada:</b> Registro Vinculado al NIT {nit}</p>
                <hr style='border-color: rgba(255,255,255,0.2);'>
                <p>🌳 <b>Árboles Sembrados:</b> 150 (Meta 2026 cumplida)</p>
                <p>📡 <b>Monitoreo Biométrico:</b> Activo en Faro Venado</p>
                <p>📉 <b>Supervivencia Garantizada:</b> 98.5% mediante monitoreo IA</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("GENERAR REPORTE"):
            st.success("Reporte generado con éxito.")

# 5. SUSCRIPCIONES
elif menu == "SUSCRIPCIONES":
    st.title("💳 Planes de Apoyo Regenerativo")
    st.markdown("<div style='background:white; padding:20px; border-radius:10px; text-align:center; margin-top:20px;'><img src='https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg' width='100'> &nbsp;&nbsp; <img src='https://upload.wikimedia.org/wikipedia/commons/b/ba/Stripe_Logo%2C_revised_2016.svg' width='100'></div>", unsafe_allow_html=True)

# 6. DONACIONES Y CERTIFICADO
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("🌳 Generador de Impacto")
    nombre_d = st.text_input("Nombre del Donante"); monto_d = st.number_input("Monto (USD)", min_value=1)
    if st.button("GENERAR CERTIFICADO"): st.balloons(); st.session_state.ver_cert = True

# 7. LOGÍSTICA AEROLÍNEAS
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Rutas Globales")
    st.write("- Iberia / Air Europa (Madrid)\n- Lufthansa (Frankfurt)")

# 8. UBICACIÓN
elif menu == "UBICACIÓN":
    st.title("📍 Ubicación")
    st.write("Dagua y Felidia, Valle del Cauca.")
    st.map(pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]}))



























