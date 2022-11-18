from loader import bot
from states.city_info import CityInfoState
from telebot.types import Message
from handlers.custom_handlers.survey import survey


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message) -> None:
    bot.set_state(message.from_user.id, CityInfoState.bestdeal, message.chat.id)
    survey(message)
