import config

import telebot
from telebot import types

from bot import utils
from bot.call_types import CallTypes


from backend.models import BotUser
from backend.templates import Messages, Keys


def language_call_handler(bot: telebot.TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    user.lang = call_type.lang
    user.save()
    text = Messages.MESSAGE_HANDLER.get(user.lang)
    bot.edit_message_text(text=text, chat_id=chat_id,
                            message_id=call.message.id)

