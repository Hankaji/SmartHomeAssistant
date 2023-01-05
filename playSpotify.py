import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred


def user_input():
    a = input("Enter a command(Play song, stop): ")
    return a


scope = 'user-read-playback-state,user-modify-playback-state,user-read-currently-playing'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret=cred.client_SECRET,
                                               redirect_uri=cred.redirect_url, scope=scope))

while True:
    command = user_input()

    if command == "play":
        try:
            res = sp.devices()

            print("Resuming playback on device:", res["devices"][0]["name"])

            sp.start_playback(res["devices"][0]["id"])
        except:
            print("Already playing!")
    elif command == "playing":
        playback = sp.current_playback()
        print("Now playing ", "by ", playback['item']['artists'][0]['name'])
    elif command == "stop":
        try:
            res = sp.devices()

            print("Stopping playback on device:",res["devices"][0]["name"])

            sp.pause_playback(res["devices"][0]["id"])
        except:
            print("Nothing is playing!")
