from telethon import events
import os
import requests
import json
from meanii.util import admin_cmd

@songsxd.on(events.NewMessage(pattern="https://?(.*)",))

async def _(event):
    if event.fwd_from:
        return
    input_str = "https://song.link/redirect?url=" + event.pattern_match.group(1) + "&to=deezer&web=true"
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith('3'):
        send = await songsxd.send_message(Config.DEEZER_BOT, "{}".format(r.headers["Location"]))
       # error="undefined"
        #if send = error
        #await event.reply("Not able to Found 😕/n{} ".format(input_str))
        
