import datetime

from telebot.types import Message
from states.my_bot_states import MyStates
from config_data.config import DEFAULT_COMMANDS
from loader import bot


def bot_not_run(func):
    def _wrapped_func(message):
        if bot.get_state(message.from_user.id, message.chat.id) != None:
            result = func(message)
            return result
        else:
            bot.reply_to(
                message, "Бот не активен. Для начала работы введите команду /start"
            )
    return _wrapped_func


@bot.message_handler(commands=["main_menu"], state="*")
@bot_not_run
def bot_restart(message: Message):
    date = datetime.date.today() + datetime.timedelta(1)
    check_in_day = f'{date.day}/{date.month}'
    parameters = {'man_amount': 1, 'days_amount': 1, 'check_in_day': check_in_day}
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        for key in parameters.keys():
            if key in data:
                parameters[key] = data[key]
    out_message = f"Вы вернулись в главное меню." \
                  f"\n" \
                  f"\nВыберите режим поиска:" \
                  f"\n" \
                  f"\n/low_price -  Подобрать самые дешевые отели;"\
                  f"\n/high_price - Подобрать самые дорогие отели;"\
                  f"\n/best_deal - Настроить поиск по цене и удаленности от центра."\
                  f"\n/user_settings - Ввести информация о количестве человек и дате заселения. "\
                  f"Текущие настройки: Количество человек - {parameters['man_amount']}, "\
                  f"дата заселения - {parameters['check_in_day']}, "\
                  f"количество ночей {parameters['days_amount']}" \
                  f"\n/history - Показать историю поиска."
    if message.text == '/main_menu':
        bot.reply_to(message, out_message)
    else:
        bot.send_message(message.chat.id, out_message)
    bot.set_state(message.from_user.id, MyStates.main_menu, message.chat.id)
    # set_start_commands(bot, START_COMMANDS)


@bot.message_handler(commands=["stop"], state="*")
@bot_not_run
def bot_stop(message: Message):
    bot.reply_to(message, f"Бот остановлен!")
    bot.reset_data(message.from_user.id)
    bot.set_state(message.from_user.id, None, message.chat.id)


@bot.message_handler(commands=["help"], state=None)
@bot_not_run
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS if command != 'help']
    bot.reply_to(message, "\n".join(text))
