# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime
from PIL import Image
import io

# --- LIBRERÍAS NUEVAS PARA MAPAS Y PDF ---
import folium
from streamlit_folium import st_folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black

# --- CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌳", layout="wide")
VERDE_SERENITY = HexColor("#2E7D32")

# --- GESTIÓN DE ESTADO (BASE DE DATOS SIMULADA) ---
if 'total_protegido' not in st.session_state:
    st.session_state.total_protegido = 80.0  # Hectáreas iniciales (Monte Guadua)
if 'donaciones_recibidas' not in st.session_state:
    st.session_state.donaciones_recibidas = 0
if 'estado_gemini' not in st.session_state:
    st.session_state.estado_gemini = "Latente"
if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- LÓGICA DE NEGOCIO: GENERADOR PDF REAL ---
def generar_pdf_certificado(nombre, monto):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    # Estética de Diploma
    c.setStrokeColor(VERDE_SERENITY)
    c.setLineWidth(5)
    c.rect(0.3*inch, 0.3*inch, 7.9*inch, 10.4*inch)
    
    # Encabezado
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(VERDE_SERENITY)
    c.drawCentredString(4.25*inch, 8.5*inch, "CERTIFICADO DE DONACIÓN")
    
    # Cuerpo
    c.setFont("Helvetica", 14)
    c.setFillColor(black)
    c.drawCentredString(4.25*inch, 7.5*inch, "SERENITY HUB S.A.S. BIC")
    c.drawCentredString(4.25*inch, 7.0*inch, f"Otorgado a: {nombre.upper()}")
    c.drawCentredString(4.25*inch, 6.5*inch, f"Por su aporte de ${monto:,.0f} USD a la regeneración biológica.")
    c.drawCentredString(4.25*inch, 6.0*inch, f"KBA Bosque San Antonio - Dagua, Valle del Cauca")
    
    # Firma
    c.drawCentredString(4.25*inch, 5.0*inch, "__________________________")
    c.drawCentredString(4.25*inch, 4.7*inch, "Jorge Carvajal")
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(4.25*inch, 4.5*inch, "Administrador Serenity S.A.S. BIC")
    
    # Pie de página
    c.setFont("Helvetica", 8)
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    c.drawCentredString(4.25*inch, 1.0*inch, f"Generado por Serenity Nexus Global | {fecha_hoy} | Verificado IA")
    
    c.save()
    buffer.seek(0)
    return buffer

# --- DISEÑO VISUAL Y ESTILOS (CSS) ---
st.markdown("""
    <style>
        .stApp { 
            background-image: linear-gradient(rgba(5, 10, 4, 0.7), rgba(5, 10, 4, 0.8)), 
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
        
        .metric-card { background: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; border: 1px solid #9BC63B; text-align: center; }
        .faro-card { border: 1px solid #9BC63B; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.6); text-align: center; height: 100%; }
        .faro-gemini { border: 2px solid #4285F4; padding: 15px; border-radius: 10px; background: rgba(66, 133, 244, 0.2); text-align: center; box-shadow: 0 0 15px #4285F4; }
        .cam-grid { background: #000; border: 1px solid #2E7D32; height: 80px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #ff0000; border-radius: 5px; }
        
        /* DIPLOMA PREVISUALIZACIÓN */
        .diploma-preview { 
            background: white !important; color: black !important; padding: 30px; 
            border: 10px double #2E7D32; text-align: center; margin: auto;
        }
        
        .logo-container { background: white; padding: 8px; border-radius: 5px; display: inline-block; margin: 3px; vertical-align: middle; }
    </style>
""", unsafe_allow_html=True)

# --- SEGURIDAD ---
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top: 50px;'><h1>SISTEMA NEXUS | SERENITY</h1></div>", unsafe_allow_html=True)
    col_sec = st.columns([1,1,1])
    with col_sec[1]:
        clave = st.text_input("PASSWORD ADMIN", type="password")
        if st.button("INGRESAR"):
            if clave == "Serenity2026":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- NAVEGACIÓN ---
menu = st.sidebar.radio("CENTRO DE CONTROL", [
    "INICIO", "RED DE FAROS (7 NODOS)", "DASHBOARD ESTADÍSTICO IA", "GESTIÓN LEY 2173 (EMPRESAS)",
    "SUSCRIPCIONES", "DONACIONES Y CERTIFICADO", "LOGÍSTICA AEROLÍNEAS", "UBICACIÓN & MAPAS"
])

# 1. INICIO
if menu == "INICIO":
    st.markdown("<h1 style='text-align:center; font-size:4rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold;'>SISTEMA REGENERATIVO BIOMÉTRICO KBA</p>", unsafe_allow_html=True)
    
    # Audio
    st.components.v1.html("""
        <audio id="audio_earth" src="sonido_Earth.mp3" loop></audio>
        <div style="text-align:center; margin-top:30px;">
            <button onclick="document.getElementById('audio_earth').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:20px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:16px;">🔊 ACTIVAR SONIDO GLOBAL EARTH</button>
        </div>
    """, height=150)
    
    st.markdown("### 🏛️ Estructura de Propiedad")
    st.info("Sandra Patricia Agredo Muñoz (40%) | Tatiana Arcila Ferreira (60%) | Admin: Jorge Carvajal")

# 2. RED DE FAROS
elif menu == "RED DE FAROS (7 NODOS)":
    st.title("🛰️ Monitoreo Perimetral")
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown("<div class='faro-card'><h3>FARO HALCÓN</h3></div>", unsafe_allow_html=True); st.button("Conectar Halcón")
    with c2: st.markdown("<div class='faro-card'><h3>FARO COLIBRÍ</h3></div>", unsafe_allow_html=True); st.button("Conectar Colibrí")
    with c3: st.markdown("<div class='faro-card'><h3>FARO RANA</h3></div>", unsafe_allow_html=True); st.button("Conectar Rana")
    
    st.write("")
    c4, c5, c6 = st.columns(3)
    with c4: st.markdown("<div class='faro-card'><h3>FARO VENADO</h3></div>", unsafe_allow_html=True); st.button("Conectar Venado")
    with c5: st.markdown("<div class='faro-card'><h3>FARO TIGRILLO</h3></div>", unsafe_allow_html=True); st.button("Conectar Tigrillo")
    with c6: st.markdown("<div class='faro-card'><h3>FARO CAPIBARA</h3></div>", unsafe_allow_html=True); st.button("Conectar Capibara")

    st.write("---")
    col_gemini = st.columns([1,2,1])
    with col_gemini[1]:
        st.markdown(f"<div class='faro-gemini'><h3>✨ FARO GEMINI ✨</h3><p>Estado: {st.session_state.estado_gemini}</p></div>", unsafe_allow_html=True)
        if st.button("ACTIVAR NÚCLEO GEMINI"): 
            st.session_state.f_activo = "GEMINI"
            st.session_state.estado_gemini = "ACTIVO - EMITIENDO"

    if "f_activo" in st.session_state:
        st.divider()
        st.header(f"📡 TRANSMISIÓN EN VIVO: {st.session_state.f_activo}")
        c_cols = st.columns(4)
        for j in range(8):
            with c_cols[j % 4]: st.markdown(f"<div class='cam-grid'>CAM {j+1}<br>● LIVE</div>", unsafe_allow_html=True)

# 3. DASHBOARD ESTADÍSTICO IA
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("📊 Análisis de Inteligencia Biológica")
    m = st.columns(4)
    m[0].markdown(f"<div class='metric-card'><h3>Especies</h3><h1>1,248</h1></div>", unsafe_allow_html=True)
    m[1].markdown(f"<div class='metric-card'><h3>Hectáreas</h3><h1>{st.session_state.total_protegido}</h1></div>", unsafe_allow_html=True)
    m[2].markdown(f"<div class='metric-card'><h3>Inversiones</h3><h1>{st.session_state.donaciones_recibidas}</h1></div>", unsafe_allow_html=True)
    m[3].markdown(f"<div class='metric-card'><h3>Salud</h3><h1>98%</h1></div>", unsafe_allow_html=True)
    st.bar_chart(pd.DataFrame({'Detecciones': [120, 450, 300, 80, 45, 110, 950]}, index=["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara", "GEMINI"]))

# 4. GESTIÓN LEY 2173
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Cumplimiento Ley 2173 de 2021")
    c1, c2 = st.columns(2)
    with c1: nit = st.text_input("Ingrese NIT de la Empresa")
    with c2: logo_emp = st.file_uploader("Suba Logo Corporativo", type=["png", "jpg"])
    if nit:
        st.markdown(f"<div class='metric-card' style='text-align:left;'><h3>EMPRESA ACTIVA: NIT {nit}</h3><p>🌳 150 Árboles Monitoreados</p></div>", unsafe_allow_html=True)
        st.download_button("⬇️ DESCARGAR CERTIFICADO LEY 2173", data=f"Reporte NIT {nit}", file_name=f"Certificado_Ley2173.txt")

# 5. SUSCRIPCIONES
elif menu == "SUSCRIPCIONES":
    st.title("💳 Planes de Apoyo Regenerativo")
    p1, p2, p3 = st.columns(3)
    with p1: 
        st.markdown("<div class='faro-card'><h3>Plan Semilla</h3><h2>$5 USD</h2><p>1 Faro / 1 Mes</p></div>", unsafe_allow_html=True)
    with p2: 
        st.markdown("<div class='faro-card'><h3>Plan Guardián</h3><h2>$25 USD</h2><p>6 Faros / 1 Mes</p></div>", unsafe_allow_html=True)
    with p3: 
        st.markdown("<div class='faro-card' style='border-color:#D4AF37;'><h3>Plan Halcón</h3><h2>$200 USD</h2><p>6 Faros / 6 Meses</p></div>", unsafe_allow_html=True)

# 6. DONACIONES Y CERTIFICADO (PDF REAL)
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("🌳 Generador de Diploma Oficial")
    st.markdown("Genera un diploma PDF firmado digitalmente por la administración.")
    
    colA, colB = st.columns([1, 1])
    with colA:
        with st.container(border=True):
            nombre_d = st.text_input("Nombre Completo del Donante")
            monto_d = st.number_input("Monto Donación (USD)", min_value=1)
            if st.button("✨ PROCESAR DONACIÓN"): 
                if nombre_d:
                    st.session_state.donaciones_recibidas += 1
                    st.session_state.estado_gemini = "ACTIVO - EMITIENDO" # Activa el faro en el mapa
                    st.session_state.pdf_buffer = generar_pdf_certificado(nombre_d, monto_d)
                    st.balloons()
                    st.success("¡Certificado generado y Faro Gemini Activado!")
                else:
                    st.warning("Ingrese un nombre.")
    
    with colB:
        if 'pdf_buffer' in st.session_state:
            # Previsualización estilo diploma
            st.markdown(f"""
                <div class="diploma-preview">
                    <h2 style="color:#2E7D32;">CERTIFICADO DE DONACIÓN</h2>
                    <h3>{nombre_d.upper()}</h3>
                    <p>Monto: ${monto_d} USD</p>
                    <hr>
                    <p style="font-size:10px;">VISTA PREVIA - DESCARGUE EL PDF OFICIAL ABAJO</p>
                </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label="📥 DESCARGAR DIPLOMA OFICIAL (PDF)",
                data=st.session_state.pdf_buffer,
                file_name=f"Diploma_Serenity_{nombre_d}.pdf",
                mime="application/pdf"
            )

# 7. LOGÍSTICA AEROLÍNEAS
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Rutas Globales")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Europa / Asia")
        st.markdown("<div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/4/44/Iberia_Logo.svg' width='80'></div> <b>Iberia</b><br><div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Lufthansa_Logo_2018.svg' width='80'></div> <b>Lufthansa</b>", unsafe_allow_html=True)
    with col2:
        st.subheader("América")
        st.markdown("<div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/d/df/Avianca_logo.svg' width='80'></div> <b>Avianca</b><br><div class='logo-container'><img src='https://upload.wikimedia.org/wikipedia/commons/0/00/American_Airlines_logo_2013.svg' width='80'></div> <b>American Airlines</b>", unsafe_allow_html=True)

# 8. UBICACIÓN & MAPAS (FOLIUM INTEGRADO)
elif menu == "UBICACIÓN & MAPAS":
    st.title("📍 Ubicación Hacienda Serenity (Dagua)")
    
    # Lógica de color dinámico para Gemini
    color_gemini_map = "green" if st.session_state.estado_gemini == "ACTIVO - EMITIENDO" else "orange"
    
    # Crear Mapa
    m = folium.Map(location=[3.455, -76.655], zoom_start=13, tiles="cartodbpositron")
    
    # 1. Marcador Gemini
    folium.Marker(
        [3.460, -76.660],
        popup=f"FARO GEMINI: {st.session_state.estado_gemini}",
        icon=folium.Icon(color=color_gemini_map, icon='bolt', prefix='fa')
    ).add_to(m)
    
    # 2. Polígono Monte Guadua (80 Ha)
    folium.Polygon(
        locations=[[3.45, -76.67], [3.47, -76.67], [3.47, -76.64], [3.45, -76.64]],
        color="darkgreen",
        fill=True,
        fill_opacity=0.4,
        tooltip="Hacienda Monte Guadua: 80 Ha Protegidas"
    ).add_to(m)
    
    # 3. Villa Michelle
    folium.CircleMarker(
        location=[3.445, -76.645],
        radius=10,
        color="blue",
        fill=True,
        fill_color="blue",
        tooltip="Finca Villa Michelle (Sede Administrativa)"
    ).add_to(m)
    
    st_folium(m, width="100%", height=600)
    st.caption("Mapa interactivo: Azul=Sede | Verde=Bosque Protegido | Naranja/Verde=Faro Gemini")







































