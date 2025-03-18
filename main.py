from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pytube import YouTube
import yt_dlp
import whisper
import openai
import os
import json

# Setup FastAPI
app = FastAPI()

# Mount static & templates folder
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# API Key OpenAI
OPENAI_API_KEY = "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"
openai.api_key = "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"

# Buat folder video & clips kalau belum ada
os.makedirs("/tmp/videos/", exist_ok=True)
os.makedirs("/tmp/clips/", exist_ok=True)

video_path = "/tmp/videos/output.mp4"
with open(video_path, "wb") as f:
    f.write(video_content)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_video(request: Request):
    data = await request.json()
    youtube_url = data["youtube_url"]
    duration = int(data["duration"])

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

    return JSONResponse({"thumbnail": info["thumbnail"], "scenes": best_scenes})

@app.post("/convert")
async def convert_to_clips():
    return JSONResponse({"message": "Proses pemotongan video dalam format 9:16..."})
