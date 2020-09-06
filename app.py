from __future__ import unicode_literals
import os
from telegram.ext import Updater, CommandHandler, ConversationHandler
from telegram.parsemode import ParseMode
from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS
import glob
from youtube_search import YoutubeSearch
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
def download_audio(query):
  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
  }
  try:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download(['https://www.youtube.com/watch?v=' + query])
  except Exception:
    return False
  

def search(bot, update):
  message = update.message.text
  input = message.split(' ')
  input.pop(0)
  user_input = " ".join(str(x) for x in input)
  print(f'Searching: {user_input}')
  results = YoutubeSearch(user_input, max_results=10).to_dict()
  # send results to the user (only id, thumbnails[0], title and duration).
  for song in results:
    for key, value in song.items():
      print(key, value)


def download(bot, update):
  message = update.message.text
  input = message.split(' ')
  input.pop(0)
  user_input = " ".join(str(x) for x in input)
  print(f'Downloading: {user_input}')
  download_audio(input)
  # send the audio file here
  for audio in glob.glob('./*mp3'):
    bot.send_audio(chat_id=update.message.chat_id, audio=open(audio, 'rb'))

def help(bot, update):
  text="Hello User, You have used <b>start</b> command. Search about developer on google, <a href='https://www.google.com/search?q=tbhaxor'>@tbhaxor</a>"
  bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

def start(bot, update):
  text="Hello User, You have used <b>start</b> command. Search about developer on google, <a href='https://www.google.com/search?q=tbhaxor'>@tbhaxor</a>"
  bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

def cancel(bot, update):
  text='Operation was cancelled!'
  bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

def main():
  updater = Updater(TELEGRAM_TOKEN)
  dp = updater.dispatcher
  
  conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={},
    fallbacks=[CommandHandler('cancel', cancel)]
  )

  dp.add_handler(conv_handler)
  dp.add_handler(CommandHandler('help',help))
  dp.add_handler(CommandHandler('start',help))
  dp.add_handler(CommandHandler('search',search))
  dp.add_handler(CommandHandler('download',download))
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main