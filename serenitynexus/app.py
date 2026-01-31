# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime

# CONFIGURACION DE IDENTIDAD - SERENITY SAS BIC
st.set_page_config(page_title="Serenity SAS BIC", page_icon="??", layout="wide")

# SISTEMA DE SEGURIDAD PARA JORGE (EL ADMINISTRADOR)
def comprobar_contrasena():
    def password_entered():
        if st.session_state["password"] == st.secrets["password_admin"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        try:
           st.image("logo_serenity.png", width=200)
    
        except:
           st.markdown("### Serenity SAS BIC")
           st.title("Acceso Privado | Serenity SAS BIC")
           st.text_input("Contraseña Maestra", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("Contraseña incorrecta. Solo Jorge tiene acceso.")
        st.text_input("Contraseña Maestra", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

# SI LA CONTRASEÑA ES CORRECTA, SE MUESTRA TODO LO DEMAS
if comprobar_contrasena():
    
    # Estilos de color para la marca
    st.markdown("""<style>
        .stApp { background-color: #050a04; color: #e8f5e9; }
        .stButton>button { background-color: #2E7D32; color: white; border-radius: 10px; width: 100%; }
    </style>""", unsafe_allow_html=True)

    # Menu Lateral
    st.sidebar.image("logo_serenity.png", use_container_width=True)
    st.sidebar.header("Serenity SAS BIC")
    opcion = st.sidebar.radio("Ir a:", ["Monitoreo de Faros", "Realidad Virtual 360", "Gestion de Donaciones", "Mapa de Ubicacion"])

    # --- PAGINA: MONITOREO ---
    if opcion == "Monitoreo de Faros":
        st.title("Nexus Global | Monitoreo Biometrico")
        
        # Audio de aves (m4a local)
        st.components.v1.html("""
            <audio id="bosque" loop><source src="sonido_bosque.m4a" type="audio/mp4"></audio>
            <button onclick="document.getElementById('bosque').play()" style="background:#9BC63B; padding:10px; border-radius:5px; cursor:pointer; border:none; font-weight:bold;">?? ACTIVAR SONIDOS DEL BOSQUE</button>
        """, height=70)

        col1, col2 = st.columns([2, 1])
        with col1:
            st.image("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800", caption="Vista en Vivo - Monte Guadua")
        with col2:
            st.subheader("Alertas de Fauna IA")
            if st.button("Escanear Bosque"):
                aves = ["Tangara Multicolor", "Barranquero", "Pava Caucana", "Colibri Inca"]
                st.success(f"Avistamiento: {random.choice(aves)} detectado.")
                st.info(f"Hora del reporte: {datetime.now().strftime('%H:%M:%S')}")

    # --- PAGINA: REALIDAD VIRTUAL ---
    elif opcion == "Realidad Virtual 360":
        st.title("Inmersion VR | Puntos Faro")
        st.write("Mueva el mouse o su celular para ver el bosque en 360 grados.")
        st.components.v1.html("""
            <script src="https://aframe.io/releases/1.2.0/aframe.min.js"></script>
            <a-scene embedded style="height: 500px; width: 100%;">
                <a-sky src="https://pannellum.org/images/alma.jpg" rotation="0 -130 0"></a-sky>
                <a-text value="Serenity SAS BIC - Faro VR" position="-1.5 2 -3" color="#9BC63B" width="6"></a-text>
            </a-scene>
        """, height=520)

    # --- PAGINA: DONACIONES ---
    elif opcion == "Gestion de Donaciones":
        st.title("Impacto Social Serenity SAS BIC")
        with st.form("donar"):
            nombre = st.text_input("Nombre del Donante")
            monto = st.number_input("Monto a donar (USD)", min_value=1)
            if st.form_submit_button("Registrar Donacion"):
                st.write(f"Gracias {nombre}. Se ha generado un registro BIC por {monto} dolares.")

    # --- PAGINA: UBICACION ---
    elif opcion == "Mapa de Ubicacion":
        st.title("Ubicacion de la Hacienda")
        mapa = pd.DataFrame({'lat': [3.4833], 'lon': [-76.6167]}) # Coordenadas Cali/San Antonio
        st.map(mapa)

    # Boton para cerrar sesion
    if st.sidebar.button("Cerrar Sesion"):
        st.session_state["password_correct"] = False

        st.rerun()



