import streamlit as st 
import pydub 
from io import BytesIO
import speech_recognition as sr 
from langchain_community.llms import Ollama

#1
st.header('Import Audio')
input_type = st.radio('', ['Upload audio file', 'Record audio'])

if input_type=='Upload audio file':
    audio =  st.file_uploader('Import audio file') 

elif input_type=='Record audio':
    audio = st.audio_input('Record audio')
if audio:
    st.audio(audio)
#2
if audio:
    # Raw audio
    audio_raw = pydub.AudioSegment.from_file(audio)

    # Convert to .wav
    audio_wav = BytesIO()
    audio_raw.export(audio_wav, format="wav")

    #convert to text 
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_wav) as source: 
        audio_txt = recognizer.record(source)
    audio_txt = recognizer.recognize_whisper(audio_txt)

#3
llm = Ollama(model='llama3.1:8b')
prompt = st.text_input('Prompt')
response = llm.invoke(prompt)

st.write(response)


#4 
if st.button('Speech-to-Text'):
    text_output = audio_txt



#5
if st.button('Main Topic'): 
    with st.spinner('Loading...'):
        text_output = llm.invoke('Identify the three main topics from the following text.Be very quick and concise: ' + audio_txt)

#6
language = st.selectbox('', options=['French', 'Spanish', 'German', 'Portuguese' ], placeholder="Translate", index=None)

if language:
    with st.spinner('Loading...'):
        text_output = llm.invoke('Translate in' + language + 'The following text:', audio_txt)
    
#features 7 and 8 from https://www.youtube.com/watch?v=pqsCZKzZdsY are irrelavants
