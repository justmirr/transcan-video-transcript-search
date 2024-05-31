from pydub import AudioSegment
import numpy as np
import streamlit as st
import whisper
import logging
import io

@st.cache_resource
def load_model():
    return whisper.load_model("tiny.en.pt")

@st.cache_data
def load_audio(file, sr=16000):
    """
    Open an audio file and read as mono waveform, resampling as necessary.
    """
    logging.info(f"Attempting to load audio from: {type(file)}")
    try:
        if isinstance(file, bytes):
            audio = AudioSegment.from_file(io.BytesIO(file))
        else:
            audio = AudioSegment.from_file(file)

        audio = audio.set_frame_rate(sr).set_channels(1)

        raw_data = audio.raw_data
        audio_data = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0

    except Exception as e:
        logging.error(f"Failed to load audio: {e}")
        raise RuntimeError(f"Failed to load audio: {e}") from e

    return audio_data

@st.cache_data
def searcher(trans_dict, query):
    results = []
    segments = trans_dict['segments']
    for segment in segments:
        if query.lower() in segment['text'].lower():
            start_m, start_s = divmod(int(segment['start']), 60)
            text = segment['text'].lower()
            results.append(f'{start_m}m {start_s}s - {text}')
    return results

@st.cache_data
def transcribe(_model, audio_array):
    return _model.transcribe(audio_array, language='english')