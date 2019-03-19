from flask import Flask, jsonify
import generate_data
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/bike-data')
def get_data():
	data = generate_data.crazy_machine_learning_function()
	print('data', data)
	return jsonify(data)
