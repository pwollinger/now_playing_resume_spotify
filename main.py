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
    curret_track = sp.current_user_playing_track()
    try:
        if(track_name != curret_track['item']['name']):
            track_name = curret_track['item']['name']
            album_name = curret_track['item']['album']['name']
            artist_name = curret_track['item']['artists'][0]['name']
            track_name_regex = re.findall("^(.*?) -", track_name)
            with open("playing.txt", "w", encoding='utf8') as song:
                
                if len(track_name_regex) > 0:
                    song.write(f"{track_name_regex[0]} - {artist_name}") #\n{album_name}")
                    print(f"Listening: {artist_name} - {track_name_regex[0]}")
                else:
                    song.write(f"{track_name} - {artist_name}") #\n{album_name}")
                    print(f"Listening: {artist_name} - {track_name}")

            response = requests.get(curret_track['item']['album']['images'][0]['url'])

            with open("album.png", "wb") as album:
                album.write(response.content)

            img = PIL.Image.open('album.png')
            blur = img.filter(ImageFilter.GaussianBlur(radius = 5))
            blur.save('album_blur.png')

    except TypeError:
        with open("playing.txt", "w", encoding='utf8') as song:
            song.write(f"")
 
    time.sleep(2)
