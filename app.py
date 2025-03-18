from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pytube import YouTube
import yt_dlp
import whisper
import openai
import os
import json
from jinja2 import Template

app = FastAPI()

# API Key OpenAI
OPENAI_API_KEY = "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"
openai.api_key = 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

# Buat folder video & clips kalau belum ada
os.makedirs("videos", exist_ok=True)
os.makedirs("clips", exist_ok=True)

# Template HTML Frontend
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>PINZ AI - YouTube Shorts Generator</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; background-color: #111; color: #fff; }
        h1 { font-size: 48px; font-weight: bold; text-shadow: 2px 2px #00ffcc; }
        input, button, select { padding: 10px; margin: 10px; font-size: 18px; }
        .thumbnail { margin-top: 20px; }
    </style>
</head>
<body>
    <h1>PINZ AI</h1>
    <p>Masukkan URL YouTube:</p>
    <form action="/generate" method="post">
        <input type="text" name="youtube_url" required>
        <select name="duration">
            <option value="30"> < 30 detik </option>
            <option value="60">30 - 60 detik</option>
            <option value="180">60 - 180 detik</option>
        </select>
        <button type="submit">Generate</button>
    </form>
    {% if thumbnail %}
        <div class="thumbnail">
            <img src="{{ thumbnail }}" width="320">
            <p>Proses AI...</p>
        </div>
        <form action="/convert" method="post">
            <button type="submit">Convert to Clips</button>
        </form>
    {% endif %}
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return html_template

@app.post("/generate", response_class=HTMLResponse)
async def process_video(youtube_url: str = Form(...), duration: int = Form(...)):
    # Download video YouTube
    ydl_opts = {"format": "best", "outtmpl": "videos/%(title)s.%(ext)s"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)

    # Transkripsi audio dengan Whisper
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    transcript = result["text"]

    # Kirim ke OpenAI buat cari scene terbaik
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Pilih bagian video yang paling menarik dan lucu."},
                  {"role": "user", "content": transcript}],
    )
    best_scenes = json.loads(response["choices"][0]["message"]["content"])

    # Render HTML
    return Template(html_template).render(thumbnail=info["thumbnail"], scenes=best_scenes)

@app.post("/convert")
async def convert_to_clips():
    return {"message": "Proses pemotongan video dalam format 9:16..."}
