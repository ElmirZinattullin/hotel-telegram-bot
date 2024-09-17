import datetime
import json
import functools
from typing import Callable, Dict, Any, List, Optional

import utils
import database
import handlers
from utils.parcing.API_error import APIError
from requests import ReadTimeout


def error_api_log_record(func: Callable) -> Callable:
    """Декоратор логирующий ошибки при выполнении запроса к API. Записывает сам запрос и ошибку"""
    @functools.wraps(func)
    def wrapped_func(methods):
        try:
            result = func(methods)
            return result
        except (APIError, ReadTimeout) as error:
            with open('error.log', 'a') as log_file:
                log_file.write(f'\nЗапрос: {methods}, Ошибка: {error}\n')
            return None

    return wrapped_func


@error_api_log_record
def reply_to_api(methods: Dict[str, Any]) -> Optional[List[dict]]:
    """Функция обрабатывающая запросы от бота к АПИ, возвращает None в случае неудачи"""
    if methods['check_in_day']:
        check_in_date = handlers.input_check.valid_input_date(methods['check_in_day'])
    else:
        check_in_date = datetime.date.today() + datetime.timedelta(1)
    try:
        json_hotels = utils.parcing.find_hotel.bot_answer_json(
            check_in_date=check_in_date,
            check_out_date=check_in_date + datetime.timedelta(int(methods['days_amount'])),
            people_amount=int(methods['man_amount']),
            method=methods['method'],
            city_id=methods['id_city'],
            answer_amount=int(methods['answer_amount']),
            photo_amount=int(methods['photo_amount']),
            headers=utils.headers_init.headers)
    except utils.parcing.API_error.APIError:
        return None
    all_hotel_info = list()
    for hotel_info in json_hotels:
        hotel = utils.hotel_info_decoder.hotel_info_decoder(hotel_info)
        all_hotel_info.append(hotel)
    query = all_hotel_info
    reply = database.reply_decoder.reply_decoder(methods)
    user_id = methods['user_id']
    record_history(user_id, reply, query)
    return query


def reply_to_db(user_id: int) -> dict[str, list[str] | list[Any]]:
    """Функция обрабатывающая запросы от бота к БД история поиска по ID пользователя. Возвращает словарь со списком
    запросов и ответов"""
    history_list = read_history(user_id)
    reply_list = list()
    query_list = list()
    print(len(history_list))
    # {'time': line.created_date, 'query': line.request, 'reply': line.response}
    for i_line, line in enumerate(history_list):
        query_line = 'Запрос №{}.\n\nВремя создания: {}; \n{}\n'.format(i_line + 1,
                                                                        line['time'].strftime('%m/%d/%y %H:%M'),
                                                                        line['query'])
        reply_line = json.loads(line['reply'])
        reply_list.append(reply_line)
        query_list.append(query_line)
    return {'request': query_list, 'response': reply_list}


def record_history(user_id: int, reply: str, query: List[dict]) -> None:
    """Функция для записи истории поиска к БД"""
    database.config_db.add_history(user_id, reply, query)


def read_history(user_id):
    return database.config_db.user_history_list(user_id)


if __name__ == '__main__':
    pass
    # text = json.dumps(str([{"hotel_info": "Название отеля: Czech Inn. \nАдрес: Francouzska 76, Prague, "
    #                                     "10100\nРасстояние от "
    #                          "центра: 2.25, км\nЦена за ночь: $25. Итоговая цена с учетом сборов: $30 total.",
    #              "photo": []}, {"hotel_info": "Название отеля: Plus Prague Hostel. \nАдрес: Praha 7 - Holesovice,"
    #                                           " Prívozní 1, Prague, 170 00\nРасстояние от центра: 3.06, км\nЦена за "
    #                                           "ночь: $36. Итоговая цена с учетом сборов: $42 total.", "photo": []}]))
    # print(text)
    # jsonfile = json.loads(text)
    # print(jsonfile)

    # database.config_db.History.create_table()
    # history_list, answer_list = reply_to_db(468289082)['request'], reply_to_db(468289082)['response']
    # for hist in history_list:
    #     print(hist)
    # for answ in answer_list:
    #         # print(answ)
    #         # print(answ)
    #         # print(answ_json)
    #         for hotel in answ:
    #             print(hotel['hotel_info'])
    #             # some_hotel = utils.hotel_info_decoder.hotel_info_decoder(hotel)
    # db = database.config_db.db_path
    # db_path = 'C:\PycharmProjects\pythonProject\python_basic_diploma\database\file.db'
    # print(db)
    # db = peewee.SqliteDatabase(db_path)
    # print(reply_to_db(111))
    # record_history(111, 'reply', 'query')
    # print(reply_to_db(111))

    #
    # some_method = {'method': 'low', 'id_city': '601763', 'answer_amount': '3', 'photo_amount': 0, 'man_amount': 1,
    #                'check_in_day': None, 'days_amount': 1, 'city_name': 'Берлингтон, Вермонт, США', 'user_id': 2222}
    # reply_to_api(some_method)
