import datetime

def identify_method(_method):
    if isinstance(_method, list):
        _new_method = "best_deal"
    else:
        if _method == "high":
            _new_method = "high_price"
        else:
            _new_method = "low_price"
    return _new_method


def reply_decoder(methods: dict):
    """
        methods = {'method': None,  # 'long': [None, None], 'short': [None],
               'id_city': None,
               'answer_amount': None,
               'photo_amount': None,
               'man_amount': 1,
               'check_in_day': None,
               'days_amount': 1
               }
    :param methods:
    :return:
    """
    if not methods['check_in_day']:
        check_in_day = datetime.date.today() + datetime.timedelta(1)
        day = f'{check_in_day.day}/{check_in_day.month}'
    else:
        day = methods['check_in_day']

    msg = ["Метод поиска: {};".format(identify_method(methods['method'])),
           "Город: {};".format(methods['city_name']),
           "Количество людей: {};".format(methods['man_amount']),
           "Дата заселения: {};".format(day),
           "Количество ночей: {};".format(methods['days_amount']),
           "Количество ответов: {};".format(methods['answer_amount']),
           "Количество фотографий: {}.".format(methods['photo_amount'])]
    if identify_method(methods['method']) == 'best_deal':
        add_msg = ["Расстояние от центра: {};".format(' - '.join(methods['method'][1])),
                   "Ценовой диапазон: {};".format(' - '.join(methods['method'][0]))]
        for record in add_msg:
            msg.insert(4, record)

    text = '\n'.join(msg)
    return text

if __name__ == '__main__':
    some_method = {'method': 'low', 'id_city': '601763', 'answer_amount': '3', 'photo_amount': 0, 'man_amount': 1, 'check_in_day': None, 'days_amount': 1, 'city_name': 'Берлингтон, Вермонт, США'}
    print(reply_decoder(some_method))
