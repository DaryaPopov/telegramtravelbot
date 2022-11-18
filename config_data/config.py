import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', 'поиск самых дешёвых отелей в городе'),
    ('highprice', 'поиск самых дорогих отелей в городе'),
    ('bestdeal', 'поиск отелей по цене и расположению от центра'),
    ('history', 'история поиска отелей')
)

url_location = "https://hotels4.p.rapidapi.com/locations/v2/search"

url_list = "https://hotels4.p.rapidapi.com/properties/list"

photos_url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

headers = {"X-RapidAPI-Key": RAPID_API_KEY,
           "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
           }

BASE_DIR = Path(__file__).resolve().parent.parent
