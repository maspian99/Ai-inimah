from flask import Flask, request, jsonify
import yt_dlp
import whisper
import os
import openai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

app = Flask(__name__)

# Download Video
def download_video(url):
    output_path = "video.mp4"
    ydl_opts = {'format': 'bestvideo+bestaudio/best', 'outtmpl': output_path}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

# Transkripsi Video
def transcribe_video(video_path):
    model = whisper.load_model("small")
    result = model.transcribe(video_path)
    return result["text"]

# Pilih Bagian Terbaik (Pakai GPT-4)
openai.api_key = "YOUR_OPENAI_API_KEY"
def select_best_part(transcript):
    prompt = f"Pilih bagian terbaik dari video ini untuk Shorts: {transcript}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Potong Video ke Shorts
def cut_video(input_file, start_time, duration, output_file):
    command = f"ffmpeg -i {input_file} -ss {start_time} -t {duration} -vf 'scale=1080:1920' -preset ultrafast -y {output_file}"
    os.system(command)
    return output_file

# Endpoint API
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    youtube_url = data["url"]

    # Download Video
    video_path = download_video(youtube_url)

    # Transkripsi & Pilih Bagian Terbaik
    transcript = transcribe_video(video_path)
    best_part = select_best_part(transcript)

    # Misalkan AI memilih mulai dari 1:30 selama 58 detik
    short_video = cut_video(video_path, "00:01:30", "00:00:58", "short.mp4")

    # Simpan di Cloud Storage (contoh: Google Drive)
    short_url = "https://drive.google.com/file/d/short.mp4"

    return jsonify({"video_url": short_url})

if __name__ == '__main__':
    app.run(debug=True)
