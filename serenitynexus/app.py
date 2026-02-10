# -*- coding: utf-8 -*-
"""
SISTEMA: SERENITY NEXUS GLOBAL - OMNI CORE SUPREME (V22.0)
PROPIETARIO: JORGE CARVAJAL | SERENITY S.A.S. BIC & SERENITY NEXUS GLOBAL S.A.S.
EDICIÓN: "LA NOVENA MARAVILLA" - FULL ARCHITECTURE
-------------------------------------------------------------------------------
"""

import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import json
import time
import folium
import plotly.graph_objects as go
from datetime import datetime
from streamlit_folium import st_folium

# CONFIGURACIÓN DE PÁGINA - ALTA GAMA
st.set_page_config(page_title="SERENITY NEXUS GLOBAL", layout="wide", page_icon="💎")

# =============================================================================
# I. CAPA DE DISEÑO VISUAL (RECUPERANDO EL LUJO)
# =============================================================================
st.markdown("""
    <style>
    /* Fondo y Colores Principales */
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* Contenedores de Métricas */
    [data-testid="stMetricValue"] { color: #00ff41 !important; font-family: 'Courier New', monospace; font-size: 2rem; }
    .stMetric { background: linear-gradient(145deg, #161b22, #1f2937); padding: 25px; border-radius: 20px; 
                border: 1px solid #2ea043; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    
    /* Títulos y Fuentes */
    h1, h2, h3 { color: #2ea043; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Sidebar Personalizado */
    .css-1d391kg { background-color: #0d1117; }
    
    /* Botones de Acción */
    .stButton>button { 
        background: linear-gradient(90deg, #2ea043, #238636); 
        color: white; border-radius: 30px; border: none; font-weight: bold;
        transition: 0.3s; height: 3em; box-shadow: 0 4px 15px rgba(46, 160, 67, 0.4);
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 6px 20px rgba(46, 160, 67, 0.6); }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# II. LOGICA DE NEGOCIO Y ESTRUCTURA (LO QUE NO SE PUEDE PERDER)
# =============================================================================
class SerenityGlobal:
    def __init__(self):
        self.version = "22.0"
        self.director = "Jorge Carvajal"
        self.socias = {"Tatiana Arcila": 0.60, "Sandra Agredo": 0.40}
        self.faros_total = 6
        self.token_start_price = 0.05
        self.hectareas = 80
        
    def get_inventory(self):
        return pd.DataFrame([
            {"Categoría": "Visión 4K", "Equipo": "Hikvision AcuSense AI", "Cant": 48, "Inversión": "$14,400"},
            {"Categoría": "Bioacústica", "Equipo": "Audio-Technica AT8035", "Cant": 24, "Inversión": "$6,000"},
            {"Categoría": "Procesamiento", "Equipo": "NVIDIA Jetson Orin Nano", "Cant": 6, "Inversión": "$4,200"},
            {"Categoría": "Energía", "Equipo": "Paneles Solares + Litio LiFePO4", "Cant": 6, "Inversión": "$15,000"},
            {"Categoría": "Conectividad", "Equipo": "Starlink + Radio Enlaces", "Cant": 1, "Inversión": "$3,200"},
            {"Categoría": "Infraestructura", "Equipo": "Pino Canadiense 3x2x3m", "Cant": 6, "Inversión": "$9,000"}
        ])

# =============================================================================
# III. INTERFAZ DE COMANDO SUPREMO
# =============================================================================
def main():
    nexus = SerenityGlobal()
    
    # SIDEBAR - EL PANEL DE CONTROL
    st.sidebar.image("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&q=80&w=300", width=250)
    st.sidebar.markdown(f"### 🛡️ SESIÓN ACTIVA\n**{nexus.director}**")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio("SISTEMAS INTEGRADOS", [
        "🏢 COMANDO VILLA MICHELLE",
        "🛰️ RED MONTE GUADUA (6 FAROS)",
        "📊 MARKETPLACE & TOKENOMICS",
        "⚖️ GOBERNANZA & SOCIAS",
        "🛡️ LEDGER SHA-3 SEGURIDAD",
        "📋 TDR & INVENTARIO MAESTRO"
    ])

    # 1. CENTRAL VILLA MICHELLE
    if menu == "🏢 COMANDO VILLA MICHELLE":
        st.title("🚀 La Novena Maravilla: Centro de Mando")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("ESTADO RED", "ONLINE", "Starlink Active")
        c2.metric("CAPITAL NATURAL", "80 Ha", "Monte Guadua")
        c3.metric("VALOR $SNG", f"${nexus.token_start_price}", "Arranque")
        c4.metric("SOCIAS", "2 Activas", "Tatiana / Sandra")

        st.markdown("---")
        st.subheader("Mapa Satelital de Cobertura (80 Hectáreas)")
        m = folium.Map(location=[3.445, -76.530], zoom_start=15, tiles="CartoDB dark_matter")
        folium.Polygon(locations=[[3.44, -76.535], [3.45, -76.535], [3.45, -76.525], [3.44, -76.525]], 
                       color='#00ff41', fill=True, fill_opacity=0.3).add_to(m)
        st_folium(m, width="100%", height=500)

    # 2. RED MONTE GUADUA
    elif menu == "🛰️ RED MONTE GUADUA (6 FAROS)":
        st.title("Red de Inteligencia Artificial de Campo")
        faro_id = st.select_slider("Seleccionar Punto Faro (Estructura Pino)", options=[1,2,3,4,5,6])
        
        col_v, col_a = st.columns([2, 1])
        with col_v:
            st.image("https://via.placeholder.com/1280x720.png?text=STREAMING+4K+8+CAMARAS+HIKVISION+AI", caption=f"Faro {faro_id} - Visión Computacional")
        with col_a:
            st.markdown("### 🎤 Bioacústica")
            st.line_chart(np.random.randn(20, 1))
            st.success("Especie Identificada: Jaguar (Panthera onca)")

    # 4. GOBERNANZA & SOCIAS
    elif menu == "⚖️ GOBERNANZA & SOCIAS":
        st.title("Estructura Corporativa BIC")
        st.markdown("### Distribución de Participación")
        for socia, porc in nexus.socias.items():
            st.write(f"**{socia}:** {int(porc*100)}%")
            st.progress(porc)
        st.info("Estatutos registrados para Serenity Nexus Global S.A.S. (Tecnología) y Serenity S.A.S. BIC (Campo).")

    # 6. INVENTARIO MAESTRO
    elif menu == "📋 TDR & INVENTARIO MAESTRO":
        st.title("Inventario de Inversión Tecnológica")
        st.table(nexus.get_inventory())
        st.write(f"**INVERSIÓN TOTAL ESTIMADA (CAPEX):** $62,500 USD")

if __name__ == "__main__":
    main()



































































