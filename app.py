# -*- coding: utf-8 -*-
import streamlit as st
from database import SerenityDB
from nexus_defense import NexusDefenseIA
from oracle_engine import NexusOracle

# --- IDENTIDAD VISUAL SERENITY ---
st.set_page_config(page_title="Serenity Nexus Búnker", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #2D4336; color: white; }
    h1, h2, h3 { color: #C5A059 !important; }
    div.stButton > button { background-color: #C5A059; color: #2D4336; font-weight: bold; border: none; }
    </style>
""", unsafe_allow_html=True)

# Inicialización de sistemas
db = SerenityDB()
ia = NexusDefenseIA()
oracle = NexusOracle(api_key="SERENITY_2026")

# --- INTERFAZ ---
st.sidebar.image("logo_serenity.png")
st.title("??? Búnker de Control: Serenity Nexus Global")
st.subheader("Donde el capital natural conecta con tu ser")

col1, col2 = st.columns([2, 1])

with col1:
    st.write("### ??? Monitoreo 360° (8 Cámaras)")
    eventos = ia.analizar_sensores()
    for e in eventos:
        st.info(f"ALERTA [{e['zona']}]: {e['objeto']} detectado con {e['confianza']:.2%} de certeza.")
        if st.button(f"Validar Hallazgo en {e['zona']}"):
            db.registrar_evento("FARO-01", e['objeto'], e['confianza'], e['zona'])
            st.success("Registrado en Base de Datos Inalterable.")

with col2:
    st.write("### ?? Estado del Token $SNG")
    status_bio = oracle.validar_capital_natural({"biodiversidad": 0.9})
    st.metric(label="Valor Regenerativo", value=status_bio['valor_token_sng'])
    st.write(f"Certificación: {status_bio['status']}")
    
    st.write("### ?? Escucha Direccional")
    st.warning(ia.triangulacion_acustica())

st.divider()
st.write("© 2026 Serenity S.A.S. BIC - Soberanía Tecnológica Ambiental")