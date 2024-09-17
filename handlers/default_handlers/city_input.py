from telebot.types import Message
from telebot import custom_filters

from loader import bot
from states.my_bot_states import MyStates

from utils import parcing
from utils import headers_init

headers = headers_init.headers
bot.add_custom_filter(custom_filters.StateFilter(bot))

# CITY_INPUT_COMMANDS = (
#     ("restart", "Начать заново"),
#     ("stop", "Остановить бота"),
#     ("help", "Вывести справку"),
#     ("history", "История запросов"),
# )

exclusive_special_signs = '<>?@!~`#№$;%^:&?*()_-+={}[]|/""1234567890'


def name_valid(name: str) -> bool:
    for symbol in list(name):
        if symbol in exclusive_special_signs:
            return False
    return True


@bot.message_handler(state=MyStates.city_input, commands=["back"])
def bot_back_city_input(message: Message):
    bot.send_message(message.chat.id, f"Вы вернулись в главном меню бота."
                                      f"\n"
                                      f"\nВыберите режим поиска:"
                                      f"\n"
                                      f"\n/low_price -  Подобрать самые дешевые отели;"
                                      f"\n/high_price - Подобрать самые дорогие отели;"
                                      f"\n/best_deal - Настроить поиск по цене и удаленности от центра;"
                                      f"\n/stop - Остановить бот.")
    bot.set_state(message.from_user.id, MyStates.main_menu, message.chat.id)


# @bot.message_handler(commands=["help"], state=MyStates.city_input)
# def bot_city_input_help(message: Message):
#     text = [f"/{command} - {desk}" for command, desk in CITY_INPUT_COMMANDS]
#     bot.reply_to(message, "\n".join(text))
#     bot.send_message(message.chat.id, f'city input')


@bot.message_handler(state=MyStates.city_input)
def bot_city_input(message: Message):
    if len(message.text) < 30 and name_valid(message.text):
        bot.reply_to(
            message, "Поиск в базе городов подождите..."
        )
        city_name = message.text
        cities = parcing.find_city.city_from_api_finder(city_name, headers)
        print(cities)
        city_info_list = list()
        city_id = list()
        city_name_list = list()
        if len(cities) > 0:
            if len(cities) == 1:
                bot.send_message(message.chat.id, "Найден {}.".format(cities[1]['name']))
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data['id_city'] = cities[1]['id']
                    data['city_name'] = cities[1]['name']
                    method = data['method']
                if method == 'short':
                    bot.set_state(message.from_user.id, MyStates.answer_amount, message.chat.id)
                    bot.send_message(message.chat.id,
                                     "Шаг 2 из 3. Сколько предложений вывести? Введите цифру от 1 до 9")
                elif method == 'long':
                    bot.set_state(message.from_user.id, MyStates.price_range, message.chat.id)
                    bot.send_message(message.chat.id, 'Шаг 2 из 5. Введите диапазон цен в $. Например 15 - 100.')
            else:
                for i_city, city_info in cities.items():
                    line = ') '.join((str(i_city), city_info['name']))
                    city_info_list.append(line)
                    city_id.append(city_info['id'])
                    city_name_list.append(city_info['name'])
                print(city_info_list)
                out_message = '\n'.join(city_info_list)
                bot.send_message(message.chat.id, "{} \n Введите нужный номер".format(out_message))
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data['citiesidcode'] = '#'.join(city_id)
                    data['citiesnamecode'] = '@'.join(city_name_list)
                bot.set_state(message.from_user.id, MyStates.city_id_input, message.chat.id)
        else:
            bot.send_message(message.chat.id, "К сожалению такой город не найден.")

        # id_city = cities[number]['id']
        # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        #     method = data['method']
        #     data['city'] = id_city
        # if method == 'short':
        #     bot.set_state(message.from_user.id, MyStates.answer_amount, message.chat.id)
        #     bot.send_message(message.chat.id, "Шаг 2 из 3. Сколько предложений вывести? Введите цифру от 1 до 9")
        # elif method == 'long':
        #     bot.set_state(message.from_user.id, MyStates.price_range, message.chat.id)
        #     bot.send_message(message.chat.id, 'Шаг 2 из 5. Введите диапазон цен в формате: "xxxx - yyyy".')
        # else:
        #     bot.send_message(message.chat.id, "Что-то пошло не так начните сначала")
    else:
        bot.send_message(message.chat.id, "Имя города не опознано. Введите другой город.")


