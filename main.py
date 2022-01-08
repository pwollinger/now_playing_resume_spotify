import os
import re
import PIL
import time
import spotipy
import requests
import configparser
from PIL import ImageFilter, Image
from spotipy.oauth2 import SpotifyOAuth

config = configparser.ConfigParser()
config.read('config.ini')

os.environ["SPOTIPY_CLIENT_ID"] = config['Credentials']['ClientID']
os.environ["SPOTIPY_CLIENT_SECRET"] = config['Credentials']['Secret']
os.environ["SPOTIPY_REDIRECT_URI"] = config['Credentials']['RedirectURI']

scope = "user-read-currently-playing"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

track_name = 'none'

while True:
    current_track = sp.current_user_playing_track()
    try:
        if(track_name != current_track['item']['name']):
            track_name = current_track['item']['name']
            #album_name = current_track['item']['album']['name']
            artist_name = current_track['item']['artists'][0]['name']
            track_name_regex = re.findall("^(.*?) -", track_name)
            with open("playing.txt", "w", encoding='utf8') as song:

                if len(track_name_regex) > 0:
                    song.write(f"{track_name_regex[0]} - {artist_name}")
                    print(f"Listening: {artist_name} - {track_name_regex[0]}")
                else:
                    song.write(f"{track_name} - {artist_name}")
                    print(f"Listening: {artist_name} - {track_name}")

            response = requests.get(current_track['item']['album']['images'][0]['url'])
            album_blur = finalImage("album.png")
            with open("album_blur.png", "wb") as album:
                album.write(response.content)

    except TypeError:
        with open("playing.txt", "w", encoding='utf8') as song:
            song.write(f"")

    song_duration = (current_track['item']['duration_ms'] - current_track['progress_ms'])/1000
    time.sleep(song_duration)

def finalImage(coverFilename):
    with Image.open(coverFilename) as cover:
        newSize = (int(round(cover.size[0]/cover.size[1]*1080)), 1080)
        coverResized = cover.resize(newSize)
        blurredCover = coverResized.filter(ImageFilter.GaussianBlur(6))

        remainder = 1920 - newSize[0]
        cutpoints = (remainder//2,
                    (1920 - remainder//2, blurredCover.size[0] - remainder%2 - remainder//2))
        strp1 = blurredCover.crop((0, 0, cutpoints[0], 1080))
        strp2 = blurredCover.crop((cutpoints[1][1], 0, blurredCover.size[0], 1080))

        finalCover = Image.new(cover.mode, (1920, 1080))
        finalCover.paste(strp1, (0,0))
        finalCover.paste(coverResized, (cutpoints[0],0))
        finalCover.paste(strp2, (cutpoints[1][0],0))
        finalCover.save('album_blur.png')