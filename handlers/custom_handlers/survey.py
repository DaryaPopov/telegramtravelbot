import re
from loader import bot
from states.city_info import CityInfoState
from telebot.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards.inline.with_photo import request_with_photo
from keyboards.inline.calendar import check_in_cal, check_out_cal, check_in_callback, check_out_callback, \
    request_check_in, request_check_out
from keyboards.inline.city_markup import city_markup
from keyboards.inline.confirmation import confirm_request
from datetime import datetime, timedelta
from handlers.custom_handlers.request_to_api import find_hotels


def survey(message: Message) -> None:
    sent_date = datetime.now()
    command = message.text
    username = message.from_user.first_name
    telegram_id = message.from_user.id
    msg = bot.send_message(message.from_user.id,
                           f'{username}, в каком городе будем смотреть отели?')

    if bot.get_state(message.from_user.id, message.chat.id) == CityInfoState.lowprice \
            or bot.get_state(message.from_user.id, message.chat.id) == CityInfoState.bestdeal:
        sort_order = 'PRICE'

    elif bot.get_state(message.from_user.id, message.chat.id) == CityInfoState.highprice:
        sort_order = 'PRICE_HIGHEST_FIRST'

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['sort_order'] = sort_order
        data['sent_date'] = sent_date
        data['command'] = command
        data['username'] = username
        data['telegram_id'] = telegram_id

    bot.register_next_step_handler(msg, check_city)


def check_city(message):
    if ''.join(re.split("-| |", message.text)).isalpha():
        try:
            bot.send_message(message.from_user.id, 'Уточните, пожалуйста:',
                             reply_markup=city_markup(message.text))
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['city'] = message.text
        except Exception:
            bot.send_message(message.from_user.id, "Такой город не найден. Нажмите /help, чтобы начать новый поиск.")
    else:
        bot.send_message(message.from_user.id, 'Название города может содержать только буквы.')


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def callback_handler(call: CallbackQuery):
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['destination_id'] = call.data
    if bot.get_state(call.from_user.id, call.message.chat.id) == CityInfoState.bestdeal:
        bot.send_message(call.message.chat.id, 'Укажите минимальную цену за ночью')
        bot.set_state(call.from_user.id, CityInfoState.price_min, call.message.chat.id)
    else:
        bot.send_message(call.message.chat.id, 'Сколько результатов поиска нужно вывести (максимум 25)?')
        bot.set_state(call.from_user.id, CityInfoState.hotels_quan, call.message.chat.id)


@bot.message_handler(state=CityInfoState.hotels_quan)
def get_hotels_quan(message: Message) -> None:
    if message.text.isdigit() and int(message.text) <= 25:
        bot.send_message(message.from_user.id, 'Нужно загрузить фотографии отелей?',
                         reply_markup=request_with_photo())
        bot.set_state(message.from_user.id, CityInfoState.with_photo, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_quan'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Количество результатов нужно указать цифрами.')


@bot.message_handler(state=CityInfoState.price_min)
def get_price_min(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Укажите максимальную цену за ночь.')
        bot.set_state(message.from_user.id, CityInfoState.price_max, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_min'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Минимальную цену нужно указать цифрами.')


@bot.message_handler(state=CityInfoState.price_max)
def get_price_max(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'В пределах какого расстояния от центра ищем отели (км)?')
        bot.set_state(message.from_user.id, CityInfoState.distance_from_center, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_max'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Минимальную цену нужно указать цифрами.')


@bot.message_handler(state=CityInfoState.distance_from_center)
def get_distance(message: Message) -> None:
    if message.text.replace(',', '').replace('.', '').replace('km', '').replace('км', '').replace(' ', '').isdigit():
        bot.send_message(message.from_user.id, 'Сколько результатов поиска нужно вывести (максимум 25)?')
        bot.set_state(message.from_user.id, CityInfoState.hotels_quan, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance_from_center'] = ''.join(re.split(" |km|км", message.text.replace(',', '.')))
    else:
        bot.send_message(message.from_user.id, 'Расстояние нужно указать цифрами.')


@bot.callback_query_handler(func=lambda call: call.data in ['with_photo', 'without_photo'])
def callback_handler(call: CallbackQuery):
    if call.data == 'with_photo':
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['with_photo'] = True
        bot.send_message(call.from_user.id, 'Сколько фотографий отеля нужно загрузить (максимум 9)?')
        bot.set_state(call.from_user.id, CityInfoState.photo_quan, call.message.chat.id)
    elif call.data == 'without_photo':
        bot.send_message(call.from_user.id, 'Укажите дату заезда', reply_markup=request_check_in())
        bot.set_state(call.from_user.id, CityInfoState.check_in, call.message.chat.id)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['photos_quan'] = '0'


@bot.message_handler(state=CityInfoState.photo_quan)
def get_photos_quan(message: Message) -> None:
    if message.text.isdigit() and int(message.text) <= 9:
        bot.send_message(message.from_user.id, 'Укажите дату заезда', reply_markup=request_check_in())
        bot.set_state(message.from_user.id, CityInfoState.check_in, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_quan'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Количество фотографий нужно указать цифрами.')


@bot.callback_query_handler(func=lambda call: call.data.startswith(check_in_callback.prefix))
def callback_handler(call: CallbackQuery):
    name, action, year, month, day = call.data.split(check_in_callback.sep)
    date = check_in_cal.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )

    if action == "DAY":
        today = datetime.today()
        if date >= datetime(today.year, today.month, today.day):
            bot.send_message(
                chat_id=call.from_user.id,
                text=f"Вы выбрали дату заезда {date.strftime('%d.%m.%Y')}",
                reply_markup=ReplyKeyboardRemove(),
            )
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                data['check_in'] = date
            bot.set_state(call.from_user.id, CityInfoState.check_out, call.message.chat.id)
            bot.send_message(call.from_user.id, 'Укажите дату выезда',
                             reply_markup=request_check_out(date + timedelta(days=1)))
        else:
            bot.send_message(call.from_user.id, "Эта дата недоступна. Укажите другую дату.",
                             reply_markup=request_check_in())

    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Попробуем снова. Нажмите /help и я расскажу, что я умею.",
            reply_markup=ReplyKeyboardRemove(),
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith(check_out_callback.prefix))
def callback_handler(call: CallbackQuery):
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        date_limit = data['check_in']

    name, action, year, month, day = call.data.split(check_out_callback.sep)
    date = check_out_cal.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )

    if action == "DAY":
        if date >= date_limit:
            bot.send_message(
                chat_id=call.from_user.id,
                text=f"Вы выбрали дату выезда {date.strftime('%d.%m.%Y')}",
                reply_markup=ReplyKeyboardRemove(),
            )
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                data['check_out'] = date
            bot.set_state(call.from_user.id, CityInfoState.confirm, call.message.chat.id)
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                text = f"Данные для поиска.\n" \
                       f"Город - {data['city']}\n" \
                       f"Количество результатов - {data['hotels_quan']}\n" \
                       f"Количество фото - {data['photo_quan']}\n" \
                       f"Даты {data['check_in'].strftime('%Y-%m-%d')} - {data['check_out'].strftime('%Y-%m-%d')}\n"
                try:
                    text = text + f"Диапазон цен - {data['price_min']} - {data['price_max']} руб.\n" \
                                  f"Расстояние от центра до {data['distance_from_center']} км.\n"
                except KeyError as err:
                    print(err)
                text = text + "Все верно?"

            bot.send_message(call.from_user.id, text, reply_markup=confirm_request())
        else:
            bot.send_message(call.from_user.id, "Эта дата недоступна. Укажите другую дату.",
                             reply_markup=request_check_out(date_limit))

    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Попробуем снова. Нажмите /help и я расскажу, что я умею.",
            reply_markup=ReplyKeyboardRemove(),
        )


@bot.callback_query_handler(func=lambda call: call.data == 'confirm' or call.data == 'cancel')
def callback_handler(call: CallbackQuery):
    if call.data == 'confirm':
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            find_hotels(chat_id=call.message.chat.id, data=data)
    else:
        bot.send_message(call.message.chat.id, 'Попробуем снова. Нажмите /help и я расскажу, что я умею.')
