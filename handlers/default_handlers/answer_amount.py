from telebot.types import Message
from telebot import custom_filters

from loader import bot
from states.my_bot_states import MyStates

bot.add_custom_filter(custom_filters.StateFilter(bot))

# ANSWER_AMOUNT_COMMANDS = (
#     ("restart", "Начать заново"),
#     ("stop", "Остановить бота"),
#     ("help", "Вывести справку"),
#     ("history", "История запросов"),
#     ("back", "Вернуться на шаг назад"),
# )


@bot.message_handler(state=MyStates.answer_amount, commands=["back"])
def bot_back_answer_amount(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        method = data['method']
    if method == 'short':
        bot.send_message(message.chat.id, "Шаг 1 из 3. Введите город для поиска.")
        bot.set_state(message.from_user.id, MyStates.city_input, message.chat.id)
    elif method == 'long':
        bot.send_message(message.chat.id, "Шаг 3 из 5. Введите в каком диапазоне расстояния от центра города будем "
                                          "искать отель?")
        bot.set_state(message.from_user.id, MyStates.distance_range, message.chat.id)
    else:
        bot_answer_amount_help(message)


# @bot.message_handler(state=MyStates.answer_amount, commands=["help"])
# def bot_answer_amount_help(message: Message):
#     text = [f"/{command} - {desk}" for command, desk in ANSWER_AMOUNT_COMMANDS]
#     bot.reply_to(message, "\n".join(text))
#     bot.send_message(message.chat.id, f'answer amount')


@bot.message_handler(state=MyStates.answer_amount)
def bot_answer_amount_input(message: Message):
    if message.text.isdigit() and 1 <= int(message.text) <= 9:
        bot.reply_to(
            message, "Вас понял!"
        )
        step, step_over = 5, 5
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['answer_amount'] = message.text
            method = data['method']
        if method == 'short':
            step, step_over = 3, 3
        bot.send_message(message.chat.id, f'Шаг {step} из {step_over}. Нужно ли фото отелей? Да/Нет')
        bot.set_state(message.from_user.id, MyStates.photo_need, message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Неверный ввод. Введите цифру от 1 до 9.')
