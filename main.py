import streamlit as st
import fitz
from groq import Groq
import os

GROQ_API_KEY = "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"
if not GROQ_API_KEY:
    st.error("A chave GROQ_API_KEY não foi definida corretamente.")
    st.stop()  
client = Groq(api_key = GROQ_API_KEY)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")

def extract_files(uploader):
    text = ""
    for pdf in uploader:
        with fitz.open(stream = pdf.read(), filetype = "pdf") as doc:
            for page in doc:
                text += page.get_text("text")
    return text

def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um assistente inteligente especializado em organização de rotina de estudos."},
            {"role": "user", "content": f"{context}\n\n Pergunta: {prompt}"}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("Gerenciamento de Tarefa Escolar")
    with st.sidebar:
        st.header("UPLoader Files")
        uploader = st.file_uploader("Adicione Arquivos", type = "pdf", accept_multiple_files = True)

    if uploader:
        text = extract_files(uploader)
        st.session_state["document-text"] = text

    user_input = st.text_input("Digite aqui...")

if __name__ == "__main__":
    main()
