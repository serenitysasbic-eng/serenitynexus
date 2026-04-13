# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import io
import os
import folium
from datetime import datetime
from streamlit_folium import st_folium

# --- LIBRERÍAS DE REPORTE (PDF) ---
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black

# --- CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌿", layout="wide")

# Colores Corporativos (Sovereign Edition)
VERDE_SERENITY = HexColor("#2E7D32")
VERDE_LIMA_NEXUS = HexColor("#9BC63B")
AZUL_IA = HexColor("#4285F4")

# --- FUNCIONES DE GENERACIÓN DE DOCUMENTOS ---

def generar_pdf_diagnostico(empresa, nit, hash_id, estudio_data, total_ton, faro_nombre="Red Nexus"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setStrokeColor(VERDE_LIMA_NEXUS)
    c.setLineWidth(2)
    c.line(0.5*inch, 10.2*inch, 8*inch, 10.2*inch)
    
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(VERDE_SERENITY)
    c.drawCentredString(4.25*inch, 9.5*inch, "DIAGNÓSTICO DE ACCIÓN CLIMÁTICA")
    
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(black)
    c.drawString(1*inch, 8.8*inch, f"ENTIDAD: {empresa.upper()}")
    c.drawString(1*inch, 8.6*inch, f"NIT: {nit}")
    c.drawString(1*inch, 8.4*inch, f"ID SEGURIDAD: {hash_id}")
    c.drawString(1*inch, 8.2*inch, f"NODO VALIDADOR: {faro_nombre}")

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(VERDE_SERENITY)
    c.drawString(1*inch, 7.8*inch, "RESULTADOS DEL ANÁLISIS (TON CO2E):")
    
    y_pos = 7.5
    c.setFont("Helvetica", 9)
    c.setFillColor(black)
    for concepto, valor in estudio_data.items():
        c.drawString(1.2*inch, y_pos*inch, f"• {concepto}:")
        c.drawRightString(7*inch, y_pos*inch, f"{valor}")
        y_pos -= 0.22

    c.save()
    buffer.seek(0)
    return buffer

def generar_pdf_corporativo(empresa, impacto, hash_id, logo_bytes=None, es_vademecum=False):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setStrokeColor(VERDE_SERENITY)
    c.setLineWidth(2)
    c.line(0.5*inch, 10.2*inch, 8*inch, 10.2*inch)
    
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(VERDE_SERENITY)
    titulo = "VADEMÉCUM TÉCNICO LEGAL" if es_vademecum else "CERTIFICADO DE COMPENSACIÓN BIOMÉTRICA"
    c.drawCentredString(4.25*inch, 8.8*inch, titulo)
    
    c.setFont("Helvetica", 12)
    c.setFillColor(black)
    c.drawCentredString(4.25*inch, 8.4*inch, f"RAZÓN SOCIAL: {empresa.upper()}")
    c.drawCentredString(4.25*inch, 8.2*inch, f"ID REGISTRO: {hash_id}")

    text_object = c.beginText(0.8*inch, 7.5*inch)
    text_object.setFont("Helvetica", 11)
    text_object.setLeading(14)
    
    lineas = [
        "SOLUCIONES INTEGRADAS SERENITY S.A.S BIC:",
        "",
        "Este documento avala el cumplimiento de la normativa ambiental vigente",
        "bajo protocolos de trazabilidad mediante la Red de Faros Nexus.",
        f"Impacto Gestionado: {impacto} unidades de restauración activa."
    ]
    for linea in lineas: text_object.textLine(linea)
    c.drawText(text_object)
    
    c.save()
    buffer.seek(0)
    return buffer

# --- GESTIÓN DE ESTADO Y SEGURIDAD ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'f_activo' not in st.session_state: st.session_state.f_activo = None

# --- ESTILOS CSS ---
st.markdown("""
    <style>
        .stApp { background-color: #050a04; color: #e8f5e9; }
        .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #9BC63B; border-radius: 8px; }
        .stButton>button:hover { background-color: #9BC63B; color: black; }
        .metric-card { background: rgba(0,0,0,0.6); padding: 15px; border-radius: 10px; border: 1px solid #9BC63B; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN ACCESO SOBERANO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#9BC63B;'>SISTEMA NEXUS | SOVEREIGN GATEWAY</h1>", unsafe_allow_html=True)
    col_sec = st.columns([1,1,1])
    with col_sec[1]:
        clave = st.text_input("PASSWORD INSTITUCIONAL", type="password")
        if st.button("AUTENTICAR", use_container_width=True):
            if clave == "Serenity2026":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- MENÚ LATERAL ---
menu = st.sidebar.radio("CENTRO DE CONTROL", [
    "INICIO", "RED DE FAROS", "DASHBOARD IA", "CUMPLIMIENTO LEGAL", "UBICACIÓN & MAPAS"
])

if menu == "INICIO":
    st.markdown("<h1 style='text-align:center; font-size:3.5rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.info("Plataforma Soberana de Infraestructura Ambiental Crítica")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Quiénes Somos")
        st.write("Líderes en el Internet de la Naturaleza (IoN), integrando biometría y blockchain para la regeneración del Valle del Cauca.")
    with col2:
        st.subheader("Misión Institucional")
        st.write("Convertir la conservación en un activo digital inmutable y verificable para el sector corporativo global.")

elif menu == "RED DE FAROS":
    st.title("🛰️ Monitoreo Perimetral Nexus")
    faros = ["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara", "REX GEMINI"]
    
    cols = st.columns(len(faros))
    for i, f in enumerate(faros):
        if cols[i].button(f, use_container_width=True):
            st.session_state.f_activo = f

    if st.session_state.f_activo:
        st.subheader(f"Feed en Vivo: Nodo {st.session_state.f_activo}")
        c_v = st.columns(4)
        for j in range(8):
            with c_v[j % 4]:
                st.image("https://via.placeholder.com/300x200.png?text=SENSOR+CAM+"+str(j+1), caption=f"Cam {j+1}")

elif menu == "DASHBOARD IA":
    st.title("🤖 Inteligencia de Datos")
    col_m = st.columns(4)
    col_m[0].metric("Biodiversidad", "87%", "+2%")
    col_m[1].metric("CO2 Capturado", "1.2 Ton", "+15kg")
    col_m[2].metric("Humedad", "64%", "Óptimo")
    col_m[3].metric("Integridad", "100%", "Safe")
    
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Biofonia', 'Fauna', 'Carbono'])
    st.line_chart(chart_data)

elif menu == "CUMPLIMIENTO LEGAL":
    st.title("⚖️ Gestión de Ley 2173 & 2169")
    with st.container(border=True):
        emp = st.text_input("Razón Social")
        nit = st.text_input("NIT")
        if st.button("Generar Vademécum de Cumplimiento"):
            h = hashlib.sha256(emp.encode()).hexdigest()[:12].upper()
            pdf = generar_pdf_corporativo(emp, 200, h, es_vademecum=True)
            st.download_button("Descargar Reporte Legal", data=pdf, file_name=f"Vademecum_{emp}.pdf")

elif menu == "UBICACIÓN & MAPAS":
    st.title("🌍 Geovigilancia de Activos")
    m = folium.Map(location=[3.65, -76.65], zoom_start=11)
    folium.Marker([3.656, -76.689], popup="Faro Principal Dagua", icon=folium.Icon(color='green', icon='leaf')).add_to(m)
    st_folium(m, width=1200, height=500)




































































































































































































































































































































































































































































































































































































































































































































































































