# encoding = utf-8

import datetime
import requests
from env_var import token

base_url = "https://api.pushbullet.com/v2/"
headers = { 
"Access-Token" : "o.emUWVWsr7wyqmyJzbVFoKiOM6Sqa8PYw"
}
payload =  {}

## Requests
def get_current_user():
	url = base_url + "users/me"
	response = _send_request(url)
	print(response.text)


def get_current_devices():
	url = base_url + "devices"
	response = _send_request(url)
	print(response.text)


def create_push():
	url = base_url + "pushes"
	create_push_payload = {
		"active": True,
		"body": "test",
		"created": datetime.datetime.now().strftime(format="%Y-%m-%d %H:%M:%s"),
		"title": "Title",
		"type": "note"
	}
	response = _send_request(url, payload=create_push_payload, method="POST")
	print(response.text)


def get_pushes():
	url = base_url + "pushes"
	response = _send_request(url)
	print(response.text)


## Functionality
def _send_request(url, method="GET", headers=headers, payload=payload):
	response = requests.request(method, url, headers=headers, data=payload)
	return response


if __name__ == "__main__":
	#get_current_user()
	#get_current_devices()
	#create_push()
	get_pushes()
