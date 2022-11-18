from loader import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_request() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Да', callback_data='confirm'),
               InlineKeyboardButton(text='Нет', callback_data='cancel'))
    return markup
