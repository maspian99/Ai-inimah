import os
import requests
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set API Key OpenAI
openai.api_key = "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"

# Direktori penyimpanan sementara (Vercel hanya bisa pakai `/tmp/`)
VIDEO_DIR = "/tmp/videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return "AI YouTube Shorts API is running!"

@app.route("/process-video", methods=["POST"])
def process_video():
    try:
        # Ambil URL video dari request
        data = request.get_json()
        video_url = data.get("url")
        if not video_url:
            return jsonify({"error": "URL video tidak diberikan"}), 400

        # Download video
        response = requests.get(video_url)
        if response.status_code != 200:
            return jsonify({"error": "Gagal mengunduh video"}), 500

        # Simpan video ke file sementara
        video_path = os.path.join(VIDEO_DIR, "input.mp4")
        with open(video_path, "wb") as f:
            f.write(response.content)

        # **(Tambahkan proses AI di sini jika ada)**
        # Misalnya: AI memilih scene terbaik lalu menghasilkan video Shorts

        # Hasil akhir (dummy response)
        output_url = "https://your-host.com/processed_video.mp4"

        return jsonify({"message": "Video berhasil diproses", "output_url": output_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
