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
        volume = res['devices'][0]['volume_percent']
        sp.volume(volume + 10, res["devices"][0]["id"])
        res = sp.devices()
        print("Increased volume to", (volume + 10))
    
    elif command == "volume down":
        res = sp.devices()
        volume = res['devices'][0]['volume_percent']
        sp.volume(volume - 10, res["devices"][0]["id"])
        res = sp.devices()
        print("Decreased volume to", (volume - 10))
    
    elif command == "search":
        a = input("Song name: ")
        
        specific = a.find(" as by ")

        if specific > -1:
            song_info = a.split(" as by ")
            a = song_info[0] + " artist:" + song_info[1]

        dev = sp.devices()
        device = dev["devices"][0]["id"]
        res = sp.search(a, limit = "1")
        song_res = res["tracks"]["items"][0]

        # if song_res["is_playable"] != True:
        #     print("Song is not playable!")
        # else:
        result = {"artist": "", "song": "", "uri": ""}
        artist = ""
        if len(song_res["artists"]) > 1:
            artist_list = ([x["name"] for x in song_res["artists"]])
            artist = " and "
            artist = artist.join(artist_list)
        else:
            artist = song_res["artists"][0]["name"]
        result["uri"] = song_res["uri"]
        result["song"] = song_res["name"]
        result["artist"] = artist
        print("Playing %s by %s!"%(result["song"], result["artist"]))
        sp.start_playback(uris = [result["uri"]])

    elif command == "s":
        break
