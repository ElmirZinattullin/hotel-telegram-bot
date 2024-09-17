import json
import requests


from config_data import config
from utils.parcing import API_error

API_key = config.RAPID_API_KEY
headers = {"X-RapidAPI-Key": API_key, "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}


def city_from_api_finder(name, _headers):
	url = "https://hotels4.p.rapidapi.com/locations/v3/search"
	querystring = {"q": name, "locale": "ru_RU"}
	response = requests.get(url, headers=headers, params=querystring, timeout=5)
	# print(response)
	if response.status_code == 200:
		city_lib = json.loads(response.text)['sr']
		select_city = dict()
		city_count = 0
		for city in city_lib:
			if city['type'] == 'CITY':
				city_count += 1
				city_info = {'id': city['gaiaId'], 'name': city['regionNames']['fullName']}
				select_city[city_count] = city_info
		return select_city
	else:
		raise API_error.APIError("Ошибка при запроса локации")

if __name__ == "__main__":
	city_name = "Берлин"
	cities = city_from_api_finder(city_name, _headers=headers)
	print(cities)