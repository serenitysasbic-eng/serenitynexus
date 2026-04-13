# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import random
import hashlib
import io
import os
import base64
from datetime import datetime

# Librería opcional: se conserva por compatibilidad con tu código original
try:
    import librosa  # noqa: F401
except Exception:
    librosa = None

# --- LIBRERÍAS DE MAPAS ---
import folium
from streamlit_folium import st_folium

# --- LIBRERÍAS DE REPORTE (PDF) ---
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black
from reportlab.lib.utils import ImageReader

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================
st.set_page_config(
    page_title="Serenity Nexus Global",
    page_icon="🌿",
    layout="wide"
)

VERDE_SERENITY = HexColor("#2E7D32")
VERDE_LIMA_NEXUS = HexColor("#9BC63B")
AZUL_GEMINI = HexColor("#4285F4")
DORADO = HexColor("#D4AF37")

ADMIN_PASSWORD = os.getenv("SERENITY_ADMIN_PASSWORD", "Serenity2026")


# =========================================================
# HELPERS
# =========================================================
def init_session_state():
    defaults = {
        "total_protegido": 87.0,
        "donaciones_recibidas": 0,
        "estado_gemini": "Latente",
        "auth": False,
        "f_activo": None,
        "wallet_connected": False,
        "p_sel": None,
        "m_plan": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def dibujar_logo_serenity(c):
    try:
        if os.path.exists("logo_serenity.png"):
            c.drawImage(
                "logo_serenity.png",
                0.5 * inch,
                9.2 * inch,
                width=1.5 * inch,
                height=0.8 * inch,
                preserveAspectRatio=True,
                mask="auto",
            )
    except Exception:
        pass


def dibujar_logo_desde_bytes(c, logo_bytes, x=6 * inch, y=9.2 * inch, w=1.5 * inch, h=0.8 * inch):
    if not logo_bytes:
        return
    try:
        if hasattr(logo_bytes, "getvalue"):
            logo_bytes = logo_bytes.getvalue()
        logo_img = ImageReader(io.BytesIO(logo_bytes))
        c.drawImage(
            logo_img,
            x,
            y,
            width=w,
            height=h,
            preserveAspectRatio=True,
            mask="auto",
        )
    except Exception:
        pass


# =========================================================
# PDFS
# =========================================================
def generar_pdf_certificado(nombre_donante, monto, hash_id):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Marco
    c.setStrokeColor(VERDE_SERENITY)
    c.setLineWidth(3)
    c.rect(0.6 * inch, 0.6 * inch, 7.3 * inch, 9.7 * inch)

    # Logo / Cabecera
    dibujar_logo_serenity(c)
    c.setStrokeColor(VERDE_LIMA_NEXUS)
    c.setLineWidth(2)
    c.line(0.7 * inch, 10.0 * inch, 7.8 * inch, 10.0 * inch)

    # Título
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(VERDE_SERENITY)
    c.drawCentredString(4.25 * inch, 8.8 * inch, "DIPLOMA DE CONTRIBUCIÓN")
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(black)
    c.drawCentredString(4.25 * inch, 8.3 * inch, "SERENITY NEXUS GLOBAL")

    # Cuerpo
    text = c.beginText(1.0 * inch, 7.4 * inch)
    text.setFont("Helvetica", 12)
    text.setLeading(18)
    text.textLine("Se deja constancia de que:")
    text.textLine("")
    text.setFont("Helvetica-Bold", 16)
    text.textLine(nombre_donante.upper())
    text.setFont("Helvetica", 12)
    text.textLine("")
    text.textLine(f"ha realizado un aporte por valor de USD ${monto:,.2f}")
    text.textLine("destinado a procesos de regeneración biométrica, protección")
    text.textLine("ecosistémica y trazabilidad ambiental dentro de la Red Nexus.")
    text.textLine("")
    text.textLine(f"Fecha de emisión: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    text.textLine(f"Hash de integridad: {hash_id}")
    text.textLine("")
    text.textLine("Este documento ha sido generado electrónicamente y su")
    text.textLine("integridad puede verificarse mediante el serial consignado.")
    c.drawText(text)

    # Pie
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(
        4.25 * inch,
        1.1 * inch,
        "Documento emitido por Nexus IA | Serenity S.A.S. BIC"
    )

    c.save()
    buffer.seek(0)
    return buffer


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

    # 1. Membrete y logos
    c.setStrokeColor(VERDE_SERENITY)
    c.setLineWidth(2)
    c.line(0.5 * inch, 10.2 * inch, 8 * inch, 10.2 * inch)

    dibujar_logo_serenity(c)
    dibujar_logo_desde_bytes(c, logo_bytes)

    # 2. Título
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(VERDE_SERENITY)
    titulo = (
        "VADEMÉCUM TÉCNICO DE CUMPLIMIENTO LEGAL"
        if es_vademecum
        else "CERTIFICADO DE COMPENSACIÓN BIOMÉTRICA"
    )
    c.drawCentredString(4.25 * inch, 8.85 * inch, titulo)

    # 3. Encabezado
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.9 * inch, 8.35 * inch, f"RAZÓN SOCIAL: {empresa.upper()}")
    if nit:
        c.drawString(0.9 * inch, 8.10 * inch, f"NIT: {nit}")
    c.drawString(0.9 * inch, 7.85 * inch, f"NODO VALIDADOR: {faro_nombre}")
    c.drawString(0.9 * inch, 7.60 * inch, f"ID DE REGISTRO NEXUS: {hash_id}")

    # 4. Cuerpo
    text_object = c.beginText(0.9 * inch, 7.0 * inch)
    text_object.setFont("Helvetica", 11)
    text_object.setLeading(15)

    if es_vademecum:
        lineas = [
            "SOLUCIONES INTEGRADAS SERENITY S.A.S BIC:",
            "",
            "1. CUMPLIMIENTO LEY 2173 DE 2021 (ÁREAS DE VIDA):",
            "   Garantizamos la siembra y mantenimiento por 3 años de 2 árboles por empleado.",
            "   Nuestra labor: Geolocalización individual y custodia en la Hacienda Monte Guadua.",
            "",
            "2. CUMPLIMIENTO LEY 2169 DE 2021 (CARBONO NEUTRALIDAD):",
            "   Monitoreo mediante Faros Gemini para la certificación de captura de CO2 real.",
            "   Transformación de pasivos ambientales en activos biológicos verificables.",
            "",
            "3. PROTOCOLO LEY 2111 DE 2021 (DELITOS AMBIENTALES):",
            "   Vigilancia perimetral mediante IA para prevenir la deforestación y el ecocidio.",
            "",
            "CONCLUSIÓN TÉCNICA:",
            "La entidad referenciada se vincula al Internet de la Naturaleza,",
            "asegurando la trazabilidad absoluta de su inversión ambiental",
            "mediante monitoreo biométrico y registro digital verificable.",
        ]
    else:
        lineas = [
            "DETALLE DE COMPENSACIÓN:",
            f"- Gestión de {impacto} individuos forestales en el corredor biológico de Dagua.",
            "- Registro biométrico activo en la Red de Faros Serenity.",
            "- Estado de mantenimiento: Vigente bajo protocolos de restauración activa.",
            "- Este certificado avala la responsabilidad social y ambiental corporativa.",
            "",
            "FIRMA AUTORIZADA: Sistema Nexus IA - Serenity S.A.S BIC",
        ]

    for linea in lineas:
        text_object.textLine(linea)

    c.drawText(text_object)

    # 5. Pie de página
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(
        4.25 * inch,
        1.2 * inch,
        "Documento generado electrónicamente. La validez de este reporte puede verificarse en la cadena de integridad Nexus."
    )

    c.save()
    buffer.seek(0)
    return buffer


def generar_pdf_corporativo_1(
    empresa,
    impacto,
    hash_id,
    nit="",
    logo_bytes=None,
    es_vademecum=False,
    faro_nombre="Red Nexus"
):
    # Wrapper de compatibilidad con tu versión anterior
    return generar_pdf_corporativo(
        empresa=empresa,
        impacto=impacto,
        hash_id=hash_id,
        nit=nit,
        logo_bytes=logo_bytes,
        es_vademecum=es_vademecum,
        faro_nombre=faro_nombre,
    )


def generar_pdf_diagnostico(
    empresa,
    nit,
    impacto,
    hash_id,
    estudio_data,
    total_ton,
    faro_nombre="Red Nexus",
    logo_bytes=None,
    **kwargs
):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Logos y membrete
    dibujar_logo_serenity(c)
    dibujar_logo_desde_bytes(c, logo_bytes)

    c.setStrokeColor(VERDE_LIMA_NEXUS)
    c.setLineWidth(2)
    c.line(0.5 * inch, 10.2 * inch, 8 * inch, 10.2 * inch)

    # Título y datos
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(VERDE_SERENITY)
    c.drawCentredString(4.25 * inch, 9.45 * inch, "DIAGNÓSTICO DE HUELLA DE CARBONO")

    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.9 * inch, 8.85 * inch, f"ENTIDAD: {empresa.upper()}")
    c.drawString(0.9 * inch, 8.60 * inch, f"NIT: {nit}")
    c.drawString(0.9 * inch, 8.35 * inch, f"SERIAL DE INTEGRIDAD: {hash_id}")
    c.drawString(0.9 * inch, 8.10 * inch, f"NODO VALIDADOR: {faro_nombre}")
    c.drawString(0.9 * inch, 7.85 * inch, f"COMPENSACIÓN REFERENCIAL: {impacto} árboles")

    # Tabla
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(VERDE_LIMA_NEXUS)
    c.drawString(0.9 * inch, 7.45 * inch, "RESULTADOS DEL ESTUDIO (FACTORES UPME COLOMBIA):")

    c.setFont("Helvetica", 9)
    c.setFillColor(black)

    y_pos = 7.15
    for concepto, valor in estudio_data.items():
        c.drawString(1.1 * inch, y_pos * inch, f"• {concepto}:")
        c.drawRightString(7.4 * inch, y_pos * inch, f"{valor}")
        y_pos -= 0.22

    # Comparativa
    y_graf = y_pos - 0.45
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.9 * inch, y_graf * inch, "COMPARATIVA SECTORIAL (TON CO2E / MES):")

    promedio_sector = total_ton * 1.15 if total_ton > 0 else 1
    denominador = total_ton + promedio_sector if (total_ton + promedio_sector) > 0 else 1
    ancho_max = 3.0 * inch

    # Empresa
    c.setFillColor(VERDE_LIMA_NEXUS)
    ancho_empresa = (total_ton / denominador) * ancho_max * 2
    c.rect(3.2 * inch, (y_graf - 0.35) * inch, ancho_empresa, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(black)
    c.drawString(1.1 * inch, (y_graf - 0.30) * inch, "Su Empresa")

    # Promedio sector
    c.setFillColor(AZUL_GEMINI)
    ancho_sector = (promedio_sector / denominador) * ancho_max * 2
    c.rect(3.2 * inch, (y_graf - 0.65) * inch, ancho_sector, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(black)
    c.drawString(1.1 * inch, (y_graf - 0.60) * inch, "Promedio Sector")

    # Pie
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(
        4.25 * inch,
        1.2 * inch,
        "Diagnóstico estimado con base en parámetros operativos declarados por la entidad."
    )

    c.save()
    buffer.seek(0)
    return buffer


# =========================================================
# ESTILOS
# =========================================================
def aplicar_estilos():
    st.markdown(
        """
        <style>
            .stApp {
                background-image:
                    linear-gradient(rgba(5, 10, 4, 0.8), rgba(5, 10, 4, 0.9)),
                    url('https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1920&q=80');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                color: #e8f5e9;
                font-family: 'Montserrat', sans-serif;
            }

            label, .stMarkdown p, [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span, .stMetricLabel {
                color: white !important;
                font-weight: 500;
            }

            [data-testid="stSidebar"] {
                background-color: rgba(10, 20, 8, 0.9) !important;
                backdrop-filter: blur(10px);
            }

            h1, h2, h3 {
                color: #9BC63B !important;
                text-shadow: 2px 2px 4px #000;
            }

            .stButton>button {
                background-color: #2E7D32;
                color: white;
                border: 1px solid #9BC63B;
                border-radius: 8px;
                width: 100%;
                font-weight: bold;
            }

            .stButton>button:hover {
                background-color: #9BC63B;
                color: black;
                box-shadow: 0 0 15px #9BC63B;
            }

            .faro-card {
                border: 1px solid #9BC63B;
                padding: 15px;
                border-radius: 10px;
                background: rgba(0,0,0,0.6);
                text-align: center;
                height: 100%;
            }

            .faro-gemini, .faro-rex-gemini {
                border: 2px solid #4285F4;
                padding: 15px;
                border-radius: 10px;
                background: rgba(66, 133, 244, 0.2);
                text-align: center;
                box-shadow: 0 0 15px #4285F4;
            }

            .cam-grid {
                background: #000;
                border: 1px solid #2E7D32;
                height: 80px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 10px;
                color: #ff0000;
                border-radius: 5px;
            }

            .metric-card {
                background: rgba(0,0,0,0.7);
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #9BC63B;
                text-align: center;
            }

            .airline-grid {
                background: white;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 10px;
                height: 120px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
            }

            .airline-grid img {
                max-width: 90%;
                max-height: 70px;
                object-fit: contain;
            }

            .airline-grid p {
                color: black !important;
                font-size: 0.7rem;
                font-weight: bold;
                margin-top: 5px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# APP
# =========================================================
init_session_state()
aplicar_estilos()

# --- LOGIN ---
if not st.session_state.auth:
    st.markdown(
        "<div style='text-align:center; padding-top: 50px;'><h1>SISTEMA NEXUS | SERENITY</h1></div>",
        unsafe_allow_html=True
    )
    col_sec = st.columns([1, 1, 1])
    with col_sec[1]:
        clave = st.text_input("PASSWORD ADMIN", type="password")
        if st.button("INGRESAR"):
            if clave == ADMIN_PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
    st.stop()

# --- MENÚ ---
menu = st.sidebar.radio(
    "CENTRO DE CONTROL",
    [
        "INICIO",
        "RED DE FAROS (7 NODOS)",
        "DASHBOARD ESTADÍSTICO IA",
        "GESTIÓN LEY 2173 (EMPRESAS)",
        "SUSCRIPCIONES",
        "BILLETERA CRYPTO (WEB3)",
        "DONACIONES Y CERTIFICADO",
        "DIAGNOSTICO HUELLA DE CARBONO",
        "UBICACIÓN & MAPAS",
    ],
)

# =========================================================
# BLOQUE 1: INICIO
# =========================================================
if menu == "INICIO":
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        if os.path.exists("logo_serenity.png"):
            st.image("logo_serenity.png", use_container_width=True)
        else:
            st.markdown(
                "<h1 style='text-align:center; color:#9BC63B;'>SERENITY NEXUS GLOBAL</h1>",
                unsafe_allow_html=True,
            )

    st.markdown(
        "<h1 style='text-align:center; font-size:3.5rem;'>Serenity Nexus Global</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold;'>SISTEMA REGENERATIVO BIOMÉTRICO KBA</p>",
        unsafe_allow_html=True,
    )

    st.components.v1.html(
        """
        <audio id="audio_earth" src="sonido_Earth.mp3" loop></audio>
        <div style="text-align:center; margin-top:20px;">
            <button onclick="document.getElementById('audio_earth').play()"
                style="background:#2E7D32; color:white; border:1px solid #9BC63B;
                padding:10px 20px; border-radius:10px; cursor:pointer; font-weight:bold;">
                ACTIVAR SONIDO GLOBAL EARTH
            </button>
        </div>
        """,
        height=100,
    )

    st.info("SPAM (40%) | TAF (60%) | JWCJ $SNG")
    st.divider()

    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        st.subheader("QUIÉNES SOMOS / WHO WE ARE")
        st.write(
            "Serenity Nexus Global es la primera plataforma Phygital (Física + Digital) del Valle del Cauca que integra la conservación ambiental con tecnología Blockchain e Inteligencia Artificial, transformando la protección de la biodiversidad en un activo digital tangible."
        )

    with col_inf2:
        st.subheader("NUESTRA MISIÓN / OUR MISSION")
        st.write(
            "Regenerar el tejido ecológico y social mediante un modelo de negocio sostenible que permita a empresas y personas compensar su huella ambiental a través de la tecnología y la transparencia."
        )

    st.write("---")

    col_inf3, col_inf4 = st.columns([1, 2])
    with col_inf3:
        st.subheader("NUESTRA VISIÓN / OUR VISION")
    with col_inf4:
        st.write(
            "Ser el referente mundial del Internet de la Naturaleza para 2030, liderando la valorización de los servicios ecosistémicos mediante nuestra red de Faros inteligentes y el token $SNG."
        )

    st.info(
        "Ubicación del Proyecto: Dagua y Felidia, Valle del Cauca - Hacienda Monte Guadua & Finca Villa Michelle."
    )

# =========================================================
# BLOQUE 2: RED DE FAROS
# =========================================================
elif menu == "RED DE FAROS (7 NODOS)":
    st.title("🛰️ Monitoreo Perimetral Nexus")

    def conectar_faro(nombre):
        st.session_state.f_activo = nombre

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='faro-card'><h3>🦅 FARO HALCÓN</h3></div>", unsafe_allow_html=True)
        st.button("Conectar Halcón", key="h1", on_click=conectar_faro, args=("Halcón",), use_container_width=True)
    with c2:
        st.markdown("<div class='faro-card'><h3>🐦 FARO COLIBRÍ</h3></div>", unsafe_allow_html=True)
        st.button("Conectar Colibrí", key="c2", on_click=conectar_faro, args=("Colibrí",), use_container_width=True)
    with c3:
        st.markdown("<div class='faro-card'><h3>🐸 FARO RANA</h3></div>", unsafe_allow_html=True)
        st.button("Conectar Rana", key="r3", on_click=conectar_faro, args=("Rana",), use_container_width=True)

    st.write("")
    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("<div class='faro-card'><h3>🦌 FARO VENADO</h3></div>", unsafe_allow_html=True)
        st.button("Conectar Venado", key="v4", on_click=conectar_faro, args=("Venado",), use_container_width=True)
    with c5:
        st.markdown("<div class='faro-card'><h3>🐆 FARO TIGRILLO</h3></div>", unsafe_allow_html=True)
        st.button("Conectar Tigrillo", key="t5", on_click=conectar_faro, args=("Tigrillo",), use_container_width=True)
    with c6:
        st.markdown("<div class='faro-card'><h3>🦫 FARO CAPIBARA</h3></div>", unsafe_allow_html=True)
        st.button("Conectar Capibara", key="cp6", on_click=conectar_faro, args=("Capibara",), use_container_width=True)

    st.divider()

    col_rex_gemini = st.columns([1, 2, 1])
    with col_rex_gemini[1]:
        st.markdown("<div class='faro-rex-gemini' style='text-align:center;'><h3>🤖 REX GEMINI</h3></div>", unsafe_allow_html=True)
        st.button("ACTIVAR REX GEMINI VISION", key="gm_btn", on_click=conectar_faro, args=("REX GEMINI",), use_container_width=True)

    f_nom = st.session_state.get("f_activo", None)

    if f_nom:
        color_f = "#4285F4" if f_nom == "REX GEMINI" else "#9BC63B"
        nombre_limpio = str(f_nom).upper()

        st.write("---")
        st.markdown(
            f"<h2 style='text-align:center; color:{color_f};'>📡 FEED EN VIVO: {nombre_limpio}</h2>",
            unsafe_allow_html=True,
        )

        st.markdown("### 🎥 Unidades de Video Perimetral")
        url_v = "https://upload.wikimedia.org/wikipedia/commons/transcoded/1/18/Forest_Mountain_River.webm/Forest_Mountain_River.webm.480p.vp9.webm"

        c_cam = st.columns(4)
        posiciones = ["0% 0%", "50% 0%", "100% 0%", "0% 50%", "50% 50%", "100% 50%", "0% 100%", "50% 100%"]

        for i in range(8):
            with c_cam[i % 4]:
                html_video = f"""
                <div style="border: 2px solid {color_f}; border-radius: 8px; overflow: hidden; height: 100px; background: black;">
                    <video width="100%" height="100%" autoplay loop muted playsinline style="object-fit: cover; object-position: {posiciones[i]};">
                        <source src="{url_v}" type="video/webm">
                    </video>
                </div>
                <p style="font-size: 10px; color: {color_f}; text-align: center; margin-top: 2px; font-weight: bold;">NODO {i+1}</p>
                """
                st.components.v1.html(html_video, height=125)

        st.write("---")
        st.subheader("🎙️ Sensores Bioacústicos")
        a_links = [
            "https://www.soundjay.com/nature/sounds/forest-birds-01.mp3",
            "https://www.soundjay.com/nature/sounds/bird-chirp-01.mp3",
            "https://www.soundjay.com/nature/sounds/forest-birds-02.mp3",
            "https://www.soundjay.com/nature/sounds/river-1.mp3",
        ]
        c_snd = st.columns(4)
        for k in range(4):
            with c_snd[k]:
                st.markdown(f"<b style='color:{color_f}; font-size:11px;'>🎧 MIC {k+1}</b>", unsafe_allow_html=True)
                st.audio(a_links[k])

# =========================================================
# BLOQUE 3: DASHBOARD ESTADÍSTICO IA
# =========================================================
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("📊 Inteligencia de Datos Nexus")
    st.markdown("### Análisis Biométrico y Predictivo del Ecosistema")

    faro_seleccionado = st.selectbox(
        "Seleccione el Faro para Auditoría IA:",
        [
            "Faro Rex",
            "Faro Halcón",
            "Faro Colibrí",
            "Faro Rana",
            "Faro Venado",
            "Faro Tigrillo",
            "Faro Capibara",
        ],
    )
    st.write(f"Analizando telemetría en tiempo real de: **{faro_seleccionado}**")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Biodiversidad Index", "84%", "+2.1%")
    with col_m2:
        st.metric("CO2 Capturado", "1.2 Ton", "+15kg")
    with col_m3:
        st.metric("Humedad Suelo", "62%", "-0.5%")
    with col_m4:
        st.metric("Nivel Sonoro", "32 dB", "Natural")

    st.write("---")
    st.subheader("📈 Flujo de Actividad (24h)")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=["Audio (Biofonía)", "Visión (Fauna)", "Captura Carbono"],
    )
    st.line_chart(chart_data)

    with st.container(border=True):
        st.markdown("#### 🤖 Consulta al Oráculo Nexus")
        pregunta = st.text_input(
            "Pregunta a la IA sobre este Faro:",
            placeholder="Ej: ¿Cuál es el estado de la fauna en el Faro Tigrillo?",
        )

        if pregunta:
            with st.spinner("Analizando datos satelitales y biométricos..."):
                st.markdown(
                    f"""
                    **Respuesta Nexus AI:**  
                    Basado en el análisis de audio del **{faro_seleccionado}**, se han detectado frecuencias consistentes con aves endémicas en las últimas 3 horas.  
                    La biomasa protegida está procesando CO2 a niveles óptimos y no se detectan intrusiones humanas ni ruidos de maquinaria.
                    """
                )
                st.info("Este análisis utiliza la API de Google Gemini para interpretar los sensores de campo.")

    st.caption("Los datos presentados son validados mediante la Red Nexus y registrados en la Blockchain para transparencia total.")

# =========================================================
# BLOQUE 4: GESTIÓN LEY 2173 (EMPRESAS)
# =========================================================
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Nexus Legal & Compliance Hub")
    st.markdown("### Soluciones Tecnológicas a la Normativa Ambiental Colombiana")

    c_l1, c_l2, c_l3 = st.columns(3)
    with c_l1:
        st.markdown(
            '<div style="background:#1e2630; padding:15px; border-radius:10px; border-left:5px solid #9BC63B; min-height:180px;"><h4 style="color:#9BC63B;">LEY 2173</h4><p style="font-size:0.8rem; color:#ccc;"><b>Áreas de Vida:</b> Obligación de 2 árboles por empleado anualmente. Serenity provee el terreno y GPS oficial para cumplimiento corporativo.</p></div>',
            unsafe_allow_html=True,
        )
    with c_l2:
        st.markdown(
            '<div style="background:#1e2630; padding:15px; border-radius:10px; border-left:5px solid #3498db; min-height:180px;"><h4 style="color:#3498db;">LEY 2169</h4><p style="font-size:0.8rem; color:#ccc;"><b>Acción Climática:</b> Ruta a la Carbono Neutralidad. Nuestra IA certifica la captura real de CO2 para reportes en el RENARE.</p></div>',
            unsafe_allow_html=True,
        )
    with c_l3:
        st.markdown(
            '<div style="background:#1e2630; padding:15px; border-radius:10px; border-left:5px solid #e74c3c; min-height:180px;"><h4 style="color:#e74c3c;">LEY 2111</h4><p style="font-size:0.8rem; color:#ccc;"><b>Justicia Ambiental:</b> Delitos Ambientales. Los Faros actúan como evidencia digital inmutable ante la deforestación.</p></div>',
            unsafe_allow_html=True,
        )

    st.write("")

    with st.container(border=True):
        st.subheader("📘 Vademécum de Soluciones Corporativas")
        st.write("Genera un documento técnico que explica cómo Serenity Nexus ayuda a tu empresa a cumplir con las leyes ambientales.")

        empresa_v = st.text_input("Razón Social para el Reporte Técnico", placeholder="Ej: Transportes del Valle SAS", key="txt_vademecum")

        if st.button("GENERAR VADEMÉCUM TÉCNICO PDF", use_container_width=True):
            if empresa_v:
                hash_v = hashlib.sha256(f"{empresa_v}VAD".encode()).hexdigest()[:12].upper()
                pdf_v = generar_pdf_corporativo(
                    empresa=empresa_v,
                    impacto=0,
                    hash_id=hash_v,
                    es_vademecum=True
                )
                st.session_state.vademecum_pdf = pdf_v.getvalue()
                st.session_state.vademecum_empresa = empresa_v
                st.success(f"Vademécum para {empresa_v} generado exitosamente.")
            else:
                st.warning("Por favor, ingrese el nombre de la empresa.")

        if "vademecum_pdf" in st.session_state:
            st.download_button(
                label="📥 DESCARGAR VADEMÉCUM (PDF ESTRUCTURADO)",
                data=st.session_state.vademecum_pdf,
                file_name=f"Vademecum_Nexus_{st.session_state.get('vademecum_empresa', 'empresa')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    st.divider()

    st.subheader("🏢 Emisión de Certificado con Logo")
    st.write("Cargue el logo de su empresa para emitir el certificado oficial de cumplimiento de la Ley 2173.")

    col_act1, col_act2 = st.columns([1, 1])

    with col_act1:
        n_corp = st.text_input("Nombre de la Compañía (Para el Certificado)", key="txt_corp")
        nit_corp = st.text_input("NIT de la Empresa", placeholder="900.123.456-1", key="nit_corp")
        n_per = st.number_input("Número de Empleados Actuales", min_value=1, value=100, key="num_emp")
        archivo_logo = st.file_uploader("Cargar Logo Corporativo (PNG/JPG)", type=["png", "jpg", "jpeg"], key="file_logo")

    with col_act2:
        st.info(f"**Requisito Ley 2173:** Su empresa debe compensar {n_per * 2} árboles este año.")

        if st.button("EMITIR CERTIFICADO OFICIAL CON LOGO", use_container_width=True):
            if n_corp and archivo_logo:
                with st.spinner("Procesando identidad corporativa..."):
                    h_c = hashlib.sha256(f"{n_corp}{nit_corp}".encode()).hexdigest()[:12].upper()
                    archivo_logo.seek(0)
                    logo_bytes = archivo_logo.getvalue()

                    pdf_c = generar_pdf_corporativo(
                        empresa=n_corp,
                        impacto=n_per * 2,
                        hash_id=h_c,
                        nit=nit_corp,
                        logo_bytes=logo_bytes,
                        es_vademecum=False,
                        faro_nombre="Faro Rex",
                    )

                    st.session_state.cert_corp_pdf = pdf_c.getvalue()
                    st.session_state.cert_corp_nombre = n_corp
                    st.success("Certificado generado exitosamente.")
            else:
                st.error("Razón Social y Logo son obligatorios.")

        if "cert_corp_pdf" in st.session_state:
            st.download_button(
                label="📥 DESCARGAR CERTIFICADO CON LOGO (PDF)",
                data=st.session_state.cert_corp_pdf,
                file_name=f"Certificado_Ley2173_{st.session_state.get('cert_corp_nombre', 'empresa')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

# =========================================================
# BLOQUE 5: SUSCRIPCIONES
# =========================================================
elif menu == "SUSCRIPCIONES":
    st.title("Membresías de Impacto Serenity")
    st.markdown("### Transforma tu aporte en regeneración real")

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown(
            """
            <div style="background:#1e2630; padding:20px; border-radius:15px; border:2px solid #9BC63B; text-align:center; min-height: 420px;">
                <h3 style="color:#9BC63B;">PLAN SEMILLA</h3>
                <h2 style="color:white;">$25 USD <small>/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;"><b>5 Árboles:</b> Siembra y mantenimiento.</p>
                <p style="text-align:left; font-size:0.9rem;"><b>1 Faro:</b> Datos biométricos básicos.</p>
                <p style="text-align:left; font-size:0.9rem;"><b>50 Tokens:</b> $SNG de respaldo.</p>
                <p style="text-align:left; font-size:0.9rem;"><b>Certificado:</b> Digital con Hash.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("ELEGIR SEMILLA", use_container_width=True, key="p_semilla"):
            st.session_state.p_sel = "SEMILLA"
            st.session_state.m_plan = 25

    with p2:
        st.markdown(
            """
            <div style="background:#1e2630; padding:20px; border-radius:15px; border:3px solid #9BC63B; text-align:center; min-height: 420px; transform: scale(1.02);">
                <h3 style="color:#9BC63B;">PLAN GUARDIÁN</h3>
                <h2 style="color:white;">$80 USD <small>/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;"><b>15 Árboles:</b> Restauración activa.</p>
                <p style="text-align:left; font-size:0.9rem;"><b>Cámaras 4K:</b> Streaming del bosque.</p>
                <p style="text-align:left; font-size:0.9rem;"><b>200 Tokens:</b> Mayor respaldo $SNG.</p>
                <p style="text-align:left; font-size:0.9rem;"><b>Reporte IA:</b> Inventario de carbono.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("ELEGIR GUARDIÁN", use_container_width=True, key="p_guardian"):
            st.session_state.p_sel = "GUARDIÁN"
            st.session_state.m_plan = 80

    with p3:
        st.markdown(
            """
            <div style="background:#1e2630; padding:20px; border-radius:15px; border:2px solid #D4AF37; text-align:center; min-height: 420px;">
                <h3 style="color:#D4AF37;">PLAN HALCÓN</h3>
                <h2 style="color:white;">$200 USD <small>/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;"><b>1 Plaza Protegida:</b> Soberanía total.</p>
                <p style="text-align:left; font-size:0.9rem;"><b>Cámaras:</b> Vigilancia perimetral.</p>
                <p style="text-align:left; font-size:0.9rem;"><b>600 Tokens:</b> Impacto Web3 máximo.</p>
                <p style="text-align:left; font-size:0.9rem;"><b>Visita 1 Persona VIP:</b> Acceso a Monte Guadua 2 Días 1 Noche.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("ELEGIR HALCÓN", use_container_width=True, key="p_halcon"):
            st.session_state.p_sel = "HALCÓN"
            st.session_state.m_plan = 200

    if st.session_state.get("p_sel"):
        st.write("---")
        st.subheader(f"Finalizar Suscripción: {st.session_state.p_sel}")

        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            with st.container(border=True):
                st.markdown("#### Tarjeta de Crédito/Débito")
                st.text_input("Titular de la cuenta")
                st.text_input("Número de Tarjeta", placeholder="xxxx xxxx xxxx xxxx")
                c_exp, c_cvc = st.columns(2)
                with c_exp:
                    st.text_input("Vencimiento (MM/AA)")
                with c_cvc:
                    st.text_input("CVC")
                if st.button("ACTIVAR SUSCRIPCIÓN", use_container_width=True):
                    st.balloons()
                    st.success(f"¡Bienvenido al Plan {st.session_state.p_sel}! Impacto activado.")

        with col_pay2:
            st.markdown("#### Pagos Locales y Alternativos")
            st.markdown(
                """
                <div style="background: #ffffff; padding: 25px; border-radius: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center; border: 1px solid #ddd;">
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/b/bf/Nequi_logo.png" width="90"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Bancolombia_logo.svg/2560px-Bancolombia_logo.svg.png" width="90"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Visa_Inc._logo.svg/2560px-Visa_Inc._logo.svg.png" width="70"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/1280px-Mastercard-logo.svg.png" width="70"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.caption("Transacciones seguras mediante Nexus Gateway (Dagua-Colombia)")

# =========================================================
# BLOQUE 6: BILLETERA CRYPTO (WEB3)
# =========================================================
elif menu == "BILLETERA CRYPTO (WEB3)":
    st.title("Nexus Finance Control")
    st.markdown("### El Futuro de la Conservación Tokenizada")

    try:
        if os.path.exists("video_sng.mp4"):
            with open("video_sng.mp4", "rb") as f:
                data = f.read()
                bin_str = base64.b64encode(data).decode()
            video_html = f"""
                <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                    <video width="60%" autoplay loop muted playsinline style="border-radius: 20px; border: 2px solid #9BC63B; box-shadow: 0 0 30px rgba(155, 198, 59, 0.3);">
                        <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
                    </video>
                </div>
            """
            st.markdown(video_html, unsafe_allow_html=True)
        else:
            st.info("🪙 Visualizador de Token $SNG Activo (Esperando archivo de video)")
    except Exception:
        st.info("🪙 Sistema de Video Nexus en Espera")

    st.write("---")

    col_buy, col_vault = st.columns(2)

    with col_buy:
        st.markdown("<h4 style='color:#9BC63B;'>¿Cómo comprar $SNG?</h4>", unsafe_allow_html=True)
        st.write("El token $SNG representa hectáreas regeneradas y datos biométricos de los Faros.")
        with st.container(border=True):
            st.markdown("<p style='color:white; font-weight:bold;'>Simulador de Intercambio (Swap)</p>", unsafe_allow_html=True)
            moneda_pago = st.selectbox("Pagar con:", ["USD (Tarjeta/Transferencia)", "USDT (Crypto)", "Ethereum"])
            cantidad_usd = st.number_input("Monto a invertir (USD):", min_value=10, step=50, key="wallet_buy_usd")
            tasa = 0.50
            st.metric("Recibirás aproximadamente:", f"{cantidad_usd / tasa:,.2f} $SNG")
            if st.button("COMPRAR TOKENS $SNG", use_container_width=True):
                st.success(f"Orden de compra enviada al Nexus Gateway usando {moneda_pago}.")

    with col_vault:
        st.markdown("<h4 style='color:#9BC63B;'>¿Cómo tener una Billetera Nexus?</h4>", unsafe_allow_html=True)
        st.write("Nexus Vault es tu llave privada al Internet de la Naturaleza.")
        st.markdown(
            """
            <div style='color:white;'>
                <p>• <b>Paso 1:</b> Descarga Nexus App o usa Metamask.</p>
                <p>• <b>Paso 2:</b> Genera tu frase semilla de 24 palabras.</p>
                <p>• <b>Paso 3:</b> Vincula tu ID de Donante Serenity.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("DESCARGAR GUÍA DE CONFIGURACIÓN", use_container_width=True)

    st.write("---")
    st.markdown("<h4 style='color:white; text-align:center;'>Centro de Conexión Web3</h4>", unsafe_allow_html=True)
    cw1, cw2, cw3 = st.columns([1, 2, 1])

    with cw2:
        if st.button("VINCULAR BILLETERA AL SISTEMA NEXUS", use_container_width=True):
            st.session_state.wallet_connected = True
            st.balloons()

    if st.session_state.get("wallet_connected", False):
        st.success("Billetera 0x71C...9A23 Conectada con éxito.")

        col_met1, col_met2 = st.columns(2)
        with col_met1:
            st.metric(label="Saldo en Bóveda", value="25,000.00 $SNG")
        with col_met2:
            st.metric(label="Respaldo Real", value="80 Hectáreas", delta="Sincronizado")

        st.write("")
        st.markdown(
            "<h5 style='color:white; text-align:center; background:#2E7D32; padding:10px; border-radius:5px;'>🔐 DESGLOSE DE ACTIVOS RESPALDADOS POR FARO</h5>",
            unsafe_allow_html=True,
        )

        data_wallet = {
            "Activo Biológico": ["Carbono Azul", "Biodiversidad", "Agua Protegida", "Suelo Regenerado"],
            "Nodo Validador": ["Faro Rex", "Faro Tigrillo", "Faro Colibrí", "Faro Halcón"],
            "Tokens $SNG": ["5,000", "8,500", "3,200", "8,300"],
            "Certificación": ["✅ Verificado", "✅ Verificado", "🔄 Sincronizando", "✅ Verificado"],
        }
        df_wallet = pd.DataFrame(data_wallet)

        st.markdown(
            """
            <style>
                .stTable td, .stTable th {
                    color: white !important;
                    font-size: 1.05rem !important;
                    text-align: center !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.table(df_wallet)
        st.caption("Los datos biométricos son actualizados cada 60 segundos por la Red de Faros.")

# =========================================================
# BLOQUE 7: DONACIONES Y CERTIFICADO
# =========================================================
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("Generador de Diploma y Certificado Nexus")
    st.markdown("### Registro de Aportes a la Regeneración Biométrica")

    colA, colB = st.columns([1, 1])

    with colA:
        with st.container(border=True):
            st.markdown("#### Datos del Donante")
            nombre_d = st.text_input("Nombre Completo o Razón Social")
            monto_d = st.number_input("Monto del Aporte (USD)", min_value=1, step=10)

            if st.button("REGISTRAR APORTE Y GENERAR HASH"):
                if nombre_d:
                    datos_hash = f"{nombre_d}{monto_d}{datetime.now()}"
                    hash_certificado = hashlib.sha256(datos_hash.encode()).hexdigest()[:16].upper()

                    st.session_state.current_hash = hash_certificado
                    st.session_state.nombre_prev = nombre_d
                    st.session_state.monto_prev = monto_d
                    st.session_state.pdf_buffer = generar_pdf_certificado(nombre_d, monto_d, hash_certificado).getvalue()

                    st.session_state.donaciones_recibidas += 1
                    st.balloons()
                    st.success("¡Certificado generado con éxito!")
                else:
                    st.warning("Ingrese el nombre del donante.")

    with colB:
        if "pdf_buffer" in st.session_state:
            st.markdown(
                f"""
                <div style="background:white; color:black; padding:30px; text-align:center; border:8px double #2E7D32; border-radius:15px;">
                    <h2 style="color:#2E7D32; margin-bottom:10px;">VISTA PREVIA</h2>
                    <hr style="border:1px solid #2E7D32;">
                    <p style="font-size:1.2rem; margin-top:20px;">Gracias por tu aporte, <b>{st.session_state.nombre_prev.upper()}</b></p>
                    <p>Has contribuido con <b>${st.session_state.monto_prev} USD</b></p>
                    <div style="background:#f0f2f6; padding:10px; border-radius:5px; margin-top:20px;">
                        <code style="font-size:0.8rem; color: #2E7D32;">HASH: {st.session_state.current_hash}</code>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")
            st.download_button(
                label="DESCARGAR DIPLOMA CON HASH (PDF)",
                data=st.session_state.pdf_buffer,
                file_name=f"Certificado_Nexus_{st.session_state.current_hash}.pdf",
                mime="application/pdf",
            )

# =========================================================
# BLOQUE 8: DIAGNOSTICO HUELLA DE CARBONO
# =========================================================
elif menu == "DIAGNOSTICO HUELLA DE CARBONO":
    st.title("🌍 Inteligencia de Carbono Nexus")
    st.markdown("### Diagnóstico Automatizado de Huella de Carbono")

    with st.container(border=True):
        col_nit1, col_nit2 = st.columns([1, 1])
        with col_nit1:
            nit_empresa = st.text_input(
                "INGRESE EL NIT DE LA EMPRESA (Sin dígito de verificación)",
                placeholder="900123456"
            )
        with col_nit2:
            nombre_empresa = st.text_input(
                "RAZÓN SOCIAL",
                placeholder="Ej: TRANSPORTES VALLE SAS"
            )

    if nit_empresa and nombre_empresa:
        st.subheader(f"🧠 Análisis de Impacto: {nombre_empresa}")

        sector_deducido = "Transporte Multimodal y Logística"
        intensidad_carbono = "ALTA"

        st.markdown(
            f"**Sector Detectado:** `{sector_deducido}` | **Intensidad de Emisión:** `{intensidad_carbono}`"
        )

        with st.expander("📦 Parámetros de Operación Mensual", expanded=True):
            col_par1, col_par2 = st.columns(2)
            with col_par1:
                consumo_energia = st.number_input("Consumo Energía (kWh/mes)", min_value=0, value=1500)
                flota_vehicular = st.number_input("Número de Vehículos / Aeronaves en Operación", min_value=0, value=5)
            with col_par2:
                residuos_ton = st.number_input("Producción de Residuos (Toneladas/mes)", min_value=0.0, value=1.2)
                operaciones_dia = st.number_input("Promedio Operaciones Diarias", min_value=1, value=10)

        huella_total_kg = (
            (consumo_energia * 0.164) +
            (flota_vehicular * operaciones_dia * 15.5) +
            (residuos_ton * 500)
        )
        huella_total_ton = huella_total_kg / 1000
        arboles_nexus = int(huella_total_kg / 20)

        res1, res2 = st.columns(2)
        with res1:
            st.metric("HUELLA ESTIMADA MÁXIMA", f"{huella_total_kg:,.2f} kg CO2e / mes")
            st.progress(85 if intensidad_carbono == "ALTA" else 30)
        with res2:
            st.metric("COMPENSACIÓN REQUERIDA", f"{arboles_nexus} Árboles", "Activos Biológicos")

        estudio_data = {
            "Sector Económico Inferido": sector_deducido,
            "Intensidad de Emisión": intensidad_carbono,
            "Consumo Energía": f"{consumo_energia:,} kWh/mes",
            "Flota Operativa": f"{flota_vehicular} unidades",
            "Residuos Generados": f"{residuos_ton:.2f} ton/mes",
            "Operaciones Promedio": f"{operaciones_dia} por día",
            "Huella Estimada": f"{huella_total_kg:,.2f} kg CO2e/mes",
            "Compensación Referencial": f"{arboles_nexus} árboles Nexus",
        }

        hash_id = hashlib.sha512(f"{nit_empresa}{huella_total_kg}".encode()).hexdigest()[:16].upper()

        pdf_diag = generar_pdf_diagnostico(
            empresa=nombre_empresa,
            nit=nit_empresa,
            impacto=arboles_nexus,
            hash_id=hash_id,
            estudio_data=estudio_data,
            total_ton=huella_total_ton,
            faro_nombre="Faro Rex"
        )

        st.download_button(
            label=f"📥 EMITIR DIAGNÓSTICO LEGAL DE COMPENSACIÓN PARA {nombre_empresa}",
            data=pdf_diag.getvalue(),
            file_name=f"Diagnostico_Nexus_{nit_empresa}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# =========================================================
# BLOQUE 9: UBICACIÓN & MAPAS
# =========================================================
elif menu == "UBICACIÓN & MAPAS":
    st.title("🗺️ Geoposicionamiento Nexus Global")
    st.markdown("### Monitoreo Satelital de Faros en KBA Bosque San Antonio")
    lat_v, lon_v = 3.485, -76.605

faros_nexus = [
        {"name": "Faro Halcón (Monte Guadua)", "lat": 3.518, "lon": -76.620, "color": "green"},
        {"name": "Faro Colibrí (Monte Guadua)", "lat": 3.519, "lon": -76.622, "color": "green"},
        {"name": "Faro Rana (Monte Guadua)", "lat": 3.517, "lon": -76.621, "color": "green"},
        {"name": "Faro Venado (Monte Guadua)", "lat": 3.516, "lon": -76.623, "color": "green"},
        {"name": "Faro Tigrillo (Monte Guadua)", "lat": 3.520, "lon": -76.619, "color": "green"},
        {"name": "Faro Capibara (Monte Guadua)", "lat": 3.515, "lon": -76.625, "color": "green"},
        {"name": "Faro Rex (Villa Michelle)", "lat": 3.485, "lon": -76.605, "color": "blue"}
    ]
    url_gmaps = f"https://www.google.com/maps/@{lat_v},{lon_v},18z/data=!3m1!1e3"

    st.markdown(
        f"""
        <div style='text-align:center; margin-bottom: 25px;'>
            <a href="{url_gmaps}" target="_blank" style="text-decoration: none;">
                <button style="background-color:#4285F4; color:white; border:none; padding:12px 25px; border-radius:8px; font-weight:bold; cursor:pointer; box-shadow: 0 4px 15px rgba(66, 133, 244, 0.4); font-family:sans-serif;">
                    ABRIR RADAR EXTERNO (GOOGLE MAPS)
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    google_map_tiles = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"

    m = folium.Map(
        location=[3.518, -76.620],
        zoom_start=14,
        tiles=google_map_tiles,
        attr="Google Satellite",
    )

for faro in faros_nexus:
    # Radio de captura de los 4 micrófonos (200 metros)
    folium.Circle(
        location=[faro['lat'], faro['lon']],
        radius=200,
        color=faro['color'],
        fill=True,
        fill_opacity=0.2,
        tooltip=f"Rango de Audio: {faro['name']}"  # <--- ASEGÚRATE QUE ESTÉ ASÍ
    ).add_to(m)

    # Marcador de estructura de pino canadiense
    folium.Marker(
        location=[faro['lat'], faro['lon']],
        popup=f"<b>{faro['name']}</b><br>Estructura: 3x2x3 Pino<br>Enlace: Starlink",
        icon=folium.Icon(color=faro['color'], icon='broadcast-tower', prefix='fa')
    ).add_to(m)




































































































































































































































































































































































































































































































































































































































































































































































































