# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import random
import hashlib
import io
import os
import base64
import time
from datetime import datetime
from io import BytesIO  # Necesario para el manejo de PDFs en memoria

# --- LIBRERÍAS DE MAPAS & GEOPOSICIONAMIENTO ---
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap  # Fundamental para los mapas de deforestación

# --- LIBRERÍAS DE REPORTE (PDF - ReportLab) ---
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black
from reportlab.lib.utils import ImageReader

# --- PROCESAMIENTO DE AUDIO (Opcional) ---
try:
    import librosa  # Se conserva por compatibilidad con bioacústica
except ImportError:
    librosa = None

# =========================================================
# CONFIGURACIÓN DE PÁGINA (Debe ser el primer comando de ST)
# =========================================================
st.set_page_config(
    page_title="Serenity Nexus Global",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================
st.set_page_config(
    page_title="Serenity Nexus Global",
    page_icon="🌿",
    layout="wide"
)

# Definición de Colores Corporativos para ReportLab (PDF)
VERDE_SERENITY = HexColor("#2E7D32")
VERDE_LIMA_NEXUS = HexColor("#9BC63B")
AZUL_GEMINI = HexColor("#4285F4")
DORADO = HexColor("#D4AF37")

# Seguridad: Contraseña de administración
ADMIN_PASSWORD = os.getenv("SERENITY_ADMIN_PASSWORD", "Serenity2026")

# =========================================================
# HELPERS (FUNCIONES DE APOYO)
# =========================================================

def init_session_state():
    """Inicializa las variables globales de la aplicación"""
    defaults = {
        "total_protegido": 87.0,
        "donaciones_recibidas": 0,
        "estado_gemini": "Latente",
        "auth": False,
        "f_activo": None,
        "wallet_connected": False,
        "p_sel": None,
        "m_plan": None,
        # Variables nuevas para evitar errores en Bloque 7 y 8
        "current_hash": None,
        "nombre_prev": "",
        "monto_prev": 0,
        "pdf_buffer": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def dibujar_logo_serenity(c):
    """Dibuja el logo principal desde un archivo local en el PDF"""
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
    """Dibuja logos dinámicos (como el QR o logos de aliados) desde memoria"""
    if not logo_bytes:
        return
    try:
        # Si recibimos un objeto BytesIO, extraemos el contenido
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

# Llamamos a la inicialización al cargar
init_session_state()

# =========================================================
# PDFS: GENERACIÓN DE DOCUMENTOS LEGALES Y TÉCNICOS
# =========================================================

def generar_pdf_certificado(nombre_donante, monto, hash_id):
    """Genera el diploma para donantes individuales (Bloque 7)"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Marco decorativo
    c.setStrokeColor(VERDE_SERENITY)
    c.setLineWidth(3)
    c.rect(0.6 * inch, 0.6 * inch, 7.3 * inch, 9.7 * inch)

    # Cabecera
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

    # Cuerpo del documento
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

    # Pie de página
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(4.25 * inch, 1.1 * inch, "Documento emitido por Nexus IA | Serenity S.A.S. BIC")

    c.save()
    buffer.seek(0)
    return buffer

def generar_pdf_corporativo(empresa, impacto, hash_id, nit="", logo_bytes=None, es_vademecum=False, faro_nombre="Red Nexus"):
    """Genera certificados de cumplimiento (Leyes 2173, 2169, 2111)"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setStrokeColor(VERDE_SERENITY)
    c.setLineWidth(2)
    c.line(0.5 * inch, 10.2 * inch, 8 * inch, 10.2 * inch)

    dibujar_logo_serenity(c)
    dibujar_logo_desde_bytes(c, logo_bytes)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(VERDE_SERENITY)
    titulo = "VADEMÉCUM TÉCNICO DE CUMPLIMIENTO LEGAL" if es_vademecum else "CERTIFICADO DE COMPENSACIÓN BIOMÉTRICA"
    c.drawCentredString(4.25 * inch, 8.85 * inch, titulo)

    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.9 * inch, 8.35 * inch, f"RAZÓN SOCIAL: {empresa.upper()}")
    if nit: c.drawString(0.9 * inch, 8.10 * inch, f"NIT: {nit}")
    c.drawString(0.9 * inch, 7.85 * inch, f"NODO VALIDADOR: {faro_nombre}")
    c.drawString(0.9 * inch, 7.60 * inch, f"ID DE REGISTRO NEXUS: {hash_id}")

    text_object = c.beginText(0.9 * inch, 7.0 * inch)
    text_object.setFont("Helvetica", 11)
    text_object.setLeading(15)

    if es_vademecum:
        lineas = [
            "SOLUCIONES INTEGRADAS SERENITY S.A.S BIC:", "",
            "1. CUMPLIMIENTO LEY 2173 DE 2021 (ÁREAS DE VIDA):",
            "   Garantizamos la siembra y mantenimiento por 3 años de 2 árboles por empleado.",
            "   Nuestra labor: Geolocalización individual y custodia en la Hacienda Monte Guadua.", "",
            "2. CUMPLIMIENTO LEY 2169 DE 2021 (CARBONO NEUTRALIDAD):",
            "   Monitoreo mediante Faros Gemini para la certificación de captura de CO2 real.",
            "   Transformación de pasivos ambientales en activos biológicos verificables.", "",
            "3. PROTOCOLO LEY 2111 DE 2021 (DELITOS AMBIENTALES):",
            "   Vigilancia perimetral mediante IA para prevenir la deforestación y el ecocidio.", "",
            "CONCLUSIÓN TÉCNICA:",
            "La entidad referenciada se vincula al Internet de la Naturaleza,",
            "asegurando la trazabilidad absoluta de su inversión ambiental.",
        ]
    else:
        lineas = [
            "DETALLE DE COMPENSACIÓN:",
            f"- Gestión de {impacto} individuos forestales en el corredor biológico de Dagua.",
            "- Registro biométrico activo en la Red de Faros Serenity.",
            "- Estado de mantenimiento: Vigente bajo protocolos de restauración activa.",
            "- Este certificado avala la responsabilidad social y ambiental corporativa.", "",
            "FIRMA AUTORIZADA: Sistema Nexus IA - Serenity S.A.S BIC",
        ]

    for linea in lineas: text_object.textLine(linea)
    c.drawText(text_object)

    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(4.25 * inch, 1.2 * inch, "La validez de este reporte puede verificarse en la cadena de integridad Nexus.")

    c.save()
    buffer.seek(0)
    return buffer

def generar_pdf_diagnostico(empresa, nit, impacto, hash_id, estudio_data, total_ton, faro_nombre="Red Nexus", logo_bytes=None, **kwargs):
    """Genera el reporte técnico de Huella de Carbono (Bloque 8)"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    dibujar_logo_serenity(c)
    dibujar_logo_desde_bytes(c, logo_bytes)

    c.setStrokeColor(VERDE_LIMA_NEXUS)
    c.setLineWidth(2)
    c.line(0.5 * inch, 10.2 * inch, 8 * inch, 10.2 * inch)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(VERDE_SERENITY)
    c.drawCentredString(4.25 * inch, 9.45 * inch, "DIAGNÓSTICO DE HUELLA DE CARBONO")

    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.9 * inch, 8.85 * inch, f"ENTIDAD: {empresa.upper()}")
    c.drawString(0.9 * inch, 8.60 * inch, f"NIT: {nit}")
    c.drawString(0.9 * inch, 8.35 * inch, f"SERIAL DE INTEGRIDAD: {hash_id}")
    c.drawString(0.9 * inch, 8.10 * inch, f"NODO VALIDADOR: {faro_nombre}")

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(VERDE_LIMA_NEXUS)
    c.drawString(0.9 * inch, 7.65 * inch, "RESULTADOS DEL ESTUDIO (FACTORES UPME COLOMBIA):")

    c.setFont("Helvetica", 9)
    c.setFillColor(black)
    y_pos = 7.35
    for concepto, valor in estudio_data.items():
        c.drawString(1.1 * inch, y_pos * inch, f"• {concepto}:")
        c.drawRightString(7.4 * inch, y_pos * inch, f"{valor}")
        y_pos -= 0.22

    # Gráfico de barras comparativo (Simple canvas drawing)
    y_graf = y_pos - 0.5
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.9 * inch, y_graf * inch, "COMPARATIVA SECTORIAL (TON CO2E / MES):")
    
    ancho_base = 3.0 * inch
    # Barra Empresa
    c.setFillColor(VERDE_LIMA_NEXUS)
    c.rect(3.2 * inch, (y_graf - 0.35) * inch, ancho_base * 0.7, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(black)
    c.drawString(1.1 * inch, (y_graf - 0.30) * inch, "Su Empresa (Actual)")
    
    # Barra Promedio
    c.setFillColor(colors.lightgrey)
    c.rect(3.2 * inch, (y_graf - 0.65) * inch, ancho_base, 0.18 * inch, fill=1, stroke=0)
    c.setFillColor(black)
    c.drawString(1.1 * inch, (y_graf - 0.60) * inch, "Promedio Industrial")

    c.save()
    buffer.seek(0)
    return buffer

# =========================================================
# ESTILOS (CSS PERSONALIZADO)
# =========================================================
def aplicar_estilos():
    st.markdown(
        """
        <style>
            /* Fondo de la aplicación con superposición oscura para legibilidad */
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

            /* Estilo de textos generales y Sidebar */
            label, .stMarkdown p, [data-testid="stSidebar"] p, 
            [data-testid="stSidebar"] span, .stMetricLabel {
                color: white !important;
                font-weight: 500;
            }

            /* Efecto Glassmorphism en el Sidebar */
            [data-testid="stSidebar"] {
                background-color: rgba(10, 20, 8, 0.9) !important;
                backdrop-filter: blur(10px);
                border-right: 1px solid #2E7D32;
            }

            /* Encabezados con color institucional Serenity */
            h1, h2, h3 {
                color: #9BC63B !important;
                text-shadow: 2px 2px 4px #000;
            }

            /* Botones estilo "Guardian" */
            .stButton>button {
                background-color: #2E7D32;
                color: white;
                border: 1px solid #9BC63B;
                border-radius: 8px;
                width: 100%;
                font-weight: bold;
                transition: all 0.3s ease;
            }

            .stButton>button:hover {
                background-color: #9BC63B;
                color: black;
                box-shadow: 0 0 15px #9BC63B;
                transform: translateY(-2px);
            }

            /* Tarjetas de los Faros (Bloque 2 y 9) */
            .faro-card {
                border: 1px solid #9BC63B;
                padding: 15px;
                border-radius: 10px;
                background: rgba(0,0,0,0.6);
                text-align: center;
                height: 100%;
            }

            /* Estilo especial para nodos integrados con Google Gemini */
            .faro-gemini, .faro-rex-gemini {
                border: 2px solid #4285F4;
                padding: 15px;
                border-radius: 10px;
                background: rgba(66, 133, 244, 0.2);
                text-align: center;
                box-shadow: 0 0 15px #4285F4;
            }

            /* Grid para el mosaico de cámaras (Bloque 2) */
            .cam-grid {
                background: #000;
                border: 1px solid #2E7D32;
                height: 80px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 10px;
                color: #ff0000; /* Color de alerta/grabación */
                border-radius: 5px;
            }

            /* Tarjetas de métricas ambientales */
            .metric-card {
                background: rgba(0,0,0,0.7);
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #9BC63B;
                text-align: center;
            }

            /* Grid para logos de aerolíneas o aliados (Diagnóstico) */
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
    # 1. Encabezado con Logo o Título Alternativo
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        if os.path.exists("logo_serenity.png"):
            st.image("logo_serenity.png", use_container_width=True)
        else:
            st.markdown(
                "<h1 style='text-align:center; color:#9BC63B; margin-bottom:0;'>SERENITY NEXUS GLOBAL</h1>",
                unsafe_allow_html=True,
            )

    # 2. Subtítulo Dinámico
    st.markdown(
        """
        <p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold; margin-top:-10px;'>
            SISTEMA REGENERATIVO BIOMÉTRICO KBA
        </p>
        """,
        unsafe_allow_html=True,
    )

    # 3. Componente de Audio (Optimizado en altura)
    st.components.v1.html(
        """
        <audio id="audio_earth" src="sonido_Earth.mp3" loop></audio>
        <div style="text-align:center;">
            <button onclick="document.getElementById('audio_earth').play()"
                style="background:#2E7D32; color:white; border:2px solid #9BC63B;
                padding:8px 16px; border-radius:10px; cursor:pointer; font-weight:bold;
                transition: 0.3s; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                🔊 ACTIVAR SONIDO GLOBAL EARTH
            </button>
        </div>
        """,
        height=60, # Reducido para evitar espacios muertos
    )

    st.info("📊 **Métricas clave:** SPAM (40%) | TAF (60%) | **Token:** JWCJ $SNG")
    st.divider()

    # 4. Información Corporativa
    col_inf1, col_inf2 = st.columns(2, gap="large")
    with col_inf1:
        st.subheader("🌐 QUIÉNES SOMOS")
        st.write(
            "Serenity Nexus Global es la primera plataforma **Phygital** (Física + Digital) "
            "del Valle del Cauca que integra la conservación ambiental con tecnología **Blockchain** "
            "e **Inteligencia Artificial**."
        )

    with col_inf2:
        st.subheader("🎯 NUESTRA MISIÓN")
        st.write(
            "Regenerar el tejido ecológico y social mediante un modelo de negocio sostenible "
            "que permita compensar la huella ambiental a través de la tecnología y la transparencia."
        )

    st.divider()

    # 5. Visión (Layout mejorado)
    col_inf3, col_inf4 = st.columns([1, 2])
    with col_inf3:
        st.subheader("🚀 NUESTRA VISIÓN")
    with col_inf4:
        st.write(
            "Ser el referente mundial del **Internet de la Naturaleza** para 2030, liderando la "
            "valorización de los servicios ecosistémicos mediante nuestra red de Faros inteligentes y el token **$SNG**."
        )

    # 6. Pie de página de inicio
    st.warning(
        "📍 **Ubicación del Proyecto:** Dagua y Felidia, Valle del Cauca — Hacienda Monte Guadua & Finca Villa Michelle."
    )


# =========================================================
# BLOQUE 2: RED DE FAROS (7 NODOS) - DISEÑO ORIGINAL RECUPERADO
# =========================================================
elif menu == "RED DE FAROS (7 NODOS)":
    st.markdown("<h1 style='text-align: center;'>📡 Red de Faros Serenity</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Seleccione un nodo para desplegar telemetría multimodal</p>", unsafe_allow_html=True)

    # Listado exacto de tus 7 Faros
    faros = ["Faro Halcon", "Faro Colibri", "Faro Tigrillo", "Faro Rana", "Faro Venado", "Faro Capibara", "Faro Rex"]

    # Cuadrícula de Selección (7 Contenedores)
    cols_faros = st.columns(7)
    
    for i, nombre in enumerate(faros):
        with cols_faros[i]:
            # Aplicar color azul si es Rex, verde para los demás
            clase_estilo = "faro-gemini" if nombre == "Faro Rex" else "faro-card"
            
            st.markdown(f'<div class="{clase_estilo}">', unsafe_allow_html=True)
            if st.button(f"📍 {nombre}", key=f"btn_{nombre}"):
                st.session_state.f_activo = nombre
            st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")

    # --- DESPLIEGUE DE INFRAESTRUCTURA AL SELECCIONAR ---
    if st.session_state.f_activo:
        f_sel = st.session_state.f_activo
        # Color de cabecera dinámico
        color_header = "#4285F4" if f_sel == "Faro Rex" else "#9BC63B"
        
        st.markdown(f"<h2 style='text-align: center; color: {color_header};'>🔍 Nodo Activo: {f_sel}</h2>", unsafe_allow_html=True)

        # 1. CUATRO CANALES DE AUDIO (4 Micrófonos)
        st.markdown("### 🎙️ Canales Bioacústicos")
        mics = st.columns(4)
        for m in range(4):
            with mics[m]:
                with st.container(border=True):
                    st.write(f"🔊 Micrófono 0{m+1}")
                    # Enlace de audio de prueba estable
                    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
                    st.caption("Frecuencia: 20Hz-22kHz")

        st.write("---")

        # 2. OCHO RECUADROS DE CÁMARA (Simulación de Cámaras)
        st.markdown("### 🛰️ Mosaico Visual (8 Cámaras)")
        
        # Generar las 8 cámaras en 2 filas de 4
        for fila in range(2):
            c_cols = st.columns(4)
            for col in range(4):
                cam_num = (fila * 4) + col + 1
                with c_cols[col]:
                    # Usamos la clase cam-grid que definiste en tus estilos para la estética REC
                    st.markdown(
                        f'''
                        <div class="cam-grid" style="height: 150px; flex-direction: column;">
                            <div style="font-size: 1.2rem;">REC 🔴</div>
                            <div>CAM 0{cam_num}</div>
                            <div style="font-size: 0.7rem; color: #555;">{f_sel} - EN VIVO</div>
                        </div>
                        ''', 
                        unsafe_allow_html=True
                    )
                    # Nota: Aquí puedes integrar iframes de RTVE o Pluto TV si tienes los links directos de streaming
                    st.caption(f"Sensor Óptico {cam_num}")

        st.write("")
        if st.button("❌ Cerrar Monitoreo Detallado", use_container_width=True):
            st.session_state.f_activo = None
            st.rerun()
    else:
        st.info("💡 Por favor, seleccione uno de los Faros superiores para desplegar los 4 canales de audio y las 8 cámaras de vigilancia.")


# =========================================================
# BLOQUE 3: DASHBOARD ESTADÍSTICO IA
# =========================================================
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("📊 Inteligencia de Datos Nexus")
    st.markdown("### Análisis Biométrico y Predictivo del Ecosistema")

    # Selector de Faro con valor por defecto
    faro_seleccionado = st.selectbox(
        "Seleccione el Faro para Auditoría IA:",
        ["Faro Rex", "Faro Halcón", "Faro Colibrí", "Faro Rana", "Faro Venado", "Faro Tigrillo", "Faro Capibara"]
    )

    # Simulación de cambio de datos según faro (Semilla basada en el nombre)
    np.random.seed(len(faro_seleccionado)) 
    
    st.write(f"Analizando telemetría en tiempo real de: **{faro_seleccionado}**")

    # Contenedor de Métricas Principales
    with st.container(border=True):
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Biodiversidad Index", f"{np.random.randint(75, 95)}%", "+2.1%")
        col_m2.metric("CO2 Capturado", f"{np.random.uniform(1.1, 1.5):.2f} Ton", "+15kg")
        col_m3.metric("Humedad Suelo", f"{np.random.randint(55, 70)}%", "-0.5%")
        col_m4.metric("Nivel Sonoro", "32 dB", "Natural")

    st.write("---")
    
    # Gráfico de actividad con datos simulados pero más coherentes
    st.subheader("📈 Flujo de Actividad (Últimas 24h)")
    
    # Crear datos que parezcan ciclos biológicos
    chart_data = pd.DataFrame(
        np.random.rand(24, 3) * [10, 5, 2],
        columns=["Audio (Biofonía)", "Visión (Fauna)", "Captura Carbono"]
    )
    st.area_chart(chart_data) # Area chart suele verse más "moderno" que line chart para bio-datos

    # Oráculo Nexus con mejor UI
    st.write("---")
    with st.container(border=True):
        st.markdown(f"#### 🤖 Oráculo Nexus: Consulta IA - {faro_seleccionado}")
        pregunta = st.text_input(
            "Consulta el estado predictivo:",
            placeholder=f"Ej: ¿Cómo estará la actividad en {faro_seleccionado} mañana?"
        )

        if pregunta:
            with st.status("Consultando Red de Faros y Google Gemini...", expanded=True) as status:
                st.write("Sincronizando con nodos locales...")
                time.sleep(1) # Simulación de latencia de red
                st.write("Analizando patrones bioacústicos...")
                time.sleep(1)
                status.update(label="Análisis completado", state="complete", expanded=False)

            # Respuesta con estilo de chatbot
            st.chat_message("assistant").write(
                f"""
                **Respuesta Nexus AI para {faro_seleccionado}:** Basado en el análisis de telemetría, se detecta una estabilidad del 98% en el ecosistema. 
                Los sensores de biomasa indican una aceleración en la captura de carbono debido a la humedad reciente.
                No hay anomalías térmicas ni sonidos de origen antrópico detectados.
                """
            )
            st.toast("Dato verificado en Blockchain SNG", icon="✅")

    # Pie de página técnico
    st.markdown("---")
    col_c1, col_c2 = st.columns([3, 1])
    col_c1.caption("Certificación: Los datos son validados por la Red Nexus y registrados en tiempo real.")
    col_c2.markdown("`HASH: 0x77...BN24`") # Simulación de hash de blockchain
    
# =========================================================
# BLOQUE 4: GESTIÓN LEY 2173 (EMPRESAS)
# =========================================================
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Nexus Legal & Compliance Hub")
    st.markdown("### Soluciones Tecnológicas a la Normativa Ambiental Colombiana")

    # Tarjetas Informativas con CSS Refinado
    st.markdown("""
        <style>
        .ley-card {
            background: #1e2630; 
            padding: 20px; 
            border-radius: 12px; 
            min-height: 220px;
            border-bottom: 4px solid transparent;
            transition: 0.3s;
        }
        .ley-card:hover { border-bottom: 4px solid #9BC63B; background: #252e3a; }
        </style>
    """, unsafe_allow_html=True)

    c_l1, c_l2, c_l3 = st.columns(3)
    with c_l1:
        st.markdown(
            '<div class="ley-card" style="border-left:5px solid #9BC63B;"><h4 style="color:#9BC63B;">LEY 2173</h4><p style="font-size:0.85rem; color:#ccc;"><b>Áreas de Vida:</b> Obligación de 2 árboles por empleado anualmente. Serenity provee el terreno y registro GPS oficial.</p></div>',
            unsafe_allow_html=True,
        )
    with c_l2:
        st.markdown(
            '<div class="ley-card" style="border-left:5px solid #3498db;"><h4 style="color:#3498db;">LEY 2169</h4><p style="font-size:0.85rem; color:#ccc;"><b>Acción Climática:</b> Ruta a la Carbono Neutralidad. Nuestra IA certifica captura real para reportes oficiales (RENARE).</p></div>',
            unsafe_allow_html=True,
        )
    with c_l3:
        st.markdown(
            '<div class="ley-card" style="border-left:5px solid #e74c3c;"><h4 style="color:#e74c3c;">LEY 2111</h4><p style="font-size:0.85rem; color:#ccc;"><b>Justicia Ambiental:</b> Delitos Ambientales. Los Faros actúan como evidencia digital inmutable ante la deforestación.</p></div>',
            unsafe_allow_html=True,
        )

    st.write("---")

    # SECCIÓN 1: VADEMÉCUM
    with st.container(border=True):
        st.subheader("📘 Vademécum de Soluciones Corporativas")
        st.write("Documento técnico sobre el cumplimiento normativo mediante Serenity Nexus.")

        empresa_v = st.text_input("Razón Social para el Reporte", placeholder="Ej: Transportes del Valle SAS", key="txt_vademecum")

        if st.button("GENERAR VADEMÉCUM TÉCNICO PDF", use_container_width=True, type="primary"):
            if empresa_v:
                with st.spinner("Generando documento estructurado..."):
                    # Asegúrate de tener 'hashlib' importado
                    hash_v = hashlib.sha256(f"{empresa_v}VAD".encode()).hexdigest()[:12].upper()
                    
                    # Llamada a tu función (asegúrate que esté definida globalmente)
                    pdf_v = generar_pdf_corporativo(
                        empresa=empresa_v,
                        impacto=0,
                        hash_id=hash_v,
                        es_vademecum=True
                    )
                    st.session_state.vademecum_pdf = pdf_v.getvalue()
                    st.session_state.vademecum_empresa = empresa_v
                    st.success(f"✅ Vademécum para {empresa_v} listo.")
            else:
                st.warning("⚠️ Ingrese el nombre de la empresa.")

        if "vademecum_pdf" in st.session_state:
            st.download_button(
                label="📥 DESCARGAR VADEMÉCUM",
                data=st.session_state.vademecum_pdf,
                file_name=f"Vademecum_Nexus_{st.session_state.vademecum_empresa}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    st.write("")

    # SECCIÓN 2: CERTIFICADO CON LOGO
    st.subheader("🏢 Emisión de Certificado Oficial")
    
    with st.expander("Configurar Datos de Certificación", expanded=True):
        col_act1, col_act2 = st.columns([1, 1])

        with col_act1:
            n_corp = st.text_input("Nombre de la Compañía", key="txt_corp")
            nit_corp = st.text_input("NIT", placeholder="900.123.456-1", key="nit_corp")
            n_per = st.number_input("Número de Empleados", min_value=1, value=100)
            archivo_logo = st.file_uploader("Logo Corporativo (PNG/JPG)", type=["png", "jpg", "jpeg"])

        with col_act2:
            arboles_req = n_per * 2
            st.metric("Árboles Requeridos", arboles_req, delta="Ley 2173", delta_color="normal")
            st.info(f"El certificado avalará la siembra de **{arboles_req}** individuos arbóreos en la Red de Faros Serenity.")

            if st.button("EMITIR CERTIFICADO CON LOGO", use_container_width=True):
                if n_corp and archivo_logo:
                    with st.spinner("Sincronizando con la Red de Faros..."):
                        h_c = hashlib.sha256(f"{n_corp}{nit_corp}".encode()).hexdigest()[:12].upper()
                        
                        # Guardar logo en bytes
                        logo_bytes = archivo_logo.getvalue()

                        pdf_c = generar_pdf_corporativo(
                            empresa=n_corp,
                            impacto=arboles_req,
                            hash_id=h_c,
                            nit=nit_corp,
                            logo_bytes=logo_bytes,
                            es_vademecum=False,
                            faro_nombre="Faro Rex"
                        )

                        st.session_state.cert_corp_pdf = pdf_c.getvalue()
                        st.session_state.cert_corp_nombre = n_corp
                        st.balloons() # Efecto visual de éxito
                else:
                    st.error("❌ Falta Razón Social o Logo.")

    if "cert_corp_pdf" in st.session_state:
        st.download_button(
            label=f"📥 DESCARGAR CERTIFICADO: {st.session_state.cert_corp_nombre}",
            data=st.session_state.cert_corp_pdf,
            file_name=f"Certificado_Ley2173_{st.session_state.cert_corp_nombre}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# =========================================================
# BLOQUE 5: SUSCRIPCIONES
# =========================================================
elif menu == "SUSCRIPCIONES":
    st.title("Membresías de Impacto Serenity")
    st.markdown("### Transforma tu aporte en regeneración real")

    # CSS para igualar alturas y efectos de hover
    st.markdown("""
        <style>
        .plan-card {
            background:#1e2630; 
            padding:25px; 
            border-radius:15px; 
            text-align:center; 
            min-height: 450px;
            transition: 0.3s ease;
        }
        .plan-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        </style>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown(
            """
            <div class="plan-card" style="border:2px solid #9BC63B;">
                <h3 style="color:#9BC63B;">PLAN SEMILLA</h3>
                <h2 style="color:white;">$25 USD <small style="font-size:12px;">/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;">🌱 <b>5 Árboles:</b> Siembra y mantenimiento.</p>
                <p style="text-align:left; font-size:0.9rem;">📡 <b>1 Faro:</b> Datos biométricos básicos.</p>
                <p style="text-align:left; font-size:0.9rem;">💎 <b>50 Tokens:</b> $SNG de respaldo.</p>
                <p style="text-align:left; font-size:0.9rem;">📜 <b>Certificado:</b> Digital con Hash.</p>
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
            <div class="plan-card" style="border:3px solid #9BC63B; background:#252e3a;">
                <h3 style="color:#9BC63B;">PLAN GUARDIÁN</h3>
                <h2 style="color:white;">$80 USD <small style="font-size:12px;">/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;">🌳 <b>15 Árboles:</b> Restauración activa.</p>
                <p style="text-align:left; font-size:0.9rem;">🎥 <b>Cámaras 4K:</b> Streaming del bosque.</p>
                <p style="text-align:left; font-size:0.9rem;">💎 <b>200 Tokens:</b> Mayor respaldo $SNG.</p>
                <p style="text-align:left; font-size:0.9rem;">🤖 <b>Reporte IA:</b> Inventario de carbono.</p>
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
            <div class="plan-card" style="border:2px solid #D4AF37;">
                <h3 style="color:#D4AF37;">PLAN HALCÓN</h3>
                <h2 style="color:white;">$200 USD <small style="font-size:12px;">/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;">🏞️ <b>1 Plaza Protegida:</b> Soberanía total.</p>
                <p style="text-align:left; font-size:0.9rem;">🛡️ <b>Cámaras:</b> Vigilancia perimetral.</p>
                <p style="text-align:left; font-size:0.9rem;">💎 <b>600 Tokens:</b> Impacto Web3 máximo.</p>
                <p style="text-align:left; font-size:0.9rem;">⛺ <b>Visita VIP:</b> Monte Guadua (2D/1N).</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("ELEGIR HALCÓN", use_container_width=True, key="p_halcon"):
            st.session_state.p_sel = "HALCÓN"
            st.session_state.m_plan = 200

    # Lógica de Checkout
    if st.session_state.get("p_sel"):
        st.write("---")
        col_t1, col_t2 = st.columns([3, 1])
        col_t1.subheader(f"💳 Finalizar Suscripción: Plan {st.session_state.p_sel}")
        if col_t2.button("Cambiar Plan"):
            st.session_state.p_sel = None
            st.rerun()

        col_pay1, col_pay2 = st.columns(2)
        
        with col_pay1:
            with st.container(border=True):
                st.markdown("#### Tarjeta de Crédito/Débito")
                st.text_input("Titular de la cuenta", placeholder="Nombre como aparece en la tarjeta")
                st.text_input("Número de Tarjeta", placeholder="xxxx xxxx xxxx xxxx")
                c_exp, c_cvc = st.columns(2)
                with c_exp:
                    st.text_input("Vencimiento (MM/AA)")
                with c_cvc:
                    st.text_input("CVC", type="password") # Ocultar código de seguridad
                
                if st.button("✅ ACTIVAR SUSCRIPCIÓN", use_container_width=True, type="primary"):
                    with st.spinner("Procesando pago seguro..."):
                        time.sleep(2)
                        st.balloons()
                        st.success(f"¡Bienvenido al Plan {st.session_state.p_sel}! Tu impacto ha sido registrado en la red.")

        with col_pay2:
            st.markdown("#### Métodos Locales y Cripto")
            st.markdown(
                """
                <div style="background: #ffffff; padding: 20px; border-radius: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px; align-items: center; border: 1px solid #ddd; filter: grayscale(20%);">
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/b/bf/Nequi_logo.png" width="80"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Bancolombia_logo.svg/2560px-Bancolombia_logo.svg.png" width="80"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Visa_Inc._logo.svg/2560px-Visa_Inc._logo.svg.png" width="60"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/1280px-Mastercard-logo.svg.png" width="60"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.info("💡 **Dato Nexus:** Al suscribirte, tus primeros tokens $SNG serán transferidos a tu cuenta en las próximas 24 horas.")
            st.caption("🔒 Transacciones seguras mediante Nexus Gateway (Dagua-Colombia)")

# =========================================================
# BLOQUE 6: BILLETERA CRYPTO (WEB3)
# =========================================================
elif menu == "BILLETERA CRYPTO (WEB3)":
    # --- FUNCIÓN INTERNA PARA LA GUÍA ---
    def obtener_guia_web3():
        return """
        🌿 SERENITY NEXUS GLOBAL - GUÍA DE CONFIGURACIÓN WEB3
        =====================================================
        
        1. INSTALACIÓN: Use MetaMask o Nexus Wallet App.
        2. SEGURIDAD: Guarde su frase semilla (12/24 palabras) en papel.
           NUNCA la comparta con nadie, ni siquiera con soporte de Serenity.
        3. RED: Asegúrese de estar conectado a la red Polygon Mainnet.
        4. IMPORTAR TOKEN:
           - Contrato: 0x71C2B4... (Contrato Oficial SNG)
           - Símbolo: $SNG
           - Decimales: 18
        
        SNG es un token respaldado por activos biológicos reales (KBA).
        """

    st.title("Nexus Finance Control")
    st.markdown("### El Futuro de la Conservación Tokenizada")

    # 1. Visualizador de Token (Video en Base64)
    if os.path.exists("video_sng.mp4"):
        try:
            with open("video_sng.mp4", "rb") as f:
                video_bytes = f.read()
                video_base64 = base64.b64encode(video_bytes).decode()
            
            video_html = f"""
                <div style="display: flex; justify-content: center; margin-bottom: 25px;">
                    <video width="50%" autoplay loop muted playsinline 
                        style="border-radius: 20px; border: 2px solid #9BC63B; 
                        box-shadow: 0 0 30px rgba(155, 198, 59, 0.4);">
                        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                    </video>
                </div>
            """
            st.markdown(video_html, unsafe_allow_html=True)
        except Exception:
            st.info("🪙 **SNG Token Activo** (Visualizador en carga...)")
    else:
        st.info("🪙 **SNG Token Viewer:** (Para ver el token 3D, asegúrate de que 'video_sng.mp4' esté en la carpeta raíz)")

    st.write("---")

    col_buy, col_vault = st.columns(2)

    # 2. Simulador de Compra / Swap
    with col_buy:
        st.markdown("<h4 style='color:#9BC63B;'>🔄 Intercambio Nexus (Swap)</h4>", unsafe_allow_html=True)
        with st.container(border=True):
            moneda_pago = st.selectbox("Pagar con:", ["USD (Tarjeta/PSE)", "USDT (Crypto)", "Ethereum (ETH)"])
            cantidad_usd = st.number_input("Monto a invertir (USD):", min_value=10, value=100, step=50)
            
            tasa = 0.50 # Precio simulado del token
            tokens_estimados = cantidad_usd / tasa
            
            st.metric("Recibirás aproximadamente:", f"{tokens_estimados:,.2f} $SNG")
            
            if st.button("COMPRAR TOKENS $SNG", use_container_width=True, type="primary"):
                with st.status("Conectando con Nexus Gateway...") as status:
                    time.sleep(1.2)
                    st.write("Verificando liquidez en el pool...")
                    time.sleep(1)
                    status.update(label="¡Orden Generada con Éxito!", state="complete")
                st.success(f"Se ha enviado la solicitud de compra por {tokens_estimados} $SNG.")

    # 3. Bóveda y Guía de Configuración
    with col_vault:
        st.markdown("<h4 style='color:#9BC63B;'>🔐 Seguridad Nexus Vault</h4>", unsafe_allow_html=True)
        st.write("Nexus Vault es tu llave privada al Internet de la Naturaleza.")
        
        st.markdown(
            """
            <div style='background: #1e2630; padding: 15px; border-radius: 12px; border-left: 5px solid #9BC63B;'>
                <p>• <b>Paso 1:</b> Descarga Nexus App o usa Metamask.</p>
                <p>• <b>Paso 2:</b> Genera tu frase semilla de 24 palabras.</p>
                <p>• <b>Paso 3:</b> Vincula tu ID de Donante Serenity.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        
        # Botón de Descarga Funcional
        st.download_button(
            label="📥 DESCARGAR GUÍA DE CONFIGURACIÓN",
            data=obtener_guia_web3(),
            file_name="Guia_Nexus_Web3.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.write("---")
    
    # 4. Conexión de Wallet
    st.markdown("<h4 style='text-align:center;'>Centro de Conexión Web3</h4>", unsafe_allow_html=True)
    cw1, cw2, cw3 = st.columns([1, 2, 1])

    with cw2:
        if st.button("VINCULAR BILLETERA AL SISTEMA NEXUS", use_container_width=True):
            st.session_state.wallet_connected = True
            st.balloons()

    # 5. Estado de la Cuenta Tokenizada
    if st.session_state.get("wallet_connected", False):
        st.success("✅ Billetera 0x71C...9A23 Conectada con éxito.")

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

        # Tabla de activos mejorada
        df_wallet = pd.DataFrame({
            "Activo Biológico": ["Carbono Azul", "Biodiversidad", "Agua Protegida", "Suelo Regenerado"],
            "Nodo Validador": ["Faro Rex", "Faro Tigrillo", "Faro Colibrí", "Faro Halcón"],
            "Tokens $SNG": [5000, 8500, 3200, 8300],
            "Certificación": ["✅ Verificado", "✅ Verificado", "🔄 Sincronizando", "✅ Verificado"]
        })

        st.dataframe(
            df_wallet, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Tokens $SNG": st.column_config.NumberColumn(format="%d $SNG")
            }
        )
        st.caption("📡 Los datos biométricos son actualizados cada 60 segundos por la Red de Faros Serenity.")


# =========================================================
# BLOQUE 7: DONACIONES Y CERTIFICADO
# =========================================================
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("Generador de Diploma y Certificado Nexus")
    st.markdown("### Registro de Aportes a la Regeneración Biométrica")

    # Inicialización de contador de donaciones si no existe
    if "donaciones_recibidas" not in st.session_state:
        st.session_state.donaciones_recibidas = 0

    colA, colB = st.columns([1, 1])

    with colA:
        with st.container(border=True):
            st.markdown("#### ✨ Datos del Donante")
            nombre_d = st.text_input("Nombre Completo o Razón Social", placeholder="Ej: Juan Pérez / Empresa Verde")
            monto_d = st.number_input("Monto del Aporte (USD)", min_value=1, value=50, step=10)
            
            st.info("💡 Cada USD $10 representa la protección activa de 100m² de bosque nativo.")

            if st.button("REGISTRAR APORTE Y GENERAR HASH", use_container_width=True, type="primary"):
                if nombre_d:
                    with st.spinner("Firmando certificado en la Red Nexus..."):
                        # Creación del Hash único (Huella digital del certificado)
                        datos_hash = f"{nombre_d}{monto_d}{datetime.now()}"
                        hash_certificado = hashlib.sha256(datos_hash.encode()).hexdigest()[:16].upper()

                        # Guardar en Session State
                        st.session_state.current_hash = hash_certificado
                        st.session_state.nombre_prev = nombre_d
                        st.session_state.monto_prev = monto_d
                        
                        # Generación del PDF (Usa tu función existente)
                        buffer = generar_pdf_certificado(nombre_d, monto_d, hash_certificado)
                        st.session_state.pdf_buffer = buffer.getvalue()

                        st.session_state.donaciones_recibidas += 1
                        st.balloons()
                        st.success(f"¡Certificado #{st.session_state.donaciones_recibidas} generado!")
                else:
                    st.error("⚠️ Por favor, ingrese el nombre del donante para continuar.")

    with colB:
        if "pdf_buffer" in st.session_state:
            # Vista previa estilizada con aspecto de "Papel de Seguridad"
            st.markdown(
                f"""
                <div style="background:#f9f9f9; color:#1a1a1a; padding:40px; text-align:center; 
                            border:10px double #2E7D32; border-radius:5px; box-shadow: 10px 10px 20px rgba(0,0,0,0.2);">
                    <h1 style="color:#2E7D32; font-family:serif; margin-bottom:0;">CERTIFICADO</h1>
                    <p style="letter-spacing: 3px; font-size: 0.8rem; color:#666;">SERENITY NEXUS GLOBAL</p>
                    <hr style="border:1px solid #2E7D32; width:80%;">
                    <p style="font-size:1.1rem; margin-top:20px;">Este documento avala que:</p>
                    <h2 style="color:#111; margin:10px 0;">{st.session_state.nombre_prev.upper()}</h2>
                    <p>Ha contribuido con la suma de <b>${st.session_state.monto_prev} USD</b></p>
                    <p style="font-size:0.9rem; font-style:italic;">Destinados a la restauración de la Red de Faros</p>
                    <div style="background:#e8f5e9; padding:15px; border-radius:5px; margin-top:30px; border: 1px dashed #2E7D32;">
                        <code style="font-size:0.9rem; color: #2E7D32; font-weight:bold;">ID VERIFICACIÓN: {st.session_state.current_hash}</code>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")
            st.download_button(
                label="📥 DESCARGAR DIPLOMA OFICIAL (PDF)",
                data=st.session_state.pdf_buffer,
                file_name=f"Certificado_Nexus_{st.session_state.current_hash}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            # Estado vacío para cuando no hay certificado generado
            st.markdown(
                """
                <div style="height:400px; display:flex; align-items:center; justify-content:center; 
                            border:2px dashed #444; border-radius:15px; color:#666;">
                    La vista previa del certificado aparecerá aquí al registrar su aporte.
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# BLOQUE 8: DIAGNÓSTICO HUELLA DE CARBONO (PRO)
# =========================================================
elif menu == "DIAGNOSTICO HUELLA DE CARBONO":
    st.title("🌍 Inteligencia de Carbono Nexus")
    st.markdown("### Diagnóstico Automatizado con Factores de Emisión Colombia")

    # --- SIMULACIÓN DE BASE DE DATOS EMPRESARIAL COLOMBIANA ---
    DB_EMPRESAS = {
        "900123456": {"nombre": "TRANSPORTES DEL VALLE SAS", "sector": "Transporte de Carga", "consumo_avg": 4500, "flota": 12},
        "800987654": {"nombre": "CONSTRUCTORA ANDINA", "sector": "Construcción / Infraestructura", "consumo_avg": 8200, "flota": 25},
        "901555444": {"nombre": "FLORES DE LA SABANA", "sector": "Agroindustria", "consumo_avg": 3100, "flota": 8},
    }

    with st.container(border=True):
        col_nit1, col_nit2 = st.columns([1, 1])
        with col_nit1:
            nit_busqueda = st.text_input("🔍 BUSCAR NIT DE LA EMPRESA", placeholder="Ej: 900123456")
        
        # Autocompletado inteligente
        if nit_busqueda in DB_EMPRESAS:
            nombre_sugerido = DB_EMPRESAS[nit_busqueda]["nombre"]
            sector_sugerido = DB_EMPRESAS[nit_busqueda]["sector"]
            st.success(f"Empresa encontrada: {nombre_sugerido}")
        else:
            nombre_sugerido = ""
            sector_sugerido = "Sector General"

        with col_nit2:
            nombre_empresa = st.text_input("RAZÓN SOCIAL", value=nombre_sugerido)

    if nit_busqueda and nombre_empresa:
        st.write("---")
        
        # Parámetros técnicos con datos sugeridos por la DB
        with st.expander("📊 Parámetros de Operación (Valores Mensuales)", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                # Si la empresa está en la DB, precargamos sus promedios
                val_kwh = DB_EMPRESAS[nit_busqueda]["consumo_avg"] if nit_busqueda in DB_EMPRESAS else 1000
                kwh = st.number_input("Consumo Eléctrico (kWh)", min_value=0, value=val_kwh)
                
                val_flota = DB_EMPRESAS[nit_busqueda]["flota"] if nit_busqueda in DB_EMPRESAS else 1
                vehiculos = st.number_input("Vehículos en Operación", min_value=0, value=val_flota)
            
            with c2:
                gasolina = st.number_input("Consumo Galones Gasolina/Diesel", min_value=0, value=100)
                residuos = st.number_input("Residuos Sólidos (Toneladas)", min_value=0.0, value=1.0)

        # --- LÓGICA DE CÁLCULO REALISTA (Factores de Emisión) ---
        # FE Energía Colombia (UPME): ~0.126 kg CO2/kWh
        # FE Diesel/Gasolina: ~10.15 kg CO2/galón
        # FE Residuos: ~450 kg CO2/ton (relleno sanitario promedio)
        
        h_energia = kwh * 0.126
        h_combustible = gasolina * 10.15
        h_residuos = residuos * 450
        
        huella_total_kg = h_energia + h_combustible + h_residuos
        huella_total_ton = huella_total_kg / 1000
        
        # Compensación: 1 árbol nativo en Colombia captura aprox 25kg CO2/año
        # Para neutralidad mensual:
        arboles_mes = int(huella_total_kg / 25)

        # Dashboard de Resultados
        st.subheader(f"📈 Reporte de Sustentabilidad: {sector_sugerido}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("HUELLA MENSUAL", f"{huella_total_ton:.2f} Ton CO2e")
        m2.metric("ÁRBOLES NEXUS / MES", f"{arboles_mes} u")
        
        # KPI de Eficiencia (Simulado)
        eficiencia = "ÓPTIMA" if huella_total_ton < 5 else "CRÍTICA"
        m3.metric("ESTADO DE EMISIONES", eficiencia, delta="-2% vs mes anterior")

        # --- VISUALIZACIÓN GRÁFICA ---
        st.write("### Desglose de Fuentes de Emisión")
        chart_data = pd.DataFrame({
            'Fuente': ['Energía', 'Combustible', 'Residuos'],
            'kg CO2e': [h_energia, h_combustible, h_residuos]
        })
        st.bar_chart(chart_data.set_index('Fuente'))

        # --- GENERACIÓN DEL DIAGNÓSTICO ---
        st.divider()
        hash_legal = hashlib.sha256(f"{nit_busqueda}{huella_total_kg}".encode()).hexdigest()[:12].upper()
        
        if st.button(f"📄 GENERAR DIAGNÓSTICO TÉCNICO PARA {nombre_empresa}", use_container_width=True):
            # Aquí llamas a tu función de PDF con los datos calculados
            pdf_data = generar_pdf_diagnostico(
                empresa=nombre_empresa,
                nit=nit_busqueda,
                impacto=arboles_mes,
                hash_id=hash_legal,
                estudio_data={
                    "Sector": sector_sugerido,
                    "Energía (kWh)": f"{kwh:,}",
                    "Combustible (Gal)": f"{gasolina:,}",
                    "Residuos (Ton)": residuos,
                    "Huella Mensual": f"{huella_total_ton:.2f} Ton"
                },
                total_ton=huella_total_ton,
                faro_nombre="Faro Rex"
            )
            
            st.download_button(
                label="📥 DESCARGAR DOCUMENTO DE CUMPLIMIENTO",
                data=pdf_data.getvalue(),
                file_name=f"Nexus_Report_{nit_busqueda}.pdf",
                mime="application/pdf",
                use_container_width=True
            )


# =========================================================
# BLOQUE 9: UBICACIÓN & MAPAS (AVANZADO)
# =========================================================
elif menu == "UBICACIÓN & MAPAS":
    from folium.plugins import HeatMap # Asegúrate de importar esto arriba
    
    st.title("🗺️ Centro de Comando Geospacial Nexus")
    st.markdown("### Análisis Satelital: Ubicación, Deforestación y Recuperación")
    
    # 1. Definición de Datos
    lat_v, lon_v = 3.518, -76.620
    
    # Datos de los Faros
    faros_nexus = [
        {"name": "Faro Halcón", "lat": 3.518, "lon": -76.620, "color": "green"},
        {"name": "Faro Colibrí", "lat": 3.519, "lon": -76.622, "color": "green"},
        {"name": "Faro Rex", "lat": 3.485, "lon": -76.605, "color": "blue"}
    ]

    # Simulación de Datos para Mapas de Calor (Lat, Lon, Intensidad)
    # Datos de Deforestación (Zonas calientes de pérdida)
    data_deforestacion = [
        [3.515, -76.610, 0.8], [3.514, -76.612, 0.9], [3.516, -76.608, 0.7],
        [3.480, -76.600, 0.9], [3.482, -76.602, 0.6]
    ]
    
    # Datos de Reforestación (Zonas de siembra activa Serenity)
    data_reforestacion = [
        [3.518, -76.620, 1.0], [3.519, -76.622, 0.8], [3.517, -76.621, 0.9],
        [3.520, -76.619, 0.7], [3.516, -76.623, 1.0]
    ]

    # 2. Configuración del Mapa Base
    google_hibrido = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
    
    m = folium.Map(
        location=[lat_v, lon_v],
        zoom_start=14,
        tiles=google_hibrido,
        attr="Google Satellite Hybrid"
    )

    # 3. Capa: Marcadores de Faros
    capa_faros = folium.FeatureGroup(name="📍 Ubicación de Faros").add_to(m)
    for faro in faros_nexus:
        folium.Marker(
            location=[faro['lat'], faro['lon']],
            popup=faro['name'],
            icon=folium.Icon(color=faro['color'], icon='broadcast-tower', prefix='fa')
        ).add_to(capa_faros)

    # 4. Capa: Mapa de Calor de Deforestación (Rojo)
    capa_defo = folium.FeatureGroup(name="🔥 Mapa de Calor: Deforestación", show=False).add_to(m)
    HeatMap(data_deforestacion, radius=25, blur=15, gradient={0.4: 'yellow', 0.65: 'orange', 1: 'red'}).add_to(capa_defo)

    # 5. Capa: Mapa de Calor de Reforestación (Verde/Azul)
    capa_refo = folium.FeatureGroup(name="🌿 Mapa de Calor: Reforestación", show=False).add_to(m)
    HeatMap(data_reforestacion, radius=25, blur=15, gradient={0.4: 'lime', 1: 'cyan'}).add_to(capa_refo)

    # 6. Control de Capas (Permite al usuario activar/desactivar en el mapa)
    folium.LayerControl(collapsed=False).add_to(m)

    # Renderizado en Streamlit
    st_folium(m, use_container_width=True, height=550)

    # 7. Métricas de Soporte
    st.write("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Área Protegida", "450 Ha", "+12 Ha")
    c2.metric("Alertas Deforestación", "3", "-2", delta_color="inverse")
    c3.metric("Tasa Supervivencia", "94%", "Especies Nativas")


# =========================================================
# BLOQUE 10: NEXUS GUARDIAN COMMAND (IA PREDICTIVA)
# =========================================================
elif menu == "NEXUS GUARDIAN COMMAND":
    st.title("🛡️ Nexus Guardian Command")
    st.markdown("### Prevención Proactiva y Análisis de Supervivencia Biótica")

    # 1. Sistema de Alerta Temprana (IA Predictiva)
    with st.container(border=True):
        col_risk1, col_risk2 = st.columns([2, 1])
        with col_risk1:
            st.subheader("⚠️ Análisis de Riesgo de Incendio y Tala")
            # Simulación de datos de sensores de humedad y calor en los Faros
            datos_riesgo = pd.DataFrame({
                'Faro': ['Rex', 'Halcón', 'Tigrillo', 'Colibrí'],
                'Humedad Suelo (%)': [45, 32, 58, 20],
                'Riesgo de Incendio': ['Bajo', 'Medio', 'Bajo', 'CRÍTICO']
            })
            st.table(datos_riesgo)
        
        with col_risk2:
            st.metric("Índice de Salud del Bosque", "92%", "+1.5%")
            st.warning("Alerta en Faro Colibrí: Estrés hídrico detectado.")

    st.write("---")

    # 2. Visión Artificial: Identificación de Especies (Cámaras de los Faros)
    st.subheader("📸 Avistamientos Recientes (IA Vision)")
    cv1, cv2, cv3 = st.columns(3)
    
    with cv1:
        st.image("https://images.unsplash.com/photo-1591824438708-218337735a11?auto=format&fit=crop&w=400", 
                 caption="Identificado: Tigrillo (Leopardus pardalis) - Confianza 98%")
    with cv2:
        st.image("https://images.unsplash.com/photo-1550159930-4014434285e0?auto=format&fit=crop&w=400", 
                 caption="Identificado: Tucán Pichifrí - Confianza 94%")
    with cv3:
        st.info("📡 Procesando streaming de Faro Rex... Esperando movimiento.")

    st.write("---")

    # 3. Nexus Community: El Muro de los Guardianes
    st.subheader("🤝 El Muro de los Guardianes")
    st.write("Interactúa con otros protectores y vota por la siguiente zona de intervención.")
    
    with st.chat_message("user"):
        st.write("¿Cuál será el próximo árbol a sembrar en Villa Michelle?")
    
    opciones = ["Guayacán Amarillo", "Roble Andino", "Cedro Rosado"]
    voto = st.radio("Votación de Gobernanza $SNG:", opciones)
    
    if st.button("ENVIAR VOTO A BLOCKCHAIN"):
        st.success(f"Voto registrado para {voto}. Tu poder de voto: 250 $SNG.")

    st.write("---")
    
    # 4. Reporte Final de Operación
    st.markdown("<h4 style='text-align:center;'>Estado de la Red Global</h4>", unsafe_allow_html=True)
    st.progress(98)
    st.caption("Uptime de la Red de Faros: 98.4% | Conectividad Starlink: Estable")


































































































































































































































































































































































































































































































































































































































































































































































































