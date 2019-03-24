from flask import Flask, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import json_util
import json

import generate_data

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
db=client['citibike-realtime']

@app.route('/')
def hello_world():
	return 'Hello, World!'

## purely test, delete this
@app.route('/bike-data')
def get_data():
	data = generate_data.crazy_machine_learning_function()
	print('data', data)
	return jsonify(data)

@app.route('/recent-data')
def get_recent():
	alldata = db.logs.find({"stationName": "6 Ave & Canal St"})
	print(list(alldata))
	two_hours_ago = datetime.now() - timedelta(hours=10)
	print(two_hours_ago)
	start = datetime(2014, 9, 24, 7, 51, 4)

	recent_data = db.logs.find({"lastCommunicationTime": { '$lte': start }})
	# print('data', list(alldata))


	return jsonify(list(recent_data))


if __name__ == "__main__":
   app.run()
