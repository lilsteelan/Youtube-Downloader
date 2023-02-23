from pytube import YouTube
import os
from pathlib import Path
import bs4

src = "/"
dest = "/main"
f = "video.mp4"
def download_video(video_url, resolution='1080p'):
    yt = YouTube(video_url)
    stream = yt.streams.filter(resolution=resolution, file_extension='mp4').first()
    stream.download("", filename=f)
    print(f"Video successfully downloaded in {resolution} resolution.")
    
    return f
