import os

from flask import Flask, request

import telebot

TOKEN = '7245262172:AAEnlFNAvSscBewXMeH10513YqtvmZZ39W8'

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)