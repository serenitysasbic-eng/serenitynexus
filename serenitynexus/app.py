# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime

# CONFIGURACION DE IDENTIDAD - SERENITY SAS BIC
st.set_page_config(page_title="Serenity SAS BIC", page_icon="🌳", layout="wide")

# SISTEMA DE SEGURIDAD INTEGRADO
def comprobar_contrasena():
    def password_entered():
        # JORGE: AQUÍ PUEDES EDITAR TU CONTRASEÑA DIRECTAMENTE
        if st.session_state["password"] == "Serenity2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        try:
            st.image("logo_serenity.png", width=200)
        except:
            st.markdown("### 🌳 Serenity SAS BIC")
            
        st.title("Acceso Privado | Nodo Nexus")
        st.text_input("Ingrese su clave de Administrador", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("Clave incorrecta. Acceso denegado.")
        st.text_input("Ingrese su clave de Administrador", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

# INICIO DEL SISTEMA TRAS VALIDACIÓN
if comprobar_contrasena():
    
    # Diseño visual Serenity
    st.markdown("""<style>
        .stApp { background-color: #050a04; color: #e8f5e9; }
        .stButton>button { background-color: #2E7D32; color: white; border-radius: 10px; border: 1px solid #9BC63B; }
        .stSidebar { background-color: #0a1408; }
    </style>""", unsafe_allow_html=True)

    # Menu Lateral
    try:
        st.sidebar.image("logo_serenity.png", use_container_width=True)
    except:
        st.sidebar.title("Serenity SAS BIC")
        
    st.sidebar.markdown("---")
    opcion = st.sidebar.radio("CENTRO DE CONTROL", ["Monitoreo de Faros", "Realidad Virtual 360", "Gestion BIC", "Mapa de Ubicacion"])

    # --- PÁGINA: MONITOREO ---
    if opcion == "Monitoreo de Faros":
        st.header("Nexus Global | Inteligencia Biológica")
        
        # Audio de aves corregido para evitar errores
        try:
            st.components.v1.html("""
                <audio id="bosque" src="sonido_bosque.m4a" loop></audio>
                <button onclick="document.getElementById('bosque').play()" 
                style="background:#2E7D32; color:white; padding:12px; border-radius:8px; cursor:pointer; border:1px solid #9BC63B; font-weight:bold;">
                🔊 ACTIVAR AMBIENTE HACIENDA
                </button>
            """, height=80)
        except:
            st.warning("El archivo de audio no está disponible.")

        col1, col2 = st.columns([2, 1])
        with col1:
            st.image("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800", caption="Monitoreo Faro Halcón")
        with col2:
            st.subheader("Alertas IA de Fauna")
            if st.button("Escanear Sensores"):
                aves = ["Tangara Multicolor", "Barranquero", "Pava Caucana", "Colibrí Inca"]
                st.success(f"Reporte: {random.choice(aves)} detectado.")
                st.info(f"Hora: {datetime.now().strftime('%H:%M:%S')}")

    # --- PÁGINA: REALIDAD VIRTUAL ---
    elif opcion == "Realidad Virtual 360":
        st.header("Inmersión VR | Puntos Faro")
        st.write("Visualización inmersiva del KBA San Antonio.")
        st.components.v1.html("""
            <script src="https://aframe.io/releases/1.2.0/aframe.min.js"></script>
            <a-scene embedded style="height: 500px; width: 100%;">
                <a-sky src="https://pannellum.org/images/alma.jpg" rotation="0 -130 0"></a-sky>
                <a-text value="Serenity SAS BIC - Faro VR" position="-1.5 2 -3" color="#9BC63B" width="6"></a-text>
            </a-scene>
        """, height=520)

    # --- PÁGINA: GESTIÓN ---
    elif opcion == "Gestion BIC":
        st.header("Impacto y Donaciones")
        with st.form("donar"):
            nombre = st.text_input("Nombre del Donante")
            monto = st.number_input("Aporte (USD)", min_value=1)
            if st.form_submit_button("Registrar en Libro BIC"):
                st.balloons()
                st.success(f"Gracias {nombre}. Registro procesado.")

    # --- PÁGINA: UBICACIÓN ---
    elif opcion == "Mapa de Ubicacion":
        st.header("Localización de la Hacienda")
        # Coordenadas San Antonio
        mapa = pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]})
        st.map(mapa)

    # Boton para cerrar sesion profesional
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["password_correct"] = False
        st.rerun()




