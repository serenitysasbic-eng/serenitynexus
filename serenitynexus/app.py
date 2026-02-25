# -*- coding: utf-8 -*-

# =========================================================
# 1. IMPORTS
# =========================================================
import streamlit as st
import pandas as pd
import random
import hashlib
from datetime import datetime
import io
import os
import base64
import librosa
import numpy as np
import folium

from streamlit_folium import st_folium

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# =========================================================
# 2. CONFIGURACIÓN GLOBAL
# =========================================================
st.set_page_config(
    page_title="Serenity Nexus Global",
    page_icon="🌎",
    layout="wide"
)

VERDE_SERENITY = HexColor("#2E7D32")

# =========================================================
# 3. FUNCIONES PDF (VERSIÓN MAESTRA UNIFICADA)
# =========================================================

def generar_pdf_corporativo(
    empresa,
    impacto,
    hash_id,
    nit="",
    logo_bytes=None,
    es_vademecum=False,
    faro_nombre="Red Nexus"
):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # --- MARCO ---
    c.setStrokeColor(VERDE_SERENITY)
    c.rect(0.5*inch, 0.5*inch, 7.5*inch, 10*inch)

    # --- LOGO SERENITY ---
    if os.path.exists("logo_serenity.png"):
        try:
            c.drawImage("logo_serenity.png", 0.7*inch, 9.3*inch,
                        width=1.5*inch, preserveAspectRatio=True)
        except:
            pass

    # --- LOGO EMPRESA ---
    if logo_bytes:
        try:
            logo_img = ImageReader(io.BytesIO(logo_bytes))
            c.drawImage(logo_img, 6*inch, 9.3*inch,
                        width=1.5*inch, preserveAspectRatio=True)
        except:
            pass

    # --- TÍTULO ---
    c.setFont("Helvetica-Bold", 16)
    titulo = "VADEMÉCUM TÉCNICO LEGAL" if es_vademecum else "CERTIFICADO DE COMPENSACIÓN"
    c.drawCentredString(4.25*inch, 9*inch, titulo)

    # --- DATOS ---
    c.setFont("Helvetica", 11)
    y = 8.2*inch
    c.drawString(1*inch, y, f"RAZÓN SOCIAL: {empresa.upper()}")
    c.drawString(1*inch, y-0.2*inch, f"NIT: {nit}")
    c.drawString(1*inch, y-0.4*inch, f"NODO VALIDADOR: {faro_nombre}")
    c.drawString(1*inch, y-0.6*inch, f"ID SEGURIDAD: {hash_id}")

    # --- CONTENIDO ---
    text = c.beginText(1*inch, 6.5*inch)
    text.setFont("Helvetica", 11)

    if es_vademecum:
        text.textLine("Cumplimiento de Leyes 2173, 2169 y 2111.")
        text.textLine("Monitoreo biométrico mediante Red de Faros Serenity.")
    else:
        text.textLine(f"Se certifica la compensación de {impacto} árboles.")

    c.drawText(text)

    # --- PIE ---
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(
        4.25*inch,
        1.2*inch,
        "Documento generado electrónicamente - Serenity Nexus Blockchain"
    )

    c.save()
    buffer.seek(0)
    return buffer


# =========================================================
# 4. FUNCIÓN FALTANTE (CERTIFICADO DONACIÓN)
# =========================================================

def generar_pdf_certificado(nombre, monto, hash_id):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(4.25*inch, 9*inch, "DIPLOMA OFICIAL DE DONACIÓN")

    c.setFont("Helvetica", 12)
    c.drawCentredString(4.25*inch, 8*inch, f"Otorgado a: {nombre}")
    c.drawCentredString(4.25*inch, 7.6*inch, f"Aporte: ${monto} USD")
    c.drawCentredString(4.25*inch, 7.2*inch, f"HASH: {hash_id}")

    c.save()
    buffer.seek(0)
    return buffer


# =========================================================
# 5. SESSION STATE
# =========================================================

if 'auth' not in st.session_state:
    st.session_state.auth = False

if 'wallet_connected' not in st.session_state:
    st.session_state.wallet_connected = False


# =========================================================
# 6. LOGIN
# =========================================================

if not st.session_state.auth:
    st.title("SISTEMA NEXUS | SERENITY")
    clave = st.text_input("PASSWORD ADMIN", type="password")

    if st.button("INGRESAR"):
        if clave == "Serenity2026":
            st.session_state.auth = True
            st.rerun()

    st.stop()


# =========================================================
# 7. MENÚ PRINCIPAL
# =========================================================

menu = st.sidebar.radio("CENTRO DE CONTROL", [
    "INICIO",
    "RED DE FAROS (7 NODOS)",
    "DASHBOARD ESTADÍSTICO IA",
    "GESTIÓN LEY 2173 (EMPRESAS)",
    "SUSCRIPCIONES",
    "BILLETERA CRYPTO (WEB3)",
    "DONACIONES Y CERTIFICADO",
    "DIAGNOSTICO HUELLA DE CARBONO",
    "UBICACIÓN & MAPAS"
])
























































































































































































































































































