# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
import hashlib
from datetime import datetime
import io
import os
import time

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
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌿", layout="wide")
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
if 'registro_plan' not in st.session_state: st.session_state.registro_plan = None

# --- DICCIONARIO TRADUCCION ---
tr = {
    'menu_opts': {
        'ES': ["INICIO", "RED DE FAROS (7 NODOS)", "DASHBOARD ESTADISTICO IA", "GESTION LEY 2173 (EMPRESAS)", "SUSCRIPCIONES", "BILLETERA CRYPTO (WEB3)", "DONACIONES Y CERTIFICADO", "LOGISTICA AEROLINEAS", "UBICACION & MAPAS"],
        'EN': ["HOME", "BEACON NETWORK (7 NODES)", "AI STATS DASHBOARD", "LAW 2173 MANAGEMENT (CORP)", "SUBSCRIPTIONS", "CRYPTO WALLET (WEB3)", "DONATIONS & CERTIFICATE", "AIRLINE LOGISTICS", "LOCATION & MAPS"]
    },
    'connect': {'ES': 'Conectar', 'EN': 'Connect'},
    'active': {'ES': 'ACTIVO - EMITIENDO', 'EN': 'ACTIVE - BROADCASTING'},
    'live': {'ES': 'TRANSMISION EN VIVO', 'EN': 'LIVE STREAM'},
    'who_title': {'ES': 'QUIENES SOMOS', 'EN': 'WHO WE ARE'},
    'who_text': {
        'ES': 'Serenity Nexus Global es la primera plataforma Phygital del Valle del Cauca.',
        'EN': 'Serenity Nexus Global is the first Phygital platform in Valle del Cauca.'
    },
    'mis_title': {'ES': 'NUESTRA MISION', 'EN': 'OUR MISSION'},
    'mis_text': {
        'ES': 'Regenerar el tejido ecologico y social mediante tecnologia.',
        'EN': 'Regenerate the ecological and social fabric through technology.'
    },
    'vis_title': {'ES': 'NUESTRA VISION', 'EN': 'OUR VISION'},
    'vis_text': {
        'ES': 'Ser el referente mundial del Internet de la Naturaleza para 2030.',
        'EN': 'To be the global benchmark for the Internet of Nature by 2030.'
    },
    'map_btn': {'ES': 'ABRIR EN GOOGLE MAPS', 'EN': 'OPEN IN GOOGLE MAPS'},
    'download': {'ES': 'DESCARGAR', 'EN': 'DOWNLOAD'}
}

def t(key):
    lang = st.session_state.get('lang', 'ES')
    return tr.get(key, {}).get(lang, key)

# --- FUNCIONES PDF ---
def generar_pdf_analisis_ia(lang):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    hash_id = hashlib.sha256(f"Serenity-{fecha}".encode()).hexdigest()[:12].upper()
    c.setStrokeColor(VERDE_SERENITY); c.setLineWidth(3); c.rect(0.5*inch, 0.5*inch, 7.5*inch, 10.0*inch)
    c.setFont("Helvetica-Bold", 20); c.drawCentredString(4.25*inch, 9.0*inch, "REPORTE IA SERENITY")
    c.setFont("Helvetica", 12); c.drawString(1*inch, 8*inch, f"Fecha: {fecha}"); c.drawString(1*inch, 7.7*inch, f"HASH: {hash_id}")
    c.save(); buffer.seek(0); return buffer

def generar_cert_empresa(nit, logo_bytes, lang):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setStrokeColor(VERDE_SERENITY); c.setLineWidth(5); c.rect(0.5*inch, 0.5*inch, 7.5*inch, 10.0*inch)
    c.setFont("Helvetica-Bold", 22); c.drawCentredString(4.25*inch, 9*inch, "CERTIFICADO LEY 2173")
    c.setFont("Helvetica", 14); c.drawCentredString(4.25*inch, 8*inch, f"NIT: {nit}")
    c.save(); buffer.seek(0); return buffer

def generar_pdf_certificado(nombre, monto, lang):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setStrokeColor(VERDE_SERENITY); c.rect(0.5*inch, 0.5*inch, 7.5*inch, 10.0*inch)
    c.drawCentredString(4.25*inch, 8*inch, f"GRACIAS {nombre.upper()} POR TU APORTE DE ${monto}")
    c.save(); buffer.seek(0); return buffer

# --- ESTILOS CSS ---
st.markdown("<style>.stApp { background-color: #050a04; color: white; }</style>", unsafe_allow_html=True)

# --- LOGIN ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>SISTEMA NEXUS | SERENITY</h1>", unsafe_allow_html=True)
    clave = st.text_input("PASSWORD ADMIN", type="password")
    if st.button("INGRESAR"):
        if clave == "Serenity2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- SIDEBAR Y NAVEGACIÓN ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Flag_of_Colombia.svg/320px-Flag_of_Colombia.svg.png", width=30)
    toggle_lang = st.toggle(" ENGLISH MODE", value=False)
    st.session_state.lang = 'EN' if toggle_lang else 'ES'
    opciones_menu = tr['menu_opts'][st.session_state.lang]
    menu_sel = st.radio("MENÚ / MENU", opciones_menu)

# =========================================================
# LÓGICA DE CONTENIDO CENTRAL
# =========================================================

# --- 0. INICIO ---
if menu_sel == opciones_menu[0]:
    st.markdown("<h1 style='text-align:center;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: st.subheader(t('who_title')); st.write(t('who_text'))
    with col2: st.subheader(t('mis_title')); st.write(t('mis_text'))
    with col3: st.subheader(t('vis_title')); st.write(t('vis_text'))
    st.info("Finca Villa Michell (40%) | Hacienda Monte Guadua (60%) | Admin: Jorge Carvajal")

# --- 1. RED DE FAROS ---
elif menu_sel == opciones_menu[1]:
    st.title("📡 Monitoreo de Faros")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🔌 Conectar Halcón"): st.session_state.f_activo = "Halcón"
    with c2: 
        if st.button("🔌 Conectar Colibrí"): st.session_state.f_activo = "Colibrí"
    with c3: 
        if st.button("📽️ VER DEMO GEMINI"): st.session_state.f_activo = "GEMINI-DEMO"

    if st.session_state.f_activo == "GEMINI-DEMO":
        st.video("https://www.youtube.com/watch?v=bUs9qYKF6mY")
    elif st.session_state.f_activo:
        st.success(f"Transmitiendo desde: {st.session_state.f_activo}")
        st.video("https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")

# --- 2. DASHBOARD IA (EL DASHBOARD VIVO) ---
elif menu_sel == opciones_menu[2]:
    st.title("📊 Análisis de Inteligencia Biológica")
    with st.status("🧬 Procesando señales en tiempo real...", expanded=True) as status:
        st.write("📡 Recibiendo telemetría de Dagua...")
        time.sleep(1)
        status.update(label="✅ Datos Sincronizados", state="complete")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🐾 Especies", "1,252", "+4")
    m2.metric("🌳 Hectáreas", "14.5 Ha", "0")
    m3.metric("🩺 Salud", "98.7%", "+0.2%")
    m4.metric("💰 $SNG", "0.085", "+0.002")

    if st.button("📥 DESCARGAR REPORTE PDF IA"):
        pdf = generar_pdf_analisis_ia(st.session_state.lang)
        st.download_button("Guardar Reporte", data=pdf, file_name="Analisis_Serenity.pdf")

# --- 3. GESTIÓN LEY 2173 ---
elif menu_sel == opciones_menu[3]:
    st.title("⚖️ Gestión Ley 2173")
    with st.container(border=True):
        nit = st.text_input("Ingrese NIT de Empresa")
        logo = st.file_uploader("Subir Logo", type=["png", "jpg"])
        if st.button("GENERAR CERTIFICADO LEY"):
            st.session_state.pdf_empresa_buffer = generar_cert_empresa(nit, logo, st.session_state.lang)
            st.success("Certificado Listo")
        if st.session_state.pdf_empresa_buffer:
            st.download_button("📥 DESCARGAR CERTIFICADO", data=st.session_state.pdf_empresa_buffer, file_name="Certificado_Ley2173.pdf")

# --- 4. SUSCRIPCIONES ---
elif menu_sel == opciones_menu[4]:
    st.title("🌱 Planes de Membresía")
    if not st.session_state.registro_plan:
        c1, c2, c3 = st.columns(3)
        with c1: 
            if st.button("ELEGIR SEMILLA"): st.session_state.registro_plan = "Semilla"; st.rerun()
        with c2: 
            if st.button("ELEGIR GUARDIAN"): st.session_state.registro_plan = "Guardian"; st.rerun()
        with c3: 
            if st.button("ELEGIR HALCON"): st.session_state.registro_plan = "Halcon"; st.rerun()
    else:
        with st.form("registro"):
            st.subheader(f"Registro: Plan {st.session_state.registro_plan}")
            tipo = st.selectbox("Tipo", ["Natural", "Juridica"])
            nom = st.text_input("Nombre / Empresa")
            pais = st.text_input("Pais")
            if st.form_submit_button("CONFIRMAR"):
                st.success("¡Bienvenido a Serenity!")
                if st.button("Volver"): st.session_state.registro_plan = None; st.rerun()

# --- 5. BILLETERA WEB3 ---
elif menu_sel == opciones_menu[5]:
    st.title("💳 Web3 Green Wallet")
    import base64
    try:
        with open("video_sng.mp4", "rb") as f:
            bin_str = base64.b64encode(f.read()).decode()
            st.markdown(f'<video width="100%" autoplay loop muted playsinline><source src="data:video/mp4;base64,{bin_str}" type="video/mp4"></video>', unsafe_allow_html=True)
    except: st.warning("Suba 'video_sng.mp4' a GitHub para ver el video sin fin.")
    if st.button("🔌 CONECTAR BILLETERA"): st.success("Conectado: 25,000 $SNG")

# --- 6. DONACIONES ---
elif menu_sel == opciones_menu[6]:
    st.title("🎁 Donaciones y Certificados")
    nom_d = st.text_input("Nombre Donante")
    mon_d = st.number_input("Monto (USD)", min_value=1)
    if st.button("PROCESAR"):
        st.session_state.pdf_buffer = generar_pdf_certificado(nom_d, mon_d, st.session_state.lang)
        st.success("Diploma Generado")
        st.download_button("📥 DESCARGAR DIPLOMA", data=st.session_state.pdf_buffer, file_name="Diploma_Serenity.pdf")

# --- 7. LOGISTICA AEROLINEAS ---
elif menu_sel == opciones_menu[7]:
    st.title("✈️ Conectividad Logística")
    st.subheader("Aerolíneas Recomendadas")
    col_a1, col_a2 = st.columns(2)
    with col_a1: st.write("- Iberia (Europa)\n- Avianca (Latam)\n- Lufthansa (Global)")
    with col_a2: st.write("- American Airlines (USA)\n- KLM (Holanda)\n- Copa (Panamá)")

# --- 8. UBICACION Y MAPAS ---
elif menu_sel == opciones_menu[8]:
    st.title("📍 Ubicación Serenity (Dagua)")
    lat, lon = 3.465, -76.634
    m = folium.Map(location=[lat, lon], zoom_start=14)
    folium.Marker([lat, lon], popup="Sede Serenity").add_to(m)
    st_folium(m, width="100%", height=500)




































































































































