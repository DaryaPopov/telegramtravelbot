import json
import re
from config_data import config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.custom_handlers.request_to_api import request_to_api


def city_founding(city):
    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}
    response = request_to_api(config.url_location, config.headers, querystring)
    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, response.text)
    if find:
        suggestions = json.loads(f"{{{find[0]}}}")
        cities = list()
        for dest_id in suggestions['entities']:  # Обрабатываем результат
            clear_destination = re.sub(r"<.*?>", '', dest_id['caption'])
            cities.append({'city_name': clear_destination, 'destination_id': dest_id['destinationId']})
        return cities


def city_markup(city='Токио'):
    cities = city_founding(city)
    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(InlineKeyboardButton(text=city['city_name'],
                                              callback_data=f'{city["destination_id"]}'))
    return destinations
