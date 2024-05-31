import streamlit as st
from utils import load_audio, searcher, load_model, transcribe
from youtube_handler import get_yt_bytes
from transcan import summarize_link, transcription, summarize_uploaded

st.set_page_config(
    page_title="TranScan - Video Transcript Search",
    page_icon="🔍"
)

@st.cache_resource
def get_model():
    return load_model()

model = get_model()

audio_ext = ["mp3", "ogg", "wav", "aac", "m4a", "flac", "avi", "wma"]
video_ext = ["mp4", "mkv", "mov", "wmv"]

reduce_header_height_style = """
    <style>
        div.block-container {padding-top:1rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

st.title('TranScan - Video Transcript Search')

upload_type = st.radio(
    "What kind of video do you want to search?",
    ('YouTube Video', 'Upload a Video')
)

if upload_type == 'YouTube Video':
    yt_link = st.text_input("Enter a YouTube Video Link:")
    if len(yt_link) > 10:
        task_youtube = st.radio(
            "What task do you want to perform?",
            ('Summarize Video', 'Search within Video')
        )
        if task_youtube == 'Summarize Video':
            method_youtube = st.radio(
                "Summarization Method",
                ('Use Transcripts', 'Load from Audio')
            )
            if method_youtube == 'Use Transcripts':
                if st.button("Summarize"):
                    try:
                        summarized_text = summarize_link(yt_link)
                        st.write("Summarized Transcript:")
                        st.write("<p style='text-align: justify;'>{}</p>".format(" ".join(summarized_text)), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Failed to summarize: {e}")
            else:
                try:
                    audio_bytes = get_yt_bytes(yt_link)
                    audio_array = load_audio(audio_bytes)
                    st.success("Audio loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading YouTube video: {e}")
                    audio_bytes = None
                if st.button("Summarize"):
                    if audio_bytes:
                        try:
                            transcript_dict = transcribe(model, audio_array)
                            full_transcript = " ".join(segment['text'] for segment in transcript_dict['segments'])
                            summarized_text = summarize_uploaded(full_transcript)
                            st.write("Summarized Transcript:")
                            st.write("<p style='text-align: justify;'>{}</p>".format(" ".join(summarized_text)), unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error during audio processing or summarization: {e}")
        else:
            transcribe_method = st.radio(
                "Transciption Method",
                ('Use Transcripts', 'Load from Audio')
            )
            if transcribe_method == 'Use Transcripts':
                transcript = transcription(yt_link)
                query = st.text_input("Enter some text to search within the video:")
                if len(query) > 0 and st.button('Search'):
                    data_load_state = st.text('Searching!')
                    results = []
                    data_load_state.text('Search done!')
                    for text, start in transcript:
                        if query.lower() in text.lower():
                            minutes = int(start // 60)
                            seconds = int(start % 60)
                            time_format = f"{minutes}m {seconds}s"
                            results.append((text, time_format))
                    if results:
                        st.write("Search results found:")
                        for result in results:
                            st.write(f"{result[1]} - '{result[0]}'")
                    else:
                        st.write("No results found for your query.")
            else:
                try:
                    audio_bytes = get_yt_bytes(yt_link)
                    st.success("YouTube video loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading YouTube video: {e}")
                    audio_bytes = None

                if audio_bytes:
                    query = st.text_input("Enter some text to search within the video:")

                    try:
                        audio_array = load_audio(audio_bytes)
                        st.success("Audio loaded successfully!")
                    except Exception as e:
                        st.error(f"Error loading audio: {e}")
                        audio_array = None

                    if audio_array is not None and st.button('Search') and len(query) > 1:
                        data_load_state = st.text('Searching!')
                        try:
                            trans_dict = transcribe(model, audio_array)
                            search_result = searcher(trans_dict, query)
                            data_load_state.text('Search done!')

                            if search_result:
                                st.write(f"We found '{query}' at the following position(s):")
                                for item in search_result:
                                    st.write(item)
                            else:
                                st.write(f"We couldn't find '{query}'")
                        except Exception as e:
                            st.error(f"Error during transcription or search: {e}")
else:
    uploaded_file = st.file_uploader("Upload a file", type=audio_ext + video_ext)
    if uploaded_file is not None:
        audio_bytes = uploaded_file.getvalue()
        st.success("File uploaded successfully!")

        task_upload = st.radio(
            "What task do you want to perform?",
            ('Summarize Video', 'Search within Video')
        )

        if task_upload == 'Summarize Video' and st.button('Summarize'):
            try:
                audio_array = load_audio(audio_bytes)
                st.success("Audio loaded successfully!")
                transcript_dict = transcribe(model, audio_array)
                full_transcript = " ".join(segment['text'] for segment in transcript_dict['segments'])
                summarized_text = summarize_uploaded(full_transcript)
                
                st.write("Summarized Transcript:")
                st.write("<p style='text-align: justify;'>{}</p>".format(" ".join(summarized_text)), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error during audio processing or summarization: {e}")

        elif task_upload == 'Search within Video':
            query = st.text_input("Enter some text to search within the video:")
            if len(query) > 1 and st.button('Search'):
                data_load_state = st.text('Searching!')
                try:
                    audio_array = load_audio(audio_bytes)
                    st.success("Audio loaded successfully!")
                    trans_dict = transcribe(model, audio_array)
                    search_result = searcher(trans_dict, query)
                    data_load_state.text('Search done!')

                    if search_result:
                        st.write(f"We found '{query}' at the following position(s):")
                        for item in search_result:
                            st.write(item)
                    else:
                        st.write(f"We couldn't find '{query}'")
                except Exception as e:
                    st.error(f"Error during transcription or search: {e}")

