from telebot.types import Message


from loader import bot
from states.my_bot_states import MyStates
import core
from handlers.default_handlers import answer

current_state = MyStates.history
previous_state = MyStates.main_menu
next_state = MyStates.answer


@bot.message_handler(state=current_state, commands=["back"])
def bot_back_history(message: Message):
    bot.reply_to(message, "Вы перешли в главное меню.")
    bot.set_state(message.from_user.id, previous_state, message.chat.id)


@bot.message_handler(state=current_state)
def bot_history_view(message: Message):
    if message.text.isdigit() and int(message.text.isdigit()) <= 10:
        response_list = history_response(message.from_user.id)
        print(response_list)
        i_response = int(message.text.isdigit())
        if len(response_list) >= int(message.text.isdigit()):
            bot.set_state(message.from_user.id, next_state, message.chat.id)
            response = response_list[i_response - 1]
            answer.send_result(message, response)
            return
    bot.send_message(message.from_user.id, 'Некорректный ввод, введите номер запроса.')


def history_all(user_id):
    # user_id = message.from_user.id
    history_dict = core.reply_to_db(user_id)
    return history_dict


def history_request(user_id):
    option = 'request'
    # user_id = message.from_user.id
    history_dict = core.reply_to_db(user_id)
    if history_dict:
        return history_dict[option]
    else:
        return None


def history_response(user_id):
    option = 'response'
    # user_id = message.from_user.id
    history_dict = core.reply_to_db(user_id)
    if history_dict:
        return history_dict[option]
    else:
        return None


if __name__ == '__main__':
    history_list = history_all(468289082)
    print(history_list)
