from flask import Flask, request, render_template, jsonify
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)  # Tambahin ini biar Flask bisa diakses dari luar
import yt_dlp
import whisper
import os
import openai

app = Flask(__name__)

openai.api_key = "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"

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

# Pilih Beberapa Klip Terbaik
def select_best_parts(transcript):
    prompt = f"""
    Dari transkripsi berikut, pilih 3 bagian terbaik untuk dijadikan video Shorts.
    Berikan hasil dalam format JSON seperti ini:
    [
        {{"start": "00:01:30", "duration": "00:00:58"}},
        {{"start": "00:04:12", "duration": "00:01:02"}},
        {{"start": "00:07:05", "duration": "00:00:55"}}
    ]
    
    Transkripsi: {transcript}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    
    clips = eval(response["choices"][0]["message"]["content"])  # Convert JSON string to Python dict
    return clips

# Potong Video
def cut_videos(input_file, clips):
    output_files = []
    for i, clip in enumerate(clips):
        output_file = f"short_{i+1}.mp4"
        command = f"ffmpeg -i {input_file} -ss {clip['start']} -t {clip['duration']} -vf 'scale=1080:1920' -preset ultrafast -y {output_file}"
        os.system(command)
        output_files.append(output_file)
    return output_files

# Route Home
@app.route('/')
def home():
    return render_template('index.html')

# Route Generate Shorts
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    youtube_url = data["url"]

    # Download Video
    video_path = download_video(youtube_url)

    # Transkripsi & Pilih Klip Terbaik
    transcript = transcribe_video(video_path)
    best_parts = select_best_parts(transcript)

    # Potong Video
    short_videos = cut_videos(video_path, best_parts)

    # Simpan URL hasil
    short_urls = [f"/static/{vid}" for vid in short_videos]

    return jsonify({"video_urls": short_urls})

if __name__ == '__main__':
    app.run(debug=True)
