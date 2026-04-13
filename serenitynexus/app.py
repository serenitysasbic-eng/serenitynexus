# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import io
import os
import pyotp
from datetime import datetime

# --- LIBRERÍAS DE MAPAS Y REPORTES ---
import folium
from streamlit_folium import st_folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black

# --- CONFIGURACIÓN E IDENTIDAD SOVEREIGN ---
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌐", layout="wide")

# Colores Corporativos
VERDE_SERENITY = HexColor("#2E7D32")
VERDE_LIMA_NEXUS = HexColor("#9BC63B")
AZUL_IA = HexColor("#4285F4")

# --- FUNCIONES DE GENERACIÓN DE DOCUMENTOS (UNIFICADAS) ---

def generar_pdf_diagnostico(empresa, nit, impacto, hash_id, estudio_data=None, total_ton=0, faro_nombre="Red Nexus"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Membrete Institucional
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
    c.drawString(1*inch, 8.4*inch, f"SERIAL DE INTEGRIDAD: {hash_id}")
    c.drawString(1*inch, 8.2*inch, f"NODO VALIDADOR: {faro_nombre}")

    # Si hay datos de estudio, crear tabla
    if estudio_data:
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(VERDE_SERENITY)
        c.drawString(1*inch, 7.8*inch, "RESULTADOS DEL ESTUDIO (FACTORES UPME COLOMBIA):")
        
        c.setFont("Helvetica", 9)
        c.setFillColor(black)
        y_pos = 7.5
        for concepto, valor in estudio_data.items():
            c.drawString(1.2*inch, y_pos*inch, f"• {concepto}:")
            c.drawRightString(7*inch, y_pos*inch, f"{valor}")
            y_pos -= 0.22

    # Comparativa Sectorial (Gráfica simple)
    if total_ton > 0:
        y_graf = 5.0
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, y_graf*inch, "COMPARATIVA SECTORIAL (TON CO2E):")
        
        ancho_max = 2.5 * inch
        promedio_sector = total_ton * 1.15
        
        c.setFillColor(VERDE_LIMA_NEXUS)
        c.rect(3*inch, (y_graf-0.4)*inch, (total_ton/(total_ton+promedio_sector))*ancho_max*2, 0.2*inch, fill=1)
        c.setFillColor(black)
        c.drawString(1.2*inch, (y_graf-0.35)*inch, "Su Empresa")

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
    titulo = "VADEMÉCUM TÉCNICO LEGAL" if es_vademecum else "CERTIFICADO DE COMPENSACIÓN"
    c.drawCentredString(4.25*inch, 9*inch, titulo)

    c.setFont("Helvetica", 12)
    c.setFillColor(black)
    c.drawString(1*inch, 8.2*inch, f"RAZÓN SOCIAL: {empresa.upper()}")
    c.drawString(1*inch, 8.0*inch, f"ID SEGURIDAD: {hash_id}")

    text_object = c.beginText(1*inch, 6.5*inch)
    text_object.setFont("Helvetica", 11)
    text_object.setLeading(14)
    
    if es_vademecum:
        lineas = ["Certifica el cumplimiento de Leyes 2173, 2169 y 2111.", 
                  "Trazabilidad absoluta mediante Red de Faros Serenity."]
    else:
        lineas = [f"Se certifica la protección de {impacto} individuos forestales.",
                  "Registro inmutable en la arquitectura Nexus Global."]
        
    for linea in lineas:
        text_object.textLine(linea)
    c.drawText(text_object)

    c.save()
    buffer.seek(0)
    return buffer

# --- GESTIÓN DE ESTADO ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'f_activo' not in st.session_state: st.session_state.f_activo = None

# --- ESTILOS CSS ---
st.markdown("""
    <style>
        .stApp { background-color: #050a04; color: #e8f5e9; }
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; }
        .stButton>button { background-color: #2E7D32; color: white; border-radius: 8px; font-weight: bold; }
        .stButton>button:hover { background-color: #9BC63B; color: black; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>SISTEMA SOVEREIGN | NEXUS</h1>", unsafe_allow_html=True)
    col_sec = st.columns([1,1,1])
    with col_sec[1]:
        clave = st.text_input("PASSWORD DE ACCESO", type="password")
        if st.button("INGRESAR"):
            if clave == "Serenity2026":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- NAVEGACIÓN ---
menu = st.sidebar.radio("CENTRO DE CONTROL", [
    "INICIO", "RED DE FAROS", "DASHBOARD IA", "CUMPLIMIENTO LEGAL", "GEOPOSICIONAMIENTO"
])

if menu == "INICIO":
    st.markdown("<h1 style='text-align:center;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.info("Ecosistema Phygital de Conservación Biométrica - Valle del Cauca")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Misión")
        st.write("Regenerar el tejido ecológico mediante transparencia tecnológica.")
    with col2:
        st.subheader("Visión 2030")
        st.write("Liderar el Internet de la Naturaleza a nivel global.")

elif menu == "RED DE FAROS":
    st.title("🛰️ Monitoreo Perimetral")
    faros = ["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara", "REX GEMINI"]
    
    cols = st.columns(3)
    for i, f in enumerate(faros):
        with cols[i % 3]:
            if st.button(f"Conectar {f}", use_container_width=True):
                st.session_state.f_activo = f
    
    if st.session_state.f_activo:
        st.success(f"Transmitiendo desde: {st.session_state.f_activo}")
        # Simulación de 8 cámaras
        c_grid = st.columns(4)
        for j in range(8):
            with c_grid[j % 4]:
                st.image("https://via.placeholder.com/150x100.png?text=CAM+"+str(j+1))

elif menu == "GEOPOSICIONAMIENTO":
    st.subheader("🌍 Infraestructura en Tiempo Real")
    m = folium.Map(location=[3.65, -76.65], zoom_start=11)
    # Ejemplo de punto
    folium.Marker([3.656, -76.689], popup="Faro Alfa - Dagua", icon=folium.Icon(color='green')).add_to(m)
    st_folium(m, width=1000, height=500)

elif menu == "CUMPLIMIENTO LEGAL":
    st.title("⚖️ Gestión de Ley 2173")
    emp = st.text_input("Razón Social")
    nit = st.text_input("NIT")
    if st.button("Generar Reporte de Cumplimiento"):
        h = hashlib.sha256(emp.encode()).hexdigest()[:10].upper()
        pdf = generar_pdf_corporativo(emp, 100, h, es_vademecum=True)
        st.download_button("Descargar Vademécum", data=pdf, file_name="Reporte_Legal.pdf")









































































































































































































































































































































































































































































































