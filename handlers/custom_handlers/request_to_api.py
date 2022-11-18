from loader import bot
import requests
from requests import get
import json
from config_data import config
from telebot.types import InputMediaPhoto
import re
from database.database import add_new_request_db


def request_to_api(url: str, headers: dict, querystring: dict):
    try:
        response = get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return response
    except Exception as e:
        pass


def request_hotels_list(url: str, headers: dict, querystring: dict) -> list:
    try:
        hotels = request_to_api(url, headers, querystring)
        pattern = r'(?<=,)"results":.+?(?=,"pagination)'
        find = re.search(pattern, hotels.text)
        if find:
            hotels_data = json.loads(f"{{{find[0]}}}")['results']
        else:
            hotels_data = []
        return hotels_data
    except Exception as e:
        pass


def filter_by_dist(hotels_list: list, distance: float) -> list:
    hotels_filter_by_dist = list(filter(lambda x:
                                        float(''.join(re.split(
                                            ' |km|км', x['landmarks'][0]['distance'])).replace(',', '.')
                                              ) <= distance, hotels_list))
    return hotels_filter_by_dist


def hotels_filtered_by_dist(hotels: list, distance: float, hotels_quan: int, querystring: dict):
    hotels_filtered = filter_by_dist(hotels_list=hotels, distance=distance)
    while len(hotels) < hotels_quan:
        querystring["pageNumber"] = str(int(querystring["pageNumber"]) + 1)
        next_page_hotels = request_hotels_list(config.url_list, config.headers, querystring)
        if len(next_page_hotels) == 0:
            break
        next_page_hotels = filter_by_dist(hotels_list=next_page_hotels, distance=distance)
        hotels_filtered.append(next_page_hotels)
    if len(hotels_filtered) > hotels_quan:
        hotels_filtered = hotels_filtered[:hotels_quan - 1]
    return hotels_filtered


def find_hotels(chat_id, data: dict):
    bot.send_message(chat_id, 'Начинаю поиск')
    querystring = {"destinationId": data['destination_id'],
                   "pageNumber": "1",
                   "pageSize": data['hotels_quan'],
                   "checkIn": data['check_in'].strftime('%Y-%m-%d'),
                   "checkOut": data['check_out'].strftime('%Y-%m-%d'),
                   "adults1": "1",
                   "sortOrder": data['sort_order'],
                   "locale": "ru_RU",
                   "currency": "RUB"
                   }
    try:
        querystring["priceMin"], querystring["priceMax"] = data['price_min'], data['price_max']
        querystring["pageSize"] = '25'
    except BaseException as err:
        pass

    hotels = request_hotels_list(config.url_list, config.headers, querystring)

    if hotels is not None:
        try:
            hotels = hotels_filtered_by_dist(hotels=hotels, distance=float(data['distance_from_center']),
                                             hotels_quan=int(data['hotels_quan']), querystring=querystring)
        except BaseException as err:
            pass

        result_text = []
        for index, i_result in enumerate(hotels):
            price_per_night = i_result['ratePlan']['price']['exactCurrent']
            stay_days = data['check_out'] - data['check_in']
            i_hotel_url = 'https://ie.hotels.com/ho{hotel_id}/?check_in={check_in}&check_out={check_out}'.format(
                hotel_id=i_result['id'],
                check_in=data['check_in'].strftime('%Y-%m-%d'),
                check_out=data['check_out'].strftime('%Y-%m-%d')
            )
            i_hotel_info = "{index}. Название отеля: {name}\nАдрес: {address}\nРасстояние до центра: {dist}\n" \
                           "Цена за ночь: {price_per_night:,.2f} {cur}\n" \
                           "Общая стоимость: {total_price:,.2f} {cur} за {days} ночи(ей)\n{url}".format(
                index=index + 1,
                name=i_result['name'],
                address=', '.join([item for item in list(i_result['address'].values())[0:5]
                                   if item != "" and type(item) == str]),
                dist=i_result['landmarks'][0]['distance'],
                price_per_night=price_per_night,
                total_price=price_per_night * stay_days.days,
                cur=querystring['currency'],
                days=stay_days.days,
                url=i_hotel_url
            )

            result_text.append('{index}. {hotel}'.format(index=index + 1, hotel=i_result['name']))

            if data['with_photo']:
                try:
                    photos = request_to_api(config.photos_url, config.headers, querystring={"id": str(i_result['id'])})
                    pattern = r'(?<=,)"hotelImages":.+?(?=,"roomImages)'
                    find = re.search(pattern, photos.text)
                    if find:
                        photos_data = json.loads(f"{{{find[0]}}}")["hotelImages"]

                        i_photos = list()
                        for j_index, j_photo in enumerate(photos_data[0:int(data['photo_quan'])]):
                            i_url = j_photo['baseUrl'].replace('{size}', 'z')
                            if j_index == 0:
                                i_photos.append(InputMediaPhoto(i_url, caption=i_hotel_info))
                            else:
                                i_photos.append(InputMediaPhoto(i_url))
                        bot.send_media_group(chat_id, i_photos)
                    else:
                        raise BaseException
                except BaseException as err:
                    bot.send_message(chat_id, i_hotel_info)
            else:
                bot.send_message(chat_id, i_hotel_info)

        add_new_request_db(username=data['username'], telegram_id=data['telegram_id'], sent_date=data['sent_date'],
                           command=data['command'], result_text='\n'.join(result_text))
    else:
        bot.send_message(chat_id, 'Ничего не найдено')
