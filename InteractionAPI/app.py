from flask import Flask, json, request
import os
import subprocess
import threading 

app = Flask(__name__)


@app.route('/run_script', methods=['POST'])
def run_script():
	def start(name):
		print(os.getcwd())
		working_dir = "/home/ollie/Documents/pi-automations/"
		#working_dir = "/home/pi/pi-automations/"
		command_to_trigger = f"cd {working_dir} && python3 -c 'from notification_engine import {name}; {name}()'"
		subprocess.run(str(command_to_trigger))

	try:
		script_name = request.args.get('name')
		errors = False
	except Exception as e:
		errors = True

	if errors is not True:
		try:
			thread = threading.Thread(target=start, args=(script_name,))
			thread.start()
			return "success"
		except Exception as e:
			return e
	else:
		return e



@app.route('/', methods=['GET'])
def check_status():

	return """Service is running..."""


def run(app):
	app.run(host="0.0.0.0", port="4000")


if __name__ == "__main__":
	run(app)

