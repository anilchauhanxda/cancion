
import os

START_STRING = """Heya!! there, I'm Akame
I'm here to help to manage your music channel.
With just adding this bot to your channel, it automatically adds audio details in it's caption with bellow format.
Join support chat @allukatm"""

class Config(object):
    LOGGER = True
 
    APP_ID = int(os.environ.get("APP_ID", 6))
    API_HASH = os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
    TOKEN = os.environ.get("TOKEN",None)
    START = os.environ.get("START",START_STRING)
    DEEZER_BOT = os.environ.get("DEEZER_BOT", "@DeezLoadBot")
    SONGS_CHANN = os.environ.get("SONGS_CHANN", "@songsxd")
    HU_STRING_SESSION = os.environ.get("HU_STRING_SESSION", None)
    SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
    
    
    
class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
