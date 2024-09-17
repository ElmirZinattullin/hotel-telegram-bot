from telebot.types import Message

from loader import bot
from states.my_bot_states import MyStates
from handlers.default_handlers import common_comands

current_state = MyStates.days_amount
previous_state = MyStates.check_in_date
next_state = MyStates.main_menu


@bot.message_handler(state=current_state, commands=["back"])
def bot_back_days_amount(message: Message):
    bot.set_state(message.from_user.id, previous_state, message.chat.id)
    bot.send_message(message.chat.id, "Шаг 2 из 3. Введите дату заселения. Формат: dd/mm.")


@bot.message_handler(state=current_state)
def bot_days_amount(message: Message):
    if message.text.isdigit() and int(message.text.isdigit()) > 0:
        bot.reply_to(
            message, "Вас понял. Возвращаю в главное меню."
        )
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['days_amount'] = message.text
        bot.set_state(message.from_user.id, next_state, message.chat.id)
        common_comands.bot_restart(message)
        # bot.send_message(message.chat.id, f"Вы находитесь в главном меню бота."
        #                                   f"\n"
        #                                   f"\nВыберите режим поиска:"
        #                                   f"\n"
        #                                   f"\n/low_price -  Подобрать самые дешевые отели;"
        #                                   f"\n/high_price - Подобрать самые дорогие отели;"
        #                                   f"\n/best_deal - Настроить поиск по цене и удаленности от центра."
        #                                   f"\n/user_settings - Ввести информация о количестве человек и дате заселения")
    else:
        bot.reply_to(
            message, "Не корректный ввод. Введите количество дней в виде числа."
        )