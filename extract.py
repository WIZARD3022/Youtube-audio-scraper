import yt_dlp
from pydub import AudioSegment
import os

# Set your YouTube video URL here
# VIDEO_URL = "https://youtu.be/irqbmMNs2Bo"  # Replace with your link
VIDEO_URL = "https://youtu.be/fZJAXopLX2o"  # Replace with your link

# Output filenames
AUDIO_MP4 = "downloaded_audio.m4a"
AUDIO_WAV = "final_audio.wav"
CAPTION_FILE = "captions.en.vtt"  # English by default

# Download audio and captions using yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': AUDIO_MP4,
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],  # or ['hi'] for Hindi, etc.
    'subtitlesformat': 'vtt',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        'preferredquality': '192',
    }],
}

print("📥 Downloading audio and captions from YouTube...")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(VIDEO_URL, download=True)

# Rename subtitles if needed
video_title = info.get("title", "video")
subtitles = info.get("requested_subtitles", {})
if subtitles and "en" in subtitles:
    subtitle_path = f"{video_title}.en.vtt"
    if os.path.exists(subtitle_path):
        os.rename(subtitle_path, CAPTION_FILE)

# Convert audio to WAV
print("🎧 Converting audio to WAV format...")
audio = AudioSegment.from_file(AUDIO_MP4)
audio.export(AUDIO_WAV, format="wav")

print(f"✅ Audio saved as: {AUDIO_WAV}")
print(f"📝 Captions saved as: {CAPTION_FILE if os.path.exists(CAPTION_FILE) else 'Not found'}")




def vtt_to_text(vtt_file, txt_file):
    with open(vtt_file, 'r', encoding='utf-8') as infile, open(txt_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if not line.strip().isdigit() and "-->" not in line and line.strip():
                outfile.write(line)

vtt_to_text("downloaded_audio.m4a.en.vtt", "captions.txt")
