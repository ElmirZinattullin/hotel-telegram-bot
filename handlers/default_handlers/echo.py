from telebot.types import Message
from telebot import custom_filters
from loader import bot
from states.my_bot_states import MyStates


@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(
        message, "Бот не активен. Для начала работы введите команду /start"
    )
    status = bot.get_state(message.from_user.id, message.chat.id)
    print(status)




