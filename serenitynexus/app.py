# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime
import io
import os

# --- LIBRERÍAS EXTENDIDAS ---
# Si te sale error aquí, recuerda instalar: pip install folium streamlit-folium reportlab
import folium
from streamlit_folium import st_folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black

# --- CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌳", layout="wide")
VERDE_SERENITY = HexColor("#2E7D32")

# --- GESTIÓN DE ESTADO (MEMORIA TEMPORAL) ---
if 'total_protegido' not in st.session_state: st.session_state.total_protegido = 87.0
if 'donaciones_recibidas' not in st.session_state: st.session_state.donaciones_recibidas = 0
if 'estado_gemini' not in st.session_state: st.session_state.estado_gemini = "Latente"
if 'auth' not in st.session_state: st.session_state.auth = False
if 'f_activo' not in st.session_state: st.session_state.f_activo = None

# --- FUNCIÓN GENERADORA DE PDF (CON LOGO) ---
def generar_pdf_certificado(nombre, monto):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # 1. Marco y Fondo
    c.setStrokeColor(VERDE_SERENITY)
    c.setLineWidth(5)
    c.rect(0.3*inch, 0.3*inch, 7.9*inch, 10.4*inch)
    
    # 2. INTENTO DE CARGAR LOGO
    # Busca 'logo_serenity.png'. Si no está, dibuja un círculo verde.
    try:
        if os.path.exists("logo_serenity.png"):
            c.drawImage("logo_serenity.png", 3.5*inch, 9.0*inch, width=1.5*inch, height=1.5*inch, mask='auto')
        else:
            # Logo Placeholder
            c.setFillColor(VERDE_SERENITY)
            c.circle(4.25*inch, 9.7*inch, 40, fill=1)
            c.setFillColor(black)
            c.drawCentredString(4.25*inch, 9.65*inch, "LOGO")
    except:
        pass 

    # 3. Textos del Diploma
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(VERDE_SERENITY)
    c.drawCentredString(4.25*inch, 8.5*inch, "CERTIFICADO DE DONACIÓN")
    
    c.setFont("Helvetica", 14)
    c.setFillColor(black)
    c.drawCentredString(4.25*inch, 7.5*inch, "SERENITY HUB S.A.S. BIC")
    c.drawCentredString(4.25*inch, 7.0*inch, f"Reconoce a: {nombre.upper()}")
    c.drawCentredString(4.25*inch, 6.5*inch, f"Por su valioso aporte de ${monto:,.0f} USD")
    c.drawCentredString(4.25*inch, 6.0*inch, f"Destinado a la regeneración del KBA Bosque San Antonio")
    
    # 4. Firma
    c.setLineWidth(1)
    c.line(2.5*inch, 4.8*inch, 6.0*inch, 4.8*inch)
    c.drawCentredString(4.25*inch, 4.6*inch, "Jorge Carvajal")
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(4.25*inch, 4.4*inch, "Administrador Serenity S.A.S. BIC")
    
    # 5. Pie de página
    c.setFont("Helvetica", 8)
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    folio = f"SH-{random.randint(1000,9999)}"
    c.drawCentredString(4.25*inch, 1.0*inch, f"Folio: {folio} | Fecha: {fecha_hoy} | Verificado por Sistema Nexus IA")
    
    c.save()
    buffer.seek(0)
    return buffer

# --- CSS (ESTILOS VISUALES) ---
st.markdown("""
    <style>
        .stApp { 
            background-image: linear-gradient(rgba(5, 10, 4, 0.8), rgba(5, 10, 4, 0.9)), 
            url('https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1920&q=80');
            background-size: cover; background-position: center; background-attachment: fixed;
            color: #e8f5e9; font-family: 'Montserrat', sans-serif; 
        }
        label, .stMarkdown p, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, .stMetricLabel { 
            color: white !important; font-weight: 500; 
        }
        [data-testid="stSidebar"] { background-color: rgba(10, 20, 8, 0.9) !important; backdrop-filter: blur(10px); }
        h1, h2, h3 { color: #9BC63B !important; text-shadow: 2px 2px 4px #000; }
        
        .stButton>button { background-color: #2E7D32; color: white; border: 1px solid #9BC63B; border-radius: 8px; width: 100%; font-weight: bold; }
        .stButton>button:hover { background-color: #9BC63B; color: black; box-shadow: 0 0 15px #9BC63B; }
        
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; height: 100%; }
        .faro-gemini { border: 2px solid #4285F4; padding: 15px; border-radius: 10px; background: rgba(66, 133, 244, 0.2); text-align: center; box-shadow: 0 0 15px #4285F4; }
        .cam-grid { background: #000; border: 1px solid #2E7D32; height









































