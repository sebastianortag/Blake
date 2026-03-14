import streamlit as st
import anthropic
import requests 
from datetime import datetime 

st.title("Agente de Freight Forwarding")
st.caption("Conectado al tipo de cambio en tiempo real")

def obtener_tipo_cambio():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        respuesta = requests.get(url)
        datos = respuesta.json()
        mxn = datos["rates"]["MXN"]
        return f"1 USD = {mxn} MXN"
    except: 
        return "No se pudo obtener el tipo de cambio"

tipo_cambio = obtener_tipo_cambio()
st.info(f"Tipo de cambio actual: {tipo_cambio}")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

if pregunta := st.chat_input("Escribe tu pregunta..."):
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    client = anthropic.Anthropic()
    respuesta = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=f"""Eres un agente experto en freight forwarding internacional.
Tienes acceso a datos en tiempo real:
- Tipo de cambio actual: {tipo_cambio}
- Fecha de hoy: {datetime.now().strftime('%Y-%m-%d')}
Responde siempre en español de manera clara y práctica.""",
        messages=st.session_state.mensajes
    )

    texto = respuesta.content[0].text
    st.session_state.mensajes.append({"role": "assistant", "content": texto})
    with st.chat_message("assistant"):
        st.markdown(texto)
        