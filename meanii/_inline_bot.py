
from math import ceil
import asyncio
import json
import re
from telethon import events, custom
from meanii.util import admin_cmd


@songsxd.on(admin_cmd(  
    pattern="ib (.[^ ]*) (.*)"
))
async def _(event):
    
    if event.fwd_from:
        return
    bot_username = event.pattern_match.group(1)
    search_query = event.pattern_match.group(2)
    try:
        output_message = ""
        bot_results = await event.client.inline_query(
            bot_username,
            search_query
        )
        i = 0
        for result in bot_results:
            output_message += "{} {} `{}`\n\n".format(
                result.title,
                result.description,
                ".icb " + bot_username + " " + str(i + 1) + " " + search_query
            )
            i = i + 1
        await event.edit(output_message)
    except Exception as e:
        await event.edit("{} did not respond correctly, for **{}**!\n\
            `{}`".format(bot_username, search_query, str(e)))



