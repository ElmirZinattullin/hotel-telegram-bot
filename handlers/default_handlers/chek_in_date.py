from telebot.types import Message

from loader import bot
from states.my_bot_states import MyStates
from handlers import input_check

current_state = MyStates.check_in_date
previous_state = MyStates.man_amount
next_state = MyStates.days_amount


@bot.message_handler(state=current_state, commands=["back"])
def bot_back_check_in_date(message: Message):
    bot.set_state(message.from_user.id, previous_state, message.chat.id)
    bot.send_message(message.chat.id, "Шаг 1 из 3. Введите количество человек.")


@bot.message_handler(state=current_state)
def bot_men_check_in_date(message: Message):

    if input_check.valid_input_date(message.text):
        bot.reply_to(
            message, "Вас понял."
        )
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['check_in_day'] = message.text
        bot.set_state(message.from_user.id, next_state, message.chat.id)
        bot.send_message(message.chat.id, "Шаг 3 из 3. Введите количество ночей.")
    else:
        bot.reply_to(
            message, "Не корректный ввод. Введите дату в формате dd/mm.")

