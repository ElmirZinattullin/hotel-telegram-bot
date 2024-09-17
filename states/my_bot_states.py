import telebot
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States

# States storage
from telebot.storage import StateMemoryStorage


class MyStates(StatesGroup):
    main_menu = State()
    city_input = State()
    city_id_input = State()
    answer_amount = State()
    photo_need = State()
    price_range = State()
    distance_range = State()
    photo_amount = State()
    answer = State()
    check_in_date = State()
    days_amount = State()
    man_amount = State()
    history = State()
    history_view = State()
