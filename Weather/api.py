# encoding=utf-8

import requests
import Weather.env_var as env_var
import json

headers = {}
payload = {}
city = "Berlin"
plz = "10317"
country_code = "DE"
token = env_var.token
base_url_current = f"https://api.openweathermap.org/data/2.5/weather?appid={token}&units=metric"
base_url_forecast = f"https://api.openweathermap.org/data/2.5/onecall?appid={token}&units=metric"
base_url_geocode = f"http://api.openweathermap.org/geo/1.0/zip?appid={token}"


## Functionality
def get_current_weather_by_city():
	url = base_url_current + f"&q={city},{country_code}"
	response_json = _send_request(url)
	return response_json


def get_current_weather_by_plz():
	url = base_url_current + f"&zip={plz},{country_code}"
	response_json = _send_request(url)
	return response_json


def get_forecast_weather(exclude_list):
	lat, lon = convert_lat_lon(plz, country_code)
	exclude_list = ",".join(exclude_list)
	url = base_url_forecast + f"&lat={str(lat)}&lon={str(lon)}&exclude={exclude_list}"
	response_json = _send_request(url)
	return response_json


## Coordinate Finder
def convert_lat_lon(plz, country_code):
	url = base_url_geocode + f"&zip={plz},{country_code}"
	try:
		response_json = _send_request(url)
		lat = response_json["lat"]
		lon = response_json["lon"]
	except Exception as e:
		lat = 52.5167
		lon = 13.4

	return lat, lon


## Workers
def _send_request(url, method="GET"):
	response = requests.request(method, url, data=payload, headers=headers)
	response_json = json.loads(response.text)
	return response_json

## Testing

def parse_alerts(response_json):
	try:
		alerts_title = response_json["alerts"]["event"]
		alerts_desc = response_json["alerts"]["description"]
		return alerts_title, alerts_desc
	except KeyError:
		return None, None


if __name__ == "__main__":
	
	response_json = get_forecast_weather(exclude_list=["current","daily"])
	x, y = parse_alerts(response_json)
	
