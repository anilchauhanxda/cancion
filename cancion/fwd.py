from telethon import events

@songsxd.on(events.NewMessage(from_users=Config.DEEZER_BOT))
async def handler(event):
    # check media type
    if event.audio:
    	await songsxd.forward_messages(Config.SONGS_CHANN, event.message)
