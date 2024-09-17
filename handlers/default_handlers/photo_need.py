from telebot.types import Message
from telebot import custom_filters

from loader import bot
from states.my_bot_states import MyStates
from . import answer

bot.add_custom_filter(custom_filters.StateFilter(bot))

# PHOTO_NEED_COMMANDS = (
#     ("restart", "Начать заново"),
#     ("stop", "Остановить бота"),
#     ("help", "Вывести справку"),
#     ("history", "История запросов"),
#     ("back", "История запросов"),
# )


@bot.message_handler(state=MyStates.photo_need, commands=["back"])
def bot_back_photo_need(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        metod = data['metod']
    if metod == 'short':
        bot.send_message(message.chat.id, "Шаг 2 из 3. Введите количество отелей для поиска от 1 до 9.")
    elif metod == 'long':
        bot.send_message(message.chat.id, "Шаг 4 из 5. Введите количество отелей для поиска от 1 до 9.")
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте сначала")
        bot.set_state(message.from_user.id, MyStates.main_menu, message.chat.id)
    bot.set_state(message.from_user.id, MyStates.answer_amount, message.chat.id)


# @bot.message_handler(state=MyStates.photo_need, commands=["help"])
# def bot_photo_need_help(message: Message):
#     text = [f"/{command} - {desk}" for command, desk in PHOTO_NEED_COMMANDS]
#     bot.reply_to(message, "\n".join(text))
#     bot.send_message(message.chat.id, f'photo неед')


@bot.message_handler(state=MyStates.photo_need)
def bot_photo_need_input(message: Message):
    if message.text.lower() == 'да':
        bot.reply_to(
            message, "Вас понял!"
        )
        bot.send_message(message.chat.id, 'Сколько фото предоставить? Введите цифру от 1 до 5')
        bot.set_state(message.from_user.id, MyStates.photo_amount, message.chat.id)
    elif message.text.lower() == 'нет':
        bot.reply_to(
            message, "Начат поиск подходящих отелей. Подождите...!"
        )
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_amount'] = 0
        hotel_msg_list = answer.search(message)
        if hotel_msg_list:
            answer.send_result(message, hotel_msg_list)
        else:
            bot.send_message(message.chat.id, 'К сожалению возникли проблемы с запросом. Повторите запрос позже.')
        bot.set_state(message.from_user.id, MyStates.answer, message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Нужно ли фото отелей? Введите только "Да" или "Нет".')

