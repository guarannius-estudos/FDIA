import streamlit as st
import fitz
from groq import Groq

GROQ_API_KEY = "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"
if not GROQ_API_KEY:
    st.error("A chave GROQ_API_KEY não foi definida corretamente.")
    st.stop()
client = Groq(api_key = GROQ_API_KEY)

def extract_files(uploader_pdf):
    text = ""
    for pdf in uploader_pdf:
        with fitz.open(stream = pdf.read(), filetype = "pdf") as doc:
            for page in doc:
                text += page.get_text("text")
    return text

def chat_with_groq(prompt, context):
    response = client.chat.completions.create(model = "llama-3.3-70b-versatile", messages = [
            {"role": "system", "content": "Você é um assistente que responde perguntas referentes a planejamento escolar, com base em documentos PDF fornecidos. Responda apenas perguntas referentes ao assunto estipulado."},
            {"role": "user", "content": f"{context}\n\nPergunta: {prompt}"}
        ]
    )
    return response.choices[0].message.content

def main():
    st.image("logo.png", width = 125)
    st.title("Gerenciamento de Tarefas Escolares")

    with st.sidebar:
        st.header("Upload de arquivos PDF")
        uploader_pdf = st.file_uploader("Adicione seu arquivo PDF", type = "pdf", accept_multiple_files = True)

    if uploader_pdf:
        text = extract_files(uploader_pdf)
        st.session_state["document_text"] = text

    user_input = st.text_input("Digite aqui:")

    if user_input and "document_text" in st.session_state:
        response = chat_with_groq(user_input, st.session_state["document_text"])
        st.write("Resposta:", response)

if __name__ == "__main__":
    main()
