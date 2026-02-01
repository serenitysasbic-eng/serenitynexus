# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="Serenity SAS BIC | Nodo Nexus", page_icon="🌳", layout="wide")

# --- DISEÑO DE TERMINAL DE CONTROL (CSS) ---
st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
            url('https://images.unsplash.com/photo-1511497584788-8767fe771d21?auto=format&fit=crop&w=1920&q=80');
            background-size: cover; background-attachment: fixed; color: #9BC63B; font-family: 'Courier New', monospace;
        }
        .cam-box {
            background: #000; border: 1px solid #2E7D32; height: 150px;
            display: flex; align-items: center; justify-content: center;
            color: #ff0000; font-size: 10px; position: relative; border-radius: 5px;
        }
        .cam-label { position: absolute; top: 5px; left: 5px; background: rgba(0,0,0,0.7); padding: 2px 5px; }
        .mic-card { background: rgba(46, 125, 50, 0.1); border: 1px solid #9BC63B; padding: 10px; border-radius: 5px; text-align: center; }
        .stButton>button { background-color: #000; color: #9BC63B; border: 1px solid #9BC63B; font-weight: bold; width: 100%; }
        .stButton>button:hover { background-color: #9BC63B; color: #000; }
    </style>
""", unsafe_allow_html=True)

# --- SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.markdown("<h1 style='text-align:center;'>SERENITY SAS BIC</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        clave = st.text_input("PASSWORD ADMIN", type="password")
        if st.button("DESBLOQUEAR NODO"):
            if clave == "Serenity2026":
                st.session_state.autenticado = True
                st.rerun()
    st.stop()

# --- NAVEGACIÓN ---
menu = st.sidebar.radio("SISTEMA", ["INICIO", "6 PUNTOS FARO", "PLANES", "DONACIONES", "HOSPEDAJE"])

if menu == "INICIO":
    st.markdown("<h1 style='text-align:center; font-size:4rem;'>Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:white;'>SISTEMA DE MONITOREO BIOMÉTRICO EN TIEMPO REAL</p>", unsafe_allow_html=True)
    st.components.v1.html("""
        <audio id="bg" src="sonido_bosque.m4a" loop></audio>
        <div style="text-align:center;"><button onclick="document.getElementById('bg').play()" style="background:none; border:1px solid #9BC63B; color:#9BC63B; padding:10px; cursor:pointer;">ACTIVAR CANAL AUDITIVO GENERAL 🔊</button></div>
    """, height=100)

elif menu == "6 PUNTOS FARO":
    st.title("🛰️ RED DE MONITOREO PERIMETRAL")
    
    # Grid de los 6 Faros
    faros = ["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara"]
    c1, c2, c3 = st.columns(3)
    for i, f in enumerate(faros):
        target = [c1, c2, c3][i % 3]
        with target:
            st.markdown(f"<div style='border:1px solid #9BC63B; padding:20px; text-align:center; margin-bottom:10px;'><h3>FARO {f.upper()}</h3></div>", unsafe_allow_html=True)
            if st.button(f"INGRESAR AL FARO {f.upper()}"):
                st.session_state.faro_activo = f

    # --- INTERFAZ DE MONITOREO INTERNO ---
    if "faro_activo" in st.session_state:
        st.markdown("---")
        st.header(f"📡 NODO: FARO {st.session_state.faro_activo.upper()} - STREAMING ACTIVO")
        
        # Grid de 8 Cámaras
        st.subheader("VIGILANCIA ÓPTICA (8 CÁMARAS)")
        cam_cols = st.columns(4)
        for j in range(8):
            with cam_cols[j % 4]:
                st.markdown(f"""
                    <div class="cam-box">
                        <div class="cam-label">CAM {j+1} - LIVE</div>
                        <div style="color:#ff0000; font-weight:bold;">● REC</div>
                    </div>
                """, unsafe_allow_html=True)
                st.caption(f"Ángulo: {random.choice(['Copa Árbol', 'Suelo', 'Norte', 'Sur'])}")

        st.markdown("---")
        # Grid de 4 Micrófonos
        st.subheader("MONITOREO BIOACÚSTICO (4 MICRÓFONOS)")
        mic_cols = st.columns(4)
        for k in range(4):
            with mic_cols[k]:
                st.markdown(f"""
                    <div class="mic-card">
                        <p style="font-size:10px;">MIC {k+1}</p>
                        <div style="color:#9BC63B; font-size:20px;">{"|" * random.randint(5,15)}</div>
                        <p style="font-size:9px; color:white;">{random.randint(15,22)} kHz</p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.success(f"IA Serenity: Detectando frecuencias de {random.choice(['Aves Paseriformes', 'Anfibios', 'Mamíferos nocturnos'])}")

elif menu == "PLANES":
    st.title("PLANES DE APOYO REGENERATIVO")
    p1, p2, p3 = st.columns(3)
    with p1: st.markdown("<div style='border:1px solid #9BC63B; padding:20px; text-align:center;'><h3>PLAN SEMILLA</h3><p>$5 USD</p></div>", unsafe_allow_html=True)
    with p2: st.markdown("<div style='border:1px solid #9BC63B; padding:20px; text-align:center;'><h3>PLAN GUARDIÁN</h3><p>$25 USD</p></div>", unsafe_allow_html=True)
    with p3: st.markdown("<div style='border:1px solid #D4AF37; padding:20px; text-align:center;'><h3>PLAN SERENITY</h3><p>$200 USD</p></div>", unsafe_allow_html=True)

# (Secciones de Donaciones y Hospedaje simplificadas para mantener enfoque en Faros)







