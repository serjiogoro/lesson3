import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
import datetime
from random import randint, choice
from glob import glob
from emoji import emojize

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']

def greet_user(update, context):
    #smile = choice(settings.USER_EMOJI)
    #smile = emojize(smile, use_aliases = True)
    smile = get_smile(context.user_data)
    user_name = update.message.from_user.first_name
    print(f'Greetings, my dear little {user_name}! {smile} You push /start')
    update.message.reply_text(f'Greetings, my dear little {user_name}! {smile} You push /start')

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, я выиграл!"
    return message

def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите целое число"
    update.message.reply_text(message)

def planet(update, context):
    user_text = update.message.text 
    l = user_text.split()
    current_time = datetime.datetime.now() 
    plnt = eval('ephem.'+l[1])(f'{current_time.year}/{current_time.day}/{current_time.month}')
    constellation = ephem.constellation(plnt)
    print(constellation)
    update.message.reply_text(constellation)

def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))

def talk_to_me(update, context):
    #smile = choice(settings.USER_EMOJI)
    #smile = emojize(smile, use_aliases=True)
    smile = get_smile(context.user_data)
    user_text = update.message.text 
    username = update.effective_user.first_name
    text = update.message.text
    #print(f'{user_name}: {user_text}')
    #update.message.reply_text(f'{user_name}: {user_text}')
    update.message.reply_text(f"Hi there, {username} {smile}! Ты написал: {text}")

def error_callback(update, error):
    try:
        raise error
    except:
        print("Telegram Error")
        print(f'Error with {update.message.text.split()[1]}')
        update.message.reply_text(f'Error with {update.message.text.split()[1]}. Try again')
        print(error)


def main():
    PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    logging.basicConfig(filename='bot.log', level=logging.INFO)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start',greet_user))
    dp.add_handler(CommandHandler('guess',guess_number))
    dp.add_handler(CommandHandler('planet',planet))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_error_handler(error_callback)

    logging.info("Bot has just started")
    mybot.start_polling()
    mybot.idle()



if __name__ == "__main__":
    main()