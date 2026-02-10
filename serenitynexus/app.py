# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
import hashlib
from datetime import datetime
import io
import os

# --- BLOQUE DE SEGURIDAD PARA CÁMARA ---
try:
    import cv2
except ImportError:
    cv2 = None

# --- LIBRERÍAS EXTENDIDAS ---
import folium
from streamlit_folium import st_folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.lib.utils import ImageReader

# --- CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="Serenity Nexus Global", page_icon="??", layout="wide")
VERDE_SERENITY = HexColor("#2E7D32")

# --- GESTIÓN DE ESTADO ---
if 'lang' not in st.session_state: st.session_state.lang = 'ES' 
if 'total_protegido' not in st.session_state: st.session_state.total_protegido = 87.0
if 'donaciones_recibidas' not in st.session_state: st.session_state.donaciones_recibidas = 0
if 'estado_gemini' not in st.session_state: st.session_state.estado_gemini = "Latente"
if 'auth' not in st.session_state: st.session_state.auth = False
if 'f_activo' not in st.session_state: st.session_state.f_activo = None
if 'wallet_connected' not in st.session_state: st.session_state.wallet_connected = False
if 'pdf_empresa_buffer' not in st.session_state: st.session_state.pdf_empresa_buffer = None

# --- DATOS LEGALES (COMPLETOS) ---
TEXTO_LEY_2173 = """
RESUMEN EJECUTIVO - LEY 2173 DE 2021 (ÁREAS DE VIDA)
Objeto: Promover la restauración ecológica a través de la siembra de árboles y creación de bosques en el territorio nacional.
Obligación: Las medianas y grandes empresas deben sembrar 2 árboles por cada empleado.
Cumplimiento: Se debe demostrar mediante certificado de 'Área de Vida' expedido por la autoridad competente o aliado ambiental.
Solución Serenity: Ofrecemos el suelo, la siembra, el mantenimiento y el reporte digital para cumplimiento corporativo.
"""
TEXTO_CONPES = """
RESUMEN EJECUTIVO - CONPES 3934 (POLÍTICA DE CRECIMIENTO VERDE)
Objeto: Impulsar la productividad y la competitividad económica del país, asegurando el uso sostenible del capital natural y la inclusión social.
Meta 2030: Aumentar la bioeconomía y los negocios verdes como motor de desarrollo.
Alineación Serenity: Nuestra plataforma integra Big Data e IoT para la gestión eficiente del capital natural del Valle del Cauca.
"""
TEXTO_DELITOS = """
RESUMEN EJECUTIVO - LEY 2111 DE 2021 (DELITOS AMBIENTALES)
Objeto: Sustituir el título de delitos contra los recursos naturales y el medio ambiente en el Código Penal.
Impacto: La deforestación, el tráfico de fauna y el daño a recursos naturales ahora tienen penas de prisión y multas severas.
Solución Serenity: Nuestro sistema de monitoreo (Faros) actúa como evidencia forense y herramienta de prevención y vigilancia.
"""
TEXTO_TRIBUTARIO = """
RESUMEN EJECUTIVO - BENEFICIOS TRIBUTARIOS (S.A.S. BIC & CTeI)
Objeto: Incentivar la inversión en ciencia, tecnología e impacto social.
Beneficio 1: Descuento en renta por donaciones a entidades ambientales sin ánimo de lucro certificadas.
Beneficio 2: Deducciones por inversión en proyectos de Ciencia, Tecnología e Innovación (Actividades Serenity Nexus).
Beneficio 3: Preferencia en contratación pública y acceso a líneas de crédito especiales.
"""

# --- DICCIONARIO DE TRADUCCIÓN ---
tr = {
    'menu_opts': {
        'ES': ["INICIO", "RED DE FAROS (7 NODOS)", "DASHBOARD ESTADÍSTICO IA", "GESTIÓN LEY 2173 (EMPRESAS)", "SUSCRIPCIONES", "BILLETERA CRYPTO (WEB3)", "DONACIONES Y CERTIFICADO", "LOGÍSTICA AEROLÍNEAS", "UBICACIÓN & MAPAS"],
        'EN': ["HOME", "BEACON NETWORK (7 NODES)", "AI STATS DASHBOARD", "LAW 2173 MANAGEMENT (CORP)", "SUBSCRIPTIONS", "CRYPTO WALLET (WEB3)", "DONATIONS & CERTIFICATE", "AIRLINE LOGISTICS", "LOCATION & MAPS"]
    },
    'connect': {'ES': 'Conectar', 'EN': 'Connect'},
    'active': {'ES': 'ACTIVO - EMITIENDO', 'EN': 'ACTIVE - BROADCASTING'},
    'live': {'ES': 'TRANSMISIÓN EN VIVO', 'EN': 'LIVE STREAM'},
    'download': {'ES': '?? DESCARGAR', 'EN': '?? DOWNLOAD'},
    'map_btn': {'ES': '??? ABRIR EN GOOGLE MAPS (GPS)', 'EN': '??? OPEN IN GOOGLE MAPS (GPS)'},
    'wallet_btn': {'ES': '?? CONECTAR METAMASK', 'EN': '?? CONNECT METAMASK'},
    'wallet_msg': {'ES': '?? Billetera Conectada: 0x71C...9A23', 'EN': '?? Wallet Connected: 0x71C...9A23'},
    
    # SECCIÓN IDENTIDAD
    'who_title': {'ES': '¿QUIÉNES SOMOS?', 'EN': 'WHO WE ARE'}, 
    'who_text': {
        'ES': 'Serenity Nexus Global es la primera plataforma **Phygital (Física + Digital)** del Valle del Cauca que integra la conservación ambiental del KBA Bosque San Antonio con tecnología Blockchain e Inteligencia Artificial. Somos guardianes de 87 hectáreas de vida, uniendo a la comunidad local con la inversión global mediante la transparencia tecnológica.',
        'EN': 'Serenity Nexus Global is the first **Phygital (Physical + Digital)** platform in Valle del Cauca integrating conservation of the KBA San Antonio Forest with Blockchain and AI technology. We are guardians of 87 hectares of life, bridging the local community with global investment through technological transparency.'
    },
    'mis_title': {'ES': 'NUESTRA MISIÓN' , 'EN': 'OUR MISSION'},
    'mis_text': {
        'ES': 'Regenerar el tejido ecológico y social mediante un modelo de negocio sostenible que garantice la protección perpetua del bosque y el bienestar económico de Dagua, utilizando la tecnología como puente de confianza.',
        'EN': 'Regenerate the ecological and social fabric through a sustainable business model ensuring perpetual forest protection and economic welfare for Dagua, using technology as a bridge of trust.'
    },
    'vis_title': {'ES': ' NUESTRA VISIÓN ', 'EN': 'OUR VISION'},
    'vis_text': {
        'ES': 'Para 2030, ser el referente mundial del "Internet de la Naturaleza", tokenizando activos ambientales reales para crear el banco de oxígeno más seguro y tecnológicamente avanzado del planeta.',
        'EN': 'By 2030, to be the global benchmark for the "Internet of Nature," tokenizing real environmental assets to create the most secure and technologically advanced oxygen bank on the planet.'
    }
}
def t(key): return tr[key][st.session_state.lang]

# --- FUNCIÓN CÁMARA REAL ---
def mostrar_camara_real(url_rstp):
    """Intenta conectar cámara real, si falla avisa."""
    if cv2 is None:
        st.error("?? Módulo de video no detectado en nube. Use la opción DEMO.")
        return
    
    st.info(f"?? Conectando a IP: {url_rstp}")
    try:
        cap = cv2.VideoCapture(url_rstp)
        frame_placeholder = st.empty()
        stop_button = st.button("? DETENER / STOP")
        while cap.isOpened() and not stop_button:
            ret, frame = cap.read()
            if not ret:
                st.warning("?? Sin señal. Para demostraciones en la nube use el botón 'VER DEMO'.")
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame, channels="RGB", use_column_width=True)
        cap.release()
    except Exception as e:
        st.error(f"Error técnico: {e}")

# --- FUNCIÓN PDF: CERTIFICADO DONANTE ---
def generar_pdf_certificado(nombre, monto, lang):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    txt_titulo = "CERTIFICADO DE DONACIÓN" if lang == 'ES' else "DONATION CERTIFICATE"
    
    c.setStrokeColor(VERDE_SERENITY); c.setLineWidth(5)
    c.rect(0.3*inch, 0.3*inch, 7.9*inch, 10.4*inch)
    try:
        if os.path.exists("logo_serenity.png"): c.drawImage("logo_serenity.png", 3.5*inch, 9.0*inch, width=1.5*inch, height=1.5*inch, mask='auto')
        else: c.setFillColor(VERDE_SERENITY); c.circle(4.25*inch, 9.7*inch, 40, fill=1)
    except: pass 
    
    c.setFont("Helvetica-Bold", 30); c.setFillColor(VERDE_SERENITY); c.drawCentredString(4.25*inch, 8.5*inch, txt_titulo)
    c.setFont("Helvetica", 14); c.setFillColor(black)
    c.drawCentredString(4.25*inch, 7.5*inch, "SERENITY HUB S.A.S. BIC")
    c.drawCentredString(4.25*inch, 7.0*inch, f"Reconoce a / Recognizes: {nombre.upper()}")
    c.drawCentredString(4.25*inch, 6.5*inch, f"Aporte / Contribution: ${monto:,.0f} USD")
    c.drawCentredString(4.25*inch, 6.0*inch, "Destinado a la Regeneración del Bosque San Antonio")
    c.setLineWidth(1); c.line(2.5*inch, 4.8*inch, 6.0*inch, 4.8*inch); c.drawCentredString(4.25*inch, 4.6*inch, "Jorge Carvajal - Admin")
    c.save(); buffer.seek(0); return buffer

# --- FUNCIÓN PDF: CERTIFICADO EMPRESA ---
def generar_cert_empresa(nit, logo_bytes, lang):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    titulo = "CERTIFICADO DE CUMPLIMIENTO" if lang == 'ES' else "COMPLIANCE CERTIFICATE"
    subtitulo = "LEY 2173 DE 2021 (ÁREAS DE VIDA)" if lang == 'ES' else "LAW 2173 OF 2021 (AREAS OF LIFE)"
    txt_nit = f"NIT / TAX ID: {nit}"
    cuerpo = "Por medio de la presente, SERENITY NEXUS GLOBAL certifica que la empresa:" if lang == 'ES' else "SERENITY NEXUS GLOBAL hereby certifies that the company:"
    cuerpo2 = "Ha cumplido con la compensación ambiental mediante la siembra y mantenimiento." if lang == 'ES' else "Has complied with environmental compensation through tree planting and maintenance."
    
    hash_input = f"{nit}{datetime.now()}SERENITY".encode()
    hash_code = hashlib.sha256(hash_input).hexdigest().upper()
    
    c.setStrokeColor(HexColor("#D4AF37")); c.setLineWidth(4)
    c.rect(0.5*inch, 0.5*inch, 7.5*inch, 10.0*inch)
    
    try:
        if os.path.exists("logo_serenity.png"): c.drawImage("logo_serenity.png", 3.75*inch, 9.5*inch, width=1.0*inch, height=1.0*inch, mask='auto')
        else: c.setFillColor(VERDE_SERENITY); c.circle(4.25*inch, 10*inch, 20, fill=1)
    except: pass

    c.setFont("Helvetica-Bold", 24); c.setFillColor(VERDE_SERENITY); c.drawCentredString(4.25*inch, 9.0*inch, titulo)
    c.setFont("Helvetica-Bold", 14); c.setFillColor(black); c.drawCentredString(4.25*inch, 8.7*inch, subtitulo)
    
    if logo_bytes is not None:
        try:
            logo_img = ImageReader(logo_bytes)
            c.drawImage(logo_img, 3.25*inch, 6.5*inch, width=2.0*inch, height=2.0*inch, preserveAspectRatio=True, mask='auto')
        except: c.drawCentredString(4.25*inch, 7.5*inch, "[LOGO EMPRESA]")
            
    c.setFont("Helvetica", 12); c.drawCentredString(4.25*inch, 6.0*inch, cuerpo)
    c.setFont("Helvetica-Bold", 18); c.drawCentredString(4.25*inch, 5.5*inch, txt_nit)
    c.setFont("Helvetica", 12); c.drawCentredString(4.25*inch, 5.0*inch, cuerpo2)
    
    c.setFont("Courier", 9); c.setFillColor(black); c.drawCentredString(4.25*inch, 3.5*inch, "BLOCKCHAIN VERIFICATION HASH:")
    c.setFont("Courier-Bold", 10); c.drawCentredString(4.25*inch, 3.3*inch, hash_code)
    
    c.setLineWidth(1); c.line(1.5*inch, 2.0*inch, 3.5*inch, 2.0*inch); c.line(5.0*inch, 2.0*inch, 7.0*inch, 2.0*inch)
    c.setFont("Helvetica", 8); c.drawString(1.8*inch, 1.8*inch, "Jorge Carvajal - CEO"); c.drawString(5.3*inch, 1.8*inch, "Sistema Nexus IA")
    c.save(); buffer.seek(0); return buffer

# --- CSS ---
st.markdown("""
    <style>
        .stApp { background-image: linear-gradient(rgba(5, 10, 4, 0.8), rgba(5, 10, 4, 0.9)), url('https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1920&q=80'); background-size: cover; background-position: center; background-attachment: fixed; color: #e8f5e9; font-family: 'Montserrat', sans-serif; }
        label, .stMarkdown p, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, .stMetricLabel { color: white !important; font-weight: 500; }
        [data-testid="stSidebar"] { background-color: rgba(10, 20, 8, 0.9) !important; backdrop-filter: blur(10px); }
        h1, h2, h3 { color: #9BC63B !important; text-shadow: 2px 2px 4px #000; }
        .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #9BC63B; border-radius: 8px; width: 100%; font-weight: bold; }
        .stButton>button:hover { background-color: #9BC63B; color: black; box-shadow: 0 0 15px #9BC63B; }
        .faro-card, .metric-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; }
        .faro-gemini { border: 2px solid #4285F4; padding: 15px; border-radius: 10px; background: rgba(66, 133, 244, 0.2); text-align: center; box-shadow: 0 0 15px #4285F4; }
        .cam-grid { background: #000; border: 1px solid #2E7D32; height: 80px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #ff0000; border-radius: 5px; }
        .trust-section { background-color: rgba(245, 245, 245, 0.95); color: #1a1a1a !important; padding: 25px; border-radius: 15px; border-left: 6px solid #2E7D32; margin-bottom: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .trust-section h3, .trust-section h4 { color: #2E7D32 !important; text-shadow: none !important; margin-bottom: 10px; }
        .trust-section p { color: #333 !important; font-weight: 500; font-size: 1rem; line-height: 1.5; }
        .airline-grid { background: rgba(255, 255, 255, 0.9); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px; height: 110px; display: flex; align-items: center; justify-content: center; flex-direction: column; border: 1px solid #ccc; transition: transform 0.2s; cursor: pointer; }
        .airline-grid:hover { transform: scale(1.05); border: 2px solid #2E7D32; }
        .airline-grid p { color: #333 !important; }
        .legal-card { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 10px; }
        .wallet-msg-box { background-color: rgba(30, 30, 30, 0.8); border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; color: #D4AF37; font-weight: bold; text-align: center; margin-top: 10px; }
        .nft-card { background: linear-gradient(135deg, #101010, #202020); border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px; color: white; }
        a { text-decoration: none; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN ---
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top: 50px;'><h1>SISTEMA NEXUS | SERENITY</h1></div>", unsafe_allow_html=True)
    col_sec = st.columns([1,1,1])
    with col_sec[1]:
        clave = st.text_input("PASSWORD ADMIN", type="password")
        if st.button("INGRESAR"):
            if clave == "Serenity2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Flag_of_Colombia.svg/320px-Flag_of_Colombia.svg.png", width=30)
    toggle_lang = st.toggle("???? ENGLISH MODE", value=False)
    st.session_state.lang = 'EN' if toggle_lang else 'ES'
    st.divider()
    menu_opts = tr['menu_opts'][st.session_state.lang]
    menu_sel = st.radio("MENÚ / MENU", menu_opts)

# --- CAMBIO 1: LOGO CENTRADO EN EL INICIO ---
if menu_sel == menu_opts[0]:
    # Definimos tres columnas para centrar la imagen en la del medio
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        # Intenta cargar el logo si el archivo existe en el repositorio
        if os.path.exists("logo_serenity.png"):
            st.image("logo_serenity.png", use_container_width=True)
        else:
            # Si no está el archivo, pone un banner elegante con el nombre
            st.markdown("""
                <div style='text-align:center; border:3px solid #9BC63B; padding:20px; border-radius:20px; background:rgba(46, 125, 50, 0.1);'>
                    <h1 style='color:#9BC63B; margin:0;'>SERENITY NEXUS GLOBAL</h1>
                    <p style='color:white; margin:0; font-weight:bold;'>PROYECTO REGENERATIVO</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Título principal de la plataforma
    st.markdown("<h1 style='text-align:center; font-size:4rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    
    # Subtítulo bilingüe
    subt = "SISTEMA REGENERATIVO BIOMÉTRICO KBA" if st.session_state.lang == 'ES' else "KBA BIOMETRIC REGENERATIVE SYSTEM"
    st.markdown(f"<p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold;'>{subt}</p>", unsafe_allow_html=True)
    btn_audio = "?? ACTIVAR SONIDO GLOBAL EARTH" if st.session_state.lang == 'ES' else "?? ACTIVATE GLOBAL EARTH SOUND"
    st.components.v1.html(f"""<audio id="audio_earth" src="sonido_Earth.mp3" loop></audio><div style="text-align:center; margin-top:30px;"><button onclick="document.getElementById('audio_earth').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:20px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:16px;">{btn_audio}</button></div>""", height=150)
    st.write("")
    
# --- CAMBIO 3: LIMPIEZA DE MISION Y VISION (SIN SIGNOS) ---
    st.markdown(f"""
        <div class="trust-section">
            <h3 style="text-align:center;">{t('who_title')}</h3>
            <p style="text-align:center;">{t('who_text')}</p>
            <hr style="border-top: 1px solid #ccc;">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-around;">
                <div style="flex: 1; min-width: 300px; padding: 10px;">
                    <h4>🌿 {t('mis_title')}</h4>
                    <p>{t('mis_text')}</p>
                </div>
                <div style="flex: 1; min-width: 300px; padding: 10px;">
                    <h4>🚀 {t('vis_title')}</h4>
                    <p>{t('vis_text')}</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.info("Finca Villa Michell SPAM (40%) | Hacienda Monte Guadua TAF (60%) | Admin: Jorge Carvajal")

# 2. RED DE FAROS (CON DEMO Y REAL)
elif menu_sel == menu_opts[1]:
    tt = "??? Monitoreo Perimetral" if st.session_state.lang == 'ES' else "??? Perimeter Monitoring"
    st.title(tt)
    lbl_conn = t('connect')
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.markdown("<div class='faro-card'><h3>FARO HALCÓN</h3></div>", unsafe_allow_html=True)
        if st.button(f"{lbl_conn} Halcón"): st.session_state.f_activo = "Halcón"
    with c2: 
        st.markdown("<div class='faro-card'><h3>FARO COLIBRÍ</h3></div>", unsafe_allow_html=True)
        if st.button(f"{lbl_conn} Colibrí"): st.session_state.f_activo = "Colibrí"
    with c3: 
        st.markdown("<div class='faro-card'><h3>FARO RANA</h3></div>", unsafe_allow_html=True)
        if st.button(f"{lbl_conn} Rana"): st.session_state.f_activo = "Rana"
    st.write("")
    c4, c5, c6 = st.columns(3)
    with c4: 
        st.markdown("<div class='faro-card'><h3>FARO VENADO</h3></div>", unsafe_allow_html=True)
        if st.button(f"{lbl_conn} Venado"): st.session_state.f_activo = "Venado"
    with c5: 
        st.markdown("<div class='faro-card'><h3>FARO TIGRILLO</h3></div>", unsafe_allow_html=True)
        if st.button(f"{lbl_conn} Tigrillo"): st.session_state.f_activo = "Tigrillo"
    with c6: 
        st.markdown("<div class='faro-card'><h3>FARO CAPIBARA</h3></div>", unsafe_allow_html=True)
        if st.button(f"{lbl_conn} Capibara"): st.session_state.f_activo = "Capibara"
    st.write("---")
    
    # SECCIÓN GEMINI CÁMARA
    col_gemini = st.columns([1,2,1])
    with col_gemini[1]:
        st_st = "Estado" if st.session_state.lang == 'ES' else "Status"
        st.markdown(f"<div class='faro-gemini'><h3>? FARO GEMINI (VTA OVO II) ?</h3><p>{st_st}: {st.session_state.estado_gemini}</p></div>", unsafe_allow_html=True)
        
        # OPCIONES DE CÁMARA
        opcion_cam = st.radio("Fuente de Video / Video Source:", ["SIMULACIÓN (DEMO NUBE)", "CÁMARA REAL (IP LOCAL)"])
        
        if opcion_cam == "SIMULACIÓN (DEMO NUBE)":
            if st.button("?? VER DEMOSTRACIÓN (VIDEO)"):
                st.session_state.f_activo = "GEMINI-DEMO"
                st.session_state.estado_gemini = t('active')
        else:
            url_camara = st.text_input("Enlace RTSP:", value="rtsp://admin:admin123@192.168.111.178:554/live/ch0")
            if st.button("ACTIVAR CÁMARA REAL"):
                st.session_state.f_activo = "GEMINI"
                st.session_state.estado_gemini = t('active')
                mostrar_camara_real(url_camara)

    # MOSTRAR EL VIDEO DEMO
    if st.session_state.f_activo == "GEMINI-DEMO":
        st.divider()
        st.markdown("<h3 style='text-align:center; color:#4285F4;'>?? TRANSMISIÓN SIMULADA (ALTA DEFINICIÓN)</h3>", unsafe_allow_html=True)
        # Video de naturaleza confiable
        st.video("https://storage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4", start_time=15)

    # MOSTRAR CÁMARAS ESTÁTICAS (SI NO ES VIDEO)
    if st.session_state.f_activo and st.session_state.f_activo not in ["GEMINI", "GEMINI-DEMO"]:
        st.divider(); live_t = t('live'); color_titulo = "#9BC63B"
        st.markdown(f"<h2 style='color:{color_titulo}; text-align:center;'>?? {live_t}: {st.session_state.f_activo.upper()}</h2>", unsafe_allow_html=True)
        c_cols = st.columns(4)
        for j in range(8):
            label = "LIVE"
            with c_cols[j % 4]: st.markdown(f"<div class='cam-grid'>CAM {j+1}<br>? {label}</div>", unsafe_allow_html=True)
            
    # --- SECCIÓN BIOACÚSTICA (MICRÓFONOS) RESTAURADA ---
    if st.session_state.f_activo:
        st.write("")
        st.subheader("Bioacústica" if st.session_state.lang == 'ES' else "Bioacoustics")
        m_cols = st.columns(4)
        for k in range(4):
            val = random.randint(85,99) if "GEMINI" in str(st.session_state.f_activo) else random.randint(40,90)
            with m_cols[k]: 
                st.markdown(f"<div style='background:rgba(155,198,59,0.2); border:1px solid #2E7D32; padding:10px; border-radius:5px; text-align:center;'><b>MIC {k+1}</b><br><span style='color:#9BC63B;'>||||| {val}%</span></div>", unsafe_allow_html=True)

# 3. DASHBOARD
elif menu_sel == menu_opts[2]:
    tt = "?? Análisis de Inteligencia Biológica" if st.session_state.lang == 'ES' else "?? Biological Intelligence Analysis"
    st.title(tt)
    l_esp = "Especies" if st.session_state.lang == 'ES' else "Species"
    l_hec = "Hectáreas" if st.session_state.lang == 'ES' else "Hectares"
    l_inv = "Inversiones" if st.session_state.lang == 'ES' else "Investments"
    l_sal = "Salud" if st.session_state.lang == 'ES' else "Health"
    m = st.columns(4)
    m[0].markdown(f"<div class='metric-card'><h3>{l_esp}</h3><h1>1,248</h1></div>", unsafe_allow_html=True)
    m[1].markdown(f"<div class='metric-card'><h3>{l_hec}</h3><h1>{st.session_state.total_protegido}</h1></div>", unsafe_allow_html=True)
    m[2].markdown(f"<div class='metric-card'><h3>{l_inv}</h3><h1>{st.session_state.donaciones_recibidas}</h1></div>", unsafe_allow_html=True)
    m[3].markdown(f"<div class='metric-card'><h3>{l_sal}</h3><h1>98%</h1></div>", unsafe_allow_html=True)
    st.bar_chart(pd.DataFrame({'Data': [120, 450, 300, 80, 45, 110, 950]}, index=["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara", "GEMINI"]))

# 4. LEY 2173
elif menu_sel == menu_opts[3]:
    tt = "?? Cumplimiento Ley 2173" if st.session_state.lang == 'ES' else "?? Law 2173 Compliance"
    st.title(tt)
    with st.container(border=True):
        st.subheader("?? Gestión Operativa" if st.session_state.lang == 'ES' else "?? Operational Management")
        c1, c2 = st.columns(2)
        with c1: nit = st.text_input("Ingrese NIT" if st.session_state.lang == 'ES' else "Enter Tax ID (NIT)")
        with c2: logo_emp = st.file_uploader("Logo Empresa / Company Logo", type=["png", "jpg", "jpeg"])
        if nit and logo_emp:
            st.info("? Datos recibidos. Generando certificado encriptado..." if st.session_state.lang == 'ES' else "? Data received. Generating encrypted certificate...")
            if st.button("GENERAR CERTIFICADO OFICIAL"):
                st.session_state.pdf_empresa_buffer = generar_cert_empresa(nit, logo_emp, st.session_state.lang)
                st.success("Certificado generado exitosamente.")
            if st.session_state.pdf_empresa_buffer:
                 btn_d = t('download') + (" CERTIFICADO" if st.session_state.lang == 'ES' else " CERTIFICATE")
                 st.download_button(btn_d, data=st.session_state.pdf_empresa_buffer, file_name=f"Certificado_Ley2173_{nit}.pdf", mime="application/pdf")
    st.write("---")
    st.subheader("?? Blindaje Jurídico" if st.session_state.lang == 'ES' else "?? Legal Framework")
    col_law1, col_law2 = st.columns(2)
    with col_law1:
        st.markdown("<div class='legal-card'><h4>Ley 2173 de 2021</h4><p>Áreas de Vida.</p></div>", unsafe_allow_html=True)
        st.download_button("?? Descargar Resumen Ley 2173", data=TEXTO_LEY_2173, file_name="Resumen_Ley_2173.txt")
        st.markdown("<div class='legal-card'><h4>CONPES 3934</h4><p>Crecimiento Verde.</p></div>", unsafe_allow_html=True)
        st.download_button("?? Descargar Resumen CONPES 3934", data=TEXTO_CONPES, file_name="Resumen_CONPES_3934.txt")
    with col_law2:
        st.markdown("<div class='legal-card'><h4>Ley 2111 de 2021</h4><p>Delitos Ambientales.</p></div>", unsafe_allow_html=True)
        st.download_button("?? Descargar Resumen Ley 2111", data=TEXTO_DELITOS, file_name="Resumen_Ley_2111.txt")
        st.markdown("<div class='legal-card'><h4>Beneficios Tributarios</h4><p>S.A.S. BIC.</p></div>", unsafe_allow_html=True)
        st.download_button("?? Descargar Guía Tributaria", data=TEXTO_TRIBUTARIO, file_name="Guia_Tributaria_Serenity.txt")

# 5. SUSCRIPCIONES
elif menu_sel == menu_opts[4]:
    st.title("?? Planes" if st.session_state.lang == 'ES' else "?? Plans")
    p1, p2, p3 = st.columns(3)
    nm = ["Plan Semilla", "Plan Guardián", "Plan Halcón"] if st.session_state.lang == 'ES' else ["Seed Plan", "Guardian Plan", "Hawk Plan"]
    per = ["1 Faro / 1 Mes", "6 Faros / 1 Mes", "6 Faros / 6 Meses"] if st.session_state.lang == 'ES' else ["1 Beacon / 1 Month", "6 Beacons / 1 Month", "6 Beacons / 6 Months"]
    btn_s = "SUSCRIBIRSE" if st.session_state.lang == 'ES' else "SUBSCRIBE"
    with p1: 
        st.markdown(f"<div class='faro-card'><h3>{nm[0]}</h3><h2>$5 USD</h2><p>{per[0]}</p></div>", unsafe_allow_html=True)
        if st.button(f"{btn_s} {nm[0]}"): st.success("OK...")
    with p2: 
        st.markdown(f"<div class='faro-card'><h3>{nm[1]}</h3><h2>$25 USD</h2><p>{per[1]}</p></div>", unsafe_allow_html=True)
        if st.button(f"{btn_s} {nm[1]}"): st.success("OK...")
    with p3: 
        st.markdown(f"<div class='faro-card' style='border-color:#D4AF37;'><h3>{nm[2]}</h3><h2>$200 USD</h2><p>{per[2]}</p></div>", unsafe_allow_html=True)
        if st.button(f"{btn_s} {nm[2]}"): st.success("OK...")

# 6. BILLETERA CRYPTO
elif menu_sel == menu_opts[5]:
    st.title("?? Web3 Green Wallet")
    col_w1, col_w2 = st.columns([1, 2])
    with col_w1:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        if not st.session_state.wallet_connected:
            st.image("https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg", width=100)
            if st.button(t('wallet_btn')): st.session_state.wallet_connected = True; st.rerun()
        else:
            st.markdown(f"<div class='wallet-msg-box'>{t('wallet_msg')}</div>", unsafe_allow_html=True)
            st.write(""); st.metric(label="SERENITY TOKEN ($SNG)", value="1,450.00", delta="+12%")
            st.metric(label="CARBON CREDITS", value="45 Tons", delta="+2")
            if st.button("DISCONNECT"): st.session_state.wallet_connected = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col_w2:
        if st.session_state.wallet_connected:
            st.subheader("Your Green Assets (NFTs)")
            c_nft1, c_nft2, c_nft3 = st.columns(3)
            with c_nft1: st.markdown("<div class='nft-card'>??<br><b>Tree #1024</b><br>Guayacán<br><i style='color:#4CAF50;'>Healthy</i></div>", unsafe_allow_html=True)
            with c_nft2: st.markdown("<div class='nft-card'>??<br><b>Tree #1025</b><br>Saman<br><i style='color:#4CAF50;'>Healthy</i></div>", unsafe_allow_html=True)
            with c_nft3: st.markdown("<div class='nft-card'>??<br><b>Land Plot A4</b><br>Monte Guadua<br><i style='color:#FFD700;'>Protected</i></div>", unsafe_allow_html=True)
            st.line_chart(pd.DataFrame({'Price': [1.2, 1.3, 1.25, 1.4, 1.45, 1.6, 1.8]}, index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]))
        else:
            msg_conn = "Conecta tu billetera para ver tus activos." if st.session_state.lang == 'ES' else "Connect wallet to view assets."
            st.markdown(f"<div style='background:rgba(255,255,255,0.1); padding:15px; border-radius:10px; text-align:center;'>?? {msg_conn}</div>", unsafe_allow_html=True)

# 7. DONACIONES
elif menu_sel == menu_opts[6]:
    tt = "?? Generador de Diploma Oficial" if st.session_state.lang == 'ES' else "?? Official Diploma Generator"
    st.title(tt)
    colA, colB = st.columns([1, 1])
    with colA:
        with st.container(border=True):
            l_n = "Nombre Completo" if st.session_state.lang == 'ES' else "Full Name"
            l_m = "Monto Donación (USD)" if st.session_state.lang == 'ES' else "Donation Amount (USD)"
            l_b = "? PROCESAR DONACIÓN" if st.session_state.lang == 'ES' else "? PROCESS DONATION"
            nombre_d = st.text_input(l_n)
            monto_d = st.number_input(l_m, min_value=1)
            if st.button(l_b): 
                if nombre_d:
                    st.session_state.donaciones_recibidas += 1
                    st.session_state.estado_gemini = t('active')
                    st.session_state.pdf_buffer = generar_pdf_certificado(nombre_d, monto_d, st.session_state.lang)
                    st.balloons(); st.success("OK!")
                else: st.warning("Name required")
    with colB:
        if 'pdf_buffer' in st.session_state:
            prev = "VISTA PREVIA" if st.session_state.lang == 'ES' else "PREVIEW"
            st.markdown(f"""<div style="background:white; color:black; padding:20px; text-align:center; border:5px double #2E7D32;"><h3 style="color:#2E7D32;">{prev}</h3><h1>{nombre_d.upper()}</h1><p>${monto_d}</p></div>""", unsafe_allow_html=True)
            dl = t('download') + " PDF"
            st.download_button(dl, data=st.session_state.pdf_buffer, file_name=f"Diploma_Serenity_{nombre_d}.pdf", mime="application/pdf")

# 8. LOGÍSTICA
elif menu_sel == menu_opts[7]:
    tt = "?? Conectividad Global a Colombia" if st.session_state.lang == 'ES' else "?? Global Connectivity to Colombia"
    subt = "Haga clic en una aerolínea para reservar." if st.session_state.lang == 'ES' else "Click on an airline to book."
    st.title(tt); st.markdown(subt)
    st.subheader("???? Europa")
    e1, e2, e3, e4 = st.columns(4)
    with e1: st.markdown("<a href='https://www.iberia.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/iberia.com'><p>IBERIA</p></div></a>", unsafe_allow_html=True)
    with e2: st.markdown("<a href='https://www.lufthansa.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/lufthansa.com'><p>LUFTHANSA</p></div></a>", unsafe_allow_html=True)
    with e3: st.markdown("<a href='https://www.airfrance.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/airfrance.com'><p>AIR FRANCE</p></div></a>", unsafe_allow_html=True)
    with e4: st.markdown("<a href='https://www.turkishairlines.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/turkishairlines.com'><p>TURKISH</p></div></a>", unsafe_allow_html=True)
    e5, e6, e7 = st.columns(3)
    with e5: st.markdown("<a href='https://www.klm.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/klm.com'><p>KLM</p></div></a>", unsafe_allow_html=True)
    with e6: st.markdown("<a href='https://www.aireuropa.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/aireuropa.com'><p>AIR EUROPA</p></div></a>", unsafe_allow_html=True)
    with e7: st.markdown("<a href='https://www.flyedelweiss.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/flyedelweiss.com'><p>EDELWEISS</p></div></a>", unsafe_allow_html=True)
    st.subheader("???? Norteamérica")
    n1, n2, n3, n4 = st.columns(4)
    with n1: st.markdown("<a href='https://www.aa.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/aa.com'><p>AMERICAN</p></div></a>", unsafe_allow_html=True)
    with n2: st.markdown("<a href='https://www.united.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/united.com'><p>UNITED</p></div></a>", unsafe_allow_html=True)
    with n3: st.markdown("<a href='https://www.delta.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/delta.com'><p>DELTA</p></div></a>", unsafe_allow_html=True)
    with n4: st.markdown("<a href='https://www.aircanada.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/aircanada.com'><p>AIR CANADA</p></div></a>", unsafe_allow_html=True)
    st.subheader("?? Latinoamérica")
    l1, l2, l3, l4 = st.columns(4)
    with l1: st.markdown("<a href='https://www.avianca.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/avianca.com'><p>AVIANCA</p></div></a>", unsafe_allow_html=True)
    with l2: st.markdown("<a href='https://www.latamairlines.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/latamairlines.com'><p>LATAM</p></div></a>", unsafe_allow_html=True)
    with l3: st.markdown("<a href='https://www.copaair.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/copaair.com'><p>COPA</p></div></a>", unsafe_allow_html=True)
    with l4: st.markdown("<a href='https://www.aeromexico.com' target='_blank'><div class='airline-grid'><img src='https://logo.clearbit.com/aeromexico.com'><p>AEROMEXICO</p></div></a>", unsafe_allow_html=True)

# 9. MAPAS (REALES)
elif menu_sel == menu_opts[8]:
    tt = "?? Ubicación Serenity (Dagua)" if st.session_state.lang == 'ES' else "?? Serenity Location (Dagua)"
    st.title(tt)
    lat_villa = 3.465028; lon_villa = -76.634778; lat_guadua = 3.477917; lon_guadua = -76.657361
    url_gmaps = f"https://www.google.com/maps/search/?api=1&query={lat_villa},{lon_villa}"
    btn_text = t('map_btn')
    st.markdown(f"""<div style='text-align:center; margin-bottom: 20px;'><a href="{url_gmaps}" target="_blank"><button style="background-color:#4285F4; color:white; border:2px solid white; padding:15px 32px; text-align:center; text-decoration:none; display:inline-block; font-size:18px; margin:4px 2px; cursor:pointer; border-radius:12px; font-weight:bold; box-shadow: 0 0 10px #4285F4;">{btn_text}</button></a></div>""", unsafe_allow_html=True)
    color_gemini_map = "green" if st.session_state.estado_gemini == t('active') else "orange"
    m = folium.Map(location=[(lat_villa + lat_guadua)/2, (lon_villa + lon_guadua)/2], zoom_start=14, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri World Imagery')
    folium.Marker([lat_guadua + 0.001, lon_guadua - 0.001], popup=f"FARO GEMINI", icon=folium.Icon(color=color_gemini_map, icon='bolt', prefix='fa')).add_to(m)
    offset = 0.004
    folium.Polygon(locations=[[lat_guadua - offset, lon_guadua - offset], [lat_guadua + offset, lon_guadua - offset], [lat_guadua + offset, lon_guadua + offset], [lat_guadua - offset, lon_guadua + offset]], color="#9BC63B", fill=True, fill_opacity=0.3, tooltip="Hacienda Monte Guadua: 80 Ha").add_to(m)
    folium.CircleMarker(location=[lat_villa, lon_villa], radius=10, color="blue", fill=True, fill_color="blue", tooltip="Finca Villa Michelle (Sede)").add_to(m)
    st_folium(m, width="100%", height=600)

















































































