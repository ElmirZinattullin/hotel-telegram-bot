from telebot.types import Message
from telebot import custom_filters

from loader import bot
from states.my_bot_states import MyStates

bot.add_custom_filter(custom_filters.StateFilter(bot))

# DISTANCE_RANGE_COMMANDS = (
#     ("restart", "Начать заново"),
#     ("stop", "Остановить бота"),
#     ("help", "Вывести справку"),
#     ("history", "История запросов"),
#     ("back", "Вернуться на шаг назад"),
# )


@bot.message_handler(state=MyStates.distance_range, commands=["back"])
def bot_distance_range_range(message: Message):
    bot.send_message(message.chat.id, 'Шаг 2 из 5. Введите диапазон цен в формате: "xxxx - yyyy".')
    bot.set_state(message.from_user.id, MyStates.price_range, message.chat.id)


# @bot.message_handler(state=MyStates.distance_range, commands=["help"])
# def bot_distance_range_help(message: Message):
#     text = [f"/{command} - {desk}" for command, desk in DISTANCE_RANGE_COMMANDS]
#     bot.reply_to(message, "\n".join(text))
#     bot.send_message(message.chat.id, f'dist range')

@bot.message_handler(state=MyStates.distance_range)
def bot_distance_range_input(message: Message):
    line = ''.join(message.text.split())  # убираем пробелы с сообщения
    distance_range = line.split('-')
    if len(distance_range) == 2 and distance_range[0].isdigit() and distance_range[1].isdigit() \
            and distance_range[0] != distance_range[1]:
        bot.reply_to(
            message, "Вас понял!"
        )
        diff = float(distance_range[1]) - float(distance_range[0])
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if diff >= 0:
                data['distance_range'] = distance_range
            else:
                data['distance_range'] = [distance_range[1], distance_range[0]]
        bot.send_message(message.chat.id, 'Шаг 4 из 5. Сколько предложений вывести? Введите цифру от 1 до 9')
        bot.set_state(message.from_user.id, MyStates.answer_amount, message.chat.id)
    else:
        bot.reply_to(
            message, "Неверный ввод. Попробуйте еще раз."
        )
        bot.send_message(message.chat.id, 'Введите диапазон в километрах в формате: "число - число".')
