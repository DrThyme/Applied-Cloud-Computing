#!flask/bin/python2
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

@app.route('/test1', methods=['GET'])
def windex():
	res = { 'x': 1,
			'y': 5,
			'z': 2}
	return jsonify(res), "hmmm"

@app.route('/test2', methods=['GET'])
def timedex():
	res = { 'x': 1,
			'y': 5,
			'z': 2}
	res2 = { 'x': 11,
			'y': 51,
			'z': 21}
	return jsonify(res)
	time.wait(5)
	return jsonify(res2)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
