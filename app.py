from __future__ import unicode_literals
import os
from telegram.ext import Updater, CommandHandler, ConversationHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.callbackquery import CallbackQuery
from telegram.parsemode import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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

results_cleaned = []

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
  
# Search on YouTube and return a list of 10 results
def search(bot, update):
  message = update.message.text
  input = message.split(' ')
  input.pop(0)
  user_input = " ".join(str(x) for x in input)
  print(f'Searching: {user_input}')
  
  results = YoutubeSearch(user_input, max_results=10).to_dict()

  # Clean results and return id, title and duration
  for song in results:
    song_cleaned={'id': song['id'], 'title': song['title'], 'duration': song['duration']}
    results_cleaned.append(song_cleaned)
  
  text=''
  for index, item in enumerate(results_cleaned):
    if index <= 7:
      text += "- {}. {}, {} \n".format(index+1, item['title'], item['duration'])
  
  
  bot.send_message(chat_id=update.message.chat_id, text=text)

  # Allow the user to select from the 8 options
  options = []
  for i in range(1, 9):
    options.append(InlineKeyboardButton(i, callback_data=i))
    
  reply_markup = InlineKeyboardMarkup([options])
  bot.send_message(chat_id=update.message.chat_id, text='Choose an option to download as mp3', reply_markup=reply_markup)

# Handle query after user selected one option
def query_handler(bot, update):
    query: CallbackQuery = update.callback_query
    query.answer()
    query.edit_message_text(text="Downloading: {} ... Please wait".format(query.data))

    song_id = results_cleaned[int(query.data)-1]['id']
    
    # send the audio file and delete the previously saved files
    download_audio(song_id)
    for audio in glob.glob('./*mp3'):
      bot.send_audio(chat_id=query.message.chat_id, audio=open(audio, 'rb'))
      os.remove(audio)


def donate(bot, update):
  donation= "<form action='https://www.paypal.com/cgi-bin/webscr' method='post' target='_top'><input type='hidden' name='cmd' value='_s-xclick' /><input type='hidden' name='hosted_button_id' value='GFM5BFJ346QUJ' /><input type='image' src='https://www.paypalobjects.com/en_US/GB/i/btn/btn_donateCC_LG.gif' border='0' name='submit' title='PayPal - The safer, easier way to pay online!' alt='Donate with PayPal button' /><img alt='donation' border='0' src='https://www.paypal.com/en_GB/i/scr/pixel.gif' width='1' height='1' /></form>"
  bot.send_message(
        chat_id=update.effective_chat.id,
        text=donation,
        parse_mode=ParseMode.HTML,
    )

def help(bot, update):
  text="To start, simply type <b>/search</b> or <b>/download</b> followed by the name of the song or artist you want to download and choose from one of the options."
  bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

def start(bot, update):
  text="To start, simply type <b>/search</b> or <b>/download</b> followed by the name of the song or artist you want to download and choose from one of the options."
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
  dp.add_handler(CommandHandler('download',search))
  # dp.add_handler(CommandHandler('donate',donate))

  updater.dispatcher.add_handler(CallbackQueryHandler(query_handler))

  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()