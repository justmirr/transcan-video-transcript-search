from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

def summarize(full_transcript):
  summarizer = pipeline('summarization')

  num_iters = len(full_transcript) // 1000
  summarized_text = []
  for i in range(num_iters + 1):
      start = i * 1000
      end = min((i + 1) * 1000, len(full_transcript))
      chunk = full_transcript[start:end]
      summary = summarizer(chunk, max_length=200, min_length=90, do_sample=False)
      summarized_text.append(summary[0]['summary_text'])
      return summarized_text

def summarize_link(yt_link):
  video_id = yt_link.split("=")[-1]
  transcript = YouTubeTranscriptApi.get_transcript(video_id)
  full_transcript = " ".join([item['text'] for item in transcript])
  return summarize(full_transcript)
  
def transcription(yt_link):
  video_id = yt_link.split("=")[-1]
  transcript = YouTubeTranscriptApi.get_transcript(video_id)
  return [(item['text'], item['start']) for item in transcript]

def summarize_uploaded(full_transcript):
  return summarize(full_transcript)