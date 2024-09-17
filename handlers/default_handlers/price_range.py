from telebot.types import Message
from telebot import custom_filters

from loader import bot
from states.my_bot_states import MyStates

bot.add_custom_filter(custom_filters.StateFilter(bot))

# PRICE_RANGE_COMMANDS = (
#     ("restart", "Начать заново"),
#     ("stop", "Остановить бота"),
#     ("help", "Вывести справку"),
#     ("history", "История запросов"),
#     ("back", "Вернуться на шаг назад"),
# )


@bot.message_handler(state=MyStates.price_range, commands=["back"])
def bot_back_price_range(message: Message):
    bot.send_message(message.chat.id, "Шаг 1 из 5. Введите город для поиска.")
    bot.set_state(message.from_user.id, MyStates.city_input, message.chat.id)


# @bot.message_handler(state=MyStates.price_range, commands=["help"])
# def bot_price_range_help(message: Message):
#     text = [f"/{command} - {desk}" for command, desk in PRICE_RANGE_COMMANDS]
#     bot.reply_to(message, "\n".join(text))


@bot.message_handler(state=MyStates.price_range)
def bot_price_range_input(message: Message):
    line = ''.join(message.text.split())  # убираем пробелы с сообщения
    price_range = line.split('-')
    if len(price_range) == 2 and price_range[0].isdigit() and price_range[1].isdigit():
        bot.reply_to(
            message, "Вас понял!"
        )
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_range'] = price_range
        bot.send_message(message.chat.id, 'Шаг 3 из 5. Введите желаемый диапазон расстояния от центра '
                                          'города в километрах для расположения предполагаемого отеля'
                                          '\n Например: "0 - 10".')
        bot.set_state(message.from_user.id, MyStates.distance_range, message.chat.id)
    else:
        bot.reply_to(
            message, "Неверный ввод. Попробуйте еще раз."
        )
        bot.send_message(message.chat.id, 'Введите диапазон цены в $ в формате: "число - число".')

