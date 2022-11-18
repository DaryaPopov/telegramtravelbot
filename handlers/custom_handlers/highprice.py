from loader import bot
from states.city_info import CityInfoState
from telebot.types import Message
from handlers.custom_handlers.survey import survey

@bot.message_handler(commands=['highprice'])
def highprice(message: Message) -> None:
    bot.set_state(message.from_user.id, CityInfoState.highprice, message.chat.id)
    survey(message)
