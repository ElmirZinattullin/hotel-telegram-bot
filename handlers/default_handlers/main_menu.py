from telebot.types import Message

from loader import bot
from states.my_bot_states import MyStates
from . import history


# MAIN_MENU_COMMANDS = (
#     ("restart", "Начать заново"),
#     ("stop", "Остановить бота"),
#     ("help", "Вывести справку"),
#     ("low_price", "Вывести сначала дешевые отели"),
#     ("high_price", "Вывести сначала дорогие отели"),
#     ("best_deal", "Подбор отелей по цене и удаленности от центра"),
#     ("history", "История запросов"),
# )



@bot.message_handler(state=MyStates.main_menu, commands=["low_price"])
def bot_low_price(message: Message):
    bot.reply_to(
        message, "Выбран поиск самых дешёвых отелей в городе."
    )
    bot.set_state(message.from_user.id, MyStates.city_input, message.chat.id)
    bot.send_message(message.chat.id, "Шаг 1 из 3. Введите город для поиска.")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['method'] = 'short'
        data['short'] = 'low'


@bot.message_handler(state=MyStates.main_menu, commands=["high_price"])
def bot_high_price(message: Message):
    bot.reply_to(
        message, "Выбран поиск самых дорогих отелей в городе."
    )
    bot.set_state(message.from_user.id, MyStates.city_input, message.chat.id)
    bot.send_message(message.chat.id, "Шаг 1 из 3. Введите город для поиска.")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['method'] = 'short'
        data['short'] = 'high'


@bot.message_handler(state=MyStates.main_menu, commands=["best_deal"])
def bot_best_deal(message: Message):
    bot.reply_to(
        message, "Выбран поиск подходящих отелей с фильтром по цене и расстоянию от центра."
    )
    bot.set_state(message.from_user.id, MyStates.city_input, message.chat.id)
    bot.send_message(message.chat.id, "Шаг 1 из 5. Введите город для поиска.")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['method'] = 'long'


@bot.message_handler(state=MyStates.main_menu, commands=["user_settings"])
def bot_user_settings(message: Message):
    bot.reply_to(
        message, "Заполните информацию о заселение."
    )
    bot.set_state(message.from_user.id, MyStates.man_amount, message.chat.id)
    bot.send_message(message.chat.id, "Шаг 1 из 3. Введите количество человек.")


@bot.message_handler(state=MyStates.main_menu, commands=["history"])
def bot_history(message: Message):
    bot.reply_to(
        message, "Ваша история запросов:"
    )
    request_list = history.history_request(message.from_user.id)
    if request_list:
        bot.send_message(message.from_user.id, '\n'.join(request_list))
        bot.set_state(message.from_user.id, MyStates.history, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите номер запроса для просмотра ответа.')
    else:
        bot.send_message(message.from_user.id, "История пуста, поскольку вы ещё не отправляли запросы.")



# @bot.message_handler(state=MyStates.main_menu, commands=["help"])
# def bot_main_menu_help(message: Message):
#     text = [f"/{command} - {desk}" for command, desk in MAIN_MENU_COMMANDS]
#     bot.reply_to(message, "\n".join(text))
#     bot.send_message(message.chat.id, "Вы в главном меню")


@bot.message_handler(state=MyStates.main_menu)
def bot_main_menu_echo(message: Message):
    bot.send_message(message.chat.id, f""
                                      f"\nЭто бот по подбору отелей. Вы находитесь в главном меню бота."
                                      f"\n"
                                      f"\nВыберите режим поиска:"
                                      f"\n"
                                      f"\n/low_price -  Подобрать самые дешевые отели;"
                                      f"\n/high_price - Подобрать самые дорогие отели;"
                                      f"\n/best_deal - Настроить поиск по цене и удаленности от центра;"
                                      f"\n/user_settings - Ввести информация о количестве человек и дате заселения. "
                                      f"По умолчанию будет производится поиск для одного человека на одну ночь на "
                                      f"завтра."
                                      f"\n/history - История запросов.")
