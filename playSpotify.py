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
        try:
            playback = sp.current_playback()
            print("Now playing", playback['item']['name'], "-", playback['item']['artists'][0]['name'])
        except:
            print("Nothing is playing!")
    elif command == "stop":
        try:
            res = sp.devices()

            print("Stopping playback on device:",res["devices"][0]["name"])

            sp.pause_playback(res["devices"][0]["id"])
        except:
            print("Nothing is playing!")
    elif command == "next":
        res = sp.devices()

        print("Skipping to next song on device:",res["devices"][0]["name"])

        sp.next_track(res["devices"][0]["id"])
    elif command == "previous":
        res = sp.devices()

        print("Reverting to previous song on device:",res["devices"][0]["name"])

        sp.previous_track(res["devices"][0]["id"])
    elif command == "volume up":
        res = sp.devices()
        print(res['devices'][0]['volume_percent'])
        sp.volume(res['devices'][0]['volume_percent'] + 10, res["devices"][0]["id"])
        res = sp.devices()
        print(res['devices'][0]['volume_percent'])
    elif command == "volume down":
        res = sp.devices()
        print(res['devices'][0]['volume_percent'])
        sp.volume(res['devices'][0]['volume_percent'] - 10, res["devices"][0]["id"])
        res = sp.devices()
        print(res['devices'][0]['volume_percent'])
    elif command == "search":
        a = input("Song name: ")
        res = sp.search(a, 1, 0,"track")
        print(res['tracks']["items"][0]["external_urls"]["spotify"])

    elif command == "s":
        break
