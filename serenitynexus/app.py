# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import random
import hashlib
import io
import os
import base64
import folium
from datetime import datetime
from streamlit_folium import st_folium

# --- LIBRERÍAS DE REPORTES (PDF) ---
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black

# =========================================================
# 1. CONFIGURACIÓN E IDENTIDAD
# =========================================================
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌿", layout="wide")
VERDE_SERENITY = HexColor("#2E7D32")
VERDE_LIMA = HexColor("#9BC63B")

# =========================================================
# 2. FUNCIONES MAESTRAS (Lógica de Negocio)
# =========================================================

def generar_pdf_corporativo(empresa, impacto, hash_id, nit="", logo_bytes=None, es_vademecum=False, faro_nombre="Red Nexus"):
    """Función única consolidada para generar todos los reportes PDF del sistema."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # --- Estética y Marcos ---
    c.setStrokeColor(VERDE_LIMA)
    c.setLineWidth(2)
    c.rect(0.5*inch, 0.5*inch, 7.5*inch, 10*inch)
    c.line(0.5*inch, 10.2*inch, 8*inch, 10.2*inch)

    # --- Gestión de Logos (Co-Branding) ---
    try:
        if os.path.exists("logo_serenity.png"):
            c.drawImage("logo_serenity.png", 0.7*inch, 9.3*inch, width=1.5*inch, preserveAspectRatio=True, mask='auto')
    except: pass

    if logo_bytes:
        try:
            from reportlab.lib.utils import ImageReader
            logo_img = ImageReader(io.BytesIO(logo_bytes))
            c.drawImage(logo_img, 6*inch, 9.3*inch, width=1.5*inch, preserveAspectRatio=True, mask='auto')
        except: pass

    # --- Títulos ---
    c.setFont("Helvetica-Bold", 16)
    titulo = "VADEMÉCUM TÉCNICO LEGAL" if es_vademecum else "CERTIFICADO DE COMPENSACIÓN"
    c.drawCentredString(4.25*inch, 9*inch, titulo)

    # --- Datos de la Entidad ---
    c.setFont("Helvetica", 11)
    c.setFillColor(black)
    y = 8.2*inch
    c.drawString(1*inch, y, f"RAZÓN SOCIAL: {empresa.upper()}")
    c.drawString(1*inch, y-0.2*inch, f"NIT: {nit}")
    c.drawString(1*inch, y-0.4*inch, f"NODO VALIDADOR: {faro_nombre}")
    c.drawString(1*inch, y-0.6*inch, f"ID SEGURIDAD (HASH): {hash_id}")

    # --- Contenido Dinámico ---
    text = c.beginText(1*inch, 6.5*inch)
    text.setFont("Helvetica", 10)
    text.setLeading(14)
    
    if es_vademecum:
        lineas = [
            "SOLUCIONES INTEGRADAS SERENITY S.A.S BIC:",
            "1. CUMPLIMIENTO LEY 2173 DE 2021 (ÁREAS DE VIDA): 2 árboles por empleado.",
            "2. CUMPLIMIENTO LEY 2169 DE 2021 (CARBONO NEUTRALIDAD): Monitoreo Faros Gemini.",
            "3. PROTOCOLO LEY 2111 DE 2021 (DELITOS AMBIENTALES): Vigilancia IA.",
            "",
            "La entidad se vincula al Internet de la Naturaleza con trazabilidad Blockchain."
        ]
    else:
        lineas = [
            "DETALLE DE COMPENSACIÓN BIOMÉTRICA:",
            f"- Gestión de {impacto} individuos forestales en el corredor biológico de Dagua.",
            "- Registro biométrico activo en la Red de Faros Serenity.",
            "- Este certificado avala la responsabilidad social y ambiental corporativa."
        ]
    
    for linea in lineas:
        text.textLine(linea)
    c.drawText(text)

    # --- Pie de página ---
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(4.25*inch, 0.8*inch, "Documento generado por Serenity Nexus Global. Verificable en Red Nexus.")

    c.save()
    buffer.seek(0)
    return buffer

def generar_pdf_certificado(nombre, monto, hash_id):
    """Función para diplomas de donación simple."""
    return generar_pdf_corporativo(nombre, monto, hash_id, nit="Persona Natural")

# =========================================================
# 3. GESTIÓN DE ESTADO (Session State)
# =========================================================
if 'auth' not in st.session_state: st.session_state.auth = False
if 'total_protegido' not in st.session_state: st.session_state.total_protegido = 87.0
if 'donaciones_recibidas' not in st.session_state: st.session_state.donaciones_recibidas = 0
if 'f_activo' not in st.session_state: st.session_state.f_activo = None

# =========================================================
# 4. ESTILOS CSS
# =========================================================
st.markdown("""
    <style>
        .stApp { 
            background-image: linear-gradient(rgba(5, 10, 4, 0.8), rgba(5, 10, 4, 0.9)), 
            url('https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1920&q=80');
            background-size: cover; background-attachment: fixed;
            color: #e8f5e9; font-family: 'Montserrat', sans-serif; 
        }
        h1, h2, h3 { color: #9BC63B !important; }
        .stButton>button { background-color: #2E7D32; color: white; border-radius: 8px; font-weight: bold; }
        .stButton>button:hover { background-color: #9BC63B; color: black; box-shadow: 0 0 15px #9BC63B; }
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 5. CONTROL DE ACCESO (LOGIN)
# =========================================================
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; padding-top: 50px;'>SISTEMA NEXUS | SERENITY</h1>", unsafe_allow_html=True)
    col_l = st.columns([1,1,1])
    with col_l[1]:
        clave = st.text_input("PASSWORD ADMIN", type="password")
        if st.button("INGRESAR"):
            if clave == "Serenity2026":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# =========================================================
# 6. MENÚ LATERAL Y NAVEGACIÓN
# =========================================================
menu = st.sidebar.radio("CENTRO DE CONTROL", [
    "INICIO", "RED DE FAROS (7 NODOS)", "DASHBOARD ESTADÍSTICO IA", 
    "GESTIÓN LEY 2173 (EMPRESAS)", "SUSCRIPCIONES", "BILLETERA CRYPTO (WEB3)", 
    "DONACIONES Y CERTIFICADO", "DIAGNOSTICO HUELLA DE CARBONO", "UBICACIÓN & MAPAS"
])

# ---------------------------------------------------------
# BLOQUE: INICIO
# ---------------------------------------------------------
if menu == "INICIO":
    st.markdown("<h1 style='text-align:center;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#9BC63B; font-weight:bold;'>SISTEMA REGENERATIVO BIOMÉTRICO KBA</p>", unsafe_allow_html=True)
    
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.subheader("QUIÉNES SOMOS")
        st.write("Plataforma Phygital del Valle del Cauca que integra conservación con Blockchain e IA.")
    with col_i2:
        st.subheader("NUESTRA MISIÓN")
        st.write("Regenerar el tejido ecológico permitiendo compensar la huella ambiental con transparencia total.")

# ---------------------------------------------------------
# BLOQUE: RED DE FAROS
# ---------------------------------------------------------
elif menu == "RED DE FAROS (7 NODOS)":
    st.title("🛰️ Monitoreo Perimetral Nexus")
    def conectar_faro(nombre): st.session_state.f_activo = nombre

    c1, c2, c3 = st.columns(3)
    with c1: st.button("🦅 FARO HALCÓN", on_click=conectar_faro, args=("Halcón",), use_container_width=True)
    with c2: st.button("🦜 FARO COLIBRÍ", on_click=conectar_faro, args=("Colibrí",), use_container_width=True)
    with c3: st.button("🐸 FARO RANA", on_click=conectar_faro, args=("Rana",), use_container_width=True)
    
    f_nom = st.session_state.get('f_activo')
    if f_nom:
        st.markdown(f"### 📽️ FEED EN VIVO: {f_nom.upper()}")
        st.components.v1.html("""<div style="background:black; color:red; height:100px; display:flex; align-items:center; justify-content:center;">STREAMING ACTIVO - NODO NEXUS</div>""", height=120)

# ---------------------------------------------------------
# BLOQUE: GESTIÓN LEY 2173
# ---------------------------------------------------------
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Nexus Legal & Compliance Hub")
    
    n_corp = st.text_input("Razón Social")
    nit_corp = st.text_input("NIT")
    archivo_logo = st.file_uploader("Cargar Logo", type=['png', 'jpg'])
    
    if st.button("EMITIR CERTIFICADO"):
        if n_corp and archivo_logo:
            h_c = hashlib.sha256(f"{n_corp}".encode()).hexdigest()[:12].upper()
            logo_bytes = archivo_logo.getvalue()
            pdf = generar_pdf_corporativo(n_corp, 100, h_c, nit=nit_corp, logo_bytes=logo_bytes)
            st.download_button("📥 DESCARGAR PDF", data=pdf, file_name="Certificado_Serenity.pdf")

# ---------------------------------------------------------
# BLOQUE: UBICACIÓN & MAPAS
# ---------------------------------------------------------
elif menu == "UBICACIÓN & MAPAS":
    st.title("🛰️ Geoposicionamiento Nexus")
    m = folium.Map(location=[3.518, -76.620], zoom_start=14)
    st_folium(m, width=1000, height=500)

# (El resto de bloques siguen la misma estructura lógica...)
























































































































































































































































































