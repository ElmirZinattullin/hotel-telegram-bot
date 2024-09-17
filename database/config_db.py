import json

import peewee
import datetime
import os


class BaseModel(peewee.Model):
    class Meta:
        db_path = "database\some_data.db"
        database = peewee.SqliteDatabase(db_path)


class History(BaseModel):
    user_id = peewee.IntegerField()
    request = peewee.TextField()
    response = peewee.TextField()
    created_date = peewee.DateTimeField(default=datetime.datetime.now)


def view_history(user_id):
    user_history = History.select().where(History.user_id == user_id) \
        .order_by(History.created_date.desc()) \
        .limit(10)
    # for line in user_history:
    #    print(line.user_id, ':', line.request, ':', line.response, ':', line.created_date)
    return user_history


def user_history_list(user_id):
    user_history_table = view_history(user_id)
    user_history = list()
    for line in user_history_table:
        line_dict = {'time': line.created_date, 'query': line.request, 'reply': line.response}
        user_history.append(line_dict)
    return user_history


def add_history(user_id, request, response):
    # json_request = json.dumps(request, ensure_ascii=False)
    str_request = request
    json_response = json.dumps(response, ensure_ascii=False)
    History.create(user_id=user_id, request=str_request, response=json_response)


def create_bd():
    # DATA_BASE_NAME = 'some_data.db'
    # path = os.path.abspath('')
    # db_path = 'C:\PycharmProjects\pythonProject\python_basic_diploma\some_data.db'
    db_path = 'database\some_data.db'
    db = peewee.SqliteDatabase(db_path)
    if not os.path.exists(db_path):
        # DATA_BASE_NAME = 'some_data.db'
        # path = os.path.abspath('')
        # db_path = 'C:\PycharmProjects\pythonProject\python_basic_diploma\some_data.db'
        History.create_table()
    return db


if __name__ == '__main__':
    History.create_table()
    print(user_history_list(468289082))
    # for y in range(5):
    #     user_id = y * 111
    #     for i in range(5):
    #         some_request = f'{user_id}request' + 'id_' + f'{i}'
    #         some_response = f'{user_id}response' + 'id_' + f'{i}'
    #         time.sleep(30)
    #         add_history(user_id, some_request, some_response)

    # path = os.path.abspath('')
    # sep = os.path.sep
    # file_name = 'file.db'
    # print(sep)
    # # for record in user_history_list(333):
    # #     print(record)
    # print(path)
    #
    # print(sep.join((path, file_name)))

    DATA_BASE_NAME = 'some_data.db'
    path = os.path.abspath('')
    # db_path = 'C:\PycharmProjects\pythonProject\python_basic_diploma\some_data.db'
    db_path = 'database\some_data.db'
    db = peewee.SqliteDatabase(db_path)
