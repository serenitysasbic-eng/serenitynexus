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

# 1. CONFIGURACIÓN MAESTRA Y ESTÉTICA
st.set_page_config(page_title="Serenity Nexus Global", layout="wide")

def aplicar_estilo_militar():
    bg_url = "https://images.unsplash.com/photo-1448375240586-882707db888b?q=80&w=2000"
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ background-image: url("{bg_url}"); background-size: cover; background-attachment: fixed; }}
    [data-testid="stSidebar"] {{ background: rgba(10, 25, 10, 0.85); backdrop-filter: blur(10px); }}
    .stMetric, .stTable {{ background: rgba(0, 0, 0, 0.7); padding: 15px; border-radius: 10px; border: 1px solid #2E7D32; }}
    h1, h2, h3, p {{ color: white !important; font-family: 'Segoe UI', sans-serif; }}
    </style>
    """, unsafe_allow_html=True)

aplicar_estilo_militar()

# 2. MOTOR DE DOCUMENTOS (Blindado contra errores NameError)
def crear_pdf_serenity(nombre, detalle, hash_id, tipo="CERTIFICADO"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 10, "SERENITY S.A.S BIC - REPORTE OFICIAL", ln=True, align='C')
    pdf.ln(20)
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, f"Entidad: {nombre}\nTipo: {tipo}\nImpacto/Detalle: {detalle}\nHash Seguridad: {hash_id}\nFecha: {datetime.now()}")
    return pdf.output(dest='S').encode('latin-1')

# 3. NAVEGACIÓN Y MENÚ
st.sidebar.title("🛡️ Molly Security OS")
menu = st.sidebar.selectbox("NAVEGACIÓN", ["INICIO", "RED DE FAROS", "DASHBOARD", "GESTION LEY", "SUSCRIPCIONES", "BILLETERA", "DONACIONES Y CERTIFICADO", "LOGISTICA AEROLINEAS", "UBICACION"])

# --- LÓGICA DE BLOQUES ---
if menu == "INICIO":
    st.title("🌿 Serenity Nexus Global")
    st.subheader("Bienvenido, Administrador Jorge Carvajal")
    c1, c2 = st.columns([2,1])
    with c1:
        st.write("Plataforma operativa al 100%. Los activos biológicos en Hacienda Monte Guadua están bajo monitoreo Gemini.")
        st.image("https://images.unsplash.com/photo-1501854140801-50d01698950b?q=80&w=800")
    with c2:
        st.metric("Árboles Protegidos", "12,450")
        st.metric("CO2 Capturado", "842 Ton")

elif menu == "RED DE FAROS":
    st.title("🛰️ Red de Faros Gemini")
    m = folium.Map(location=[3.642, -76.685], zoom_start=15)
    folium.Marker([3.642, -76.685], popup="Faro Villa Michelle").add_to(m)
    st_folium(m, width=800, height=400)
    st.audio("https://www.soundjay.com/nature/sounds/forest-birds-01.mp3")

elif menu == "DASHBOARD":
    st.title("📊 IA Analytics")
    st.bar_chart(pd.DataFrame({'Impacto': [120, 580, 142]}, index=['Michelle', 'Guadua', 'Dagua']))

elif menu == "GESTION LEY":
    st.title("⚖️ Gestión de Cumplimiento")
    emp = st.text_input("Nombre Empresa")
    if st.button("Generar"):
        pdf_bytes = crear_pdf_serenity(emp, "Cumplimiento Ley 2173", "SNG-2026", "VADEMECUM")
        st.download_button("Descargar", pdf_bytes, "Vademecum.pdf")

elif menu == "BILLETERA":
    st.title("👛 Billetera SNG")
    col_vid, col_dat = st.columns(2)
    with col_vid:
        if os.path.exists("video_sng.mp4"):
            with open("video_sng.mp4", "rb") as f:
                v_64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<video width="100%" autoplay loop muted playsinline><source src="data:video/mp4;base64,{v_64}"></video>', unsafe_allow_html=True)
        else: st.info("Visualizando activo SNG...")
    with col_dat:
        st.metric("Saldo", "1,250.00 SNG")
        st.button("Firmar Transacción")

elif menu == "UBICACION":
    st.title("📍 Ubicación Estratégica")
    st.write("Hacienda Monte Guadua y Finca Villa Michelle")
    st.map(pd.DataFrame({'lat': [3.642, 3.648], 'lon': [-76.685, -76.678]}))

# (Secciones restantes simplificadas para evitar fallos)
else:
    st.title(f"Sección: {menu}")
    st.info("Módulo operativo. Procesando datos de Serenity Nexus...")



































































































































































































