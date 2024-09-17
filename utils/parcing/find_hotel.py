import json
import requests
import datetime

from config_data import config
from utils.parcing.hotel_payload import basic_payload_maker
from utils.parcing.hotel_payload import payload_result_scrolling
from utils.parcing.API_error import APIError
from utils.parcing.hotel_info import hotel_address_and_photo_from_api


def price_range(_json_response):
    # возвращает словарь  {'__typename': 'PriceRange', 'max': 106.25, 'min': 55.89}
    return _json_response['data']['propertySearch']['filterMetadata']['priceRange']


def hotel_lib_from_api(_json_response):
    def miles_to_kilometers(miles):
        return round(miles * 1.61, 2)

    hotels = list()
    # for i_hotel in range(i_start, i_finish):
    #     hotel = _json_response['data']['propertySearch']['properties'][i_hotel]
    for hotel in _json_response['data']['propertySearch']['properties']:
        hotel_info = dict()
        hotel_info['name'] = hotel['name']
        hotel_info['distance'] = hotel['destinationInfo']['distanceFromDestination']['value']
        if hotel['destinationInfo']['distanceFromDestination']['unit'] == 'MILE':
            hotel_info['distance'] = miles_to_kilometers(hotel_info['distance'])
        try:
            hotel_info['price'] = hotel['price']['displayMessages'][0]['lineItems'][1]['price']['formatted']
        except (IndexError, TypeError):
            # hotel_info['price'] = hotel['price']['displayMessages'][0]['lineItems'][0]['price']['formatted']
            hotel_info['price'] = f"Undefined {hotel['id']}"
            continue
        try:
            hotel_info['total_price'] = hotel['price']['displayMessages'][1]['lineItems'][0]['value']
        except (IndexError, TypeError):
            hotel_info['total_price'] = f"Undefined {hotel['id']}"
            continue
        hotel_info['id'] = hotel['id']
        # address_and_photo = hotel_address_and_photo_from_api(hotel['id'], amount_photo, _headers)
        # if address_and_photo:
        #     hotel_info.update(address_and_photo)
        hotels.append(hotel_info)
    return hotels


def hotel_distance_filter(_hotel_list, distance_range):
    filtered_list = list()
    count = 0
    for hotel in _hotel_list:
        count += 1
        if float(distance_range[0]) < float(hotel['distance']) < float(distance_range[1]):
            filtered_list.append(hotel)
    return filtered_list


# city_id = '2058'
# API_key = config.RAPID_API_KEY
# url = "https://hotels4.p.rapidapi.com/properties/v2/list"
# check_in_date = datetime.date(2023, 5, 15)
# check_out_date = datetime.date(2023, 5, 16)
# method = 'low'
# headers = {"X-RapidAPI-Key": API_key, "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}


def hotel_search(_method, _city_id, _check_in_date, _check_out_date, _people_amount, _headers):
    _url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    hotels = list()

    def find_method(_method, people_amount):
        if isinstance(_method, list):
            _new_method = {"best_deal": _method[0]}
        else:
            if _method == "high":
                price_for_high = [200 * people_amount, 10000 * people_amount]
                _new_method = {"high": price_for_high}
            else:
                _new_method = {"low"}
        return _new_method

    def best_deal_hotel_lib(_json_response, _method, payload):
        distance_range = _method[1]
        hotels_lib = hotel_lib_from_api(_json_response)
        best_deal_hotels = hotel_distance_filter(hotels_lib, distance_range)
        while (len(best_deal_hotels) < 100 and
               len(hotels_lib) > 199 and
               float(hotels_lib[199]['distance']) < float(distance_range[1])):
            best_deal_payload = payload_result_scrolling(payload)
            new_response = requests.post(_url, json=best_deal_payload, headers=_headers, timeout=10)
            if new_response.status_code == 200:
                json_response = json.loads(new_response.text)
                hotels_lib = hotel_lib_from_api(json_response)
                new_best_deal_hotels = hotel_distance_filter(hotels_lib, distance_range)
                best_deal_hotels.extend(new_best_deal_hotels)
            else:
                raise APIError
        return best_deal_hotels

    def high_price_hotel_lib(_json_response, _method, payload):
        high_price_range = price_range(_json_response)
        max_price = int(high_price_range['max'] * 5)
        payload['filters']['price']['max'] = int(max_price)
        min_price = int(int(high_price_range['max'] / 3))
        hotels_lib = hotel_lib_from_api(_json_response)
        while not (100 < len(hotels_lib) < 199):
            if len(hotels_lib) < 100:
                payload['filters']['price']['min'] = int(min_price / 2)
            elif len(hotels_lib) > 199:
                payload['filters']['price']['min'] = int(min_price * 1.5)
            # print(payload['filters']['price']['max'], payload['filters']['price']['min'])
            new_response = requests.post(_url, json=payload, headers=_headers, timeout=10)
            if new_response.status_code == 200:
                json_response = json.loads(new_response.text)
                hotels_lib = hotel_lib_from_api(json_response)
                # print(len(hotels_lib))
                high_price_range = price_range(json_response)
                min_price = high_price_range['min']
            else:
                raise APIError
        rev_hotels_lib = list(reversed(hotels_lib))
        return rev_hotels_lib

    new_method = find_method(_method, _people_amount)
    _payload = basic_payload_maker(_city_id, _check_in_date, _check_out_date,
                                                 _people_amount, method=new_method)
    response = requests.post(_url, json=_payload, headers=_headers, timeout=10)
    if response.status_code == 200:
        json_response = json.loads(response.text)
        # hotels_lib = hotel_lib_from_api(_json_response)
        if "low" in new_method:
            hotels = hotel_lib_from_api(json_response)
        elif "best_deal" in new_method:
            hotels = best_deal_hotel_lib(json_response, _method=_method, payload=_payload)
        elif "high" in new_method:
            hotels = high_price_hotel_lib(json_response, _method=new_method, payload=_payload)
    else:
        raise APIError
    return hotels


def one_hotel_info_extender(hotel_id, amount_photo, headers):
    hotel_info = hotel_address_and_photo_from_api(hotel_id, amount_photo, headers)
    return hotel_info


def bot_answer_json(check_in_date, check_out_date, people_amount, method, city_id, answer_amount, photo_amount,
                    headers):
    answer = list()
    hotels_lib = hotel_search(method, city_id, check_in_date, check_out_date, people_amount, headers)
    if len(hotels_lib) > 0:
        for i in range(answer_amount):
            hotel_id = hotels_lib[i]['id']
            address_info = one_hotel_info_extender(hotel_id, photo_amount, headers)
            hotels_lib[i].update(address_info)
            answer.append(hotels_lib[i])
    return answer


if __name__ == "__main__":

    def print_hotel(method):
        hotels = hotel_search(method, city_id, check_in_date, check_out_date, people_amount, headers)
        for hotel in hotels:
            print(hotel)
        print()
        print(len(hotels))


    city_id = '2058'
    API_key = config.RAPID_API_KEY
    # url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    check_in_date = datetime.date(2023, 5, 15)
    check_out_date = datetime.date(2023, 5, 16)
    people_amount = 3
    answer_amount = 5
    amount_photo = 3
    headers = {"X-RapidAPI-Key": API_key, "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
    method = 'low'
    # print(method)
    # print_hotel(method)
    # print('=' * 150)
    my_answer = bot_answer_json(check_in_date, check_out_date, people_amount, method, city_id, answer_amount,
                            amount_photo, headers)
    print(my_answer)
