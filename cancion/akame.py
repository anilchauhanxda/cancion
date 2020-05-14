from telegram.ext import Updater, MessageHandler, Filters
import json
import logging
import mutagen
from telegram.ext import CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(Config.TOKEN)
dispatcher = updater.dispatcher

class Audio:
    def __init__(self, bot, update):
        self.bot = bot
        self.update = update
        self.chat_id = update.effective_message.chat_id
        self.message_id = update.effective_message.message_id
        self.audio = self.download_audio()

    def download_audio(self):
        audio = self.update.effective_message.effective_attachment
        file_id = audio.file_id
        new_file = self.bot.get_file(file_id)

        logging.log(logging.INFO, "Downloading file")
        self.bot.edit_message_caption(chat_id=self.chat_id, message_id=self.message_id, caption="downloading...")

        new_file.download('file.mp3')
        logging.log(logging.INFO, "File downloaded")

        return mutagen.File('file.mp3')

    def set_new_caption(self):
        title = ""
        artist = ""
        album = ""
        genre = ""
        try:
            title = self.audio.tags["TIT2"]
        except:
            pass
        try:
            artist = self.audio.tags["TPE1"]
        except:
            pass
        try:
            album = self.audio.tags["TALB"]
        except:
            pass
        try:
            genre = self.audio.tags["TCON"]
        except:
            pass

        new_caption = '''✏️ Title: {0}
👤 Artist: {1}
💽 Album:  {2}
🎼 Genre: {3}'''.format(title, artist, album, genre)

        self.bot.edit_message_caption(chat_id=self.chat_id, message_id=self.message_id, caption=new_caption)
        logging.log(logging.INFO, "Caption changed")


def change_caption(bot, update):
    logging.log(logging.INFO, "Changing caption")
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id

    audio = Audio(bot, update)
    audio.set_new_caption()

def start(bot, update):
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id
    start_message = """Heya!! there, I'm Akame
I'm here to help to manage your music channel.
With just adding this bot to your channel, it automatically adds audio details in it's caption with bellow format.
Join support chat @allukatm"""
    bot.send_message(chat_id=chat_id, text=start_message, reply_to_message_id=message_id)


handler = MessageHandler(Filters.audio, change_caption, channel_post_updates=True, message_updates=False)
dispatcher.add_handler(handler=handler)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


POLLING_INTERVAL = 0.2
updater.start_polling(poll_interval=POLLING_INTERVAL)
updater.idle()
