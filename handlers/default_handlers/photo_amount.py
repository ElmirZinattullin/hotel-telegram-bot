from telebot.types import Message
from telebot import custom_filters

from loader import bot
from states.my_bot_states import MyStates
from . import answer

bot.add_custom_filter(custom_filters.StateFilter(bot))

# PHOTO_AMOUNT_COMMANDS = (
#     ("restart", "Начать заново"),
#     ("stop", "Остановить бота"),
#     ("help", "Вывести справку"),
#     ("history", "История запросов"),
#     ("back", "История запросов"),
# )


@bot.message_handler(state=MyStates.photo_amount, commands=["back"])
def bot_back_photo_amount(message: Message):
    step, step_over = 5, 5
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        method = data['method']
    if method == 'short':
        step, step_over = 3, 3
    bot.send_message(message.chat.id, f'Шаг {step} из {step_over}. Нужно ли фото отелей? Да/Нет')
    bot.set_state(message.from_user.id, MyStates.photo_need, message.chat.id)


# @bot.message_handler(state=MyStates.photo_amount, commands=["help"])
# def bot_photo_need_help(message: Message):
#     text = [f"/{command} - {desk}" for command, desk in PHOTO_AMOUNT_COMMANDS]
#     bot.reply_to(message, "\n".join(text))
#     bot.send_message(message.chat.id, f'photo amount')


@bot.message_handler(state=MyStates.photo_amount)
def bot_photo_amount_input(message: Message):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        bot.reply_to(
            message, "Вас понял! Начат поиск подходящих отелей. Подождите..."
        )
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_amount'] = message.text
        # bot.send_message(message.chat.id, 'Тут функция по поиску отелей')
        hotel_msg_list = answer.search(message)
        if hotel_msg_list:
            answer.send_result(message, hotel_msg_list)
        else:
            bot.send_message(message.chat.id, 'К сожалению возникли проблемы с запросом. Повторите запрос позже.')
        bot.set_state(message.from_user.id, MyStates.answer, message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Введите цифру от 1 до 5 - количество необходимых фото.')

