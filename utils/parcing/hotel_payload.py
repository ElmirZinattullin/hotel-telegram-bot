import datetime


def basic_payload_maker(city_id, check_in_day: datetime, check_out_day: datetime, man_amount, method=None):

    def low_price():
        low_price_payload = {
            "sort": "PRICE_LOW_TO_HIGH",
            "filters": {}
        }
        return low_price_payload

    def best_deal(_price_range):
        best_deal_payload = {
            "sort": "DISTANCE",
            "filters": {"price": {"max": max(_price_range), "min": min(_price_range)}}
        }
        return best_deal_payload

    def price_range_search(_price_range):
        price_range_payload = {
            "sort": "PRICE_LOW_TO_HIGH",
            "filters": {"price": {"max": max(_price_range), "min": min(_price_range)}}
        }
        return price_range_payload

    def determine_method(_method):
        if "best_deal" in _method:
            return best_deal(_method["best_deal"])
        elif "low" in _method:
            return low_price()
        elif "high" in _method:
            return price_range_search(_method["high"])
        else:
            raise ValueError('В методе high не указана ценовой диапазон price_range: list[int]')

    _payload = {"currency": "USD",
                "eapid": 1,
                "locale": "ru_RU",
                "siteId": 300000001,
                "destination": {"regionId": city_id},
                "checkInDate": {"day": check_in_day.day,
                                "month": check_in_day.month,
                                "year": check_in_day.year},
                "checkOutDate":
                               {"day": check_out_day.day,
                                "month": check_out_day.month,
                                "year": check_out_day.year},
                "rooms": [{"adults": man_amount, "children": []}],
                "resultsStartingIndex": 0,
                "resultsSize": 200}
    method_payload = determine_method(method)
    _payload.update(method_payload)
    return _payload

def payload_result_scrolling(_payload):
    _payload["resultsStartingIndex"] += _payload['resultsSize']
    return _payload

if __name__ == '__main__':
    # payload = basic_payload_maker('2058', datetime.date(2023, 5, 15), datetime.date(2023, 5, 16), 2, {"best_deal":[
    #     10, 90]})
    # print(payload)
    # payload_low = basic_payload_maker('2058', datetime.date(2023, 5, 15), datetime.date(2023, 5, 16), 2,
    #                                   method={'low'})
    # print()
    # print(payload_low)
    payload_high = basic_payload_maker('2058', datetime.date(2023, 5, 15), datetime.date(2023, 5, 16), 2,
                                       method={'high':[10, 90]})
    print()
    print(payload_high)
    # print(payload_result_scrolling(payload_high))
    #payload = basic_payload_maker('2058', datetime.date(2023, 5, 15), datetime.date(2023, 5, 16), 2)
# payload = {"currency": "USD", "eapid": 1, "locale": "ru_RU", "siteId": 300000001,
#            "destination": {"regionId": city_id},
#            "checkInDate": {"day": 15, "month": 5, "year": 2023},
#            "checkOutDate": {"day": 16, "month": 5, "year": 2023},
#            "rooms": [{"adults": 2, "children": []}],
#            "resultsStartingIndex": 0,
#            "resultsSize": 200,
#            "sort": "PRICE_LOW_TO_HIGH",
#            "filters": {"price": {"max": 1000, "min": 1}}
#            }