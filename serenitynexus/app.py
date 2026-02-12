# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import hashlib
import os
import io
import base64
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
from datetime import datetime

# =========================================================
# 1. CONFIGURACIÓN DE SEGURIDAD Y ESTILO (ESTILO GEMINI)
# =========================================================
st.set_page_config(page_title="Serenity Nexus Global", layout="wide", initial_sidebar_state="expanded")

# Fondo de Pantalla: Bosque Profundo con Capa de Seguridad (Glassmorphism)
def apply_military_ui():
    bg_url = "https://images.unsplash.com/photo-1448375240586-882707db888b?q=80&w=2000"
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    [data-testid="stSidebar"] {{
        background: rgba(10, 25, 10, 0.8);
        backdrop-filter: blur(10px);
    }}
    .stMetric {{
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    h1, h2, h3, p {{ color: #e0e0e0 !important; }}
    </style>
    """, unsafe_allow_html=True)

apply_military_ui()

# =========================================================
# 2. MOTOR LÓGICO DE SERENITY (PDF Y SEGURIDAD)
# =========================================================
def generar_pdf(entidad, impacto, hash_id, tipo="CERTIFICADO"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Logo
    if os.path.exists("logo_serenity.png"):
        pdf.image("logo_serenity.png", x=10, y=10, w=35)
        
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(46, 125, 50)
    pdf.ln(40)
    
    titulo = "VADEMÉCUM LEGAL" if tipo == "VADEMECUM" else "CERTIFICADO DE IMPACTO"
    pdf.cell(0, 10, titulo, ln=True, align='C')
    
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(50, 50, 50)
    cuerpo = f"Entidad: {entidad}\nImpacto: {impacto}\nFecha: {datetime.now().strftime('%Y-%m-%d')}\nID Blockchain: {hash_id}"
    pdf.multi_cell(0, 10, cuerpo, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# =========================================================
# 3. NAVEGACIÓN (ORDEN JORGE CARVAJAL)
# =========================================================
st.sidebar.title("🛡️ Nexus Security Hub")
st.sidebar.markdown(f"**ID Sesión:** `{hashlib.sha1(str(datetime.now()).encode()).hexdigest()[:10].upper()}`")

menu = st.sidebar.selectbox("MENÚ PRINCIPAL", 
    ["INICIO", "RED DE FAROS", "DASHBOARD", "GESTION LEY", "SUSCRIPCIONES", "BILLETERA", "DONACIONES Y CERTIFICADO", "LOGISTICA AEROLINEAS", "UBICACION"])

# --- SECCIÓN: INICIO ---
if menu == "INICIO":
    st.title("🌿 Serenity Nexus Global")
    st.subheader("Plataforma de Regeneración Biológica Sostenible")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Bienvenido, Jorge Carvajal")
        st.write("Molly está operativa. Todos los sistemas de monitoreo en Hacienda Monte Guadua reportan estado óptimo.")
        st.image("https://images.unsplash.com/photo-1501854140801-50d01698950b?q=80&w=1000", caption="Reserva Protectora Serenity")
    
    with col2:
        st.metric("Árboles Protegidos", "12,450", "+120")
        st.metric("CO2 Neutralizado", "842 Ton", "Nivel 4")
        st.success("🔒 Enlace Encriptado con Éxito")

# --- SECCIÓN: RED DE FAROS ---
elif menu == "RED DE FAROS":
    st.title("🛰️ Monitoreo Perimetral IA")
    col_v, col_t = st.columns([2, 1])
    
    with col_v:
        # Video de Gemini Vision (con respaldo de imagen)
        vid_path = "video_gemini_vision.mp4"
        if os.path.exists(vid_path):
            with open(vid_path, "rb") as f:
                v_64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<video width="100%" autoplay loop muted playsinline><source src="data:video/mp4;base64,{v_64}"></video>', unsafe_allow_html=True)
        else:
            st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1000", caption="Simulación Visión Gemini")

    with col_t:
        st.write("#### Micrófonos Activos")
        st.audio("https://www.soundjay.com/nature/sounds/rain-01.mp3")
        st.info("Faro 04: Sonido ambiente normal.")

# --- SECCIÓN: BILLETERA (VIDEO INFINITO) ---
elif menu == "BILLETERA":
    st.title("👛 Billetera SNG $")
    col_v, col_m = st.columns([1, 1])
    
    with col_v:
        # Video Moneda Infinito
        vid_sng = "video_sng.mp4"
        if os.path.exists(vid_sng):
            with open(vid_sng, "rb") as f:
                s_64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<video width="100%" autoplay loop muted playsinline><source src="data:video/mp4;base64,{s_64}"></video>', unsafe_allow_html=True)
        else:
            st.image("https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=1000")

    with col_m:
        st.metric("Saldo SNG", "1,250.00")
        st.button("Recibir SNG")
        st.button("Enviar SNG")

# --- SECCIÓN: GESTION LEY ---
elif menu == "GESTION LEY":
    st.title("⚖️ Gestión de Cumplimiento")
    empresa = st.text_input("Empresa")
    if st.button("Generar Vademécum"):
        v_pdf = generar_pdf(empresa, "Leyes 2173/2169/2111", "VAD-SNG", "VADEMECUM")
        st.download_button("📥 Descargar", v_pdf, "Vademecum.pdf")

# (Agrega los demás elif con estructuras similares para no romper el código)
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Serenity S.A.S BIC | v4.0 Militar Grade")


































































































































































































