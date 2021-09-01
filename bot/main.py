import config

import telebot
from telebot import types

from bot import utils, language
from bot.call_types import CallTypes

from backend.models import BotUser, Books
from backend.templates import Messages, Keys

bot = telebot.TeleBot(
    token=config.TOKEN,
    num_threads=3,
    parse_mode='HTML',
)

def language_keyboard_handler():
    keyboard = types.InlineKeyboardMarkup()

    uz_language_button = utils.make_inline_button(
        text=Keys.LANGUAGE.get(BotUser.Lang.UZ),
        CallType=CallTypes.Language,
        lang=BotUser.Lang.UZ,
    )
    ru_language_button = utils.make_inline_button(
        text=Keys.LANGUAGE.get(BotUser.Lang.RU),
        CallType=CallTypes.Language,
        lang=BotUser.Lang.RU,
    )
    en_language_button = utils.make_inline_button( 
        text=Keys.LANGUAGE.get(BotUser.Lang.EN),
        CallType=CallTypes.Language,
        lang=BotUser.Lang.EN,
    )

    keyboard.add(uz_language_button)
    keyboard.add(ru_language_button)
    keyboard.add(en_language_button)

    return keyboard


@bot.message_handler(commands=['start', 'language'])
def welcome_message_handler(message):
    chat_id = message.chat.id
    full_name = message.from_user.first_name
    user = BotUser.objects.filter(chat_id=chat_id)
    if not user.exists():
        BotUser.objects.create(chat_id=chat_id, full_name=full_name)
        keyboard = language_keyboard_handler()
        text = Messages.WELCOME_USER_MESSAGE.text
        bot.send_message(chat_id, text,
                        reply_markup=keyboard)
    else:
        user = BotUser.objects.get(chat_id=chat_id)
        text = Messages.MESSAGE_HANDLER.get(user.lang)
        print(user.lang)
        bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['help'])
def help_message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = Messages.HELP_MESSAGE_HANDLER.get(user.lang)
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['author'])
def help_message_handler(message):
    text = message.text.split('/author ')
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    books = Books.objects.filter(name=text[1])
    if not books.exists():
        text = Messages.NOT_BOOKS.get(user.lang)
        bot.send_message(chat_id=chat_id, text=text)
        return

    text = Messages.HELP_MESSAGE_HANDLER.get(user.lang)
    bot.send_message(chat_id=chat_id, text=text)
    
@bot.message_handler(commands=['language'])
def help_message_handler(message):
    chat_id = message.chat.id
    keyboard = language_keyboard_handler()
    text = Messages.WELCOME_USER_MESSAGE.text
    bot.send_message(chat_id, text,
                    reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help_message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = Messages.HELP_MESSAGE_HANDLER.get(user.lang)
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['help'])
def help_message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = Messages.HELP_MESSAGE_HANDLER.get(user.lang)
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['help'])
def help_message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = Messages.HELP_MESSAGE_HANDLER.get(user.lang)
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['help'])
def help_message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = Messages.HELP_MESSAGE_HANDLER.get(user.lang)
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['help'])
def help_message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = Messages.HELP_MESSAGE_HANDLER.get(user.lang)
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['help'])
def help_message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = Messages.HELP_MESSAGE_HANDLER.get(user.lang)
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['help'])
def help_message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = Messages.HELP_MESSAGE_HANDLER.get(user.lang)
    bot.send_message(chat_id=chat_id, text=text)

@bot.message_handler(commands=['help'])
def help_message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = Messages.HELP_MESSAGE_HANDLER.get(user.lang)
    bot.send_message(chat_id=chat_id, text=text)

callback_query_handlers = {
    CallTypes.Nothing: lambda _, __: True,
    # CallTypes.Back: language.back_call_handler,
    CallTypes.Language: language.language_call_handler,

}
@bot.callback_query_handler(func=lambda _: True)
def callback_query_handler(call):
    call_type = CallTypes.parse_data(call.data)
    chat_id = call.message.chat.id
   
    for CallType, query_handler in callback_query_handlers.items():
        if call_type.__class__ == CallType:
            query_handler(bot, call)
            break

if __name__ == "__main__":
    # bot.polling()
    bot.infinity_polling()