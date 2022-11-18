from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def request_with_photo() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Да', callback_data='with_photo'),
               InlineKeyboardButton(text='Нет', callback_data='without_photo'))
    return markup
