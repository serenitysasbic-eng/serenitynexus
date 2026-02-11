# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
from datetime import datetime
import io
import os

# --- LIBRERÍAS EXTENDIDAS ---
import folium
from streamlit_folium import st_folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black

# --- CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌿", layout="wide")
VERDE_SERENITY = HexColor("#2E7D32")

# --- GESTIÓN DE ESTADO ---
if 'total_protegido' not in st.session_state: st.session_state.total_protegido = 87.0
if 'donaciones_recibidas' not in st.session_state: st.session_state.donaciones_recibidas = 0
if 'estado_gemini' not in st.session_state: st.session_state.estado_gemini = "Latente"
if 'auth' not in st.session_state: st.session_state.auth = False
if 'f_activo' not in st.session_state: st.session_state.f_activo = None

# --- FUNCIÓN GENERADORA DE PDF ---
def generar_pdf_certificado(nombre, monto):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setStrokeColor(VERDE_SERENITY)
    c.setLineWidth(5)
    c.rect(0.3*inch, 0.3*inch, 7.9*inch, 10.4*inch)
    try:
        if os.path.exists("logo_serenity.png"):
            c.drawImage("logo_serenity.png", 3.5*inch, 9.0*inch, width=1.5*inch, height=1.5*inch, mask='auto')
        else:
            c.setFillColor(VERDE_SERENITY)
            c.circle(4.25*inch, 9.7*inch, 40, fill=1)
            c.setFillColor(black)
            c.drawCentredString(4.25*inch, 9.65*inch, "LOGO")
    except:
        pass 

    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(VERDE_SERENITY)
    c.drawCentredString(4.25*inch, 8.5*inch, "CERTIFICADO DE DONACIÓN")
    c.setFont("Helvetica", 14)
    c.setFillColor(black)
    c.drawCentredString(4.25*inch, 7.5*inch, "SERENITY HUB S.A.S. BIC")
    c.drawCentredString(4.25*inch, 7.0*inch, f"Reconoce a: {nombre.upper()}")
    c.drawCentredString(4.25*inch, 6.5*inch, f"Por su valioso aporte de ${monto:,.0f} USD")
    c.drawCentredString(4.25*inch, 6.0*inch, f"Destinado a la regeneración del KBA Bosque San Antonio")
    c.setLineWidth(1)
    c.line(2.5*inch, 4.8*inch, 6.0*inch, 4.8*inch)
    c.drawCentredString(4.25*inch, 4.6*inch, "Jorge Carvajal")
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(4.25*inch, 4.4*inch, "Administrador Serenity S.A.S. BIC")
    c.setFont("Helvetica", 8)
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    folio = f"SH-{random.randint(1000,9999)}"
    c.drawCentredString(4.25*inch, 1.0*inch, f"Folio: {folio} | Fecha: {fecha_hoy} | Verificado por Sistema Nexus IA")
    c.save()
    buffer.seek(0)
    return buffer

# --- CSS (ESTILOS) ---
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
        .cam-grid { background: #000; border: 1px solid #2E7D32; height: 80px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #ff0000; border-radius: 5px; }
        .metric-card { background: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; border: 1px solid #9BC63B; text-align: center; }
        .airline-grid { 
            background: white; 
            padding: 10px; 
            border-radius: 10px; 
            text-align: center; 
            margin-bottom: 10px;
            height: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }
        .airline-grid img { max-width: 90%; max-height: 70px; object-fit: contain; }
        .airline-grid p { color: black !important; font-size: 0.7rem; font-weight: bold; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN ---
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

# --- BUSCA ESTA SECCIÓN Y ACTUALIZA LA LISTA ---
menu = st.sidebar.radio("CENTRO DE CONTROL", [
    "INICIO", 
    "RED DE FAROS (7 NODOS)", 
    "DASHBOARD ESTADÍSTICO IA", 
    "GESTIÓN LEY 2173 (EMPRESAS)",
    "SUSCRIPCIONES", 
    "BILLETERA CRYPTO (WEB3)",  
    "DONACIONES Y CERTIFICADO", 
    "LOGÍSTICA AEROLÍNEAS", 
    "UBICACIÓN & MAPAS"
])

# 1. INICIO - RESTAURACIÓN COMPLETA
if menu == "INICIO":
    # --- LOGO CENTRADO ---
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        if os.path.exists("logo_serenity.png"):
            st.image("logo_serenity.png", use_container_width=True)
        else:
            st.markdown("<h1 style='text-align:center; color:#9BC63B;'>SERENITY NEXUS GLOBAL</h1>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; font-size:3.5rem;'>Serenity Nexus Global</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; color:#9BC63B; font-weight:bold;'>SISTEMA REGENERATIVO BIOMÉTRICO KBA</p>", unsafe_allow_html=True)
    
    # --- AUDIO EARTH ---
    st.components.v1.html("""
        <audio id="audio_earth" src="sonido_Earth.mp3" loop></audio>
        <div style="text-align:center; margin-top:20px;">
            <button onclick="document.getElementById('audio_earth').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:10px 20px; border-radius:10px; cursor:pointer; font-weight:bold;">🔊 ACTIVAR SONIDO GLOBAL EARTH</button>
        </div>
    """, height=100)

    # --- DATOS DE GOBERNANZA ---
    st.info("Sandra Patricia Agredo Muñoz (40%) | Tatiana Arcila Ferreira (60%) | Admin: Jorge Carvajal")

    st.divider()

    # --- QUIÉNES SOMOS, MISIÓN Y VISIÓN ---
    col_inf1, col_inf2 = st.columns(2)
    
    with col_inf1:
        st.subheader("🌿 QUIÉNES SOMOS / WHO WE ARE")
        st.write("Serenity Nexus Global es la primera plataforma Phygital (Física + Digital) del Valle del Cauca que integra la conservación ambiental con tecnología Blockchain e Inteligencia Artificial, transformando la protección de la biodiversidad en un activo digital tangible.")

    with col_inf2:
        st.subheader("🎯 NUESTRA MISIÓN / OUR MISSION")
        st.write("Regenerar el tejido ecológico y social mediante un modelo de negocio sostenible que permita a empresas y personas compensar su huella ambiental a través de la tecnología y la transparencia.")

    st.write("---")
    
    col_inf3, col_inf4 = st.columns([1, 2])
    with col_inf3:
        st.subheader("🚀 NUESTRA VISIÓN / OUR VISION")
    with col_inf4:
        st.write("Ser el referente mundial del Internet de la Naturaleza para 2030, liderando la valorización de los servicios ecosistémicos mediante nuestra red de Faros inteligentes y el token $SNG.")

    st.info("📍 Ubicación del Proyecto: Dagua y Felidia, Valle del Cauca - Hacienda Monte Guadua & Finca Villa Michelle.")

# 2. RED DE FAROS
elif menu == "RED DE FAROS (7 NODOS)":
    st.title("📡 Monitoreo Perimetral")
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.markdown("<div class='faro-card'><h3>FARO HALCÓN</h3></div>", unsafe_allow_html=True)
        if st.button("Conectar Halcón"): st.session_state.f_activo = "Halcón"
    with c2: 
        st.markdown("<div class='faro-card'><h3>FARO COLIBRÍ</h3></div>", unsafe_allow_html=True)
        if st.button("Conectar Colibrí"): st.session_state.f_activo = "Colibrí"
    with c3: 
        st.markdown("<div class='faro-card'><h3>FARO RANA</h3></div>", unsafe_allow_html=True)
        if st.button("Conectar Rana"): st.session_state.f_activo = "Rana"
    
    st.write("")
    c4, c5, c6 = st.columns(3)
    with c4: 
        st.markdown("<div class='faro-card'><h3>FARO VENADO</h3></div>", unsafe_allow_html=True)
        if st.button("Conectar Venado"): st.session_state.f_activo = "Venado"
    with c5: 
        st.markdown("<div class='faro-card'><h3>FARO TIGRILLO</h3></div>", unsafe_allow_html=True)
        if st.button("Conectar Tigrillo"): st.session_state.f_activo = "Tigrillo"
    with c6: 
        st.markdown("<div class='faro-card'><h3>FARO CAPIBARA</h3></div>", unsafe_allow_html=True)
        if st.button("Conectar Capibara"): st.session_state.f_activo = "Capibara"

    st.write("---")
    col_gemini = st.columns([1,2,1])
    with col_gemini[1]:
        st.markdown(f"<div class='faro-gemini'><h3>🤖 FARO GEMINI 🤖</h3><p>Estado: {st.session_state.estado_gemini}</p></div>", unsafe_allow_html=True)
        if st.button("ACTIVAR NÚCLEO GEMINI"): 
            st.session_state.f_activo = "GEMINI"
            st.session_state.estado_gemini = "ACTIVO - EMITIENDO"

    if st.session_state.f_activo:
        st.divider()
        color_titulo = "#4285F4" if st.session_state.f_activo == "GEMINI" else "#9BC63B"
        st.markdown(f"<h2 style='color:{color_titulo}; text-align:center;'>📹 TRANSMISIÓN EN VIVO: {st.session_state.f_activo.upper()}</h2>", unsafe_allow_html=True)
        c_cols = st.columns(4)
        for j in range(8):
            label = "IA-ANALYSIS" if st.session_state.f_activo == "GEMINI" else "LIVE"
            with c_cols[j % 4]: st.markdown(f"<div class='cam-grid'>CAM {j+1}<br>📡 {label}</div>", unsafe_allow_html=True)
        
        st.subheader("Bioacústica")
        m_cols = st.columns(4)
        for k in range(4):
            val = random.randint(85,99) if st.session_state.f_activo == "GEMINI" else random.randint(40,90)
            with m_cols[k]: st.markdown(f"<div style='background:rgba(155,198,59,0.2); border:1px solid #2E7D32; padding:10px; border-radius:5px; text-align:center;'><b>MIC {k+1}</b><br><span style='color:#9BC63B;'>||||| {val}%</span></div>", unsafe_allow_html=True)

# 3. DASHBOARD
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("📊 Análisis de Inteligencia Biológica")
    m = st.columns(4)
    m[0].markdown(f"<div class='metric-card'><h3>Especies</h3><h1>1,248</h1></div>", unsafe_allow_html=True)
    m[1].markdown(f"<div class='metric-card'><h3>Hectáreas</h3><h1>{st.session_state.total_protegido}</h1></div>", unsafe_allow_html=True)
    m[2].markdown(f"<div class='metric-card'><h3>Inversiones</h3><h1>{st.session_state.donaciones_recibidas}</h1></div>", unsafe_allow_html=True)
    m[3].markdown(f"<div class='metric-card'><h3>Salud</h3><h1>98%</h1></div>", unsafe_allow_html=True)
    st.bar_chart(pd.DataFrame({'Detecciones': [120, 450, 300, 80, 45, 110, 950]}, index=["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara", "GEMINI"]))

# 4. LEY 2173
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Cumplimiento Ley 2173")
    c1, c2 = st.columns(2)
    with c1: nit = st.text_input("Ingrese NIT de la Empresa")
    with c2: logo_emp = st.file_uploader("Suba Logo Corporativo", type=["png", "jpg"])
    if nit:
        st.markdown(f"<div class='metric-card' style='text-align:left;'><h3>EMPRESA ACTIVA: NIT {nit}</h3><p>🌳 150 Árboles Monitoreados</p></div>", unsafe_allow_html=True)
        st.download_button("📄 DESCARGAR CERTIFICADO LEY 2173", data=f"Reporte NIT {nit}", file_name=f"Certificado_Ley2173.txt")

# 5. SUSCRIPCIONES
elif menu == "SUSCRIPCIONES":
    st.title("💎 Planes de Apoyo Regenerativo")
    p1, p2, p3 = st.columns(3)
    with p1: 
        st.markdown("<div class='faro-card'><h3>Plan Semilla</h3><h2>$5 USD</h2><p>1 Faro / 1 Mes</p></div>", unsafe_allow_html=True)
        if st.button("SUSCRIBIRSE SEMILLA"): st.success("Procesando pago Semilla...")
    with p2: 
        st.markdown("<div class='faro-card'><h3>Plan Guardián</h3><h2>$25 USD</h2><p>6 Faros / 1 Mes</p></div>", unsafe_allow_html=True)
        if st.button("SUSCRIBIRSE GUARDIÁN"): st.success("Procesando pago Guardián...")
    with p3: 
        st.markdown("<div class='faro-card' style='border-color:#D4AF37;'><h3>Plan Halcón</h3><h2>$200 USD</h2><p>6 Faros / 6 Meses</p></div>", unsafe_allow_html=True)
        if st.button("SUSCRIBIRSE HALCÓN"): st.success("Procesando pago Halcón...")
# --- PESTAÑA 5: BILLETERA CRYPTO (WEB3) ---
elif menu == "BILLETERA CRYPTO (WEB3)":
    st.title("💳 Web3 Green Wallet - Serenity Nexus")
    st.info("Conecta tu billetera para visualizar tus activos digitales ($SNG).")

    import base64
    try:
        with open("video_sng.mp4", "rb") as f:
            data = f.read()
            bin_str = base64.b64encode(data).decode()
            
        video_html = f"""
            <div style="display: flex; justify-content: center;">
                <video width="80%" height="auto" autoplay loop muted playsinline style="border-radius: 20px; border: 3px solid #9BC63B; box-shadow: 0 0 20px rgba(155, 198, 59, 0.5);">
                    <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
                </video>
            </div>
        """
        st.markdown(video_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ El archivo 'video_sng.mp4' no se detecta en el repositorio.")

    st.write("")
    if st.button("🔌 CONECTAR BILLETERA WEB3"):
        st.success("Billetera Conectada: 0x71C...9A23")
        st.metric(label="Saldo en $SNG", value="25,000.00")            

# 6. DONACIONES
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("📜 Generador de Diploma Oficial")
    colA, colB = st.columns([1, 1])
    with colA:
        with st.container(border=True):
            nombre_d = st.text_input("Nombre Completo del Donante")
            monto_d = st.number_input("Monto Donación (USD)", min_value=1)
            if st.button("✅ PROCESAR DONACIÓN"): 
                if nombre_d:
                    st.session_state.donaciones_recibidas += 1
                    st.session_state.estado_gemini = "ACTIVO - EMITIENDO"
                    st.session_state.pdf_buffer = generar_pdf_certificado(nombre_d, monto_d)
                    st.balloons()
                    st.success("¡Certificado generado y Faro Gemini Activado!")
                else:
                    st.warning("Ingrese un nombre.")
    with colB:
        if 'pdf_buffer' in st.session_state:
            st.markdown(f"""
                <div style="background:white; color:black; padding:20px; text-align:center; border:5px double #2E7D32;">
                    <h3 style="color:#2E7D32;">VISTA PREVIA</h3>
                    <h1>{nombre_d.upper()}</h1>
                    <p>Monto: ${monto_d}</p>
                </div>
            """, unsafe_allow_html=True)
            st.download_button("📥 DESCARGAR DIPLOMA (PDF)", data=st.session_state.pdf_buffer, file_name=f"Diploma_Serenity_{nombre_d}.pdf", mime="application/pdf")

# 7. LOGÍSTICA AEROLÍNEAS
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Conectividad Global a Colombia")
    st.subheader("🇪🇺 Europa")
    e1, e2, e3, e4 = st.columns(4)
    with e1: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Iberia_Logo.svg/320px-Iberia_Logo.svg.png'><p>IBERIA</p></div>", unsafe_allow_html=True)
    with e2: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Lufthansa_Logo_2018.svg/320px-Lufthansa_Logo_2018.svg.png'><p>LUFTHANSA</p></div>", unsafe_allow_html=True)
    with e3: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Air_France_Logo.svg/320px-Air_France_Logo.svg.png'><p>AIR FRANCE</p></div>", unsafe_allow_html=True)
    with e4: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Turkish_Airlines_logo_2019.svg/320px-Turkish_Airlines_logo_2019.svg.png'><p>TURKISH</p></div>", unsafe_allow_html=True)
    st.subheader("🇺🇸 Norteamérica")
    n1, n2, n3, n4 = st.columns(4)
    with n1: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/American_Airlines_logo_2013.svg/320px-American_Airlines_logo_2013.svg.png'><p>AMERICAN</p></div>", unsafe_allow_html=True)
    with n2: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/United_Airlines_Logo.svg/320px-United_Airlines_Logo.svg.png'><p>UNITED</p></div>", unsafe_allow_html=True)
    with n3: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Delta_logo.svg/320px-Delta_logo.svg.png'><p>DELTA</p></div>", unsafe_allow_html=True)
    with n4: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Air_Canada_Logo.svg/320px-Air_Canada_Logo.svg.png'><p>AIR CANADA</p></div>", unsafe_allow_html=True)
    st.subheader("🌎 Latinoamérica")
    l1, l2, l3, l4 = st.columns(4)
    with l1: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Avianca_logo_2016.svg/320px-Avianca_logo_2016.svg.png'><p>AVIANCA</p></div>", unsafe_allow_html=True)
    with l2: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Latam-logo_-_v2.svg/320px-Latam-logo_-_v2.svg.png'><p>LATAM</p></div>", unsafe_allow_html=True)
    with l3: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Copa_Airlines_logo.svg/320px-Copa_Airlines_logo.svg.png'><p>COPA</p></div>", unsafe_allow_html=True)
    with l4: st.markdown("<div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Aeromexico_Logo_2024.svg/320px-Aeromexico_Logo_2024.svg.png'><p>AEROMEXICO</p></div>", unsafe_allow_html=True)

# 8. MAPAS
elif menu == "UBICACIÓN & MAPAS":
    st.title("📍 Ubicación Hacienda Serenity (Dagua)")
    color_gemini_map = "green" if st.session_state.estado_gemini == "ACTIVO - EMITIENDO" else "orange"
    m = folium.Map(location=[3.455, -76.655], zoom_start=13, tiles="cartodbpositron")
    folium.Marker([3.460, -76.660], popup=f"FARO GEMINI: {st.session_state.estado_gemini}", icon=folium.Icon(color=color_gemini_map, icon='bolt', prefix='fa')).add_to(m)
    folium.Polygon(locations=[[3.45, -76.67], [3.47, -76.67], [3.47, -76.64], [3.45, -76.64]], color="darkgreen", fill=True, fill_opacity=0.4, tooltip="Hacienda Monte Guadua: 80 Ha").add_to(m)
    folium.CircleMarker(location=[3.445, -76.645], radius=10, color="blue", fill=True, fill_color="blue", tooltip="Finca Villa Michelle").add_to(m)
    st_folium(m, width="100%", height=600)
































































































































