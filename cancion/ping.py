from telethon import events
from datetime import datetime
from meanii.util import admin_cmd


@songsxd.on(admin_cmd(pattern="ping"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit("Pong!\n{}".format(ms))
