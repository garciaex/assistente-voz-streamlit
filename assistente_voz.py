import streamlit as st
import speech_recognition as sr
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from gtts import gTTS
import os

# Configuração do chatbot
chatbot = ChatBot('Assistente')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.portuguese")  # Treina com corpus em português

# Função para reconhecer fala
def ouvir_microfone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Diga algo...")
        audio = recognizer.listen(source)
        try:
            texto = recognizer.recognize_google(audio, language="pt-BR")
            st.write(f"Você disse: {texto}")
            return texto
        except sr.UnknownValueError:
            st.write("Não entendi o que você disse.")
            return None
        except sr.RequestError:
            st.write("Erro ao conectar ao serviço de reconhecimento de fala.")
            return None

# Função para sintetizar voz
def falar(texto):
    tts = gTTS(text=texto, lang='pt', slow=False, tld='com.br')  # Voz feminina em português
    tts.save("resposta.mp3")
    st.audio("resposta.mp3", format="audio/mp3")

# Interface do Streamlit
st.title("Assistente de Voz em Português  ")
st.write("Clique no botão abaixo e fale algo para interagir com o assistente.")

if st.button("Falar com o Assistente"):
    comando = ouvir_microfone()
    if comando:
        resposta = chatbot.get_response(comando)
        st.write(f"Assistente: {resposta}")
        falar(str(resposta))