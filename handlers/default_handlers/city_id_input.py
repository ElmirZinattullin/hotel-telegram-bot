from telebot.types import Message
from telebot import custom_filters

from loader import bot
from states.my_bot_states import MyStates
#from utils.parcing import find_city
from config_data import config

bot.add_custom_filter(custom_filters.StateFilter(bot))

current_state = MyStates.city_id_input
previous_state = MyStates.city_input


@bot.message_handler(state=current_state, commands=["back"])
def bot_back_city_id_input(message: Message):
    bot.reply_to(message, "Введите город для поиска.")
    bot.set_state(message.from_user.id, previous_state, message.chat.id)


@bot.message_handler(state=current_state)
def bot_city_id_input(message: Message):
    try:
        i_city = int(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            id_cities = data['citiesidcode'].split('#')
            city_name_list = data['citiesnamecode'].split('@')
            id_city =id_cities[int(i_city) - 1]
            city_name = city_name_list[int(i_city) - 1]
            data['id_city'] = id_city
            data['city_name'] = city_name
            method = data['method']
        bot.send_message(message.chat.id, "Вы выбрали {}".format(city_name))
        if method == 'short':
            bot.set_state(message.from_user.id, MyStates.answer_amount, message.chat.id)
            bot.send_message(message.chat.id, "Шаг 2 из 3. Сколько предложений вывести? Введите цифру от 1 до 9")
        elif method == 'long':
            bot.set_state(message.from_user.id, MyStates.price_range, message.chat.id)
            bot.send_message(message.chat.id, 'Шаг 2 из 5. Введите диапазон цен в $. Например 15 - 100.')
    except:
        bot.send_message(message.chat.id, "Некорректный ввод. Введите номер варианта.")


