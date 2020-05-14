
import logging
import os
import sys
from pathlib import Path
from meanii import meanii
from meanii.storage import Storage
from telethon.sessions import StringSession


logging.basicConfig(level=logging.INFO)

# the secret configuration specific things
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from sample_config import Config
else:
    if os.path.exists("config.py"):
        from config import Development as Config
    else:
        logging.warning("No config.py Found!")
        logging.info("Please run the command, again, after creating config.py similar to README.md")
        sys.exit(1)




if len(Config.SUDO_USERS) >= 0:
    Config.SUDO_USERS.add("me")


if Config.HU_STRING_SESSION is not None:
    # for Running on Heroku
    session_name = str(Config.HU_STRING_SESSION)
    songsxd = meanii(
        StringSession(session_name),
        n_plugin_path="cancion/",
        api_config=Config,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
    )
    songsxd.run_until_disconnected()
elif len(sys.argv) == 2:
    # for running on GNU/Linux
    session_name = str(sys.argv[1])
    songsxd = meanii(
        session_name,
        n_plugin_path="cancion/",
        connection_retries=None,
        api_config=Config,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
    )
    songsxd.run_until_disconnected()
else:
    # throw error
    logging.error("USAGE EXAMPLE:\n"
                  "python3 -m cancion <SESSION_NAME>"
                  "\nPlease follow the above format to run your userbot."
                  "\n Bot quitting.")
