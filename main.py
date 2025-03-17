from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Konfigurasi untuk membaca template
templates = Jinja2Templates(directory="templates")

# Endpoint untuk menampilkan index.html
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Jika ada static files (CSS, JS, dll.), bisa diatur seperti ini:
app.mount("/static", StaticFiles(directory="static"), name="static")
