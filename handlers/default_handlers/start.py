from telebot.types import Message

from states.my_bot_states import MyStates

from loader import bot


@bot.message_handler(commands=["start"], state=None)
def bot_start(message: Message):
    if bot.get_state(message.from_user.id, message.chat.id) == None:
        bot.reply_to(message, f"Бот запущен! Для просмотра доступных команд воспользуйтесь командой /help")
        bot.send_message(message.chat.id, f"Привет, {message.from_user.full_name}!"
                                          f"\nЭто бот по подбору отелей. Вы находитесь в главном меню бота."
                                          f"\n"
                                          f"\nВыберите режим поиска:"
                                          f"\n"
                                          f"\n/low_price -  Подобрать самые дешевые отели;"
                                          f"\n/high_price - Подобрать самые дорогие отели;"
                                          f"\n/best_deal - Настроить поиск по цене и удаленности от центра."
                                          f"\n/user_settings - Ввести информация о количестве человек и дате заселения. "
                                          f"По умолчанию будет производится поиск для одного человека на одну ночь на "
                                          f"завтра."
                                          f"\n/history - Посмотреть историю запросов.")
        bot.set_state(message.from_user.id, MyStates.main_menu, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Бот уже в работе!")

    # status = bot.get_state(message.from_user.id, message.chat.id)


