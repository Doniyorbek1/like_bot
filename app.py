from flask import Flask,request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackContext,CallbackQueryHandler, Dispatcher
from telegram import Update,  Bot
from handler import start, get_image, callback_like

import os

# get token from environment variable
TOKEN = os.environ['TOKEN'] 

bot = Bot(TOKEN)

app = Flask(__name__)

@app.route('/home', methods=['POST'])
def main():
    
    data = request.get_json(force=True)
    
    #dispatcher
    dp : Dispatcher = Dispatcher(bot, None, workers=0)
    
    #update
    update: Update = Update.de_json(data, bot)
    
    print(request.form)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.photo, get_image))
    dp.add_handler(CallbackQueryHandler(callback_like))
    
    dp.process_update(update)
    return {"status":200}

if __name__ == '__main__':
    app.run(debug=True)
    