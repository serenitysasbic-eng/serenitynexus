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

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌿", layout="wide")
VERDE_SERENITY = HexColor("#2E7D32")

# --- GESTIÓN DE ESTADO ---
if 'lang' not in st.session_state: st.session_state.lang = 'ES'
if 'auth' not in st.session_state: st.session_state.auth = False
if 'f_activo' not in st.session_state: st.session_state.f_activo = None
if 'estado_gemini' not in st.session_state: st.session_state.estado_gemini = "Latente"

# --- DICCIONARIO BILINGÜE (RESTAURADO) ---
tr = {
    'menu_opts': {
        'ES': ["INICIO", "RED DE FAROS (7 NODOS)", "DASHBOARD ESTADÍSTICO IA", "GESTIÓN LEY 2173 (EMPRESAS)", "SUSCRIPCIONES", "BILLETERA CRYPTO (WEB3)", "DONACIONES Y CERTIFICADO", "LOGÍSTICA AEROLÍNEAS", "UBICACIÓN & MAPAS"],
        'EN': ["HOME", "BEACON NETWORK (7 NODES)", "AI STATS DASHBOARD", "LAW 2173 MANAGEMENT (CORP)", "SUBSCRIPTIONS", "CRYPTO WALLET (WEB3)", "DONATIONS & CERTIFICATE", "AIRLINE LOGISTICS", "LOCATION & MAPS"]
    },
    'who_title': {'ES': 'QUIENES SOMOS', 'EN': 'WHO WE ARE'},
    'who_text': {
        'ES': 'Serenity Nexus Global es la primera plataforma Phygital del Valle del Cauca que integra conservación con Blockchain e IA.',
        'EN': 'Serenity Nexus Global is the first Phygital platform in Valle del Cauca integrating conservation with Blockchain and AI.'
    }
}

def t(key):
    lang = st.session_state.get('lang', 'ES')
    return tr.get(key, {}).get(lang, key)

# --- LOGIN ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>SISTEMA NEXUS | SERENITY</h1>", unsafe_allow_html=True)
    clave = st.text_input("PASSWORD ADMIN", type="password")
    if st.button("INGRESAR"):
        if clave == "Serenity2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- SIDEBAR (CON SELECTOR DE IDIOMA) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Flag_of_Colombia.svg/320px-Flag_of_Colombia.svg.png", width=30)
    toggle_lang = st.toggle(" ENGLISH MODE", value=(st.session_state.lang == 'EN'))
    st.session_state.lang = 'EN' if toggle_lang else 'ES'
    menu_opts = tr['menu_opts'][st.session_state.lang]
    menu_sel = st.radio("MENÚ / MENU", menu_opts)

# =========================================================
# CONTENIDO CENTRAL
# =========================================================

# 0. INICIO (CON LOGO Y SOCIAS)
if menu_sel == menu_opts[0]:
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        if os.path.exists("logo_serenity.png"): st.image("logo_serenity.png", use_container_width=True)
    st.markdown("<h1 style='text-align:center; font-size:4rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.info("Sandra Patricia Agredo Muñoz (40%) | Tatiana Arcila Ferreira (60%) | Admin: Jorge Carvajal")

# 1. RED DE FAROS (RESTAURADA CON VIDEOS)
elif menu_sel == menu_opts[1]:
    st.title("📡 Monitoreo Perimetral")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("Conectar Halcón"): st.session_state.f_activo = "Halcón"
    with c3:
        if st.button("📽️ VER DEMO GEMINI"): st.session_state.f_activo = "GEMINI-DEMO"
    
    if st.session_state.f_activo == "GEMINI-DEMO":
        st.video("https://www.youtube.com/watch?v=bUs9qYKF6mY")
    elif st.session_state.f_activo:
        st.video("https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")

# 5. BILLETERA WEB3 (CON VIDEO $SNG EN BUCLE)
elif menu_sel == menu_opts[5]:
    st.title("💳 Web3 Green Wallet")
    try:
        with open("video_sng.mp4", "rb") as f:
            data = f.read()
            bin_str = base64.b64encode(data).decode()
        video_html = f'<video width="100%" autoplay loop muted playsinline style="border-radius: 15px;"><source src="data:video/mp4;base64,{bin_str}" type="video/mp4"></video>'
        st.markdown(video_html, unsafe_allow_html=True)
    except: st.warning("Suba 'video_sng.mp4' para activar el bucle.")
    if st.button("🔌 CONECTAR BILLETERA"): st.success("Saldo: 25,000 $SNG")

# 7. LOGÍSTICA (RESTAURADA CON LOGOS)
elif menu_sel == menu_opts[7]:
    st.title("✈️ Logística Aerolíneas")
    e1, e2 = st.columns(2)
    with e1: st.markdown("<div style='background:white; padding:10px; border-radius:10px; text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Iberia_Logo.svg/320px-Iberia_Logo.svg.png' width='100'><p style='color:black;'>IBERIA</p></div>", unsafe_allow_html=True)






































































































































