from loader import bot
from telebot.types import Message
from database.models import db
from database.database import get_requests_history_dict


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    with db:
        try:
            for item in get_requests_history_dict(message):
                bot.send_message(chat_id=message.from_user.id,
                                 text='Поиск {command} \nДата поиска - {date} \nНайдены результаты:\n{result}'.format(
                                        command=item['command'],
                                        date=item['sent_date'],
                                        result=item['result'])
                                 )
        except TypeError as err:
            print(err)
            bot.send_message(chat_id=message.from_user.id, text="Записей не найдено.")
