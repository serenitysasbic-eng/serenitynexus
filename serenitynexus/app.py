# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA - SERENITY SAS BIC
st.set_page_config(page_title="Serenity SAS BIC", page_icon="🌳", layout="wide")

# --- DISEÑO VISUAL INMERSIVO (COLORES DE TU PC + NATURALEZA) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        .stApp {
            background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), 
            url('https://images.unsplash.com/photo-1511497584788-8767fe771d21?auto=format&fit=crop&w=1920&q=80');
            background-size: cover; background-attachment: fixed; color: #f0f0f0; font-family: 'Montserrat', sans-serif;
        }
        h1, h2, h3 { font-family: 'Merriweather', serif; color: #9BC63B; }
        .stButton>button {
            background-color: #2E7D32; color: white; border: 1px solid #9BC63B;
            border-radius: 8px; font-weight: 600; text-transform: uppercase; width: 100%; height: 50px;
        }
        .stButton>button:hover { background-color: #9BC63B; color: black; box-shadow: 0 0 20px #9BC63B; }
        .card-faro { background: rgba(0,0,0,0.5); padding: 15px; border-radius: 12px; border: 1px solid rgba(155,198,59,0.3); text-align: center; margin-bottom: 10px; }
        .card-plan { background: rgba(255,255,255,0.08); padding: 20px; border-radius: 15px; border: 1px solid #9BC63B; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE SEGURIDAD (PASSWORD: Serenity2026) ---
def comprobar_contrasena():
    if "password_correct" not in st.session_state:
        st.markdown("<div style='text-align:center; padding-top:50px;'>", unsafe_allow_html=True)
        try: st.image("logo_serenity.png", width=250)
        except: st.title("🌳 SERENITY SAS BIC")
        st.markdown("</div>", unsafe_allow_html=True)
        
        col_l1, col_l2, col_l3 = st.columns([1,2,1])
        with col_l2:
            pw = st.text_input("CLAVE MAESTRA", type="password")
            if st.button("INGRESAR AL SISTEMA"):
                if pw == "Serenity2026":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else: st.error("Acceso denegado.")
        return False
    return True

if comprobar_contrasena():
    # BARRA LATERAL
    try: st.sidebar.image("logo_serenity.png", use_container_width=True)
    except: st.sidebar.markdown("### 🌳 Serenity SAS BIC")
    
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("NAVEGACIÓN", 
        ["Inicio", "6 Puntos Faro", "Planes de Apoyo", "Donaciones Libres", "Hospedaje", "Ubicación"])

    # 1. INICIO
    if menu == "Inicio":
        st.markdown("<h1 style='text-align:center; font-size:3.5rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; letter-spacing:5px; color:#9BC63B;'>SISTEMA REGENERATIVO BIOMÉTRICO</p>", unsafe_allow_html=True)
        
        st.components.v1.html("""
            <audio id="nature" src="sonido_bosque.m4a" loop></audio>
            <div style="text-align:center; margin-top:30px;">
                <button onclick="document.getElementById('nature').play()" 
                style="background:#2E7D32; color:white; border:2px solid #9BC63B; padding:20px; border-radius:10px; cursor:pointer; font-weight:bold;">
                🔊 ACTIVAR SONIDOS DE LA HACIENDA
                </button>
            </div>
        """, height=120)

    # 2. LOS 6 PUNTOS FARO
    elif menu == "6 Puntos Faro":
        st.title("Monitoreo de Biodiversidad")
        st.write("Seleccione uno de los 6 nodos de vigilancia ambiental:")
        
        faros_config = {
            "Halcón": "https://images.unsplash.com/photo-1534951470249-18433505f67e?w=800",
            "Colibrí": "https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=800",
            "Rana": "https://images.unsplash.com/photo-1515080719827-4c9f444835f0?w=800",
            "Venado": "https://images.unsplash.com/photo-1484406566174-9da000fda645?w=800",
            "Tigrillo": "https://images.unsplash.com/photo-1541414779316-956a5084c0d4?w=800",
            "Capibara": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=800"
        }
        
        c1, c2, c3 = st.columns(3)
        for i, (nombre, img_url) in enumerate(faros_config.items()):
            target_col = [c1, c2, c3][i % 3]
            with target_col:
                st.markdown(f"<div class='card-faro'><h3>Faro {nombre}</h3></div>", unsafe_allow_html=True)
                if st.button(f"Sincronizar {nombre}"):
                    st.session_state.f_img = img_url
                    st.session_state.f_nom = nombre

        if "f_img" in st.session_state:
            st.markdown(f"---")
            st.subheader(f"Vista del Faro {st.session_state.f_nom}")
            st.image(st.session_state.f_img, use_container_width=True)
            st.info(f"Estado: {random.choice(['Activo - Transmitiendo', 'IA: Sin novedades en el dosel', 'IA: Movimiento detectado'])}")

    # 3. PLANES DE APOYO
    elif menu == "Planes de Apoyo":
        st.title("Suscripciones de Guardianes")
        p1, p2, p3 = st.columns(3)
        with p1:
            st.markdown("<div class='card-plan'><h3>Plan Semilla</h3><h2>$5 USD</h2></div>", unsafe_allow_html=True)
            st.button("Suscribirse Semilla")
        with p2:
            st.markdown("<div class='card-plan'><h3>Plan Guardián</h3><h2>$25 USD</h2></div>", unsafe_allow_html=True)
            st.button("Suscribirse Guardián")
        with p3:
            st.markdown("<div class='card-plan' style='border-color:#D4AF37;'><h3>Plan Serenity</h3><h2>$200 USD</h2></div>", unsafe_allow_html=True)
            st.button("Suscribirse Serenity")

    # 4. DONACIONES & CERTIFICADOS
    elif menu == "Donaciones Libres":
        st.title("Aportes al Planeta")
        col_don1, col_don2 = st.columns(2)
        with col_don1:
            nom_cert = st.text_input("Nombre para el Certificado")
            m_don = st.number_input("Monto de Donación (USD)", min_value=1)
            if st.button("Generar Diploma"):
                st.balloons()
                st.session_state.cert = True
        
        if "cert" in st.session_state:
            with col_don2:
                st.markdown(f"""
                    <div style="background:white; color:#050a04; padding:30px; border:10px double #D4AF37; text-align:center; font-family:serif;">
                        <h1 style="color:#2E7D32;">CERTIFICADO DE GUARDIÁN</h1>
                        <p>Serenity SAS BIC agradece a <b>{nom_cert}</b></p>
                        <p>por su valioso aporte a la regeneración de la Hacienda.</p>
                    </div>
                """, unsafe_allow_html=True)

    # 5. HOSPEDAJE
    elif menu == "Hospedaje":
        st.title("Reservas Serenity Eco-Lodge")
        h1, h2 = st.columns(2)
        with h1:
            st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600", caption="Villa Michelle")
            st.button("Reservar en Villa Michelle")
        with h2:
            st.image("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600", caption="Monte Guadua")
            st.button("Reservar en Monte Guadua")

    # 6. UBICACIÓN
    elif menu == "Ubicación":
        st.title("Localización de Serenity SAS BIC")
        st.map(pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]}))

    st.sidebar.markdown("---")
    if st.sidebar.button("🔒 SALIR DEL SISTEMA"):
        st.session_state.clear()
        st.rerun()






