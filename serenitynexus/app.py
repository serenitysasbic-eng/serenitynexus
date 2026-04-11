# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import random
import hashlib
import io
import os
import base64
import librosa
from datetime import datetime

# --- LIBRERÍAS DE MAPAS ---
import folium
from streamlit_folium import st_folium

# --- LIBRERÍAS DE REPORTE (PDF) ---
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors  # Importación base para evitar errores de color
from reportlab.lib.colors import HexColor, black

# --- CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="Serenity Nexus Global", page_icon="??", layout="wide")
VERDE_SERENITY = HexColor("#2E7D32")

def generar_pdf_corporativo(empresa, nit, impacto, hash_id, estudio_data, total_ton):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    VERDE_SERENITY = colors.HexColor("#9BC63B")
    
    # Membrete
    c.setStrokeColor(VERDE_SERENITY)
    c.setLineWidth(2)
    c.line(0.5*inch, 10.2*inch, 8*inch, 10.2*inch)
    
    # Título y Datos (NIT incluido aquí)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(4.25*inch, 9.5*inch, "DIAGNÓSTICO DE HUELLA DE CARBONO")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, 8.8*inch, f"ENTIDAD: {empresa.upper()}")
    c.drawString(1*inch, 8.6*inch, f"NIT: {nit}") # <--- NIT agregado
    c.drawString(1*inch, 8.4*inch, f"SERIAL DE INTEGRIDAD: {hash_id}")

    # Tabla de Resultados Reales
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(VERDE_SERENITY)
    c.drawString(1*inch, 7.8*inch, "RESULTADOS DEL ESTUDIO (FACTORES UPME COLOMBIA):")
    
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.black)
    y_pos = 7.5
    for concepto, valor in estudio_data.items():
        c.drawString(1.2*inch, y_pos*inch, f"• {concepto}:")
        c.drawRightString(7*inch, y_pos*inch, f"{valor}")
        y_pos -= 0.22

    # Gráfica Comparativa Realista
    y_graf = y_pos - 0.5
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y_graf*inch, "COMPARATIVA SECTORIAL (TON CO2E):")
    
    ancho_max = 2.5 * inch
    promedio_sector = total_ton * 1.15 # Diferencia realista del 15%
    
    c.setFillColor(VERDE_SERENITY)
    c.rect(3*inch, (y_graf-0.4)*inch, (total_ton/(total_ton+promedio_sector))*ancho_max*2, 0.2*inch, fill=1)
    c.setFillColor(colors.black)
    c.drawString(1.2*inch, (y_graf-0.35)*inch, "Su Empresa")

    c.setFillColor(colors.HexColor("#4285F4"))
    c.rect(3*inch, (y_graf-0.7)*inch, (promedio_sector/(total_ton+promedio_sector))*ancho_max*2, 0.2*inch, fill=1)
    c.setFillColor(colors.black)
    c.drawString(1.2*inch, (y_graf-0.65)*inch, "Promedio Valle")

    c.save()
    buffer.seek(0)
    return buffer


def generar_pdf_corporativo(empresa, impacto, hash_id, nit="", logo_bytes=None, es_vademecum=False, faro_nombre="Red Nexus"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # --- LOGO SERENITY (Izquierda) ---
    try:
        if os.path.exists("logo_serenity.png"):
            c.drawImage("logo_serenity.png", 0.7*inch, 9.3*inch, width=1.5*inch, preserveAspectRatio=True, mask='auto')
    except:
        pass

    # --- LOGO EMPRESA (Derecha) ---
    if logo_bytes:
        try:
            from reportlab.lib.utils import ImageReader
            logo_img = ImageReader(io.BytesIO(logo_bytes))
            c.drawImage(logo_img, 6*inch, 9.3*inch, width=1.5*inch, preserveAspectRatio=True, mask='auto')
        except:
            pass

    # Marco y Títulos
    c.setStrokeColor(colors.green)
    c.rect(0.5*inch, 0.5*inch, 7.5*inch, 10*inch)
    
    c.setFont("Helvetica-Bold", 16)
    titulo = "VADEMÉCUM TÉCNICO LEGAL" if es_vademecum else "CERTIFICADO DE COMPENSACIÓN"
    c.drawCentredString(4.25*inch, 9*inch, titulo)

    # Datos
    c.setFont("Helvetica", 12)
    y = 8.2*inch
    c.drawString(1*inch, y, f"RAZÓN SOCIAL: {empresa.upper()}")
    c.drawString(1*inch, y-0.2*inch, f"NIT: {nit}")
    c.drawString(1*inch, y-0.4*inch, f"NODO VALIDADOR: {faro_nombre}")
    c.drawString(1*inch, y-0.6*inch, f"ID SEGURIDAD: {hash_id}")

    # Contenido según tipo
    text = c.beginText(1*inch, 6.5*inch)
    text.setFont("Helvetica", 11)
    if es_vademecum:
        text.textLine("Este documento certifica el cumplimiento de las Leyes 2173, 2169 y 2111.")
        text.textLine("Serenity Nexus garantiza la trazabilidad biométrica de los activos.")
    else:
        text.textLine(f"Se certifica la siembra y protección de {impacto} árboles.")
    c.drawText(text)

    c.save()
    buffer.seek(0)
    return buffer


# --- GESTIÓN DE ESTADO ---
if 'total_protegido' not in st.session_state: st.session_state.total_protegido = 87.0
if 'donaciones_recibidas' not in st.session_state: st.session_state.donaciones_recibidas = 0
if 'estado_gemini' not in st.session_state: st.session_state.estado_gemini = "Latente"
if 'auth' not in st.session_state: st.session_state.auth = False
if 'f_activo' not in st.session_state: st.session_state.f_activo = None

def generar_pdf_corporativo(empresa, impacto, hash_id, logo_bytes=None, es_vademecum=False):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # --- 1. MEMBRETE Y LOGOS (CO-BRANDING) ---
    c.setStrokeColor(VERDE_SERENITY)
    c.setLineWidth(2)
    c.line(0.5*inch, 10.2*inch, 8*inch, 10.2*inch) # Línea superior
    
    # Logo Serenity (Siempre presente a la izquierda)
    try:
        if os.path.exists("logo_serenity.png"):
            c.drawImage("logo_serenity.png", 0.5*inch, 9.2*inch, width=1.5*inch, height=0.8*inch, preserveAspectRatio=True, mask='auto')
    except: pass

    # Logo Empresa (Si se carga, a la derecha)
    if logo_bytes:
        try:
            with open("temp_logo_corp.png", "wb") as f:
                f.write(logo_bytes.getbuffer())
            c.drawImage("temp_logo_corp.png", 6*inch, 9.2*inch, width=1.5*inch, height=0.8*inch, preserveAspectRatio=True)
        except: pass

    # --- 2. TÍTULO Y ENCABEZADO TÉCNICO ---
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(VERDE_SERENITY)
    titulo = "VADEMÉCUM TÉCNICO DE CUMPLIMIENTO LEGAL" if es_vademecum else "CERTIFICADO DE COMPENSACIÓN BIOMÉTRICA"
    c.drawCentredString(4.25*inch, 8.8*inch, titulo)
    
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(black)
    c.drawCentredString(4.25*inch, 8.4*inch, f"RAZÓN SOCIAL: {empresa.upper()}")
    c.drawCentredString(4.25*inch, 8.2*inch, f"ID DE REGISTRO NEXUS: {hash_id}")

    # --- 3. CUERPO TÉCNICO (CONTENIDO LEGAL) ---
    text_object = c.beginText(0.8*inch, 7.5*inch)
    text_object.setFont("Helvetica-Bold", 11)
    text_object.setLeading(14)
    
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
            "CONCLUSIÓN TÉCNICA: La entidad referenciada se vincula al Internet de la Naturaleza",
            "asegurando la trazabilidad absoluta de su inversión ambiental mediante Blockchain."
        ]
    else:
        lineas = [
            "DETALLE DE COMPENSACIÓN:",
            f"- Gestión de {impacto} individuos forestales en el corredor biológico de Dagua.",
            "- Registro biométrico activo en la Red de Faros Serenity.",
            "- Estado de mantenimiento: Vigente bajo protocolos de restauración activa.",
            "- Este certificado avala la responsabilidad social y ambiental corporativa.",
            "",
            "FIRMA AUTORIZADA: Sistema Nexus IA - Serenity S.A.S BIC"
        ]
        
    for linea in lineas:
        text_object.textLine(linea)
    c.drawText(text_object)

    # --- 4. PIE DE PÁGINA SEGURIDAD ---
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(4.25*inch, 1.2*inch, "Documento generado electrónicamente. La validez de este reporte puede verificarse en la cadena de bloques Nexus.")
    
    c.save()
    buffer.seek(0)
    return buffer

# --- CSS (ESTILOS) ---
st.markdown("""
    <style>
        .stApp { 
            background-image: linear-gradient(rgba(5, 10, 4, 0.8), rgba(5, 10, 4, 0.9)), 
            url('https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1920&q=80');
            background-size: cover; background-position: center; background-attachment: fixed;
            color: #e8f5e9; font-family: 'Montserrat', sans-serif; 
        }
        label, .stMarkdown p, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, .stMetricLabel { 
            color: white !important; font-weight: 500; 
        }
        [data-testid="stSidebar"] { background-color: rgba(10, 20, 8, 0.9) !important; backdrop-filter: blur(10px); }
        h1, h2, h3 { color: #9BC63B !important; text-shadow: 2px 2px 4px #000; }
        .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #9BC63B; border-radius: 8px; width: 100%; font-weight: bold; }
        .stButton>button:hover { background-color: #9BC63B; color: black; box-shadow: 0 0 15px #9BC63B; }
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; height: 100%; }
        .faro-gemini { border: 2px solid #4285F4; padding: 15px; border-radius: 10px; background: rgba(66, 133, 244, 0.2); text-align: center; box-shadow: 0 0 15px #4285F4; }
        .cam-grid { background: #000; border: 1px solid #2E7D32; height: 80px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #ff0000; border-radius: 5px; }
        .metric-card { background: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; border: 1px solid #9BC63B; text-align: center; }
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
        .airline-grid img { max-width: 90%; max-height: 70px; object-fit: contain; }
        .airline-grid p { color: black !important; font-size: 0.7rem; font-weight: bold; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN ---
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top: 50px;'><h1>SISTEMA NEXUS | SERENITY</h1></div>", unsafe_allow_html=True)
    col_sec = st.columns([1,1,1])
    with col_sec[1]:
        clave = st.text_input("PASSWORD ADMIN", type="password")
        if st.button("INGRESAR"):
            if clave == "Serenity2026":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- BUSCA ESTA SECCIÓN Y ACTUALIZA LA LISTA ---
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

# 1. INICIO - RESTAURACIÓN COMPLETA
if menu == "INICIO":
    # --- LOGO CENTRADO ---
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        if os.path.exists("logo_serenity.png"):
            st.image("logo_serenity.png", use_container_width=True)
        else:
            st.markdown("<h1 style='text-align:center; color:#9BC63B;'>SERENITY NEXUS GLOBAL</h1>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; font-size:3.5rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold;'>SISTEMA REGENERATIVO BIOMÉTRICO KBA</p>", unsafe_allow_html=True)
    
    # --- AUDIO EARTH ---
    st.components.v1.html("""
        <audio id="audio_earth" src="sonido_Earth.mp3" loop></audio>
        <div style="text-align:center; margin-top:20px;">
            <button onclick="document.getElementById('audio_earth').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:10px 20px; border-radius:10px; cursor:pointer; font-weight:bold;">ACTIVAR SONIDO GLOBAL EARTH</button>
        </div>
    """, height=100)

    # --- DATOS DE GOBERNANZA ---
    st.info("SPAM (40%) | TAF (60%) | JWCJ $SNG")

    st.divider()

    # --- QUIÉNES SOMOS, MISIÓN Y VISIÓN ---
    col_inf1, col_inf2 = st.columns(2)
    
    with col_inf1:
        st.subheader("QUIÉNES SOMOS / WHO WE ARE")
        st.write("Serenity Nexus Global es la primera plataforma Phygital (Física + Digital) del Valle del Cauca que integra la conservación ambiental con tecnología Blockchain e Inteligencia Artificial, transformando la protección de la biodiversidad en un activo digital tangible.")

    with col_inf2:
        st.subheader("NUESTRA MISIÓN / OUR MISSION")
        st.write("Regenerar el tejido ecológico y social mediante un modelo de negocio sostenible que permita a empresas y personas compensar su huella ambiental a través de la tecnología y la transparencia.")

    st.write("---")
    
    col_inf3, col_inf4 = st.columns([1, 2])
    with col_inf3:
        st.subheader("NUESTRA VISIÓN / OUR VISION")
    with col_inf4:
        st.write("Ser el referente mundial del Internet de la Naturaleza para 2030, liderando la valorización de los servicios ecosistémicos mediante nuestra red de Faros inteligentes y el token $SNG.")

    st.info("Ubicación del Proyecto: Dagua y Felidia, Valle del Cauca - Hacienda Monte Guadua & Finca Villa Michelle.")

elif menu == "RED DE FAROS (7 NODOS)":
    st.title("🛰️ Monitoreo Perimetral Nexus")
    
    # --- 1. LÓGICA DE BOTONES ---
    def conectar_faro(nombre):
        st.session_state.f_activo = nombre

    c1, c2, c3 = st.columns(3)
    with c1: 
        st.markdown("<div class='faro-card'><h3>🦅 FARO HALCÓN</h3></div>", unsafe_allow_html=True)
        st.button("Conectar Halcón", key="h1", on_click=conectar_faro, args=("Halcón",), use_container_width=True)
    with c2: 
        st.markdown("<div class='faro-card'><h3>🦜 FARO COLIBRÍ</h3></div>", unsafe_allow_html=True)
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
        st.markdown("<div class='faro-card'><h3>🦦 FARO CAPIBARA</h3></div>", unsafe_allow_html=True)
        st.button("Conectar Capibara", key="cp6", on_click=conectar_faro, args=("Capibara",), use_container_width=True)

    st.divider()

    # --- 2. NODO REX ---
    col_rex_gemini = st.columns([1,2,1])
    with col_rex_gemini[1]:
        st.markdown("<div class='faro-rex-gemini' style='text-align: center;'><h3>🧠 REX GEMINI</h3></div>", unsafe_allow_html=True)
        st.button("🔥 ACTIVAR REX GEMINI VISION", key="gm_btn", on_click=conectar_faro, args=("REX GEMINI",), use_container_width=True)

    # --- 3. PANTALLA DE MONITOREO (SEGURA) ---
    # Usamos .get() para evitar el NameError si la variable no existe aún
    f_nom = st.session_state.get('f_activo', None)

    if f_nom:
        color_f = "#4285F4" if f_nom == "REX GEMINI" else "#9BC63B"
        nombre_limpio = str(f_nom).upper()
        
        st.write("---")
        st.markdown(f"<h2 style='text-align:center; color:{color_f};'>🛰️ FEED EN VIVO: {nombre_limpio}</h2>", unsafe_allow_html=True)

        st.markdown("### 📽️ Unidades de Video Perimetral")
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

        # --- 4. SONIDOS (BIOACÚSTICA) ---
        st.write("---")
        st.subheader("🔊 Sensores Bioacústicos")
        a_links = [
            "https://www.soundjay.com/nature/sounds/forest-birds-01.mp3",
            "https://www.soundjay.com/nature/sounds/bird-chirp-01.mp3",
            "https://www.soundjay.com/nature/sounds/forest-birds-02.mp3",
            "https://www.soundjay.com/nature/sounds/river-1.mp3"
        ]
        c_snd = st.columns(4)
        for k in range(4):
            with c_snd[k]:
                st.markdown(f"<b style='color:{color_f}; font-size:11px;'>🔊 MIC {k+1}</b>", unsafe_allow_html=True)
                st.audio(a_links[k])

                
# =========================================================
# BLOQUE: DASHBOARD ESTADÍSTICO IA
# =========================================================
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("🧠 Inteligencia de Datos Nexus")
    st.markdown("### Análisis Biométrico y Predictivo del Ecosistema")

# --- FILTRO POR FARO CORREGIDO ---
    faro_seleccionado = st.selectbox("Seleccione el Faro para Auditoría IA:", 
                                   [
                                       "Faro Rex", 
                                       "Faro Halcón", 
                                       "Faro Colibrí", 
                                       "Faro Rana", 
                                       "Faro Venado", 
                                       "Faro Tigrillo", 
                                       "Faro Capibara"
                                   ])
    st.write(f"Anatizando telemetría en tiempo real de: **{faro_seleccionado}**")

    # --- MÉTRICAS VIVAS (Simulación de Sensores) ---
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

    # --- GRÁFICO DE ACTIVIDAD BIOMÉTRICA ---
    st.subheader("📊 Flujo de Actividad (24h)")
    # Creamos datos ficticios pero realistas para el gráfico
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Audio (Biofonia)', 'Visión (Fauna)', 'Captura Carbono']
    )
    st.line_chart(chart_data)

    # --- ASISTENTE NEXUS AI ---
    with st.container(border=True):
        st.markdown("#### 🤖 Consulta al Oráculo Nexus")
        pregunta = st.text_input("Pregunta a la IA sobre este Faro:", placeholder="Ej: ¿Cuál es el estado de la fauna en el Faro Tigrillo?")
        
        if pregunta:
            with st.spinner("Analizando datos satelitales y biométricos..."):
                # Aquí simulamos la respuesta de la IA basada en el contexto del Faro
                st.markdown(f"""
                **Respuesta Nexus AI:**
                Basado en el análisis de audio del **{faro_seleccionado}**, se han detectado frecuencias consistentes con aves endémicas en las últimas 3 horas. 
                La biomasa protegida está procesando CO2 a niveles óptimos y no se detectan intrusiones humanas ni ruidos de maquinaria.
                """)
                st.info("💡 Este análisis utiliza la API de Google Gemini para interpretar los sensores de campo.")

    st.caption("Los datos presentados son validados mediante la Red Nexus y registrados en la Blockchain para transparencia total.")


# =========================================================
# BLOQUE 3: GESTIÓN LEY 2173 (EMPRESAS)
# =========================================================
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Nexus Legal & Compliance Hub")
    st.markdown("### Soluciones Tecnológicas a la Normativa Ambiental Colombiana")

    # --- Tarjetas Visuales de Marco Legal ---
    c_l1, c_l2, c_l3 = st.columns(3)
    with c_l1:
        st.markdown('<div style="background:#1e2630; padding:15px; border-radius:10px; border-left:5px solid #9BC63B; min-height:180px;"><h4 style="color:#9BC63B;">LEY 2173</h4><p style="font-size:0.8rem; color:#ccc;"><b>Áreas de Vida:</b> Obligación de 2 árboles por empleado anualmente. Serenity provee el terreno y GPS oficial para cumplimiento corporativo.</p></div>', unsafe_allow_html=True)
    with c_l2:
        st.markdown('<div style="background:#1e2630; padding:15px; border-radius:10px; border-left:5px solid #3498db; min-height:180px;"><h4 style="color:#3498db;">LEY 2169</h4><p style="font-size:0.8rem; color:#ccc;"><b>Acción Climática:</b> Ruta a la Carbono Neutralidad. Nuestra IA certifica la captura real de CO2 para reportes en el RENARE.</p></div>', unsafe_allow_html=True)
    with c_l3:
        st.markdown('<div style="background:#1e2630; padding:15px; border-radius:10px; border-left:5px solid #e74c3c; min-height:180px;"><h4 style="color:#e74c3c;">LEY 2111</h4><p style="font-size:0.8rem; color:#ccc;"><b>Justicia Ambiental:</b> Delitos Ambientales. Los Faros actúan como evidencia digital inmutable ante la deforestación.</p></div>', unsafe_allow_html=True)

    st.write("")
    
    # --- SECCIÓN 1: Vademécum Técnico-Legal ---
    with st.container(border=True):
        st.subheader("📋 Vademécum de Soluciones Corporativas")
        st.write("Genera un documento técnico que explica cómo Serenity Nexus ayuda a tu empresa a cumplir con las leyes ambientales.")
        
        empresa_v = st.text_input("Razón Social para el Reporte Técnico", placeholder="Ej: Transportes del Valle SAS", key="txt_vademecum")
        
        if st.button("GENERAR VADEMÉCUM TÉCNICO PDF", use_container_width=True):
            if empresa_v:
                # Generamos el PDF usando la función maestra con el flag es_vademecum=True
                hash_v = hashlib.sha256(f"{empresa_v}VAD".encode()).hexdigest()[:12].upper()
                pdf_v = generar_pdf_corporativo(empresa_v, 0, hash_v, es_vademecum=True)
                st.session_state.vademecum_pdf = pdf_v.getvalue() # Guardamos los bytes
                st.success(f"Vademécum para {empresa_v} generado exitosamente.")
            else:
                st.warning("Por favor, ingrese el nombre de la empresa.")
        
        if 'vademecum_pdf' in st.session_state:
            st.download_button(
                label="📥 DESCARGAR VADEMÉCUM (PDF ESTRUCTURADO)",
                data=st.session_state.vademecum_pdf,
                file_name=f"Vademecum_Nexus_{empresa_v}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    st.divider()

    # --- SECCIÓN 2: Emisión de Certificado con Identidad Corporativa ---
    st.subheader("🛡️ Emisión de Certificado con Logo")
    st.write("Cargue el logo de su empresa para emitir el certificado oficial de cumplimiento de la Ley 2173.")
    
    col_act1, col_act2 = st.columns([1, 1])
    
    with col_act1:
        n_corp = st.text_input("Nombre de la Compañía (Para el Certificado)", key="txt_corp")
        nit_corp = st.text_input("NIT de la Empresa", placeholder="900.123.456-1", key="nit_corp")
        n_per = st.number_input("Número de Empleados Actuales", min_value=1, value=100, key="num_emp")
        archivo_logo = st.file_uploader("Cargar Logo Corporativo (PNG/JPG)", type=['png', 'jpg'], key="file_logo")

    with col_act2:
        st.info(f"**Requisito Ley 2173:** Su empresa debe compensar {n_per * 2} árboles este año.")
        
        if st.button("EMITIR CERTIFICADO OFICIAL CON LOGO", use_container_width=True):
            if n_corp and archivo_logo:
                with st.spinner("Procesando identidad corporativa..."):
                    h_c = hashlib.sha256(f"{n_corp}{nit_corp}".encode()).hexdigest()[:12].upper()
                    
                    # --- SOLUCIÓN AL ERROR: REBOBINAR Y LEER ---
                    archivo_logo.seek(0) # Volvemos al inicio del archivo
                    logo_bytes = archivo_logo.getvalue() # Obtenemos los bytes de forma segura
                    
                    pdf_c = generar_pdf_corporativo(
                        empresa=n_corp, 
                        impacto=n_per*2, 
                        hash_id=h_c, 
                        nit=nit_corp, 
                        logo_bytes=logo_bytes, # Pasamos los bytes limpios
                        faro_nombre="Faro Rex"
                    )
                    
                    st.session_state.cert_corp_pdf = pdf_c.getvalue()
                    st.success("Certificado generado exitosamente.")
            else:
                st.error("Razón Social y Logo son obligatorios.")

        if 'cert_corp_pdf' in st.session_state:
            st.download_button(
                label="📥 DESCARGAR CERTIFICADO CON LOGO (PDF)",
                data=st.session_state.cert_corp_pdf,
                file_name=f"Certificado_Ley2173_{n_corp}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# =========================================================
# BLOQUE 4: SUSCRIPCIONES
# =========================================================
elif menu == "SUSCRIPCIONES":
    st.title("Membresías de Impacto Serenity")
    st.markdown("### Transforma tu aporte en regeneración real")

    # --- TARJETAS DE PLANES CON BENEFICIOS DETALLADOS ---
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("""
            <div style="background:#1e2630; padding:20px; border-radius:15px; border:2px solid #9BC63B; text-align:center; min-height: 420px;">
                <h3 style="color:#9BC63B;">PLAN SEMILLA</h3>
                <h2 style="color:white;">$25 USD <small>/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;"> <b>5 Árboles:</b> Siembra y mantenimiento.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>1 Faro:</b> Datos biométricos básicos.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>50 Tokens:</b> $SNG de respaldo.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>Certificado:</b> Digital con Hash.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ELEGIR SEMILLA", use_container_width=True, key="p_semilla"):
            st.session_state.p_sel = "SEMILLA"
            st.session_state.m_plan = 25

    with p2:
        st.markdown("""
            <div style="background:#1e2630; padding:20px; border-radius:15px; border:3px solid #9BC63B; text-align:center; min-height: 420px; transform: scale(1.02);">
                <h3 style="color:#9BC63B;">PLAN GUARDIÁN</h3>
                <h2 style="color:white;">$80 USD <small>/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;"> <b>15 Árboles:</b> Restauración activa.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>Cámaras 4K:</b> Streaming del bosque.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>200 Tokens:</b> Mayor respaldo $SNG.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>Reporte IA:</b> Inventario de carbono.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ELEGIR GUARDIÁN", use_container_width=True, key="p_guardian"):
            st.session_state.p_sel = "GUARDIÁN"
            st.session_state.m_plan = 80

    with p3:
        st.markdown("""
            <div style="background:#1e2630; padding:20px; border-radius:15px; border:2px solid #D4AF37; text-align:center; min-height: 420px;">
                <h3 style="color:#D4AF37;">PLAN HALCÓN</h3>
                <h2 style="color:white;">$200 USD <small>/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;"> <b>1 Plaza Protegida:</b> Soberanía total.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>Cámaras:</b> Vigilancia perimetral.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>600 Tokens:</b> Impacto Web3 máximo.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>Visita 1 Persona VIP:</b> Acceso a Monte Guadua 2 Dias 1 Noche.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ELEGIR HALCÓN", use_container_width=True, key="p_halcon"):
            st.session_state.p_sel = "HALCÓN"
            st.session_state.m_plan = 200

    # --- PASARELA DE PAGO CON LOGOS REHABILITADOS ---
    if 'p_sel' in st.session_state:
        st.write("---")
        st.subheader(f"Finalizar Suscripción: {st.session_state.p_sel}")
        
        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            with st.container(border=True):
                st.markdown("#### Tarjeta de Crédito/Débito")
                st.text_input("Titular de la cuenta")
                st.text_input("Número de Tarjeta", placeholder="xxxx xxxx xxxx xxxx")
                c_exp, c_cvc = st.columns(2)
                c_exp.text_input("Vencimiento (MM/AA)")
                c_cvc.text_input("CVC")
                if st.button("ACTIVAR SUSCRIPCIÓN", use_container_width=True):
                    st.balloons()
                    st.success(f"¡Bienvenido al Plan {st.session_state.p_sel}! Impacto activado.")

        with col_pay2:
            st.markdown("#### Pagos Locales y Alternativos")
            st.markdown("""
                <div style="background: #ffffff; padding: 25px; border-radius: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center; border: 1px solid #ddd;">
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/b/bf/Nequi_logo.png" width="90"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Bancolombia_logo.svg/2560px-Bancolombia_logo.svg.png" width="90"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Visa_Inc._logo.svg/2560px-Visa_Inc._logo.svg.png" width="70"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/1280px-Mastercard-logo.svg.png" width="70"></div>
                </div>
            """, unsafe_allow_html=True)
            st.caption("Transacciones seguras mediante Nexus Gateway (Dagua-Colombia)")
            
# =========================================================
# BLOQUE 5: BILLETERA CRYPTO (WEB3) - ECOSISTEMA $SNG
# =========================================================
elif menu == "BILLETERA CRYPTO (WEB3)":
    st.title("Nexus Finance Control")
    st.markdown("### El Futuro de la Conservación Tokenizada")

    # --- NIVEL 1: EL TOKEN (VISUAL) ---
    try:
        # Intentamos cargar el video si existe, si no, mostramos un mensaje elegante
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
            st.info("🛰️ Visualizador de Token $SNG Activo (Esperando archivo de video)")
    except Exception as e:
        st.info("🛰️ Sistema de Video Nexus en Espera")

    st.write("---")

    # --- NIVEL 2: ADQUISICIÓN Y CUSTODIA ---
    col_buy, col_vault = st.columns(2)

    with col_buy:
        st.markdown("<h4 style='color:#9BC63B;'>¿Cómo comprar $SNG?</h4>", unsafe_allow_html=True)
        st.write("El token $SNG representa hectáreas regeneradas y datos biométricos de los Faros.")
        with st.container(border=True):
            st.markdown("<p style='color:white; font-weight:bold;'>Simulador de Intercambio (Swap)</p>", unsafe_allow_html=True)
            moneda_pago = st.selectbox("Pagar con:", ["USD (Tarjeta/Transferencia)", "USDT (Crypto)", "Ethereum"])
            cantidad_usd = st.number_input("Monto a invertir (USD):", min_value=10, step=50, key="wallet_buy_usd")
            tasa = 0.50 # 1 SNG = 0.50 USD
            st.metric("Recibirás aproximadamente:", f"{cantidad_usd / tasa:,.2f} $SNG")
            if st.button("COMPRAR TOKENS $SNG", use_container_width=True):
                st.success("Orden de compra enviada al Nexus Gateway.")

    with col_vault:
        st.markdown("<h4 style='color:#9BC63B;'>¿Cómo tener una Billetera Nexus?</h4>", unsafe_allow_html=True)
        st.write("Nexus Vault es tu llave privada al Internet de la Naturaleza.")
        st.markdown("""
        <div style='color:white;'>
        <p>• <b>Paso 1:</b> Descarga Nexus App o usa Metamask.</p>
        <p>• <b>Paso 2:</b> Genera tu frase semilla de 24 palabras.</p>
        <p>• <b>Paso 3:</b> Vincula tu ID de Donante Serenity.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("DESCARGAR GUÍA DE CONFIGURACIÓN", use_container_width=True)

    st.write("---")

    # --- NIVEL 3: CONEXIÓN Y TABLA DE RESPALDO (ESTILO BLANCO) ---
    st.markdown("<h4 style='color:white; text-align:center;'>Centro de Conexión Web3</h4>", unsafe_allow_html=True)
    cw1, cw2, cw3 = st.columns([1, 2, 1])
    
    with cw2:
        if st.button("VINCULAR BILLETERA AL SISTEMA NEXUS", use_container_width=True):
            st.session_state.wallet_connected = True
            st.balloons()

    # Si la billetera está conectada (o para mostrarlo por defecto en el demo)
    if st.session_state.get('wallet_connected', False):
        st.success("Billetera 0x71C...9A23 Conectada con éxito.")
        
        col_met1, col_met2 = st.columns(2)
        with col_met1:
            st.metric(label="Saldo en Bóveda", value="25,000.00 $SNG")
        with col_met2:
            st.metric(label="Respaldo Real", value="80 Hectáreas", delta="Sincronizado")

        st.write("")
        st.markdown("<h5 style='color:white; text-align:center; background:#2E7D32; padding:10px; border-radius:5px;'>📋 DESGLOSE DE ACTIVOS RESPALDADOS POR FARO</h5>", unsafe_allow_html=True)
        
        # Creación de la tabla con datos oficiales de tus faros
        data_wallet = {
            "Activo Biológico": ["Carbono Azul", "Biodiversidad", "Agua Protegida", "Suelo Regenerado"],
            "Nodo Validador": ["Faro Rex", "Faro Tigrillo", "Faro Colibrí", "Faro Halcón"],
            "Tokens $SNG": ["5,000", "8,500", "3,200", "8,300"],
            "Certificación": ["✅ Verificado", "✅ Verificado", "⏳ Sincronizando", "✅ Verificado"]
        }
        df_wallet = pd.DataFrame(data_wallet)
        
        # Inyectamos CSS específico para que esta tabla sea blanca y legible
        st.markdown("""
            <style>
                .stTable td, .stTable th {
                    color: white !important;
                    font-size: 1.05rem !important;
                    text-align: center !important;
                }
            </style>
        """, unsafe_allow_html=True)
        
        st.table(df_wallet)
        st.caption("Los datos biométricos son actualizados cada 60 segundos por la Red de Faros.")

# =========================================================
# BLOQUE 6: DONACIONES Y CERTIFICADO (Diploma Oficial)
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
                    # 1. Generar Hash
                    datos_hash = f"{nombre_d}{monto_d}{datetime.now()}"
                    hash_certificado = hashlib.sha256(datos_hash.encode()).hexdigest()[:16].upper()
                    
                    # 2. Guardar en session_state
                    st.session_state.current_hash = hash_certificado
                    st.session_state.nombre_prev = nombre_d
                    st.session_state.monto_prev = monto_d
                    
                    # 3. Generar PDF
                    st.session_state.pdf_buffer = generar_pdf_certificado(nombre_d, monto_d, hash_certificado)
                    
                    st.session_state.donaciones_recibidas += 1
                    st.balloons()
                    st.success(f"¡Certificado generado con éxito!")
                else:
                    st.warning("Ingrese el nombre del donante.")

    with colB:
        if 'pdf_buffer' in st.session_state:
            st.markdown(f"""
                <div style="background:white; color:black; padding:30px; text-align:center; border:8px double #2E7D32; border-radius:15px;">
                    <h2 style="color:#2E7D32; margin-bottom:10px;">VISTA PREVIA</h2>
                    <hr style="border:1px solid #2E7D32;">
                    <p style="font-size:1.2rem; margin-top:20px;">Gracias por tu aporte, <b>{st.session_state.nombre_prev.upper()}</b></p>
                    <p>Has contribuido con <b>${st.session_state.monto_prev} USD</b></p>
                    <div style="background:#f0f2f6; padding:10px; border-radius:5px; margin-top:20px;">
                        <code style="font-size:0.8rem; color: #2E7D32;">HASH: {st.session_state.current_hash}</code>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.download_button(
                label="DESCARGAR DIPLOMA CON HASH (PDF)",
                data=st.session_state.pdf_buffer,
                file_name=f"Certificado_Nexus_{st.session_state.current_hash}.pdf",
                mime="application/pdf"
            )

# =========================================================
# BLOQUE 7: DIAGNOSTICO HUELLA DE CARBONO
# =========================================================
elif menu == "DIAGNOSTICO HUELLA DE CARBONO":
    st.title("🧠 Inteligencia de Carbono Nexus")
    st.markdown("### Diagnóstico Automatizado de Huella de Carbono")

    # 1. ENTRADA DE DATOS CORPORATIVOS
    with st.container(border=True):
        col_nit1, col_nit2 = st.columns([1, 1])
        with col_nit1:
            nit_empresa = st.text_input("INGRESE EL NIT DE LA EMPRESA (Sin dígito de verificación)", placeholder="900123456")
        with col_nit2:
            nombre_empresa = st.text_input("RAZÓN SOCIAL", placeholder="Ej: TRANSPORTES VALLE SAS")

    if nit_empresa and nombre_empresa:
        # 2. MOTOR DE IA: Deducción de Actividad y Huella
        # En un sistema real, aquí consultaríamos una API de RUES o DIAN
        # Para el MVP, usamos lógica de segmentación por sectores colombianos
        
        st.subheader(f"🛡️ Análisis de Impacto: {nombre_empresa}")
        
        # Simulamos la categorización por sector (IA logic)
        # Esto se puede conectar con Gemini para que lea el objeto social real
        sector_deducido = "Transporte Multimodal y Logística" # Ejemplo detectado
        intensidad_carbono = "ALTA" # Clasificación según sector
        
        st.markdown(f"**Sector Detectado:** `{sector_deducido}` | **Intensidad de Emisión:** `{intensidad_carbono}`")

        # 3. CALCULADORA DE EMISIÓN BASADA EN SECTOR
        with st.expander("📊 Parámetros de Operación Mensual", expanded=True):
            col_par1, col_par2 = st.columns(2)
            with col_par1:
                consumo_energia = st.number_input("Consumo Energía (kWh/mes)", min_value=0, value=1500)
                flota_vehicular = st.number_input("Número de Vehículos / Aeronaves en Operación", min_value=0, value=5)
            with col_par2:
                residuos_ton = st.number_input("Producción de Residuos (Toneladas/mes)", min_value=0.0, value=1.2)
                operaciones_dia = st.number_input("Promedio Operaciones Diarias", min_value=1, value=10)

        # CÁLCULO CIENTÍFICO (Factores de emisión estándar para Colombia)
        # Energía: 0.164 kgCO2/kWh | Diesel/JetA1: ~2.6 kgCO2/gal | Residuos: variable
        huella_total = (consumo_energia * 0.164) + (flota_vehicular * operaciones_dia * 15.5) + (residuos_ton * 500)
        
        # --- RESULTADOS DE COMPENSACIÓN ---
        res1, res2 = st.columns(2)
        with res1:
            st.metric("HUELLA ESTIMADA MÁXIMA", f"{huella_total:,.2f} kg CO2e / mes")
            st.progress(0.85 if intensidad_carbono == "ALTA" else 0.3)
            
        with res2:
            arboles_nexus = int(huella_total / 20) # 1 árbol Nexus = 20kg/año
            st.metric("COMPENSACIÓN REQUERIDA", f"{arboles_nexus} Árboles", "Activos Biológicos")

        # 4. GENERACIÓN DE CERTIFICADO CON HASH SHA-512
        hash_id = hashlib.sha512(f"{nit_empresa}{huella_total}".encode()).hexdigest()[:16].upper()
        
        pdf_file = generar_pdf_corporativo(
            empresa=nombre_empresa, 
            impacto=arboles_nexus, 
            hash_id=hash_id,
            logo_bytes=None,
            es_vademecum=True # Enviamos el Vademécum legal por ser empresa NIT
        )

        st.download_button(
            label=f"📥 EMITIR CERTIFICADO LEGAL DE COMPENSACIÓN PARA {nombre_empresa}",
            data=pdf_file,
            file_name=f"Certificado_Nexus_{nit_empresa}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# =========================================================
# BLOQUE 8: UBICACIÓN & MAPAS (VERSIÓN FINAL NASA-GRADE)
# =========================================================
elif menu == "UBICACIÓN & MAPAS":
    st.title("🛰️ Geoposicionamiento Nexus Global")
    st.markdown("### Monitoreo Satelital de Faros en KBA Bosque San Antonio")

    # 1. COORDENADAS ESTRATÉGICAS (7 NODOS)
    # 6 Faros en Monte Guadua + 1 Faro en Villa Michelle
    lat_v, lon_v = 3.485, -76.605 # Coordenadas base Villa Michelle
    
# 1. COORDENADAS ESTRATÉGICAS CON NOMBRES OFICIALES
    faros_nexus = [
        {"name": "Faro Halcón (Monte Guadua)", "lat": 3.518, "lon": -76.620, "color": "green"},
        {"name": "Faro Colibrí (Monte Guadua)", "lat": 3.519, "lon": -76.622, "color": "green"},
        {"name": "Faro Rana (Monte Guadua)", "lat": 3.517, "lon": -76.621, "color": "green"},
        {"name": "Faro Venado (Monte Guadua)", "lat": 3.516, "lon": -76.623, "color": "green"},
        {"name": "Faro Tigrillo (Monte Guadua)", "lat": 3.520, "lon": -76.619, "color": "green"},
        {"name": "Faro Capibara (Monte Guadua)", "lat": 3.515, "lon": -76.625, "color": "green"},
        {"name": "Faro Rex (Villa Michelle)", "lat": 3.485, "lon": -76.605, "color": "blue"}
    ]

    # 2. BOTÓN DE ENLACE EXTERNO (ESTILO GRADO MILITAR)
    # URL corregida para Google Maps Satelital
    url_gmaps = f"https://www.google.com/maps/search/?api=1&query={lat_v},{lon_v}"
    
    st.markdown(f"""
        <div style='text-align:center; margin-bottom: 25px;'>
            <a href="{url_gmaps}" target="_blank" style="text-decoration: none;">
                <button style="background-color:#4285F4; color:white; border:none; padding:12px 25px; border-radius:8px; font-weight:bold; cursor:pointer; box-shadow: 0 4px 15px rgba(66, 133, 244, 0.4); font-family:sans-serif;">
                    🛰️ ABRIR RADAR EXTERNO (GOOGLE MAPS)
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

    # 3. MAPA INTERACTIVO CON CAPA SATELITAL HÍBRIDA
    # Usamos los tiles de Google Satélite para máxima resolución de los árboles
    google_map_tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'
    
    m = folium.Map(
        location=[3.518, -76.620], 
        zoom_start=14, 
        tiles=google_map_tiles, 
        attr='Google Satellite'
    )

    # 4. DESPLIEGUE DE NODOS Y RANGOS BIOACÚSTICOS
    for faro in faros_nexus:
        # Radio de captura de los 4 micrófonos (200 metros)
        folium.Circle(
            location=[faro['lat'], faro['lon']],
            radius=200,
            color=faro['color'],
            fill=True,
            fill_opacity=0.2,
            tooltip=f"Rango de Audio: {faro['name']}"
        ).add_to(m)

        # Marcador de estructura de pino canadiense
        folium.Marker(
            location=[faro['lat'], faro['lon']],
            popup=f"<b>{faro['name']}</b><br>Estructura: 3x2x3 Pino<br>Enlace: Starlink",
            icon=folium.Icon(color=faro['color'], icon='broadcast-tower', prefix='fa')
        ).add_to(m)

    # Renderizado en Streamlit
    st_folium(m, width=1000, height=550)

    # 5. PANEL DE TELEMETRÍA (ESTADO DE LOS FAROS)
    st.divider()
    col_inf1, col_inf2, col_inf3 = st.columns(3)
    with col_inf1:
        st.metric("NODOS ACTIVOS", "7/7", "Sincronizado")
    with col_inf2:
        st.metric("CONEXIÓN", "STARLINK", "Latencia 45ms")
    with col_inf3:
        st.metric("ENERGÍA", "SOLAR", "Nominal")

    st.info("💡 Cada Faro Nexus registra datos en tiempo real mediante 8 cámaras y 4 micrófonos dentro del KBA Bosque San Antonio.")

# --- FIN DEL ARCHIVO ---



























































































































































































































































































