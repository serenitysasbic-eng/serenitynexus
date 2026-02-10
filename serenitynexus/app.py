# -*- coding: utf-8 -*-
"""
SISTEMA: SERENITY NEXUS GLOBAL - OMNI CORE SUPREME (V23.0)
PROPIETARIO: JORGE CARVAJAL | SERENITY S.A.S. BIC & SERENITY NEXUS GLOBAL S.A.S.
EDICIÓN: RESTAURACIÓN TOTAL - NOVENA MARAVILLA
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

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL (EL LUJO QUE TENÍAMOS)
st.set_page_config(page_title="SERENITY NEXUS GLOBAL", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    [data-testid="stMetricValue"] { color: #00ff41 !important; font-family: 'Courier New', monospace; }
    .stMetric { background: linear-gradient(145deg, #161b22, #1f2937); padding: 20px; border-radius: 15px; border: 1px solid #2ea043; }
    h1, h2, h3 { color: #2ea043; font-weight: 800; text-transform: uppercase; }
    .stButton>button { background: linear-gradient(90deg, #2ea043, #238636); color: white; border-radius: 20px; border: none; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. LÓGICA DE NEGOCIO (SOCIAS E INVENTARIO)
class SerenityCore:
    def __init__(self):
        self.director = "Jorge Carvajal"
        self.socias = {"Tatiana Arcila": 0.60, "Sandra Agredo": 0.40}
        self.hectareas = 80
        self.token_start = 0.05
        
    def get_full_inventory(self):
        return pd.DataFrame([
            {"Ítem": "Cámaras Hikvision 4K AI", "Cant": 48, "Inversión": "$14,400"},
            {"Ítem": "Mics Audio-Technica AT8035", "Cant": 24, "Inversión": "$6,000"},
            {"Ítem": "NVIDIA Jetson Orin Nano", "Cant": 6, "Inversión": "$4,200"},
            {"Ítem": "Pino Canadiense (3x2x3m)", "Cant": 6, "Inversión": "$9,000"},
            {"Ítem": "Starlink + Radio Enlaces", "Cant": 1, "Inversión": "$3,200"}
        ])

# 3. INTERFAZ DE USUARIO INTEGRAL
def main():
    nexus = SerenityCore()
    
    st.sidebar.title("💎 COMANDO NEXUS")
    st.sidebar.markdown(f"**Director:** {nexus.director}")
    
    menu = st.sidebar.radio("SISTEMAS", [
        "🏢 CENTRAL VILLA MICHELLE",
        "🛰️ RED MONTE GUADUA",
        "📊 MARKETPLACE $SNG",
        "⚖️ GOBERNANZA & SOCIAS",
        "🛡️ SEGURIDAD SHA-3",
        "📦 INVENTARIO COMPLETO"
    ])

    if menu == "🏢 CENTRAL VILLA MICHELLE":
        st.title("🚀 Centro de Mando: La Novena Maravilla")
        c1, c2, c3 = st.columns(3)
        c1.metric("ESTADO", "CONECTADO", "Starlink")
        c2.metric("ÁREA", "80 Ha", "Monte Guadua")
        c3.metric("VALOR $SNG", f"${nexus.token_start}", "Arranque")
        
        st.markdown("---")
        st.subheader("Ubicación Geo-Referenciada")
        m = folium.Map(location=[3.445, -76.530], zoom_start=15, tiles="CartoDB dark_matter")
        folium.Polygon(locations=[[3.44, -76.535], [3.45, -76.535], [3.45, -76.525], [3.44, -76.525]], 
                       color='#00ff41', fill=True, fill_opacity=0.3).add_to(m)
        st_folium(m, width="100%", height=400)

    elif menu == "🛰️ RED MONTE GUADUA":
        st.title("Monitoreo en Vivo (48 Cámaras)")
        faro_id = st.selectbox("Seleccionar Faro", [1,2,3,4,5,6])
        st.image(f"https://via.placeholder.com/800x400.png?text=STREAMING+FARO+{faro_id}+4K", caption="Visión AI")
        st.write("🎤 Audio Bioacústico: Identificando fauna...")

    elif menu == "⚖️ GOBERNANZA & SOCIAS":
        st.title("Estructura de Socios")
        for s, p in nexus.socias.items():
            st.write(f"**{s}:** {int(p*100)}%")
            st.progress(p)

    elif menu == "📦 INVENTARIO COMPLETO":
        st.title("Inventario Maestro (CAPEX)")
        st.table(nexus.get_full_inventory())
        st.write("**Inversión Estimada:** $62,500 USD")

if __name__ == "__main__":
    main()





































































