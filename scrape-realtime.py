import requests
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db=client['citibike-realtime']

##
## Get data from API
##
def get_data():
	req = requests.get("https://feeds.citibikenyc.com/stations/stations.json")

	req_json = req.json()

	## Times are in NYC timezone
	req_json['executionTime'] = datetime.strptime(req_json['executionTime'], '%Y-%m-%d %I:%M:%S %p')
	return req_json

##
## Store data in Mongo
##
def store_data(req_json):
	for log in req_json['stationBeanList']:
		log['executionTime'] = req_json['executionTime']
		db.logs.insert(log)


req_data = get_data()
store_data(req_data)