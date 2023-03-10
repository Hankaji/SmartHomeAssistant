from .bot_command import MikuCommand
import bot_commands.cred as cred
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyObject(MikuCommand):
    
    
    def __init__(self, commandID: str):
        super().__init__(commandID)
        scope = 'user-read-playback-state,user-modify-playback-state,user-read-currently-playing'

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret=cred.client_SECRET,
                                               redirect_uri=cred.redirect_url, scope=scope))
        
    def active_device(self):
        res = self.sp.devices()
        if len(res["devices"]) > 0:
            devices = res["devices"]
            for i in devices:
                if i["is_active"] == True:
                    return [i["name"], i["id"]] #[0] is name of device, [1] is id of device
        else: 
            return -1

    def execute(self, text_list: list) -> str:
        device = self.active_device()
        if device == -1:
            return "but there is no active device right now, please connect spotify to a device"
        else:
            try:
                dev_name = device[0]
                dev_id = device[1]
            except TypeError:
                return " but there is no active device right now, please connect spotify to a device"
            if text_list[0] == "spotify":
                command = text_list[1]
                if command == "resume":
                    try:
                        self.sp.start_playback()
                        return "Resuming playback"
                    except spotipy.exceptions.SpotifyException:
                        return "but something is already playing right now."
                elif command == "stop":
                    try:
                        self.sp.pause_playback()
                        return "Stopping playback"
                    except spotipy.exceptions.SpotifyException:
                        return "but nothing is playing right now."
                elif command == "next":
                    try:
                        self.sp.next_track()
                        return "Skipping to next track"
                    except spotipy.exceptions.SpotifyException:
                        return "but I cannot do this right now."
                elif command == "previous":
                    try:
                        self.sp.previous_track()
                        return "Skipping to next track"
                    except spotipy.exceptions.SpotifyException:
                        return "but I cannot do this right now."
                elif command == "play":
                    try:
                        command = " ".join(text_list[2:])
                        specific = command.find(" as by ")

                        if specific > -1:
                            song_info = command.split(" as by ")
                            command = song_info[0] + " artist:" + song_info[1]

                        res = self.sp.search(command, limit = "1")
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
                        self.sp.start_playback(uris = [result["uri"]])
                    except: 
                        return " but I cannot do this right now"
                    return str("Playing %s by %s!"%(result["song"], result["artist"]))
