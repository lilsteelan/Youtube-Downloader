from flask import Flask, send_file, render_template, jsonify, request, flash, redirect, url_for, session
#from flask_caching import Cache
from flask_session import Session
from os import path
import os
import os.path
import json
from pytube import YouTube
import downloader
import requests
from bs4 import BeautifulSoup
import glob

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}


app = Flask(__name__)
app.config["SECRET_KEY"] = "47C61A0FA8738BA77308A8A600F88E4B"
app.config['UPLOAD_FOLDER']='videos'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#app.config.from_mapping(config)
#cache = Cache(app)
#cache = Cache(app)
global src
src = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])

def download_video(video_url, resolution='1080p'):
    yt = YouTube(video_url)
    #stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    stream = yt.streams.get_highest_resolution()
    stream.download(src)
    print(src)
    print(f"Video successfully downloaded in {resolution} resolution.")

def getVideo():
    #path = "/videos" #path directory
    path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    #latest_file = max(path, key=os.path.getctime)
    print(path)
    return path + f"\\video.mp4"

def clearVideos():
    files = glob.glob(app.config['UPLOAD_FOLDER'])
    try:
        for f in files:
            os.remove(f)
            print("cleared", f)
    except:
        print("Failed to delete videos")
        print("Manual deletion will be needed")

global name,url

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        url = request.form['link']
        print(url)
        download_video(url)
        session["hasDownloaded"] = False
        return render_template("download.html", hasDownloaded = session["hasDownloaded"])
    else:
        print(request.args)
        clearVideos()
        return render_template("index.html")

@app.route("/download", methods=["GET", "POST"])
def download():
    fname = getVideo()
    print("filename: ", fname)
    dir = src
    files = glob.glob(os.path.join(dir, '*.mp4'))
    print(files)
    latest_file = max(files, key=os.path.getctime)
    session["hasDownloaded"] = True
    print(session["hasDownloaded"])
    #files[0]
    return send_file(latest_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=8000)