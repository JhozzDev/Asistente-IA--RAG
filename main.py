from groq import Groq
from dotenv import load_dotenv
import PyPDF2
import streamlit as st


load_dotenv()
client = Groq()

st.title("AI PDF Assistant")
st.write("Sube tu documento y tendras un asistente personal")

pdf = st.file_uploader("Sube tu documento PDF", type="pdf")

if pdf:
    lector = PyPDF2.PdfReader(pdf)
    documento = ""
    for pagina in lector.pages:
        documento += pagina.extract_text()

    if "historial" not in st.session_state:
        st.session_state.historial = [{
        "role": "system",
        "content": f"""Eres un asistente experto en analizar documentos.
        Responde ÚNICAMENTE basándote en el siguiente documento:
        
        {documento}
        
        Si la respuesta no está en el documento, dilo claramente."""
    }]
        
  
    for message in st.session_state.historial[1:]:
        if message["role"] == "user":
            st.chat_message("User").write(message["content"])
        else:
            st.chat_message("Assistant").write(message["content"])

    pregunta = st.chat_input("Hazle una pregunta a sobre tu documento...")

    if pregunta:
                st.session_state.historial.append({"role": "user", "content": pregunta})
                st.chat_message("User").write(pregunta)

                process = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                        messages=st.session_state.historial
                    )

                respuesta = process.choices[0].message.content
                st.session_state.historial.append({"role": "assistant", "content": respuesta})
                st.chat_message("Assistant").write(respuesta)

