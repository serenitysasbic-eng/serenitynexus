# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
import hashlib
from datetime import datetime
import io
import os
import base64

# --- LIBRERÍAS ---
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
if 'pdf_empresa_buffer' not in st.session_state: st.session_state.pdf_empresa_buffer = None

# --- DICCIONARIO BILINGÜE (RESTAURADO AL 100%) ---
tr = {
    'menu_opts': {
        'ES': ["INICIO", "RED DE FAROS (7 NODOS)", "DASHBOARD ESTADÍSTICO IA", "GESTIÓN LEY 2173 (EMPRESAS)", "SUSCRIPCIONES", "BILLETERA CRYPTO (WEB3)", "DONACIONES Y CERTIFICADO", "LOGÍSTICA AEROLÍNEAS", "UBICACIÓN & MAPAS"],
        'EN': ["HOME", "BEACON NETWORK (7 NODES)", "AI STATS DASHBOARD", "LAW 2173 MANAGEMENT (CORP)", "SUBSCRIPTIONS", "CRYPTO WALLET (WEB3)", "DONATIONS & CERTIFICATE", "AIRLINE LOGISTICS", "LOCATION & MAPS"]
    },
    'who_title': {'ES': 'QUIENES SOMOS', 'EN': 'WHO WE ARE'},
    'who_text': {
        'ES': 'Serenity Nexus Global es la primera plataforma Phygital del Valle del Cauca que integra la conservación ambiental con tecnología Blockchain e Inteligencia Artificial.',
        'EN': 'Serenity Nexus Global is the first Phygital platform in Valle del Cauca integrating environmental conservation with Blockchain and AI.'
    },
    'mis_title': {'ES': 'NUESTRA MISIÓN', 'EN': 'OUR MISSION'},
    'mis_text': {
        'ES': 'Regenerar el tejido ecológico y social mediante un modelo de negocio sostenible.',
        'EN': 'Regenerate the ecological and social fabric through a sustainable business model.'
    },
    'vis_title': {'ES': 'NUESTRA VISIÓN', 'EN': 'OUR VISION'},
    'vis_text': {
        'ES': 'Ser el referente mundial del Internet de la Naturaleza para 2030.',
        'EN': 'To be the global benchmark for the Internet of Nature by 2030.'
    }
}

def t(key):
    lang = st.session_state.get('lang', 'ES')
    return tr.get(key, {}).get(lang, key)

# --- CSS (ESTILOS ORIGINALES RECUPERADOS) ---
st.markdown("""
    <style>
        .stApp { background-image: linear-gradient(rgba(5, 10, 4, 0.8), rgba(5, 10, 4, 0.9)), url('https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1920&q=80'); background-size: cover; background-attachment: fixed; color: #e8f5e9; }
        h1, h2, h3 { color: #9BC63B !important; }
        .airline-grid { background: white; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; height: 120px; display: flex; align-items: center; justify-content: center; flex-direction: column; }
        .airline-grid img { max-width: 90%; max-height: 70px; object-fit: contain; }
        .airline-grid p { color: black !important; font-weight: bold; font-size: 0.8rem; }
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>SISTEMA NEXUS | SERENITY</h1>", unsafe_allow_html=True)
    clave = st.text_input("PASSWORD ADMIN", type="password")
    if st.button("INGRESAR"):
        if clave == "Serenity2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    toggle_lang = st.toggle(" ENGLISH MODE", value=(st.session_state.lang == 'EN'))
    st.session_state.lang = 'EN' if toggle_lang else 'ES'
    opciones_menu = tr['menu_opts'][st.session_state.lang]
    menu_sel = st.radio("CENTRO DE CONTROL", opciones_menu)

# --- BLOQUES DE CONTENIDO ---

# 0. INICIO
if menu_sel == opciones_menu[0]:
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        if os.path.exists("logo_serenity.png"): st.image("logo_serenity.png", use_container_width=True)
    st.markdown("<h1 style='text-align:center;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.info(f"Hacienda Monte Guadua (60%) Tatiana Arcila Ferreira | Finca Villa Michelle (40%) Sandra Patricia Agredo Muñoz")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"🌿 {t('mis_title')}"); st.write(t('mis_text'))
    with col2:
        st.subheader(f"🚀 {t('vis_title')}"); st.write(t('vis_text'))

# 1. RED DE FAROS (RECUPERADO)
elif menu_sel == opciones_menu[1]:
    st.title("📡 Monitoreo Perimetral")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown("<div class='faro-card'><h3>FARO HALCÓN</h3></div>", unsafe_allow_html=True)
    with c3:
        if st.button("📽️ VER DEMO GEMINI"): st.session_state.f_activo = "GEMINI-DEMO"
    
    if st.session_state.f_activo == "GEMINI-DEMO":
        st.video("https://www.youtube.com/watch?v=bUs9qYKF6mY")

# 7. LOGÍSTICA (RESTAURADO CON LOGOS PNG)
elif menu_sel == opciones_menu[7]:
    st.title("✈️ Conectividad Global")
    e1, e2, e3, e4 = st.columns(4)
    with e1: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Iberia_Logo.svg/320px-Iberia_Logo.svg.png'><p>IBERIA</p></div>", unsafe_allow_html=True)
    with l1: # Ejemplo de Avianca que pediste
        st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Avianca_logo_2016.svg/320px-Avianca_logo_2016.svg.png'><p>AVIANCA</p></div>", unsafe_allow_html=True)

# 8. MAPAS
elif menu_sel == opciones_menu[8]:
    st.title("📍 Ubicación Dagua y Felidia")
    m = folium.Map(location=[3.465, -76.634], zoom_start=13)
    st_folium(m, width="100%", height=500)































































































































