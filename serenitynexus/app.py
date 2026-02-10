import streamlit as st
import hashlib
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# --- 1. CONFIGURACIÓN DE SEGURIDAD (SHA-3 512) ---
def generar_hash_inmutable(datos):
    return hashlib.sha3_512(datos.encode('utf-8')).hexdigest()

# --- 2. MOTOR DE CERTIFICADOS (LEY 2173) ---
def generar_pdf_legal(nombre, tipo, hash_id):
    filename = f"Certificado_{nombre.replace(' ', '_')}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "SERENITY S.A.S BIC - CERTIFICADO AMBIENTAL")
    c.setFont("Helvetica", 10)
    c.drawString(100, 730, "En cumplimiento con la Ley 2173 de Colombia")
    c.line(100, 725, 500, 725)
    c.drawString(100, 700, f"Titular: {nombre}")
    c.drawString(100, 680, f"Acción: {tipo}")
    c.drawString(100, 660, f"Ubicación: Hacienda Monte Guadua, Valle del Cauca")
    c.setFont("Courier", 7)
    c.drawString(100, 620, f"Sello Digital de Autenticidad (SHA-3):")
    c.drawString(100, 610, f"{hash_id}")
    c.save()
    return filename

# --- 3. CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="Serenity Nexus Global", layout="wide", page_icon="🌿")

# --- 4. CABECERA CON LOGO Y FILOSOFÍA ---
col_logo, col_tit = st.columns([1, 4])
with col_logo:
    # IMPORTANTE: Reemplaza 'logo_serenity.png' con tu archivo real
    try:
        st.image("logo_serenity.png", width=150)
    except:
        st.info("Logo: Serenity S.A.S BIC")

with col_tit:
    st.title("SERENITY NEXUS GLOBAL")
    st.markdown("### *La Novena Maravilla del Mundo*")

st.sidebar.markdown("## Panel de Control")
menu = st.sidebar.radio("Navegación Principal", 
    ["Inicio (Misión/Visión)", "Puntos Faro (Monitoreo)", "SNG Digital & Socias", "Certificados Legales"])

# --- 5. LÓGICA DE NAVEGACIÓN ---

if menu == "Inicio (Misión/Visión)":
    st.header("🌿 Nuestra Identidad")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Misión")
        st.write("Fomentar la protección de la biodiversidad en la Hacienda Monte Guadua mediante tecnología disruptiva y ecoturismo de lujo.")
    with col2:
        st.subheader("Visión")
        st.write("Ser el modelo global de regeneración ambiental inmutable para 2030.")
    st.divider()
    st.markdown(f"**Administrador del Sistema:** Jorge Carvajal")

elif menu == "Puntos Faro (Monitoreo)":
    st.header("📡 Red de Puntos Faro - Hacienda Monte Guadua")
    faros = [f"Punto Faro {i}" for i in range(1, 7)] + ["Punto Faro Gemini (Honorario)"]
    faro_sel = st.selectbox("Seleccione Faro para visualización:", faros)
    
    st.success(f"Conexión Establecida con {faro_sel}")
    
    # Matriz de 8 Cámaras y 4 Micrófonos
    st.subheader("🎥 Feed de Cámaras (8)")
    cols_cam = st.columns(4)
    for i in range(1, 9):
        with cols_cam[(i-1)%4]:
            st.button(f"Cam {faro_sel[-1]}.{i}")
            st.image(f"https://via.placeholder.com/150?text=CAM+{i}", use_container_width=True)
    
    st.subheader("🎙️ Sensores de Audio (4)")
    cols_mic = st.columns(4)
    for i in range(1, 5):
        cols_mic[i-1].audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        cols_mic[i-1].caption(f"Micrófono {i} - ONLINE")

elif menu == "SNG Digital & Socias":
    st.header("💎 Ecosistema Serenity Nexus Global")
    
    # Lógica de Socias
    st.subheader("Gobernanza de Socias")
    col_t, col_s = st.columns(2)
    col_t.metric("Tatiana Arcila Ferreira", "60% Participación")
    col_s.metric("Sandra Patricia Agredo Muñoz", "40% Participación")
    
    # Token SNG
    st.divider()
    st.subheader("Moneda SNG")
    ha = st.number_input("Hectáreas bajo protección:", 0, 80)
    tokens = ha * 1000
    st.info(f"Emisión proyectada de SNG: {tokens} Tokens")

elif menu == "Certificados Legales":
    st.header("📜 Emisor de Certificados Inmutables")
    nombre_user = st.text_input("Nombre del Beneficiario:")
    tipo_accion = st.selectbox("Tipo de Acción Ambiental:", ["Siembra Directa", "Protección de Bosque", "Monitoreo de Especies"])
    
    if st.button("Generar Certificado con Hash SHA-3"):
        if nombre_user:
            datos_raw = f"{nombre_user}-{tipo_accion}-{datetime.now()}"
            hash_digital = generar_hash_inmutable(datos_raw)
            pdf_path = generar_pdf_legal(nombre_user, tipo_accion, hash_digital)
            
            st.success(f"Certificado generado exitosamente.")
            st.code(f"HASH DE SEGURIDAD: {hash_digital}")
            with open(pdf_path, "rb") as file:
                st.download_button("Descargar PDF Oficial", data=file, file_name=pdf_path)
        else:
            st.error("Por favor ingrese un nombre.")

# --- 6. FOOTER DE SEGURIDAD ---
st.sidebar.divider()
if st.sidebar.button("🚨 PROTOCOLO DE CIERRE (KILL SWITCH)"):
    st.sidebar.error("SISTEMA DESCONECTADO POR SEGURIDAD")










































































