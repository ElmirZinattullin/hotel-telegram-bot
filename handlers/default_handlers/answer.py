import datetime

from telebot.types import Message, InputMediaPhoto
from loader import bot
from states.my_bot_states import MyStates
from handlers import input_check
import core


def search(message):
    methods = {'method': None,  # 'long': [None, None], 'short': [None],
               'id_city': None,
               'answer_amount': None,
               'photo_amount': None,
               'man_amount': 1,
               'check_in_day': None,
               'days_amount': 1,
               'city_name': None,
               'user_id': message.from_user.id
               }
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        for key in methods.keys():
            if key in data:
                methods[key] = data[key]
        if methods['method'] == 'short':
            methods['method'] = data['short']
        elif methods['method'] == 'long':
            methods['method'] = [data['price_range'], data['distance_range']]
        else:
            print('Что-то пошло не так.')

    # if methods['check_in_day']:
    #     print(methods['check_in_day'])
    #     check_in_date = input_check.valid_input_date(methods['check_in_day'])
    # else:
    #     check_in_date = datetime.date.today() + datetime.timedelta(1)
    hotels_info = core.reply_to_api(methods)
    return hotels_info


def send_result(message, hotels_info):
    for hotel in hotels_info:
        bot.send_message(message.chat.id, hotel['hotel_info'])
        if hotel['photo']:
            bot.send_media_group(message.chat.id, [InputMediaPhoto(photo) for photo in hotel['photo']])

@bot.message_handler(state=MyStates.answer)
def bot_echo(message: Message):
    bot.reply_to(
        message, "/main_menu - Вернутся в главное меню;"
                 "\n/stop - Остановить работу бота."
    )
