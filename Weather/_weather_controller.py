# encoding=utf-8

import requests
import env_var

headers = {}
payload = {}
city = "Berlin"
plz = "10317"
country_code = "DE"
token = env_var.token
base_url_current = f"https://api.openweathermap.org/data/2.5/weather?appid={token}&units=metric"
base_url_forecast = f"https://api.openweathermap.org/data/2.5/onecall?appid={token}&units=metric"
base_url_geocode = f"http://api.openweatehermap.org/geo/1.0/zip?appid={token}"


## Functionality
def get_current_weather_by_city():
	url = base_url_current + f"&q={city},{country_code}"
	response = _send_request(url)
	print(response.text)


def get_current_weather_by_plz():
	url = base_url_current + f"&zip={plz},{country_code}"
	response = _send_request(url)
	print(response.text)


def get_forecast_weather(exclude_list):
	lat, lon = convert_lat_lon(plz, country_code)
	exclude_list = ",".join(exclude_list)
	url = base_url_forecast + f"&lat={str(lat)}&lon={str(lon)}&exclude={exclude_list}"
	response = _send_request(url)
	print(response.text)



## Workers
def _send_request(url, method="GET"):
	response = requests.request(method, url, data=payload, headers=headers)
	return response


def convert_lat_lon(plz, country_code):
	url = base_url_geocode + f"&zip={plz},{country_code}"
	try:
		response = _send_request(url)
		response_json = json.loads(response.text)
		lat = response.text["lat"]
		lon = response.text["lon"]
	except:
		print("Fallback: using Berlin...")
		lat = 52.5167
		lon = 13.4

	return lat, lon


def parse_alerts(response_json):
	if response_json["alerts"] is not None:
		alerts_title = response_json["alerts"]["event"]
		alerts_desc = response_json["alerts"]["description"]
		return alerts_title, alerts_desc
	else:
		return None, None


if __name__ == "__main__":
	#get_current_weather_by_plz()
	#convert_lat_long(plz, country_code)
	get_forecast_weather(exclude_list=["daily","minutely"])
