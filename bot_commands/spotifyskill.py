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
        
    def active_device():
        res = self.sp.devices()
        if len(res["devices"]) > 0:
            devices = res["devices"]
            for i in devices:
                if i["is_active"] == True:
                    return [i["name"], i["id"]] #[0] is name of device, [1] is id of device
        else: 
            return -1

    def execute(self, text_list: list):
        if text_list[0] == "spotify":
            command = text_list[1]
            match command:
                case "resume":
                    try:
                        self.sp.start_playback()
                        return "Resuming playback"
                    except spotipy.exceptions.SpotifyException:
                        return "but something is already playing right now."
                case "stop":
                    try:
                        print("Stop")
                        self.sp.pause_playback()
                        return "Stopping playback"
                    except spotipy.exceptions.SpotifyException:
                        return "but nothing is playing right now."
                case "next":
                    pass
                case "previous":
                    pass
                case "play":
                    pass
