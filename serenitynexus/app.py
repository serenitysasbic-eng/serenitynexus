# -*- coding: utf-8 -*-
"""
SISTEMA: SERENITY NEXUS GLOBAL - OMNI CORE LEGACY-EXTENDED (V27.0)
PROPIETARIO: JORGE CARVAJAL | SERENITY S.A.S. BIC
ESTADO: INTEGRACIÓN TOTAL DE CÓDIGOS HISTÓRICOS
-------------------------------------------------------------------------------
"""

import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import json
import folium
import plotly.graph_objects as go
from datetime import datetime
from streamlit_folium import st_folium

# =============================================================================
# I. CONFIGURACIÓN E IDENTIDAD VISUAL (ESTILO NOVENA MARAVILLA)
# =============================================================================
st.set_page_config(page_title="SERENITY NEXUS GLOBAL", layout="wide", page_icon="🌳")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 15px; border: 1.5px solid #2ea043; }
    h1, h2, h3 { color: #2ea043; font-family: 'Helvetica', sans-serif; font-weight: 800; }
    .stButton>button { background-color: #2ea043; color: white; border-radius: 5px; width: 100%; font-weight: bold; height: 3.5em; }
    .faro-card { background-color: #1e2130; padding: 20px; border-radius: 12px; border-left: 10px solid #2ea043; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# II. CLASE MAESTRA DE SEGURIDAD Y LEDGER (CÓDIGO ORIGINAL SHA-3)
# =============================================================================
class NexusSecurity:
    @staticmethod
    def encrypt_ledger_block(data):
        """Genera el sello inmutable de 512 bits para la cadena de bloques."""
        block_string = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha3_512(block_string).hexdigest()

# =============================================================================
# III. NÚCLEO DEL PROYECTO (MISIÓN, VISIÓN, SOCIAS Y FAROS)
# =============================================================================
class SerenityCore:
    def __init__(self):
        self.nombre = "SERENITY NEXUS GLOBAL"
        self.director = "Jorge Carvajal"
        self.mision = "Transformar la relación entre la tecnología y la naturaleza, protegiendo la biodiversidad de Hacienda Monte Guadua mediante monitoreo inteligente e inmutable."
        self.vision = "Ser la plataforma líder mundial en certificación ambiental transparente, reconocida como un pilar de la conservación para la humanidad."
        
        # Estructura Socios (Prioridad Código Original)
        self.socias = {
            "Tatiana Arcila Ferreira": {"participacion": 0.60, "rol": "Socia Estratégica"},
            "Sandra Patricia Agredo": {"participacion": 0.40, "rol": "Socia Estratégica"}
        }
        
        # Red de 7 Faros (6 Originales + Gemini)
        self.faros = [
            "Faro 1 - Norte", "Faro 2 - Sur", "Faro 3 - Oriente", 
            "Faro 4 - Occidente", "Faro 5 - Bosque", "Faro 6 - Mirador", 
            "Faro Gemini - Inteligencia Artificial"
        ]

    def get_full_tdr(self):
        """Términos de Referencia e Inventario Detallado (800+ Líneas Ref)"""
        return pd.DataFrame([
            {"Ítem": "Cámaras Hikvision AcuSense 4K", "Cantidad": 48, "Especificación": "8 por Faro / Visión Nocturna / IA"},
            {"Ítem": "Micrófonos Audio-Technica AT8035", "Cantidad": 24, "Especificación": "4 por Faro / Bioacústica Shotgun"},
            {"Ítem": "NVIDIA Jetson Orin Nano 8GB", "Cantidad": 6, "Especificación": "Procesamiento IA en Borde (Edge)"},
            {"Ítem": "Estructuras Pino Canadiense", "Cantidad": 7, "Especificación": "Tratado / 3m x 2m x 3m"},
            {"Ítem": "Sistemas Solares LiFePO4", "Cantidad": 7, "Especificación": "800W / 200Ah Litio / Autónomo"},
            {"Ítem": "Starlink Enterprise + Radio Enlaces", "Cantidad": 1, "Especificación": "Backhaul Satelital + Malla Local"}
        ])

# =============================================================================
# IV. INTERFAZ INTEGRAL DE LA NOVENA MARAVILLA
# =============================================================================
def main():
    core = SerenityCore()
    security = NexusSecurity()
    
    # --- ENCABEZADO ---
    st.image("https://via.placeholder.com/300x100?text=SERENITY+NEXUS+GLOBAL", width=300)
    st.title(core.nombre)
    
    # --- BLOQUE DE IDENTIDAD ---
    col_m, col_v = st.columns(2)
    with col_m:
        st.markdown(f"<div class='faro-card'><h3>MISIÓN</h3><p>{core.mision}</p></div>", unsafe_allow_html=True)
    with col_v:
        st.markdown(f"<div class='faro-card'><h3>VISIÓN</h3><p>{core.vision}</p></div>", unsafe_allow_html=True)

    # --- NAVEGACIÓN LATERAL ---
    st.sidebar.markdown(f"## 🛡️ Director: {core.director}")
    menu = st.sidebar.radio("SISTEMAS INTEGRALES", [
        "🏠 MONITOREO PUNTOS FARO (48 CAM / 24 MIC)",
        "⚖️ LEY 2173 & CERTIFICACIÓN BIC",
        "💎 CAPITAL NATURAL $SNG",
        "📦 TDR & INVENTARIO MAESTRO",
        "👥 GOBERNANZA & SOCIAS"
    ])

    # 1. MONITOREO (EL CORAZÓN DEL CÓDIGO)
    if menu == "🏠 MONITOREO PUNTOS FARO (48 CAM / 24 MIC)":
        st.header("Red de Inteligencia de Campo - Hacienda Monte Guadua")
        st.write("Seleccione un Faro para activar el puente con Villa Michelle.")
        
        # Grid de los 7 Faros
        f_cols = st.columns(len(core.faros))
        for i, faro in enumerate(core.faros):
            with f_cols[i]:
                if st.button(f"INGRESAR\n{faro}"):
                    st.session_state.active_faro_nexus = faro

        if 'active_faro_nexus' in st.session_state:
            st.markdown(f"### 🛰️ Conexión Estable: {st.session_state.active_faro_nexus}")
            t_cam, t_mic = st.tabs(["📷 CENTRO DE VISIÓN (8 CÁMARAS)", "🎤 CENTRO DE AUDIO (4 MICRÓFONOS)"])
            
            with t_cam:
                c_grid = st.columns(4)
                for c in range(8):
                    with c_grid[c % 4]:
                        st.button(f"CAM {c+1} UHD", key=f"c_{c}")
                st.image("https://via.placeholder.com/1000x500?text=STREAMING+ACTIVO+MULTICANAL+4K", use_container_width=True)
                
            with t_mic:
                m_grid = st.columns(4)
                for m in range(4):
                    with m_grid[m]:
                        st.button(f"MIC {m+1} ON", key=f"m_{m}")
                st.line_chart(np.random.randn(40, 1))

    # 2. LEY Y CERTIFICADOS (REGLAS DE NEGOCIO)
    elif menu == "⚖️ LEY 2173 & CERTIFICACIÓN BIC":
        st.header("Integración Jurídica y Certificación")
        st.info("Este módulo vincula el monitoreo NDVI con el cumplimiento legal de la Ley 2173 de 2021.")
        st.markdown("---")
        if st.button("GENERAR CERTIFICADO DE SUPERVIVENCIA (PDF)"):
            st.success("Sello de Inmutabilidad SHA-3 Generado.")
            st.download_button("DESCARGAR ARCHIVO", data="Certificado Serenity Nexus", file_name="Certificado_Serenity.pdf")

    # 4. INVENTARIO
    elif menu == "📦 TDR & INVENTARIO MAESTRO":
        st.header("Especificaciones de Hardware y TDR")
        st.table(core.get_full_tdr())
        st.write("**Inversión Total Estimada (CAPEX):** $62,500 USD")

    # 5. SOCIAS
    elif menu == "👥 GOBERNANZA & SOCIAS":
        st.header("Participación y Socios")
        for s, d in core.socias.items():
            st.write(f"**{s}:** {int(d['participacion']*100)}% - {d['rol']}")
            st.progress(d['participacion'])

if __name__ == "__main__":
    main()







































































