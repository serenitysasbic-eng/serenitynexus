# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Serenity SAS BIC", page_icon="🌳", layout="wide")

# --- ESTILOS VISUALES DE TU PC (CSS) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        .stApp {
            background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1920&q=80');
            background-size: cover; color: white; font-family: 'Montserrat', sans-serif;
        }
        h1, h2, h3 { font-family: 'Merriweather', serif; color: #9BC63B; }
        .stButton>button {
            background-color: #2E7D32; color: white; border: 1px solid #9BC63B;
            border-radius: 5px; font-weight: bold; text-transform: uppercase; width: 100%;
        }
        .stButton>button:hover { border: 1px solid white; color: #9BC63B; box-shadow: 0 0 15px #9BC63B; }
        .card { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(155,198,59,0.2); }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE SEGURIDAD ---
def comprobar_contrasena():
    if "password_correct" not in st.session_state:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        try: st.image("logo_serenity.png", width=250)
        except: st.title("Serenity SAS BIC")
        st.markdown("</div>", unsafe_allow_html=True)
        
        pw = st.text_input("Ingrese Clave de Administrador", type="password")
        if st.button("INGRESAR AL SISTEMA"):
            if pw == "Serenity2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("Clave Incorrecta")
        return False
    return True

if comprobar_contrasena():
    # BARRA LATERAL (NAVEGACIÓN COMPLETA)
    st.sidebar.image("logo_serenity.png", use_container_width=True)
    menu = st.sidebar.radio("MENÚ PRINCIPAL", 
        ["Inicio", "Puntos Faro", "Planes de Apoyo", "Donaciones & Certificados", "Hospedaje", "Ubicación"])

    # 1. INICIO
    if menu == "Inicio":
        st.markdown("<h1 style='text-align:center; font-size:3.5rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; letter-spacing:4px;'>SISTEMA REGENERATIVO BIOMÉTRICO</p>", unsafe_allow_html=True)
        
        st.components.v1.html("""
            <audio id="audio" src="sonido_bosque.m4a" loop></audio>
            <div style="text-align:center;"><button onclick="document.getElementById('audio').play()" 
            style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:15px 30px; border-radius:5px; cursor:pointer;">
            🔊 ACTIVAR SONIDO AMBIENTAL</button></div>
        """, height=100)

    # 2. PUNTOS FARO (VR Y MONITOREO)
    elif menu == "Puntos Faro":
        st.title("Monitoreo de Puntos Faro")
        colA, colB, colC = st.columns(3)
        faros = ["🦅 Halcón", "🌸 Colibrí", "🐸 Rana", "🦌 Venado", "🐾 Tigrillo", "💧 Capibara"]
        for i, faro in enumerate(faros):
            target = [colA, colB, colC][i % 3]
            if target.button(f"Ver {faro}"):
                st.session_state.faro_actual = faro

        if "faro_actual" in st.session_state:
            st.markdown(f"### Visualización: {st.session_state.faro_actual}")
            st.components.v1.html("""
                <script src="https://aframe.io/releases/1.2.0/aframe.min.js"></script>
                <a-scene embedded style="height: 350px;">
                    <a-sky src="https://pannellum.org/images/alma.jpg" rotation="0 -130 0"></a-sky>
                </a-scene>
            """, height=350)
            st.info(f"IA Alerta: {random.choice(['Sin novedades', 'Movimiento detectado', 'Canto de ave registrado'])}")

    # 3. PLANES DE APOYO (SUSCRIPCIONES)
    elif menu == "Planes de Apoyo":
        st.title("Planes de Apoyo Regenerativo")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='card'><h3>Plan Semilla</h3><p>USD 5 / mes</p></div>", unsafe_allow_html=True)
            if st.button("Suscribirse Semilla"): st.success("Redirigiendo a Pasarela...")
        with c2:
            st.markdown("<div class='card'><h3>Plan Guardián</h3><p>USD 25 / mes</p></div>", unsafe_allow_html=True)
            if st.button("Suscribirse Guardián"): st.success("Redirigiendo a Pasarela...")
        with c3:
            st.markdown("<div class='card'><h3>Plan Serenity</h3><p>USD 200 / mes</p></div>", unsafe_allow_html=True)
            if st.button("Suscribirse Serenity"): st.success("Redirigiendo a Pasarela...")

    # 4. DONACIONES & CERTIFICADOS
    elif menu == "Donaciones & Certificados":
        st.title("Donaciones al Planeta")
        monto = st.number_input("Monto de Donación Voluntaria (USD)", min_value=1)
        nombre = st.text_input("Nombre para el Certificado")
        if st.button("Donar y Generar Certificado"):
            st.balloons()
            st.markdown(f"""
                <div style="background:white; color:black; padding:40px; border:10px double #D4AF37; text-align:center; font-family:serif;">
                    <h1 style="color:#2E7D32;">CERTIFICADO DE DONACIÓN</h1>
                    <p>Serenity SAS BIC reconoce a: <b>{nombre}</b></p>
                    <p>Por su valioso aporte de {monto} USD a la regeneración del KBA San Antonio.</p>
                </div>
            """, unsafe_allow_html=True)

    # 5. HOSPEDAJE
    elif menu == "Hospedaje":
        st.title("Reservas Eco-Lodge")
        h1, h2 = st.columns(2)
        with h1:
            st.markdown("<div class='card'><h3>Villa Michelle</h3><p>Confort y Naturaleza</p></div>", unsafe_allow_html=True)
            st.button("Reservar en Villa Michelle")
        with h2:
            st.markdown("<div class='card'><h3>Monte Guadua</h3><p>Inmersión Total</p></div>", unsafe_allow_html=True)
            st.button("Reservar en Monte Guadua")

    # 6. UBICACIÓN
    elif menu == "Ubicación":
        st.title("Nuestra Ubicación")
        df_map = pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]})
        st.map(df_map)

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.clear()
        st.rerun()




