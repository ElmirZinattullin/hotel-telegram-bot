def hotel_info_decoder(hotel_info: dict) -> dict:
    """
    Функция преобразующая информацию об отеле с json формата в строку с наглядным выводом
    :param hotel_info: Информация об отеле в надлежащем формате словаря с ключами
    {'name': 'str', 'distance': str, 'price': 'str', 'total_price': 'str', 'id': 'str', 'address': 'str',
    'photo': [str, ... , str]}
    :return: str
    """

    photo_list = hotel_info['photo']
    hotel_info = "Название отеля: {0}. \n" \
                 "Адрес: {1}\n" \
                 "Расстояние от центра: {2}, км\n" \
                 "Цена за ночь: {3}. Итоговая цена с учетом сборов: {4}.".format(hotel_info['name'],
                                                                                 hotel_info['address'],
                                                                                 hotel_info['distance'],
                                                                                 hotel_info['price'],
                                                                                hotel_info['total_price'])
    hotel_info_dict = {'hotel_info': hotel_info, 'photo': photo_list}
    return hotel_info_dict
