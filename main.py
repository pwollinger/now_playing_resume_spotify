import os
import re
import time
import spotipy
import requests
import configparser
from spotipy.oauth2 import SpotifyOAuth
from album_cover_generator import generate_final_cover

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
            time.sleep(1)
            generate_final_cover(response.content, "album.jpeg")

    except TypeError:
        with open("playing.txt", "w", encoding='utf8') as song:
            song.write(f"")

    song_duration = (current_track['item']['duration_ms'] - current_track['progress_ms'])/1000
    time.sleep(song_duration)