import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Serenity Nexus Global - V27.0", layout="wide", page_icon="🌿")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #2e7d32; color: white; }
    .faro-card { padding: 20px; border-radius: 15px; background-color: white; border-left: 5px solid #1b5e20; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (LOGOS Y NAVEGACIÓN) ---
with st.sidebar:
    st.image("https://via.placeholder.com/150?text=SERENITY+LOGO", width=150) # Aquí va tu logo original
    st.title("Serenity S.A.S BIC")
    menu = st.radio("Navegación", ["Inicio", "Puntos Faro", "Certificados", "Seguridad y Ley", "SNG Digital"])

# --- SECCIÓN 1: INICIO (MISIÓN Y VISIÓN) ---
if menu == "Inicio":
    st.title("🌿 Serenity Nexus Global")
    st.subheader("La Novena Maravilla: Ecoturismo y Tecnología")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("### Misión\nTransformar la relación entre el ser humano y la biodiversidad mediante tecnología de vanguardia y conservación activa en la Hacienda Monte Guadua.")
    with col2:
        st.success("### Visión\nSer el referente mundial en monitoreo ambiental y turismo de lujo sostenible para el año 2030.")

    st.write("---")
    st.markdown("### Estado del Proyecto")
    st.write(f"**Administrador:** Jorge Carvajal")
    st.write(f"**Ubicación:** Dagua y Felidia, Valle del Cauca, Colombia")

# --- SECCIÓN 2: PUNTOS FARO (MONITOREO) ---
elif menu == "Puntos Faro":
    st.header("📡 Red de Monitoreo - Hacienda Monte Guadua")
    
    faros = ["Faro 1", "Faro 2", "Faro 3", "Faro 4", "Faro 5", "Faro 6", "Faro Gemini (Especial)"]
    
    selected_faro = st.selectbox("Seleccione un Punto Faro para ingresar:", faros)
    
    st.markdown(f"<div class='faro-card'><h3>Acceso a {selected_faro}</h3></div>", unsafe_allow_html=True)
    
    col_cam, col_mic = st.columns([2, 1])
    
    with col_cam:
        st.subheader("🎥 Cámaras de Seguridad y Biodiversidad")
        c1, c2, c3, c4 = st.columns(4)
        c5, c6, c7, c8 = st.columns(4)
        for i, col in enumerate([c1, c2, c3, c4, c5, c6, c7, c8], 1):
            col.button(f"Cam {i}")
            col.image(f"https://via.placeholder.com/100?text=Feed+Cam+{i}", use_container_width=True)
            
    with col_mic:
        st.subheader("🎙️ Sensores de Audio")
        for j in range(1, 5):
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Simulación de audio
            st.caption(f"Micrófono {j} - Activo")

# --- SECCIÓN 3: CERTIFICADOS (LEY 2173) ---
elif menu == "Certificados":
    st.header("📜 Gestión de Certificados Ambientales")
    st.write("Descarga de certificados de protección y siembra.")
    
    nombre = st.text_input("Nombre del Donante / Empresa")
    tipo = st.selectbox("Tipo de Certificado", ["Siembra de Árbol", "Protección de Hectárea", "Carbono Neutro"])
    
    if st.button("Generar y Descargar Certificado"):
        st.write(f"Generando certificado para {nombre}...")
        # Aquí se integra la lógica de ReportLab/SHA-3 que teníamos
        st.success("✅ Certificado generado exitosamente (Simulación de descarga)")

# --- SECCIÓN 4: SEGURIDAD Y LEY ---
elif menu == "Seguridad y Ley":
    st.header("⚖️ Integración con la Ley")
    st.warning("Conexión directa con autoridades ambientales y policía nacional.")
    if st.button("🚨 ACTIVAR ALERTA DE INTRUSIÓN"):
        st.error("Alerta enviada a los cuadrantes de Dagua y Felidia.")

# --- SECCIÓN 5: SNG DIGITAL ---
elif menu == "SNG Digital":
    st.header("💰 Serenity Nexus Global (SNG) Token")
    st.metric(label="Valor SNG", value="$1.00 USD", delta="0.05%")
    st.write("Gestión de donaciones y recompensas del ecosistema Serenity.")









































































