from django.shortcuts import render
from pathlib import Path
import urllib3
import moviepy.editor as mpe
import json
import requests

# Create your views here.
from reddit_doenloader.download_logic.download import download

BASE_DIR = Path(__file__).resolve().parent.parent


def home(request):

    print(BASE_DIR)
    return render(request, 'home.html')


def func(request):
    urlx = request.POST.get('link')

    if download(urlx):
        uploaded_file_url = "main.mp4"
        return render(request, 'home.html', {'uploaded_file_url': uploaded_file_url})
    else:
        return render(request, 'home.html')


def combine_audio(vidname, audname, outname):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname)
