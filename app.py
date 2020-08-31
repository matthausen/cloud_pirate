import os
from telegram.ext import Updater, CommandHandler, ConversationHandler
from telegram.parsemode import ParseMode
from __future__ import unicode_literals
from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS
import re
import youtube_dl
from dotenv import load_dotenv
load_dotenv()

load_dotenv(verbose=True)
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

TELEGRAM_TOKEN = os.getenv("TOKEN")
# Download the mp3 audio from a youtube video
''' ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc']) '''

def help(bot, update):
  text="Hello User, You have used <b>start</b> command. Search about developer on google, <a href='https://www.google.com/search?q=tbhaxor'>@tbhaxor</a>"
  bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

def download(bot, update):
  url='http://localhost:3000'
  user_input = update.message.text
  print(f'Downloading: {url}. User input was: {user_input}')

def start():
  print('start')

def cancel():
  print('cancel!')

def main():
  updater = Updater(TELEGRAM_TOKEN)
  dp = updater.dispatcher
  
  conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    fallbacks=[CommandHandler('cancel', cancel)]
  )
  
  dp.add_handler(conv_handler)
  dp.add_handler(CommandHandler('help',help))
  dp.add_handler(CommandHandler('start',help))
  dp.add_handler(CommandHandler('download',download))
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()