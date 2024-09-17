import json
import requests

from config_data import config


def hotel_address(json_response):
    return json_response['data']['propertyInfo']['summary']['location']['address']['addressLine']


def hotel_photos(json_response, amount_photo):
    photo_lib = json_response['data']['propertyInfo']['propertyGallery']['images']
    i_photo = 0
    photo_gallery = list()
    while i_photo < amount_photo and i_photo < len(photo_lib):
        photo_url = photo_lib[i_photo]['image']['url']
        photo_gallery.append(photo_url)
        i_photo += 1
    return photo_gallery


def hotel_address_and_photo_from_api(hotel_id, amount_photo, headers):
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    payload = {"locale": "ru_RU", "propertyId": hotel_id}
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    if response.status_code == 200:
        hotel_json = json.loads(response.text)
        hotel_info = dict()
        hotel_info['address'] = hotel_address(hotel_json)
        hotel_info['photo'] = hotel_photos(hotel_json, amount_photo)
        return hotel_info
    else:
        return None

API_key = config.RAPID_API_KEY
headers = {"X-RapidAPI-Key": API_key, "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

if __name__ == '__main__':
    hotel_id = '91716654'
    amount_photo = 3
    hotel_info = hotel_address_and_photo_from_api(hotel_id, amount_photo, headers)
    print(hotel_info)

