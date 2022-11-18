from telebot.handler_backends import State, StatesGroup


class CityInfoState(StatesGroup):
    lowprice = State()
    highprice = State()
    bestdeal = State()
    city = State()
    dest_id = State()
    dest_id_bd = State()
    hotels_quan = State()
    with_photo = State()
    photo_quan = State()
    check_in = State()
    check_out = State()
    price_min = State()
    price_max = State()
    distance_from_center = State()
    confirm = State()
