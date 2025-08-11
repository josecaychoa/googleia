import streamlit as st
import google.generativeai as genai
import os

# --- Configuración de la página de Streamlit ---
# Es bueno poner esto al principio para que la página cargue con la configuración correcta.
st.set_page_config(
    page_title="Contador de Tokens con Gemini",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Contador de Tokens con Gemini")
st.caption("Una aplicación para contar los tokens de un texto usando el modelo Gemini de Google.")

# --- Configuración de la API Key ---
# Usamos st.secrets para mayor seguridad al desplegar en Streamlit Community Cloud.
# El usuario debe agregar su GOOGLE_API_KEY en los secretos de la aplicación.
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash') # Usamos el modelo recomendado
    st.success("API Key cargada correctamente desde los secretos.")
except KeyError:
    st.error("Error: La GOOGLE_API_KEY no se encontró en los secretos de Streamlit.")
    st.info("Por favor, agrega tu clave de API en la configuración de secretos de tu aplicación en Streamlit Cloud.")
    st.stop() # Detiene la ejecución si no hay API Key

# --- Interfaz de Usuario ---
st.header("Ingresa tu texto aquí")

# Usamos un área de texto para que el usuario pueda pegar textos largos.
user_text = st.text_area(
    "Escribe o pega el texto que quieres analizar:",
    height=200,
    placeholder="El rápido zorro marrón salta sobre el perro perezoso."
)

if st.button("Contar Tokens", type="primary"):
    if user_text:
        with st.spinner("Contando tokens..."):
            try:
                # Llama a la API para contar los tokens
                response = model.count_tokens(user_text)
                
                # Muestra el resultado
                st.subheader("Resultado")
                st.metric(label="Frase analizada", value=f'"{user_text[:50]}..."')
                st.metric(label="Cantidad Total de Tokens", value=response.total_tokens)

            except Exception as e:
                st.error(f"Ocurrió un error al contactar la API de Gemini: {e}")
    else:
        st.warning("Por favor, ingresa un texto para poder contar los tokens.")