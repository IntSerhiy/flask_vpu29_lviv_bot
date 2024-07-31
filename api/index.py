from flask import Flask, request

import telebot

from flask_openai_bot.service.main import generetive_message

app = Flask(__name__)

TOKEN = '7245262172:AAEnlFNAvSscBewXMeH10513YqtvmZZ39W8'


def init_bot():
    bot = telebot.TeleBot(TOKEN)

    # @bot.message_handler(commands=['start'])
    # def start(message):
    #     bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    #
    # @bot.message_handler(func=lambda message: True, content_types=['text'])
    # def echo_message(message):
    #     bot.reply_to(message, message.text)

    return bot


@app.route('/test')
def home():
    message = request.args.get('m')
    return generetive_message(message)


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot = init_bot()
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    chat_id = update.message.from_user.id
    message = update.message.text
    reply = generetive_message(message, chat_id)
    bot.send_message(chat_id, reply)
    return '!', 200


@app.route('/webhook')
def webhook():
    bot = init_bot()
    bot.remove_webhook()
    bot.set_webhook(url='https://flaskvpu29lvivbot-git-main-intserhiys-projects.vercel.app/' + TOKEN)
    # bot.set_webhook(url='https://1d75-31-148-51-243.ngrok-free.a
    #
    #
    #
    #
    # pp/' + TOKEN)
    return '!', 200
