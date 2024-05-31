from pytube import YouTube
import streamlit as st
import os

@st.cache_data
def get_yt_bytes(yt_link):
    audio = YouTube(yt_link).streams.filter(only_audio=True).first().download()
    _bytes = None
    with open(audio, "rb") as f:
        _bytes = f.read()
    # After reading the file, ensure the file handle is closed
    # Then remove the file
    if _bytes is not None:
        os.remove(audio)

    return _bytes