from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    welcome_sticker = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.from_user.id, welcome_sticker)
    bot.reply_to(message, f"Добро пожаловать, {message.from_user.first_name}!"
                          f"\nМеня зовут <b>{bot.get_me().first_name}</b>, я - бот для поиска отелей. "
                          f"Нажмите /help и я расскажу, что я умею.",
                 parse_mode='HTML')
