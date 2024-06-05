import pyaudio
import streamlit as st
import wave
import whisper

# Function to handle speech input using Whisper
def get_speech_input():
    filename = "ui/tmp/output.wav"
    speechtotext(filename)
    st.success("Processing...")
    audio = whisper.load_audio(filename)
    result = st.session_state.whisper_model.transcribe(audio, fp16=False)
    st.session_state.is_listening = False
    return result["text"]

# Function to handle audio recording
def speechtotext(filename="output.wav", duration=5, fs=44100):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024)
    
    st.info("Recording...")
    frames = []
    for _ in range(0, int(fs / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    st.success("Recording finished.")