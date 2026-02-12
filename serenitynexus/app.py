# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
import hashlib  # <--- ESTA ES LA LÍNEA QUE FALTA
from datetime import datetime
import io
import os
import base64

# --- LIBRERÍAS EXTENDIDAS ---
import folium
from streamlit_folium import st_folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black

# --- CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="Serenity Nexus Global", page_icon="??", layout="wide")
VERDE_SERENITY = HexColor("#2E7D32")

# --- GESTIÓN DE ESTADO ---
if 'total_protegido' not in st.session_state: st.session_state.total_protegido = 87.0
if 'donaciones_recibidas' not in st.session_state: st.session_state.donaciones_recibidas = 0
if 'estado_gemini' not in st.session_state: st.session_state.estado_gemini = "Latente"
if 'auth' not in st.session_state: st.session_state.auth = False
if 'f_activo' not in st.session_state: st.session_state.f_activo = None

def generar_pdf_certificado(nombre, monto, hash_id):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # 1. Marco de Seguridad (Borde Verde Serenity)
    c.setStrokeColor(VERDE_SERENITY)
    c.setLineWidth(5)
    c.rect(0.3*inch, 0.3*inch, 7.9*inch, 10.4*inch)
    
    # 2. LOGO (Arreglado para no salir achatado)
    try:
        if os.path.exists("logo_serenity.png"):
            # Usamos preserveAspectRatio para que mantenga su forma original
            c.drawImage("logo_serenity.png", 3.25*inch, 8.8*inch, width=2*inch, height=1.2*inch, mask='auto', preserveAspectRatio=True)
    except:
        pass

    # 3. TEXTO DE CABECERA (Dividido y Centrado como pediste)
    c.setFillColor(VERDE_SERENITY)
    
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(4.25*inch, 8.3*inch, "CERTIFICADO DE:")
    
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(4.25*inch, 7.8*inch, "DONACIÓN REGENERATIVA")
    
    # 4. CUERPO DEL DIPLOMA
    c.setFont("Helvetica", 16)
    c.setFillColor(black)
    c.drawCentredString(4.25*inch, 7.0*inch, "SERENITY HUB S.A.S. BIC")
    
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(4.25*inch, 6.2*inch, f"{nombre.upper()}")
    
    c.setFont("Helvetica", 14)
    c.drawCentredString(4.25*inch, 5.5*inch, f"Por su valioso aporte de ${monto:,.0f} USD")
    c.drawCentredString(4.25*inch, 5.1*inch, "Destinado a la Regeneración del KBA Bosque San Antonio")
    
    # Mensaje de impacto
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(4.25*inch, 4.4*inch, "Tu contribución permite que la biodiversidad de Dagua y Felidia")
    c.drawCentredString(4.25*inch, 4.2*inch, "se transforme en un activo vivo para el planeta. ¡Gracias!")

    # 5. FIRMA
    c.setLineWidth(1)
    c.line(3*inch, 3.0*inch, 5.5*inch, 3.0*inch)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(4.25*inch, 2.8*inch, "Jorge Carvajal")
    c.setFont("Helvetica", 10)
    c.drawCentredString(4.25*inch, 2.6*inch, "Administrador Serenity S.A.S. BIC")
    
    # 6. HASH DE SEGURIDAD (Nexus Verification)
    c.setFillColor(HexColor("#444444"))
    c.setFont("Courier-Bold", 10)
    c.drawCentredString(4.25*inch, 1.5*inch, f"HASH DE VERIFICACIÓN: {hash_id}")
    
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.setFont("Helvetica", 8)
    c.drawCentredString(4.25*inch, 1.2*inch, f"Emitido por Sistema Nexus IA | Fecha de registro: {fecha_hoy}")
    
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
            <button onclick="document.getElementById('audio_earth').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:10px 20px; border-radius:10px; cursor:pointer; font-weight:bold;">?? ACTIVAR SONIDO GLOBAL EARTH</button>
        </div>
    """, height=100)

    # --- DATOS DE GOBERNANZA ---
    st.info("SPAM (40%) | TAF (60%) | JWCJ $SNG")

    st.divider()

    # --- QUIÉNES SOMOS, MISIÓN Y VISIÓN ---
    col_inf1, col_inf2 = st.columns(2)
    
    with col_inf1:
        st.subheader("QUIÉNES SOMOS / WHO WE ARE")
        st.write("Serenity Nexus Global es la primera plataforma Phygital (Física + Digital) del Valle del Cauca que integra la conservación ambiental con tecnología Blockchain e Inteligencia Artificial, transformando la protección de la biodiversidad en un activo digital tangible.")

    with col_inf2:
        st.subheader("NUESTRA MISIÓN / OUR MISSION")
        st.write("Regenerar el tejido ecológico y social mediante un modelo de negocio sostenible que permita a empresas y personas compensar su huella ambiental a través de la tecnología y la transparencia.")

    st.write("---")
    
    col_inf3, col_inf4 = st.columns([1, 2])
    with col_inf3:
        st.subheader("NUESTRA VISIÓN / OUR VISION")
    with col_inf4:
        st.write("Ser el referente mundial del Internet de la Naturaleza para 2030, liderando la valorización de los servicios ecosistémicos mediante nuestra red de Faros inteligentes y el token $SNG.")

    st.info("Ubicación del Proyecto: Dagua y Felidia, Valle del Cauca - Hacienda Monte Guadua & Finca Villa Michelle.")

# 2. RED DE FAROS
elif menu == "RED DE FAROS (7 NODOS)":
    st.title("Monitoreo Perimetral")
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
        st.markdown(f"<div class='faro-gemini'><h3>?? FARO GEMINI ??</h3><p>Estado: {st.session_state.estado_gemini}</p></div>", unsafe_allow_html=True)
        if st.button("ACTIVAR NÚCLEO GEMINI"): 
            st.session_state.f_activo = "GEMINI"
            st.session_state.estado_gemini = "ACTIVO - EMITIENDO"

    if st.session_state.f_activo:
        st.divider()
        color_titulo = "#4285F4" if st.session_state.f_activo == "GEMINI" else "#9BC63B"
        st.markdown(f"<h2 style='color:{color_titulo}; text-align:center;'>?? TRANSMISIÓN EN VIVO: {st.session_state.f_activo.upper()}</h2>", unsafe_allow_html=True)
        c_cols = st.columns(4)
        for j in range(8):
            label = "IA-ANALYSIS" if st.session_state.f_activo == "GEMINI" else "LIVE"
            with c_cols[j % 4]: st.markdown(f"<div class='cam-grid'>CAM {j+1}<br>?? {label}</div>", unsafe_allow_html=True)
        
        st.subheader("Bioacústica")
        m_cols = st.columns(4)
        for k in range(4):
            val = random.randint(85,99) if st.session_state.f_activo == "GEMINI" else random.randint(40,90)
            with m_cols[k]: st.markdown(f"<div style='background:rgba(155,198,59,0.2); border:1px solid #2E7D32; padding:10px; border-radius:5px; text-align:center;'><b>MIC {k+1}</b><br><span style='color:#9BC63B;'>||||| {val}%</span></div>", unsafe_allow_html=True)

# 3. DASHBOARD
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("Análisis de Inteligencia Biológica")
    m = st.columns(4)
    m[0].markdown(f"<div class='metric-card'><h3>Especies</h3><h1>1,248</h1></div>", unsafe_allow_html=True)
    m[1].markdown(f"<div class='metric-card'><h3>Hectáreas</h3><h1>{st.session_state.total_protegido}</h1></div>", unsafe_allow_html=True)
    m[2].markdown(f"<div class='metric-card'><h3>Inversiones</h3><h1>{st.session_state.donaciones_recibidas}</h1></div>", unsafe_allow_html=True)
    m[3].markdown(f"<div class='metric-card'><h3>Salud</h3><h1>98%</h1></div>", unsafe_allow_html=True)
    st.bar_chart(pd.DataFrame({'Detecciones': [120, 450, 300, 80, 45, 110, 950]}, index=["Halcón", "Colibrí", "Rana", "Venado", "Tigrillo", "Capibara", "GEMINI"]))


# =========================================================
# BLOQUE 3: GESTIÓN LEY 2173 (EMPRESAS)
# =========================================================
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("Nexus Legal & Compliance Hub")
    st.markdown("### Soluciones Tecnológicas a la Normativa Ambiental")

    # --- Tarjetas Visuales ---
    c_l1, c_l2, c_l3 = st.columns(3)
    with c_l1:
        st.markdown('<div style="background:#1e2630; padding:15px; border-radius:10px; border-left:5px solid #9BC63B; min-height:180px;"><h4 style="color:#9BC63B;">LEY 2173</h4><p style="font-size:0.8rem; color:#ccc;">Obligación de 2 árboles por empleado. Serenity provee el terreno y GPS oficial.</p></div>', unsafe_allow_html=True)
    with c_l2:
        st.markdown('<div style="background:#1e2630; padding:15px; border-radius:10px; border-left:5px solid #3498db; min-height:180px;"><h4 style="color:#3498db;">LEY 2169</h4><p style="font-size:0.8rem; color:#ccc;">Ruta a la Carbono Neutralidad. Nuestra IA certifica la captura real de CO2.</p></div>', unsafe_allow_html=True)
    with c_l3:
        st.markdown('<div style="background:#1e2630; padding:15px; border-radius:10px; border-left:5px solid #e74c3c; min-height:180px;"><h4 style="color:#e74c3c;">LEY 2111</h4><p style="font-size:0.8rem; color:#ccc;">Justicia Ambiental. Faros Gemini como evidencia digital.</p></div>', unsafe_allow_html=True)

    st.write("")
    
    # --- Vademécum ---
    with st.container(border=True):
        st.subheader("Vademécum de Soluciones Corporativas")
        empresa_v = st.text_input("Nombre de la empresa para el reporte técnico", key="txt_vademecum")
        if st.button("GENERAR VADEMÉCUM TÉCNICO PDF", use_container_width=True):
            if empresa_v:
                pdf_v = generar_pdf_corporativo(empresa_v, 0, "NEXUS-VAD-2026", es_vademecum=True)
                st.session_state.vademecum_pdf = pdf_v
                st.success("Vademécum Profesional generado.")
            else:
                st.warning("Ingrese el nombre de la empresa.")
        
        if 'vademecum_pdf' in st.session_state:
            st.download_button("DESCARGAR VADEMÉCUM (PDF ESTRUCTURADO)", st.session_state.vademecum_pdf, "Vademecum_Legal.pdf", "application/pdf", use_container_width=True)

    st.divider()

    # --- Certificado con Logo ---
    st.subheader("Emisión de Certificado con Logo")
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        n_corp = st.text_input("Razón Social de la Compañía", key="txt_corp")
        n_per = st.number_input("Número de Empleados", min_value=1, value=100, key="num_emp")
        archivo_logo = st.file_uploader("Cargar Logo Corporativo", type=['png', 'jpg'], key="file_logo")

    with col_act2:
        if st.button("EMITIR CERTIFICADO OFICIAL", use_container_width=True):
            if n_corp and archivo_logo:
                h_c = hashlib.sha256(f"{n_corp}".encode()).hexdigest()[:12].upper()
                pdf_c = generar_pdf_corporativo(n_corp, n_per*2, h_c, logo_bytes=archivo_logo)
                st.session_state.cert_corp_pdf = pdf_c
                st.success("Certificado con logo vinculado.")
            else:
                st.error("Se requiere Razón Social y Logo.")

        if 'cert_corp_pdf' in st.session_state:
            st.download_button("DESCARGAR CERTIFICADO CON LOGO", st.session_state.cert_corp_pdf, "Certificado_Nexus_Logo.pdf", "application/pdf", use_container_width=True)
# =========================================================
# BLOQUE 4: SUSCRIPCIONES
# =========================================================
elif menu == "SUSCRIPCIONES":
    st.title("Membresías de Impacto Serenity")
    st.markdown("### Transforma tu aporte en regeneración real")

    # --- TARJETAS DE PLANES CON BENEFICIOS DETALLADOS ---
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("""
            <div style="background:#1e2630; padding:20px; border-radius:15px; border:2px solid #9BC63B; text-align:center; min-height: 420px;">
                <h3 style="color:#9BC63B;">PLAN SEMILLA</h3>
                <h2 style="color:white;">$25 USD <small>/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;"> <b>5 Árboles:</b> Siembra y mantenimiento.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>1 Faro:</b> Datos biométricos básicos.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>50 Tokens:</b> $SNG de respaldo.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>Certificado:</b> Digital con Hash.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ELEGIR SEMILLA", use_container_width=True, key="p_semilla"):
            st.session_state.p_sel = "SEMILLA"
            st.session_state.m_plan = 25

    with p2:
        st.markdown("""
            <div style="background:#1e2630; padding:20px; border-radius:15px; border:3px solid #9BC63B; text-align:center; min-height: 420px; transform: scale(1.02);">
                <h3 style="color:#9BC63B;">PLAN GUARDIÁN</h3>
                <h2 style="color:white;">$80 USD <small>/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;"> <b>15 Árboles:</b> Restauración activa.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>Cámaras 4K:</b> Streaming del bosque.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>200 Tokens:</b> Mayor respaldo $SNG.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>Reporte IA:</b> Inventario de carbono.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ELEGIR GUARDIÁN", use_container_width=True, key="p_guardian"):
            st.session_state.p_sel = "GUARDIÁN"
            st.session_state.m_plan = 80

    with p3:
        st.markdown("""
            <div style="background:#1e2630; padding:20px; border-radius:15px; border:2px solid #D4AF37; text-align:center; min-height: 420px;">
                <h3 style="color:#D4AF37;">PLAN HALCÓN</h3>
                <h2 style="color:white;">$200 USD <small>/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;"> <b>1 Plaza Protegida:</b> Soberanía total.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>Cámaras:</b> Vigilancia perimetral.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>600 Tokens:</b> Impacto Web3 máximo.</p>
                <p style="text-align:left; font-size:0.9rem;"> <b>Visita 1 Persona VIP:</b> Acceso a Monte Guadua 2 Dias 1 Noche.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ELEGIR HALCÓN", use_container_width=True, key="p_halcon"):
            st.session_state.p_sel = "HALCÓN"
            st.session_state.m_plan = 200

    # --- PASARELA DE PAGO CON LOGOS REHABILITADOS ---
    if 'p_sel' in st.session_state:
        st.write("---")
        st.subheader(f"Finalizar Suscripción: {st.session_state.p_sel}")
        
        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            with st.container(border=True):
                st.markdown("#### Tarjeta de Crédito/Débito")
                st.text_input("Titular de la cuenta")
                st.text_input("Número de Tarjeta", placeholder="xxxx xxxx xxxx xxxx")
                c_exp, c_cvc = st.columns(2)
                c_exp.text_input("Vencimiento (MM/AA)")
                c_cvc.text_input("CVC")
                if st.button("ACTIVAR SUSCRIPCIÓN", use_container_width=True):
                    st.balloons()
                    st.success(f"¡Bienvenido al Plan {st.session_state.p_sel}! Impacto activado.")

        with col_pay2:
            st.markdown("#### Pagos Locales y Alternativos")
            st.markdown("""
                <div style="background: #ffffff; padding: 25px; border-radius: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center; border: 1px solid #ddd;">
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/b/bf/Nequi_logo.png" width="90"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Bancolombia_logo.svg/2560px-Bancolombia_logo.svg.png" width="90"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Visa_Inc._logo.svg/2560px-Visa_Inc._logo.svg.png" width="70"></div>
                    <div style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/1280px-Mastercard-logo.svg.png" width="70"></div>
                </div>
            """, unsafe_allow_html=True)
            st.caption("Transacciones seguras mediante Nexus Gateway (Dagua-Colombia)")
            
# =========================================================
# BLOQUE 5: BILLETERA CRYPTO (WEB3) - ECOSISTEMA $SNG
# =========================================================
elif menu == "BILLETERA CRYPTO (WEB3)":
    st.title("Nexus Finance Control")
    st.markdown("### El Futuro de la Conservación Tokenizada")

    # --- NIVEL 1: EL TOKEN (VISUAL) ---
    try:
        with open("video_sng.mp4", "rb") as f:
            data = f.read()
            bin_str = base64.b64encode(data).decode()
        video_html = f"""
            <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                <video width="60%" autoplay loop muted playsinline style="border-radius: 20px; border: 2px solid #9BC63B; box-shadow: 0 0 30px rgba(155, 198, 59, 0.3);">
                    <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
                </video>
            </div>
        """
        st.markdown(video_html, unsafe_allow_html=True)
    except:
        st.info("?? Visualizador de Token $SNG Activo")

    st.write("---")

    # --- NIVEL 2: ADQUISICIÓN Y CUSTODIA (Tus dos preguntas) ---
    col_buy, col_vault = st.columns(2)

    with col_buy:
        st.markdown("####  ¿Cómo comprar $SNG?")
        st.write("El token $SNG representa hectáreas regeneradas y datos biométricos de los Faros.")
        with st.container(border=True):
            st.write("**Simulador de Intercambio (Swap)**")
            moneda_pago = st.selectbox("Pagar con:", ["USD (Tarjeta/Transferencia)", "USDT (Crypto)", "Ethereum"])
            cantidad_usd = st.number_input("Monto a invertir (USD):", min_value=10, step=50)
            tasa = 0.50 # Ejemplo: 1 SNG = 0.50 USD
            st.metric("Recibirás aproximadamente:", f"{cantidad_usd / tasa:,.2f} $SNG")
            if st.button("COMPRAR TOKENS $SNG"):
                st.success("Orden de compra enviada al Nexus Gateway.")

    with col_vault:
        st.markdown("#### ?? ¿Cómo tener una Billetera Nexus?")
        st.write("Nexus Vault no es solo una App, es tu llave privada al Internet de la Naturaleza.")
        st.markdown("""
        * **Paso 1:** Descarga Nexus App o usa una compatible (Metamask/Ledger).
        * **Paso 2:** Genera tu frase semilla de 24 palabras.
        * **Paso 3:** Vincula tu ID de Donante Serenity para recibir beneficios.
        """)
        st.button("DESCARGAR GUÍA DE CONFIGURACIÓN")

    st.write("---")

    # --- NIVEL 3: CONEXIÓN FINAL ---
    st.markdown("Centro de Conexión Web3")
    cw1, cw2, cw3 = st.columns([1, 2, 1])
    with cw2:
        if st.button("VINCULAR BILLETERA AL SISTEMA NEXUS"):
            st.balloons()
            st.success("Billetera 0x71C...9A23 Conectada con éxito.")
            st.metric(label="Saldo en Bóveda", value="25,000.00 $SNG", delta="80 Hectáreas Respaldadas")
            st.write("Verificado por Nodo Gemini en Finca Villa Michelle")            

# =========================================================
# BLOQUE 6: DONACIONES Y CERTIFICADO (Diploma Oficial)
# =========================================================
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("Generador de Diploma y Certificado Nexus")
    st.markdown("### Registro de Aportes a la Regeneración Biométrica")
    
    colA, colB = st.columns([1, 1])
    
    with colA:
        with st.container(border=True):
            st.markdown("#### Datos del Donante")
            nombre_d = st.text_input("Nombre Completo o Razón Social")
            monto_d = st.number_input("Monto del Aporte (USD)", min_value=1, step=10)
            
            if st.button("REGISTRAR APORTE Y GENERAR HASH"): 
                if nombre_d:
                    # 1. Generar Hash
                    datos_hash = f"{nombre_d}{monto_d}{datetime.now()}"
                    hash_certificado = hashlib.sha256(datos_hash.encode()).hexdigest()[:16].upper()
                    
                    # 2. Guardar en session_state
                    st.session_state.current_hash = hash_certificado
                    st.session_state.nombre_prev = nombre_d
                    st.session_state.monto_prev = monto_d
                    
                    # 3. Generar PDF
                    st.session_state.pdf_buffer = generar_pdf_certificado(nombre_d, monto_d, hash_certificado)
                    
                    st.session_state.donaciones_recibidas += 1
                    st.balloons()
                    st.success(f"¡Certificado generado con éxito!")
                else:
                    st.warning("Ingrese el nombre del donante.")

    with colB:
        if 'pdf_buffer' in st.session_state:
            st.markdown(f"""
                <div style="background:white; color:black; padding:30px; text-align:center; border:8px double #2E7D32; border-radius:15px;">
                    <h2 style="color:#2E7D32; margin-bottom:10px;">VISTA PREVIA</h2>
                    <hr style="border:1px solid #2E7D32;">
                    <p style="font-size:1.2rem; margin-top:20px;">Gracias por tu aporte, <b>{st.session_state.nombre_prev.upper()}</b></p>
                    <p>Has contribuido con <b>${st.session_state.monto_prev} USD</b></p>
                    <div style="background:#f0f2f6; padding:10px; border-radius:5px; margin-top:20px;">
                        <code style="font-size:0.8rem; color: #2E7D32;">HASH: {st.session_state.current_hash}</code>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.download_button(
                label="DESCARGAR DIPLOMA CON HASH (PDF)",
                data=st.session_state.pdf_buffer,
                file_name=f"Certificado_Nexus_{st.session_state.current_hash}.pdf",
                mime="application/pdf"
            )
# =========================================================
# BLOQUE 7: LOGÍSTICA AEROLÍNEAS (Conexiones Globales)
# =========================================================
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("Conectividad Global a Colombia")
    st.markdown("Principales aerolíneas con conexión directa a Bogotá (BOG), Cali (CLO) o Medellín (MDE).")
    
    # --- EUROPA ---
    st.subheader("Europa")
    e1, e2, e3, e4 = st.columns(4)
    with e1: 
        st.markdown("<a href='https://www.iberia.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Iberia_Logo.svg/320px-Iberia_Logo.svg.png'><p>IBERIA</p></div></a>", unsafe_allow_html=True)
    with e2: 
        st.markdown("<a href='https://www.lufthansa.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Lufthansa_Logo_2018.svg/320px-Lufthansa_Logo_2018.svg.png'><p>LUFTHANSA</p></div></a>", unsafe_allow_html=True)
    with e3: 
        st.markdown("<a href='https://www.airfrance.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Air_France_Logo.svg/320px-Air_France_Logo.svg.png'><p>AIR FRANCE</p></div></a>", unsafe_allow_html=True)
    with e4: 
        st.markdown("<a href='https://www.turkishairlines.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Turkish_Airlines_logo_2019.svg/320px-Turkish_Airlines_logo_2019.svg.png'><p>TURKISH</p></div></a>", unsafe_allow_html=True)
    
    e5, e6, e7 = st.columns(3)
    with e5: 
        st.markdown("<a href='https://www.klm.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/KLM_logo.svg/320px-KLM_logo.svg.png'><p>KLM</p></div></a>", unsafe_allow_html=True)
    with e6: 
        st.markdown("<a href='https://www.aireuropa.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Air_Europa_Logo.svg/320px-Air_Europa_Logo.svg.png'><p>AIR EUROPA</p></div></a>", unsafe_allow_html=True)
    with e7: 
        st.markdown("<a href='https://www.flyedelweiss.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Edelweiss_Air_Logo.svg/320px-Edelweiss_Air_Logo.svg.png'><p>EDELWEISS</p></div></a>", unsafe_allow_html=True)

    # --- NORTEAMÉRICA ---
    st.subheader("Norteamérica")
    n1, n2, n3, n4 = st.columns(4)
    with n1: 
        st.markdown("<a href='https://www.aa.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/American_Airlines_logo_2013.svg/320px-American_Airlines_logo_2013.svg.png'><p>AMERICAN</p></div></a>", unsafe_allow_html=True)
    with n2: 
        st.markdown("<a href='https://www.united.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/United_Airlines_Logo.svg/320px-United_Airlines_Logo.svg.png'><p>UNITED</p></div></a>", unsafe_allow_html=True)
    with n3: 
        st.markdown("<a href='https://www.delta.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Delta_logo.svg/320px-Delta_logo.svg.png'><p>DELTA</p></div></a>", unsafe_allow_html=True)
    with n4: 
        st.markdown("<a href='https://www.aircanada.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Air_Canada_Logo.svg/320px-Air_Canada_Logo.svg.png'><p>AIR CANADA</p></div></a>", unsafe_allow_html=True)

    # --- LATINOAMÉRICA ---
    st.subheader("Latinoamérica")
    l1, l2, l3, l4 = st.columns(4)
    with l1: 
        st.markdown("<a href='https://www.avianca.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Avianca_logo_2016.svg/320px-Avianca_logo_2016.svg.png'><p>AVIANCA</p></div></a>", unsafe_allow_html=True)
    with l2: 
        st.markdown("<a href='https://www.latamairlines.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Latam-logo_-_v2.svg/320px-Latam-logo_-_v2.svg.png'><p>LATAM</p></div></a>", unsafe_allow_html=True)
    with l3: 
        st.markdown("<a href='https://www.copaair.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Copa_Airlines_logo.svg/320px-Copa_Airlines_logo.svg.png'><p>COPA</p></div></a>", unsafe_allow_html=True)
    with l4: 
        st.markdown("<a href='https://www.aeromexico.com' target='_blank'><div class='airline-grid'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Aeromexico_Logo_2024.svg/320px-Aeromexico_Logo_2024.svg.png'><p>AEROMEXICO</p></div></a>", unsafe_allow_html=True)
# =========================================================
# BLOQUE FINAL: UBICACIÓN & MAPAS (Dagua y Felidia)
# =========================================================
elif menu == "UBICACIÓN & MAPAS":
    st.title("Ubicación Estratégica Serenity")
    st.markdown("### Finca Villa Michelle & Hacienda Monte Guadua")
    
    # Coordenadas exactas
    lat_villa = 3.465028; lon_villa = -76.634778
    lat_guadua = 3.477917; lon_guadua = -76.657361
    
    # Botón directo a la interfaz de Google Maps
    url_gmaps = f"https://www.google.com/maps/search/?api=1&query={lat_villa},{lon_villa}"
    st.markdown(f"""
        <div style='text-align:center; margin-bottom: 20px;'>
            <a href="{url_gmaps}" target="_blank">
                <button style="background-color:#4285F4; color:white; border:none; padding:15px 30px; border-radius:10px; font-weight:bold; cursor:pointer; box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);">
                    VER EN GOOGLE MAPS (SISTEMA EXTERNO)
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

    # Configuración del mapa interactivo con capa satelital de Google
    # Nota: Usamos la URL de los tiles de Google Maps directamente
    google_map_tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'
    
    m = folium.Map(
        location=[lat_villa, lon_villa], 
        zoom_start=15, 
        tiles=google_map_tiles, 
        attr='Google Maps Satellite'
    )
    
    # --- CAMBIO SOLICITADO: FARO GEMINI EN VILLA MICHELLE ---
    color_gemini_map = "green" if st.session_state.estado_gemini == "ACTIVO - EMITIENDO" else "orange"
    
    folium.Marker(
        [lat_villa, lon_villa], 
        popup=f"NÚCLEO CENTRAL: FARO GEMINI - Villa Michelle", 
        icon=folium.Icon(color=color_gemini_map, icon='bolt', prefix='fa')
    ).add_to(m)
    
    # Marcador de Hacienda Monte Guadua (Reserva)
    folium.Marker(
        [lat_guadua, lon_guadua], 
        popup="Reserva Hacienda Monte Guadua", 
        icon=folium.Icon(color='darkgreen', icon='leaf', prefix='fa')
    ).add_to(m)
    
    # Delimitación del área de reserva en Monte Guadua
    folium.Polygon(
        locations=[
            [3.475, -76.660], [3.480, -76.660], 
            [3.480, -76.654], [3.475, -76.654]
        ], 
        color="#9BC63B", 
        fill=True, 
        fill_opacity=0.3, 
        tooltip="Área de Conservación Serenity: 80 Ha"
    ).add_to(m)
    
    st_folium(m, width="100%", height=600)

# --- FIN DEL ARCHIVO ---






































































































































































































