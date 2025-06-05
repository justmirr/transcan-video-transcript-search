# TranScan

TranScan is a **Streamlit application** designed for **summarizing and searching video transcripts**. It leverages **YouTube_Transcript_API** and **Whisper** for audio to fetch transcripts, **Hugging Face's Transformers** for summarization, and **PyDub** with **FFmpeg** for audio processing. This tool enables users to easily access key information with keyword searches and timestamped results.

## Features

- **Summarize Video Transcripts**: Generate concise summaries of long video transcripts.
- **Keyword Search**: Search for keywords within video transcripts and display matching results with timestamps.
- **Audio Processing**: Utilize PyDub with FFmpeg to handle audio processing tasks.
- **Streamlit Interface**: User-friendly web interface built with Streamlit.

## Installation

To install TranScan, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/justmirr/transcan-video-transcript-search.git
    cd transcan-video-transcript-search
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Ensure FFmpeg is available**:
   - Download and install FFmpeg from [FFmpeg official site](https://ffmpeg.org/download.html).
   - Make sure FFmpeg is accessible in your PATH, or specify its path in the code.

## How to Run

1. **Start the Streamlit app**:
    ```sh
    streamlit run main.py
    ```

2. **Using the Application**:
   - Open your browser and go to `http://localhost:8501`.
   - Select either **"YouTube Video"** or **"Upload a Video"**.
   - If selecting **"YouTube Video"**, enter the video URL.
   - Choose between **"Summarize"** or **"Search within the video"**.
   - If selecting **"Upload a Video"**, upload your video file.
   - View the summarized transcript or search results with timestamps.
  
## Demonstration
   - Check out the live demonstration [here](https://transcan-video-transcript-search.streamlit.app/).
