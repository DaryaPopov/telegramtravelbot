from loader import bot
from telebot.types import InlineKeyboardMarkup
from telebot_calendar import Calendar, CallbackData
import datetime

check_in_cal = Calendar()
check_out_cal = Calendar()
check_in_callback = CallbackData("check_in_cal", "action", "year", "month", "day")
check_out_callback = CallbackData("check_out_cal", "action", "year", "month", "day")


def request_check_in(date=datetime.datetime.today()) -> InlineKeyboardMarkup:
    inline_cal = check_in_cal.create_calendar(name=check_in_callback.prefix, year=date.year, month=date.month)
    return inline_cal


def request_check_out(date=datetime.datetime.today()) -> InlineKeyboardMarkup:
    inline_cal = check_out_cal.create_calendar(name=check_out_callback.prefix, year=date.year, month=date.month)
    return inline_cal
