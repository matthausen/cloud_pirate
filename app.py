from telegram.ext import Updater, CommandHandler, ConversationHandler
from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS
import re

def download(url):
  print(f'Downloading: {url}')

def start():
  print('start')

def cancel():
  print('cancel!')

def main():
  updater = Updater('YOUR_TOKEN')
  url="YourUrlHere"
  dp = updater.dispatcher
  
  conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    fallbacks=[CommandHandler('cancel', cancel)]
  )
  #dp.add_handler(CommandHandler('bop',download(url)))
  dp.add_handler(conv_handler)
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()