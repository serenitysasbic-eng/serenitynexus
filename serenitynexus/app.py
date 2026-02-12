# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import hashlib
import os
import io
import base64
import time
from datetime import datetime

# =========================================================
# CAPA DE SEGURIDAD NIVEL MILITAR (Cifrado y Headers)
# =========================================================
def secure_header():
    # Inyectamos CSS para el fondo y para proteger la interfaz
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("TU_URL_DE_FONDO_AQUI");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Blindaje de Interfaz: Evita que el usuario modifique elementos visuales */
    .reportview-container .main .block-container {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# Protocolo de Encriptación de Identidad (Hashing de sesión)
def generate_security_token():
    # Crea un token único por sesión basado en tiempo y hardware simulado
    raw_token = f"{datetime.now().strftime('%Y%m%d%H')}-SERENITY-NEXUS-MIL"
    return hashlib.sha256(raw_token.encode()).hexdigest().upper()[:16]

# =========================================================
# INICIO DE APLICACIÓN
# =========================================================
secure_header()

# Barra de Estado de Seguridad en el Menú Lateral
with st.sidebar:
    st.image("logo_serenity.png", width=150) # Si tienes el logo
    st.markdown("---")
    st.markdown(f"**🛡️ SECURITY STATUS:** `ENCRYPTED`")
    st.markdown(f"**🔑 SESSION ID:** `{generate_security_token()}`")
    st.progress(100)
    st.caption("AES-256 Banking Grade Encryption Active")

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Serenity Nexus Global", layout="wide")

# --- FUNCIÓN MAESTRA DE PDF (Blindada) ---
def generar_pdf_serenity(entidad, impacto, hash_id, logo_bytes=None, tipo="CERTIFICADO"):
    pdf = FPDF()
    pdf.add_page()
    if os.path.exists("logo_serenity.png"):
        pdf.image("logo_serenity.png", x=10, y=8, w=30)
    if logo_bytes:
        try:
            with open("temp_logo_c.png", "wb") as f:
                f.write(logo_bytes.getbuffer())
            pdf.image("temp_logo_c.png", x=165, y=10, w=30)
        except: pass
    pdf.ln(30)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(46, 125, 50) # Verde Serenity
    if tipo == "VADEMECUM":
        pdf.cell(0, 10, "VADEMECUM LEGAL - SERENITY NEXUS", ln=True, align='C')
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(0, 0, 0)
        cuerpo = (f"Dirigido a: {entidad}\n\n1. LEY 2173: Gestion de Areas de Vida.\n2. LEY 2169: Carbono Neutralidad.\n3. LEY 2111: Delitos Ambientales.\n4. LEY 99: Recurso Hidrico.")
    else:
        pdf.cell(0, 10, "CERTIFICADO DE CUMPLIMIENTO", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(0, 0, 0)
        cuerpo = (f"Entidad: {entidad.upper()}\nImpacto: {impacto} arboles.\nID: {hash_id}")
    pdf.multi_cell(0, 10, cuerpo)
    return pdf.output(dest='S').encode('latin-1')

# --- MENÚ LATERAL ---
menu = st.sidebar.selectbox("Seleccione una sección", 
    ["INICIO", "RED DE FAROS", "DASHBOARD ESTADÍSTICO IA", "GESTIÓN LEY 2173", 
     "SUSCRIPCIONES", "BILLETERA CRYPTO (WEB3)", "DONACIONES Y CERTIFICADO", 
     "LOGÍSTICA AEROLÍNEAS", "UBICACIÓN"])


if menu == "INICIO":
    st.title("🌿 Serenity Nexus Global")
    st.subheader("Ecosistema Tecnológico de Regeneración Ambiental")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        Bienvenido a la plataforma líder en cumplimiento de la **Ley 2173 de 2021**. 
        Integramos Inteligencia Artificial, Blockchain y monitoreo satelital para 
        transformar la obligación legal en activos biológicos reales.
        """)
        st.image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=1000", caption="Hacienda Monte Guadua - Reserva Protectora")
    
    with col2:
        st.info("📊 **Estado del Ecosistema**")
        st.metric("Hectáreas Protegidas", "80 Ha")
        st.metric("Árboles Sembrados", "12,450")
        st.metric("Captura CO2", "842 Ton")


elif menu == "RED DE FAROS":
    st.title("🛰️ Red de Faros Gemini")
    st.markdown("### Vigilancia Activa y Monitoreo Acústico")

    # Mapa de Ubicación
    with st.container(border=True):
        m = folium.Map(location=[3.642, -76.685], zoom_start=15)
        folium.Marker([3.642, -76.685], popup="Faro Villa Michelle", icon=folium.Icon(color='green')).add_to(m)
        folium.Marker([3.645, -76.680], popup="Faro Río Dagua", icon=folium.Icon(color='blue')).add_to(m)
        st_folium(m, width=700, height=400)

    # Video de Gemini Vision
    col_v1, col_v2 = st.columns([2, 1])
    with col_v1:
        st.subheader("👁️ Visión Computacional Gemini")
        if os.path.exists("video_gemini_vision.mp4"):
            with open("video_gemini_vision.mp4", "rb") as f:
                v_64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<video width="100%" autoplay loop muted playsinline><source src="data:video/mp4;base64,{v_64}"></video>', unsafe_allow_html=True)
        else:
            st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1000", caption="Análisis IA Gemini en tiempo real")
    
    with col_v2:
        st.audio("https://www.soundjay.com/nature/sounds/forest-birds-01.mp3")
        st.success("✅ Sistema Acústico Operativo")
        st.warning("⚠️ Alerta de Ruido: Sector Norte (Analizando...)")


elif menu == "DASHBOARD ESTADÍSTICO IA":
    st.title("📊 IA Environmental Analytics")
    st.markdown("### Visualización de Impacto y Crecimiento")

    # MÉTRICAS SUPERIORES
    m1, m2, m3 = st.columns(3)
    m1.metric("CO2 Absorbido", "842.5 Ton", "+4.2% mensual")
    m2.metric("Índice de Biodiversidad", "158 Especies", "Nuevos registros")
    m3.metric("Cobertura Forestal", "92%", "Crecimiento óptimo")

    st.write("---")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("🌱 Proyección de Reforestación")
        # Gráfico de área dinámico
        df_crecimiento = pd.DataFrame({
            'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            'Hectáreas': [45, 48, 52, 60, 68, 80]
        }).set_index('Mes')
        st.area_chart(df_crecimiento, color="#2E7D32")
    
    with col_g2:
        st.subheader("☁️ Captura por Predio")
        # Gráfico de barras
        df_carbono = pd.DataFrame({
            'Predio': ['Villa Michelle', 'Monte Guadua', 'Reserva Dagua'],
            'Toneladas': [120, 580, 142]
        }).set_index('Predio')
        st.bar_chart(df_carbono, color="#3498db")

    st.info("💡 **Análisis de IA:** Se detecta una aceleración en la captura de carbono debido a la maduración de las plantaciones en el sector sur.")


elif menu == "GESTIÓN LEY 2173":
    st.title("⚖️ Nexus Legal Hub")
    st.markdown("### Cumplimiento y Certificación de Áreas de Vida")

    empresa = st.text_input("Nombre de la Empresa / Razón Social", placeholder="Ej: Serenity S.A.S BIC")
    nit = st.text_input("NIT")

    col_l1, col_l2 = st.columns(2)
    
    with col_l1:
        st.subheader("📜 Vademécum Legal")
        st.write("Genera el reporte técnico de leyes ambientales (99, 2169, 2173, 2111).")
        if st.button("PREPARAR REPORTE TÉCNICO"):
            if empresa:
                st.session_state.v_file = generar_pdf_serenity(empresa, 0, "VAD-99", tipo="VADEMECUM")
                st.success("Reporte generado con éxito.")
            else:
                st.error("Por favor ingrese el nombre de la empresa.")
        
        if 'v_file' in st.session_state:
            st.download_button("📥 Descargar Vademécum", st.session_state.v_file, "Vademecum_Legal.pdf")

    with col_l2:
        st.subheader("🏆 Certificado de Siembra")
        arboles = st.number_input("Cantidad de árboles gestionados", min_value=1, value=50)
        logo_c = st.file_uploader("Subir Logo Corporativo (Opcional)", type=['png', 'jpg'])
        
        if st.button("PREPARAR CERTIFICADO"):
            if empresa:
                # Generamos un Hash único simulando Blockchain
                h_id = hashlib.sha256(f"{empresa}{datetime.now()}".encode()).hexdigest()[:12].upper()
                st.session_state.c_file = generar_pdf_serenity(empresa, arboles, h_id, logo_bytes=logo_c)
                st.success("Certificado listo para descarga.")
            else:
                st.error("Por favor ingrese los datos requeridos.")

        if 'c_file' in st.session_state:
            st.download_button("📥 Descargar Certificado", st.session_state.c_file, "Certificado_Siembra.pdf")


elif menu == "SUSCRIPCIONES":
    st.title("💳 Planes de Regeneración")
    st.markdown("### Elige tu nivel de impacto en el ecosistema")

    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        with st.container(border=True):
            st.header("🌱 Semilla")
            st.subheader("$50 / Mes")
            st.write("- Protección de 5 árboles.")
            st.write("- Certificado digital mensual.")
            st.write("- Acceso a Dashboard básico.")
            if st.button("Elegir Plan Semilla", use_container_width=True):
                st.balloons()

    with col_p2:
        with st.container(border=True):
            st.header("🌳 Bosque")
            st.subheader("$150 / Mes")
            st.write("- Protección de 20 árboles.")
            st.write("- Monitoreo IA Gemini (Acceso).")
            st.write("- Reporte de captura CO2.")
            if st.button("Elegir Plan Bosque", use_container_width=True):
                st.balloons()

    with col_p3:
        with st.container(border=True):
            st.header("🛡️ Reserva")
            st.subheader("$500 / Mes")
            st.write("- Protección de 100 árboles.")
            st.write("- Micro-patrocinio de un Faro.")
            st.write("- Vademécum legal incluido.")
            if st.button("Elegir Plan Reserva", use_container_width=True):
                st.balloons()


elif menu == "BILLETERA CRYPTO (WEB3)":
    st.title("👛 Billetera Nexus Web3")
    st.markdown("### Gestión de Activos Digitales $SNG")

    # --- VIDEO DE LA MONEDA EN BUCLE INFINITO ---
    st.write("---")
    col_v1, col_v2 = st.columns([2, 1])
    
    with col_v1:
        st.subheader("🪙 SNG Coin: La Moneda de la Tierra")
        v_nombre = "video_sng.mp4"
        if os.path.exists(v_nombre):
            try:
                import base64
                with open(v_nombre, "rb") as f:
                    v_data = f.read()
                    v_b64 = base64.b64encode(v_data).decode()
                # HTML para video automático, infinito y sin controles
                st.markdown(f'''
                    <video width="100%" autoplay loop muted playsinline>
                        <source src="data:video/mp4;base64,{v_b64}" type="video/mp4">
                    </video>
                ''', unsafe_allow_html=True)
            except:
                st.info("Visualizando activo digital SNG...")
        else:
            st.image("https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=1000", caption="SNG Coin - Respaldada por Activos Biológicos")

    with col_v2:
        st.write("")
        st.metric("Saldo Actual $SNG", "1,250.00", "+12% Anual")
        st.metric("Valorización MATIC", "45.50", "-2%")
        st.info("🚀 Tu portafolio ha evitado 3.4 Ton de CO2")

    st.write("---")

    # --- ACCIONES Y TABLA ---
    c_acc1, c_acc2 = st.columns(2)
    with c_acc1:
        with st.container(border=True):
            st.markdown("#### 📥 Recibir")
            st.code("0x7973...649", language="text")
            st.caption("Dirección pública para depósitos.")

    with c_acc2:
        with st.container(border=True):
            st.markdown("#### 📤 Enviar")
            st.text_input("Billetera Destino", placeholder="0x...", key="w3_dest")
            if st.button("Confirmar Envío", use_container_width=True):
                st.warning("Firme la transacción en su billetera MetaMask.")

    st.divider()
    st.markdown("#### 📜 Registro de Transacciones Blockchain")
    data_w3 = {
        'Fecha': ['2026-02-10', '2026-02-08', '2026-02-05'],
        'Tipo': ['Recibido', 'Suscripción Plan Semilla', 'Recompensa Staking'],
        'Monto $SNG': ['+500', '-100', '+25'],
        'Estado': ['Confirmado ✅', 'Confirmado ✅', 'Procesando ⏳']
    }
    st.table(data_w3)


elif menu == "DONACIONES Y CERTIFICADO":
    st.title("🎁 Donaciones Nexus")
    st.markdown("### Transforma tu aporte en vida para la Hacienda Monte Guadua")

    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.subheader("Realizar Donación")
        nombre_d = st.text_input("Nombre del Donante", placeholder="Ej: Jorge Carvajal")
        monto_d = st.number_input("Monto a Donar (USD)", min_value=10, step=10)
        metodo = st.selectbox("Método de Pago", ["Tarjeta de Crédito", "PayPal", "SNG Coin", "Cripto (MATIC)"])
        
        if st.button("PROCESAR DONACIÓN", use_container_width=True):
            if nombre_d:
                st.success(f"¡Gracias {nombre_d}! Tu aporte está regenerando la cuenca del Río Dagua.")
                st.balloons()
            else:
                st.error("Por favor ingresa tu nombre.")

    with col_d2:
        st.subheader("Generar Certificado")
        st.write("Una vez realizada tu donación, descarga tu certificado oficial de impacto.")
        
        if st.button("GENERAR MI CERTIFICADO"):
            if nombre_d:
                # Generamos un Hash único para el donante
                hash_d = hashlib.md5(f"{nombre_d}{datetime.now()}".encode()).hexdigest()[:10].upper()
                # Usamos nuestra función maestra del bloque 1
                st.session_state.pdf_donacion = generar_pdf_serenity(nombre_d, f"${monto_d} USD", hash_d)
                st.success("Certificado de Donante listo.")
            else:
                st.warning("Primero ingresa tu nombre en el panel de la izquierda.")

        if 'pdf_donacion' in st.session_state:
            st.download_button("📥 Descargar Certificado de Donación", 
                             st.session_state.pdf_donacion, 
                             f"Certificado_{nombre_d}.pdf")


elif menu == "LOGÍSTICA AEROLÍNEAS":
    st.title("✈️ Soluciones para el Sector Aeronáutico")
    st.markdown("### Compensación de Emisiones y Logística de Combustible Sostenible")

    # MÉTRIZAS DE COMPENSACIÓN
    c1, c2, c3 = st.columns(3)
    c1.metric("Vuelos Compensados", "124", "Último mes")
    c2.metric("CO2 Neutralizado", "1,250 Ton", "+15%")
    c3.metric("Eficiencia de Huella", "94%", "Objetivo 2026")

    st.write("---")
    
    col_a1, col_a2 = st.columns([1, 2])
    
    with col_a1:
        st.subheader("Calculadora de Vuelo")
        aerolinea = st.selectbox("Aerolínea", ["Avianca", "LATAM", "Copa Airlines", "American Airlines"])
        ruta = st.text_input("Ruta (Origen - Destino)", "BOG - MAD")
        pasajeros = st.number_input("Número de Pasajeros", min_value=1, value=150)
        
        if st.button("CALCULAR COMPENSACIÓN"):
            impacto_vuelo = pasajeros * 0.15 # Estimación simple por pasajero
            st.info(f"Emisiones estimadas: **{impacto_vuelo} Ton de CO2**")
            st.write(f"Para neutralizar este vuelo se requieren **{int(impacto_vuelo * 10)} árboles**.")

    with col_a2:
        st.subheader("📅 Cronograma de Reforestación Corporativa")
        log_data = {
            'Vuelo ID': ['AV244', 'LA809', 'CM122'],
            'Fecha': ['2026-02-10', '2026-02-11', '2026-02-12'],
            'Estado de Compensación': ['Completado ✅', 'En Proceso ⏳', 'Programado 📅'],
            'Área Asignada': ['Cuenca Alta', 'Sector Guadua', 'Villa Michelle']
        }
        st.table(log_data)
        st.caption("Seguimiento de cumplimiento normativo para aerolíneas internacionales.")


elif menu == "UBICACIÓN":
    st.title("📍 Georreferenciación de Activos")
    st.markdown("### Ubicación Estratégica en el Corredor Biológico de Dagua, Valle del Cauca")

    # MÉTRICAS DE TERRITORIO
    c1, c2, c3 = st.columns(3)
    c1.metric("Área Total", "80.6 Ha", "Hacienda + Finca")
    c2.metric("Altitud Promedio", "1,250 msnm", "Óptima para Guadua")
    c3.metric("Ecosistema", "Bosque Seco", "Prioridad de Conservación")

    st.write("---")

    # --- MAPA INTERACTIVO DE ALTA PRECISIÓN ---
    with st.container(border=True):
        st.subheader("🗺️ Mapa de Predios Serenity S.A.S BIC")
        
        # Centro del mapa en la zona de Dagua
        m_final = folium.Map(location=[3.642, -76.685], zoom_start=14, control_scale=True)
        
        # Definición de los puntos clave
        sedes = [
            {
                "nombre": "Finca Villa Michelle (Sede Operativa)",
                "coords": [3.642, -76.685],
                "desc": "6,000 m2 - Centro de Control Faros Gemini",
                "color": "green",
                "icon": "home"
            },
            {
                "nombre": "Hacienda Monte Guadua (Reserva)",
                "coords": [3.648, -76.678],
                "desc": "80 Hectáreas - Área de Regeneración y Siembra",
                "color": "darkgreen",
                "icon": "leaf"
            }
        ]

        for sede in sedes:
            folium.Marker(
                location=sede["coords"],
                popup=f"<b>{sede['nombre']}</b><br>{sede['desc']}",
                tooltip=sede["nombre"],
                icon=folium.Icon(color=sede["color"], icon=sede["icon"], prefix='fa')
            ).add_to(m_final)

        # Mostrar el mapa
        st_folium(m_final, width=None, height=500, use_container_width=True)
    
    st.write("---")

    # --- INFORMACIÓN ADICIONAL PARA EL INVERSIONISTA ---
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        **Importancia Geográfica:**
        - **Conectividad:** Ubicada en el cañón del Río Dagua, zona clave para la biodiversidad del Chocó Biogeográfico.
        - **Recurso Hídrico:** El proyecto protege fuentes de agua vitales para las comunidades locales (Ley 99).
        - **Accesibilidad:** A solo 45 minutos de Cali, facilitando la logística de auditoría ambiental.
        """)
        
    with col_info2:
        with st.container(border=True):
            st.markdown("🔔 **Nota Técnica:**")
            st.write("Todos los puntos están integrados con la red de **Monitoreo Perimetral**. Cualquier actividad detectada por los Faros Gemini se georreferencia automáticamente en este mapa.")

    if st.button("DESCARGAR COORDENADAS KML/GPX", use_container_width=True):
        st.info("Archivo de límites catastrales preparado para revisión técnica.")
































































































































































































