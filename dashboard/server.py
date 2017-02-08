import os
from collections import deque
import csv
from datetime import datetime
from datetime import timedelta
from flask import Flask, url_for, send_from_directory, Response
from flask.json import jsonify
import pandas as pd

app = Flask(__name__, static_folder='static')

@app.route('/')
def root():
	return read_file('static/index.html')


@app.route('/api/currentTemperature')
def current_temperature():
	data = pd.read_csv('../data/temperature.csv', parse_dates=True, index_col='date')
	return str(data.tail(1).iloc[0][0])


@app.route('/api/temperature/<int:days_time_range>/<resolution>')
def get_temperature(days_time_range = 7, resolution = ''):
	return get_data_from_file('../data/temperature.csv', days_time_range, resolution)


@app.route('/api/humidity/<int:days_time_range>/<resolution>')
def get_humidity(days_time_range = 7, resolution = ''):
	return get_data_from_file('../data/humidity.csv', days_time_range, resolution)


@app.route('/api/pressure/<int:days_time_range>/<resolution>')
def get_pressure(days_time_range = 7, resolution = ''):
	return get_data_from_file('../data/pressure.csv', days_time_range, resolution)


def read_file(file_name):
	content = ''
	with open(file_name, 'r') as csv_file:
		content = csv_file.read()
	return content


def get_data_from_file(file_name, days_time_range = 0, sampling =''):
	time_range_start = datetime.min
	if days_time_range > 0:
		time_range_start = datetime.now() - timedelta(days=days_time_range)

	data = pd.read_csv(file_name, parse_dates=True, index_col='date')

	# Filter out entries older than desired range
	data = data[data.index >= time_range_start]

	# Resample the data
	if sampling != '':
		data = data.resample(sampling).mean()

	return data.to_csv()


def get_data_from_file2(file_name, days_time_range = 0, resolution=0):
	with open(file_name, 'r') as csv_file:
		result = ''

		time_range_start = datetime.min
		if days_time_range > 0:
			time_range_start = datetime.now() - timedelta(days=days_time_range)

		reader = csv.reader(csv_file, delimiter=',')

		for row in reader:
			if result == '':
				result += ', '.join(row) + '\n'
			else:
				timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')

				if timestamp >= time_range_start:
					result += ', '.join(row) + '\n'

		print('Responded with {0} items.'.format(len(result.split('\n')) -1))
		return result

if __name__ == '__main__':
	app.run()