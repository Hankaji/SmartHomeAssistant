import spotipy
from spotipy.oauth2 import SpotifyOAuth
import bot_commands.cred as cred


def user_input():
    a = input("Enter a command(Play song, stop): ")
    return a


def active_device():
    res = sp.devices()
    if len(res["devices"]) > 0:
        devices = res["devices"]
        for i in devices:
            if i["is_active"] == True:
                return [i["name"], i["id"]] #[0] is name of device, [1] is id of device
    else: 
        return -1

    


scope = 'user-read-playback-state,user-modify-playback-state,user-read-currently-playing'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret=cred.client_SECRET,
                                               redirect_uri=cred.redirect_url, scope=scope))

while True:
    command = user_input()

    if command == "s":
        break
    device = active_device()
    if device == -1:
        print("No currently active device")
        continue
    else:
        dev_name = device[0]
        dev_id = device[1]
        if command == "resume":
            try:
                print("Resuming playback on device:", dev_name)

                sp.start_playback(dev_id)
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
                print("Stopping playback on device:", dev_name)

                sp.pause_playback(dev_id)
            except:
                print("Nothing is playing!")
        
        elif command == "next":
            print("Skipping to next song on device:", dev_name)

            sp.next_track(dev_id)
        
        elif command == "previous":
            print("Reverting to previous song on device:", dev_name)

            sp.previous_track(dev_id)
        
        elif command == "volume up":
            volume = res['devices'][0]['volume_percent']
            sp.volume(volume + 10, dev_id)
            print("Increased volume to", (volume + 10))
        
        elif command == "volume down":
            volume = res['devices'][0]['volume_percent']
            sp.volume(volume - 10, dev_id)
            print("Decreased volume to", (volume - 10))
        
        elif command == "play":
            a = input("Song name: ")
            if a == "cancel":
                continue
            specific = a.find(" as by ")

            if specific > -1:
                song_info = a.split(" as by ")
                a = song_info[0] + " artist:" + song_info[1]

            res = sp.search(a, limit = "1")
            song_res = res["tracks"]["items"][0]

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

        elif command == "devices":
            res = sp.devices()
            print(res["devices"])

        # elif command == "queue":
        #     res = sp.queue()
        #     print(res)
        
        elif command == "add to q":
            a = input("Song name: ")
            if a == "cancel":
                continue
            specific = a.find(" as by ")

            if specific > -1:
                song_info = a.split(" as by ")
                a = song_info[0] + " artist:" + song_info[1]

            res = sp.search(a, limit = "1")
            song_res = res["tracks"]["items"][0]

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
            print("Adding %s by %s to queue!"%(result["song"], result["artist"]))
            sp.add_to_queue(uri = result["uri"], device_id= dev_id)
