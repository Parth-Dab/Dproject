import urllib3
import moviepy.editor as mpe
import json
import requests

from Dproject.settings import STATICFILES_DIRS, STATIC_URL


def download(urlx):
    if urlx.find('?'):
        urlx = urlx[:urlx.find('?')].strip()

    urlx += '.json'
    http = urllib3.PoolManager()

    try:
        r_dict = http.request("GET", urlx)
        r_dict = json.loads(r_dict.data.decode("utf-8"))

        try:
            is_vid = r_dict[0]['data']['children'][0]['data']['is_video']
        except:
            is_vid = False

        try:
            is_gif = r_dict[0]['data']['children'][0]['data']['preview']['reddit_video_preview']['is_gif']
        except:
            is_gif = False

        # print(is_vid)
        # print(is_gif)

        if is_vid:
            dic = r_dict[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
            vid_url = ""
            for i in dic:
                vid_url += i

            vid_url = vid_url[:vid_url.find('?source')].strip()
            aud_url = vid_url[:vid_url.find('DASH_')].strip()
            aud_url += 'DASH_audio.mp4'

            response = requests.get(aud_url)
            if response.status_code == 200:
                print("audio!")
                combine_audio(vid_url, aud_url, "media/main.mp4")
                return True
            else:
                print("no audio!!")
                my_clip = mpe.VideoFileClip(vid_url)
                my_clip.write_videofile("media/main.mp4")
                return True

        elif is_gif:
            dic = r_dict[0]['data']['children'][0]['data']['preview']['reddit_video_preview']['fallback_url']
            vid_url = ""
            for i in dic:
                vid_url += i

            my_clip = mpe.VideoFileClip(vid_url)
            my_clip.write_videofile("media/main.gif")
            return True
        else:
            print("Link isn't video!!!!")
            return False
    except:
        print("Link is either invalid or not a reddit link!!!")
        return False


def combine_audio(vidname, audname, outname):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname)
