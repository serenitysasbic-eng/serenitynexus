import streamlit as st
import pandas as pd
import hashlib
import os
import io
import base64
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
from datetime import datetime

# En lugar de HexColor, definimos el color de Serenity en formato simple para FPDF
# Verde Serenity: (46, 125, 50) en formato RGB

# ESTA ES TU HERRAMIENTA PARA HACER PDFs (Tu licuadora)
def generar_pdf_serenity(entidad, impacto, hash_id, logo_bytes=None, tipo="CERTIFICADO"):
    pdf = FPDF()
    pdf.add_page()
    
    # Logos
    if os.path.exists("logo_serenity.png"):
        pdf.image("logo_serenity.png", x=10, y=8, w=30)
    if logo_bytes:
        with open("temp_logo_c.png", "wb") as f:
            f.write(logo_bytes.getbuffer())
        pdf.image("temp_logo_c.png", x=165, y=10, w=30)

    pdf.ln(30)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(30, 70, 32)
    
    if tipo == "VADEMECUM":
        pdf.cell(0, 10, "VADEMECUM DE SOLUCIONES LEGALES", ln=True, align='C')
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(0, 0, 0)
        cuerpo = (f"Entidad: {entidad}\n\n"
                  "1. LEY 2173: Gestion de Areas de Vida.\n"
                  "2. LEY 2169: Carbono Neutralidad e IA.\n"
                  "3. LEY 2111: Vigilancia contra delitos ambientales.\n"
                  "4. LEY 99: Conservacion de cuencas (1% hidrico).")
    else:
        pdf.cell(0, 10, "CERTIFICADO DE IMPACTO AMBIENTAL", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(0, 0, 0)
        cuerpo = (f"Serenity Nexus Global certifica a:\n\n{entidad.upper()}\n\n"
                  f"Por su contribucion de: {impacto} unidades de regeneracion.\n"
                  f"Ubicacion: Hacienda Monte Guadua, Dagua.\n"
                  f"ID de Seguimiento: {hash_id}")

    pdf.multi_cell(0, 10, cuerpo, align='C' if tipo != "VADEMECUM" else 'L')
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, f"Autenticidad Blockchain: {hash_id}", ln=True, align='C')
    
    # Retornamos el archivo listo para descargar
    return pdf.output(dest='S').encode('latin-1')

import hashlib
import os
import io
import base64
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="Serenity Nexus Global", page_icon="🌿", layout="wide")


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
    c.drawCentredString(4.25*inch, 7.0*inch, "SERENITY S.A.S. BIC")
    
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(4.25*inch, 6.2*inch, f"{nombre.upper()}")
    
    c.setFont("Helvetica", 14)
    c.drawCentredString(4.25*inch, 5.5*inch, f"Por su valioso aporte de ${monto:,.0f} USD")
    c.drawCentredString(4.25*inch, 5.1*inch, "Destinado a la regeneración del KBA Bosque San Antonio")
    
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
            <button onclick="document.getElementById('audio_earth').play()" style="background:#2E7D32; color:white; border:1px solid #9BC63B; padding:10px 20px; border-radius:10px; cursor:pointer; font-weight:bold;">🔊 ACTIVAR SONIDO GLOBAL EARTH</button>
        </div>
    """, height=100)

    # --- DATOS DE GOBERNANZA ---
    st.info("SPAM (40%) | TAF (60%) | JWCJ $SNG")

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


# =========================================================
# BLOQUE 6: DASHBOARD ESTADÍSTICO IA - MONITOREO EN VIVO
# =========================================================
elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("📊 IA Environmental Analytics")
    st.markdown("### Monitorización en Tiempo Real de Activos Biológicos")

    # --- 1. MÉTRICAS DE IMPACTO GLOBAL (DINÁMICAS) ---
    st.write("---")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="🌳 Árboles Protegidos", value="12,450", delta="+120 esta semana")
    with m2:
        st.metric(label="💨 CO2 Capturado (Ton)", value="842.5", delta="4.2%")
    with m3:
        st.metric(label="🦉 Biodiversidad (Especies)", value="158", delta="Nuevos avistamientos")
    with m4:
        st.metric(label="🛡️ Faros Gemini Activos", value="24", delta="100% Cobertura")

    st.write("")

# =========================================================
# BLOQUE 7: MONITOREO PERIMETRAL - RED DE FAROS GEMINI
# =========================================================
elif menu == "MONITOREO PERIMETRAL":
    st.title("🛰️ Red de Faros Gemini - Vigilancia Activa")
    st.markdown("### Protección Biométrica y Acústica de la Reserva")

    # --- 1. MAPA DINÁMICO DE PUNTOS FARO ---
    with st.container(border=True):
        st.subheader("📍 Ubicación Satelital de Dispositivos")
        # Coordenadas aproximadas de la zona de reserva
        m = folium.Map(location=[3.642, -76.685], zoom_start=15, control_scale=True)
        
        # Añadir marcadores de los Faros
        puntos = [
            {"name": "Faro 01 - Entrada", "pos": [3.642, -76.685], "color": "green"},
            {"name": "Faro 04 - Río Dagua", "pos": [3.645, -76.680], "color": "blue"},
            {"name": "Faro 08 - Límite Sur", "pos": [3.640, -76.690], "color": "red"}
        ]
        
        for p in puntos:
            folium.Marker(p["pos"], popup=p["name"], icon=folium.Icon(color=p["color"])).add_to(m)
        
        st_folium(m, width=700, height=400)
        st.caption("Mapa georreferenciado de la Red de Faros en tiempo real.")

    st.write("---")

    # --- 2. VIDEO DE INTELIGENCIA GEMINI (VISIÓN IA) ---
    col_v1, col_v2 = st.columns([2, 1])
    with col_v1:
        st.subheader("👁️ Visión Computacional")
        video_n = "video_gemini_vision.mp4"
        if os.path.exists(video_n):
            with open(video_n, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
            st.markdown(f'<video width="100%" autoplay loop muted playsinline><source src="data:video/mp4;base64,{b64}"></video>', unsafe_allow_html=True)
        else:
            st.warning("Analizando patrones de biodiversidad...")
            st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1000")

    with col_v2:
        st.info("**Estatus IA**")
        st.write("✅ Detección de fauna")
        st.write("✅ Alerta de intrusión")
        st.metric("Precisión", "98.2%")

    st.write("---")

    # --- 3. MICRÓFONOS ACTIVOS (MONITOREO SÓNICO) ---
    st.subheader("🎧 Monitoreo Acústico (Ley 2111)")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Faro 04**")
        st.audio("https://www.soundjay.com/nature/sounds/rain-01.mp3")
    with c2:
        st.markdown("**Faro 08**")
        st.error("⚠️ Ruido Sospechoso")
        st.image("https://upload.wikimedia.org/wikipedia/commons/6/69/Waveform.png", width=120)
    with c3:
        st.markdown("**Faro 12**")
        st.audio("https://www.soundjay.com/nature/sounds/forest-birds-01.mp3")

    st.divider()
    if st.button("🚨 ACTIVAR ALERTA GLOBAL", use_container_width=True):
        st.error("NOTIFICACIÓN ENVIADA - PROTOCOLO DE SEGURIDAD ACTIVADO")

# =========================================================
# BLOQUE 3: GESTIÓN LEY 2173 (EMPRESAS)
# =========================================================
elif menu == "GESTIÓN LEY 2173 (EMPRESAS)":
    st.title("⚖️ Nexus Legal & Compliance Hub")
    
    # Campo único para el nombre
    nombre_empresa = st.text_input("Razón Social de la Empresa", placeholder="Ej: EcoVida S.A.S")
    
    st.write("---")
    
    col_pdf1, col_pdf2 = st.columns(2)
    
    with col_pdf1:
        st.subheader("📄 Reporte de Leyes")
        if st.button("PREPARAR VADEMÉCUM"):
            if nombre_empresa:
                archivo_v = generar_pdf_corporativo(nombre_empresa, 0, "VAD-NEXUS-2026", es_vademecum=True)
                st.session_state.v_pdf = archivo_v
                st.success("Vademécum Técnico Generado")
        
        if 'v_pdf' in st.session_state:
            st.download_button("📥 Descargar Vademécum", st.session_state.v_pdf, f"Vademecum_{nombre_empresa}.pdf")

    with col_pdf2:
        st.subheader("🛡️ Certificado Oficial")
        tu_logo = st.file_uploader("Logo de la Empresa", type=['png', 'jpg'])
        if st.button("PREPARAR CERTIFICADO"):
            if nombre_empresa and tu_logo:
                archivo_c = generar_pdf_corporativo(nombre_empresa, 200, "CERT-2173-LAW", logo_bytes=tu_logo)
                st.session_state.c_pdf = archivo_c
                st.success("Certificado Enlazado")
        
        if 'c_pdf' in st.session_state:
            st.download_button("📥 Descargar Certificado", st.session_state.c_pdf, f"Certificado_{nombre_empresa}.pdf")

# =========================================================
# BLOQUE 4: SUSCRIPCIONES
# =========================================================
elif menu == "SUSCRIPCIONES":
    st.title("🌱 Membresías de Impacto Serenity")
    st.markdown("### Transforma tu aporte en regeneración real")

    # --- TARJETAS DE PLANES CON BENEFICIOS DETALLADOS ---
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("""
            <div style="background:#1e2630; padding:20px; border-radius:15px; border:2px solid #9BC63B; text-align:center; min-height: 420px;">
                <h3 style="color:#9BC63B;">PLAN SEMILLA</h3>
                <h2 style="color:white;">$25 USD <small>/mes</small></h2>
                <hr style="border-color:#444;">
                <p style="text-align:left; font-size:0.9rem;">🌲 <b>5 Árboles:</b> Siembra y mantenimiento.</p>
                <p style="text-align:left; font-size:0.9rem;">📡 <b>1 Faro:</b> Datos biométricos básicos.</p>
                <p style="text-align:left; font-size:0.9rem;">🪙 <b>50 Tokens:</b> $SNG de respaldo.</p>
                <p style="text-align:left; font-size:0.9rem;">📑 <b>Certificado:</b> Digital con Hash.</p>
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
                <p style="text-align:left; font-size:0.9rem;">🌳 <b>15 Árboles:</b> Restauración activa.</p>
                <p style="text-align:left; font-size:0.9rem;">🎥 <b>Cámaras 4K:</b> Streaming del bosque.</p>
                <p style="text-align:left; font-size:0.9rem;">🪙 <b>200 Tokens:</b> Mayor respaldo $SNG.</p>
                <p style="text-align:left; font-size:0.9rem;">📊 <b>Reporte IA:</b> Inventario de carbono.</p>
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
                <p style="text-align:left; font-size:0.9rem;">🐆 <b>1 Ha Protegida:</b> Soberanía total.</p>
                <p style="text-align:left; font-size:0.9rem;">🛸 <b>Drones:</b> Vigilancia perimetral.</p>
                <p style="text-align:left; font-size:0.9rem;">🪙 <b>600 Tokens:</b> Impacto Web3 máximo.</p>
                <p style="text-align:left; font-size:0.9rem;">👑 <b>Visita VIP:</b> Acceso a Monte Guadua.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ELEGIR HALCÓN", use_container_width=True, key="p_halcon"):
            st.session_state.p_sel = "HALCÓN"
            st.session_state.m_plan = 200

    # --- PASARELA DE PAGO CON LOGOS REHABILITADOS ---
    if 'p_sel' in st.session_state:
        st.write("---")
        st.subheader(f"💳 Finalizar Suscripción: {st.session_state.p_sel}")
        
        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            with st.container(border=True):
                st.markdown("#### Tarjeta de Crédito/Débito")
                st.text_input("Titular de la cuenta")
                st.text_input("Número de Tarjeta", placeholder="xxxx xxxx xxxx xxxx")
                c_exp, c_cvc = st.columns(2)
                c_exp.text_input("Vencimiento (MM/AA)")
                c_cvc.text_input("CVC")
                if st.button("🚀 ACTIVAR SUSCRIPCIÓN", use_container_width=True):
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
            st.caption("🔒 Transacciones seguras mediante Nexus Gateway (Dagua-Colombia)")
            
# =========================================================
# BLOQUE 5: BILLETERA CRYPTO (WEB3) - ECOSISTEMA $SNG
# =========================================================
elif menu == "BILLETERA CRYPTO (WEB3)":
    st.title("👛 Tu Billetera Nexus")
    st.markdown("### Gestión de Activos Digitales y Gobernanza Ambiental")

    # --- 1. EL VIDEO DE LA MONEDA EN BUCLE (LOOP INFINITO) ---
    st.write("---")
    col_v1, col_v2 = st.columns([2, 1])
    
    with col_v1:
        st.subheader("🪙 SNG Coin: Activo Digital Verde")
        nombre_del_archivo = "video_sng.mp4" 
        
        if os.path.exists(nombre_del_archivo):
            try:
                import base64
                with open(nombre_del_archivo, "rb") as f:
                    data = f.read()
                    base64_video = base64.b64encode(data).decode()
                
                # HTML para video automático, infinito y sin controles
                video_html = f'''
                    <video width="100%" height="auto" autoplay loop muted playsinline>
                        <source src="data:video/mp4;base64,{base64_video}" type="video/mp4">
                        Tu navegador no soporta el video.
                    </video>
                '''
                st.markdown(video_html, unsafe_allow_html=True)
            except Exception:
                st.error("Error visualizando el video infinito.")
        else:
            st.info("Visualizando activo digital SNG...")
            st.image("https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=1000", caption="SNG Coin")

    with col_v2:
        st.markdown("""
        **Respaldo SNG:**
        - **Activo:** Biomasa Real Certificada.
        - **Red:** Web3 / Polygon PoS.
        - **Propósito:** Trazabilidad de CO2.
        """)

    st.write("---")

    # --- 2. SALDOS Y MÉTRICAS ---
    c_b1, c_b2, c_b3 = st.columns(3)
    with c_b1:
        st.metric(label="Saldo $SNG", value="1,250.00", delta="12% Mensual")
    with c_b2:
        st.metric(label="Saldo MATIC", value="45.50", delta="-2%")
    with c_b3:
        st.metric(label="Carbono Capturado (Ton)", value="3.4", delta="0.5")

    st.write("")
    
    # --- 3. ACCIONES DE BILLETERA (RECIBIR Y ENVIAR) ---
    col_acc1, col_acc2 = st.columns(2)
    with col_acc1:
        with st.container(border=True):
            st.markdown("#### 📥 Recibir")
            st.code("0x7973...649", language="text")
            st.caption("Dirección pública para recibir activos $SNG.")
            
    with col_acc2:
        with st.container(border=True):
            st.markdown("#### 📤 Enviar")
            destino = st.text_input("Dirección de destino", placeholder="0x...", key="web3_dest")
            monto = st.number_input("Monto a enviar", min_value=0.0, key="web3_amount")
            if st.button("Confirmar Envío", use_container_width=True):
                st.warning("Firma la transacción en tu MetaMask para continuar.")

    st.divider()
    
    # --- 4. HISTORIAL DE TRANSACCIONES ---
    st.markdown("#### 📜 Historial de Transacciones (Blockchain Explorer)")
    data_web3 = {
        'Fecha': ['2026-02-10', '2026-02-08', '2026-02-05'],
        'Tipo': ['Recibido', 'Suscripción Plan Semilla', 'Recompensa Staking'],
        'Monto $SNG': ['+500', '-100', '+25'],
        'Estado': ['Confirmado ✅', 'Confirmado ✅', 'Procesando ⏳']
    }
    st.table(data_web3)           

# =========================================================
# BLOQUE 6: DONACIONES Y CERTIFICADO (Diploma Oficial)
# =========================================================
elif menu == "DONACIONES Y CERTIFICADO":
    st.title("📜 Generador de Diploma y Certificado Nexus")
    st.markdown("### Registro de Aportes a la Regeneración Biométrica")
    
    colA, colB = st.columns([1, 1])
    
    with colA:
        with st.container(border=True):
            st.markdown("#### Datos del Donante")
            nombre_d = st.text_input("Nombre Completo o Razón Social")
            monto_d = st.number_input("Monto del Aporte (USD)", min_value=1, step=10)
            
            if st.button("✅ REGISTRAR APORTE Y GENERAR HASH"): 
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
                label="📥 DESCARGAR DIPLOMA CON HASH (PDF)",
                data=st.session_state.pdf_buffer,
                file_name=f"Certificado_Nexus_{st.session_state.current_hash}.pdf",
                mime="application/pdf"
            )
# =========================================================
# BLOQUE 7: LOGÍSTICA AEROLÍNEAS (Conexiones Globales)
# =========================================================
elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Conectividad Global a Colombia")
    st.markdown("Principales aerolíneas con conexión directa a Bogotá (BOG), Cali (CLO) o Medellín (MDE).")
    
    # --- EUROPA ---
    st.subheader("🇪🇺 Europa")
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
    st.subheader("🇺🇸 Norteamérica")
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
    st.subheader("🌎 Latinoamérica")
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
    st.title("📍 Ubicación Estratégica Serenity")
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
                    🌐 VER EN GOOGLE MAPS (SISTEMA EXTERNO)
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




























































































































































































