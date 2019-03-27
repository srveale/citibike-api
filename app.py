from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import json_util
import json

import generate_data

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017", connect=False)
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
	station_id = int(request.args.get('stationid', default=72))
	two_hours_ago = datetime.now() - timedelta(hours=6)

	recent_data = list(db.logs.find({
		"executionTime": { '$gte': two_hours_ago },
		"id": station_id
	}))

	for i, log in enumerate(recent_data):
		recent_data[i]['_id'] = str(recent_data[i]['_id'])

	return jsonify(recent_data)

@app.route('/hourly-averages')
def get_hourly_averages():
	station_id = int(request.args.get('stationid', default=72))

	hourly_averages = list(db.hourly_averages.find({ "id": station_id }))

	for i, log in enumerate(hourly_averages):
		hourly_averages[i]['_id'] = str(hourly_averages[i]['_id'])

	return jsonify(hourly_averages)

if __name__ == "__main__":
   app.run()

