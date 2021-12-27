from flask import Flask, json

app = Flask(__name__)


@app.route('/run_script', methods=['POST'])
def run_script():
	try:
		script_name = request.args.get('name')
		errors = False
		return errors, script_name
	except Exception as e:
		errors = True
		return errors, e


@app.route('/', methods=['GET'])
def check_status():

	return """Service is running..."""


def run(app):
	app.run(host="0.0.0.0", port="4000")


if __name__ == "__main__":
	run(app)

