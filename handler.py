import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
import requests
from pprint import pprint
# Handler for /start command
def start(update:Update, context:CallbackContext):

    update.message.reply_text('Hi!')

# Handler for get image
def get_image(update:Update, context:CallbackContext):
    """
    Get the image from the user and send to backend
    """
    # Get the message id
    message_id = update.message.message_id
    # Get image id
    image_id = update.message.photo[-1].file_id
    # Print message id and image id to the log

    print(f"Message id: {message_id}, Image id: {image_id}")
    # Send image to backend
    # endpoint url
    url = 'http://likedislikeapi.pythonanywhere.com/api/addImage'
    # Payload
    payload = {
        'message_id': message_id,
        'image_id': image_id
    }
    # Send request
    response = requests.post(url, json=payload)
    # Print status code
    print(response.status_code)
    # data = requests.get('http://likedislikeapi.pythonanywhere.com/api/{message_id}')
    # data = data.json()
    # likes = data["like"]
    # dislikes = data["dislike"]
    keyboard = InlineKeyboardMarkup([
        [
        InlineKeyboardButton(f"👍", callback_data=f'like:{message_id}'),
        InlineKeyboardButton(f"👎", callback_data=f'dislike:{message_id}')
        
        ]
    ])


    
    channel_id = '@sinov_uchun11'
    # Send image to channel
    context.bot.send_photo(
        chat_id=channel_id, 
        photo=image_id,
        caption="Rasmga reaksiya bildirishni unitmang!!!",
        reply_markup=keyboard
        )
    

def callback_like(update:Update, context:CallbackContext):
    query = update.callback_query
    # Get query data
    pprint(query.data)
    like,message_id = query.data.split(':')
    #  Get user id
    user_id = query.from_user.id
    # Get message id
    print(like)
    if like == 'like':
        url = "http://likedislikeapi.pythonanywhere.com/add-like"
        payload = {
            "user_id ":user_id,
            "img_id":message_id,
        }
        r = requests.post(url, json=payload)     
    else:
        url = "http://likedislikeapi.pythonanywhere.com/add-dislike"
        payload = {
            "user_id ":user_id,
            "img_id":message_id,
        }
        r = requests.post(url, json=payload)  


    
    query.answer(
        f' Data: {like}, "image_id":{message_id}', 
        show_alert=True
        )
    # query.edit_message_text(text="Selected option: {}".format(query.data))
    
    return {"status":200}