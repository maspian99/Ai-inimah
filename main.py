from fastapi import FastAPI
import yt_dlp  # Buat download video YouTube
import moviepy.editor as mp  # Buat edit video

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI YouTube Shorts Converter Ready"}

@app.get("/convert")
def convert_video(url: str):
    # Download video YouTube
    ydl_opts = {'format': 'best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_url = info['url']

    # Proses video (misal, potong jadi Shorts)
    video = mp.VideoFileClip(video_url)
    short_clip = video.subclip(0, 60)  # Potong jadi 60 detik
    short_clip.write_videofile("output.mp4")

    return {"message": "Shorts created!", "video": "output.mp4"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
