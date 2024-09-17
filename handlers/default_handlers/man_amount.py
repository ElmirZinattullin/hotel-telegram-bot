from telebot.types import Message

from loader import bot
from states.my_bot_states import MyStates
from handlers.default_handlers import start

current_state = MyStates.man_amount
previous_state = MyStates.main_menu
next_state = MyStates.check_in_date

@bot.message_handler(state=MyStates.man_amount, commands=["back"])
def bot_back_man_amount(message: Message):
    bot.set_state(message.from_user.id, MyStates.main_menu, message.chat.id)
    bot.send_message(message.chat.id, "Вы вернулись в главное меню.")

@bot.message_handler(state=MyStates.man_amount)
def bot_man_amount(message: Message):
    if message.text.isdigit() and int(message.text.isdigit()) > 0:
        bot.reply_to(
            message, "Вас понял."
        )
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['man_amount'] = message.text
        bot.set_state(message.from_user.id, MyStates.check_in_date, message.chat.id)
        bot.send_message(message.chat.id, "Шаг 2 из 3. Введите дату заселения. Формат: dd/mm.")
    else:
        bot.reply_to(
            message, "Не корректный ввод. Введите количество человек в виде числа."
        )