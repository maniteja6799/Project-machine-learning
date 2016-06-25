#!/usr/bin/env python
from flask import Flask, jsonify, abort, make_response, request

import sys
sys.path.insert(0, 'inputmatrix')
from generatematrix import test

app = Flask(__name__)

@app.route('/entity', methods=['GET'])
def get_tasks():
	arr = [[1, "jugal"] , [2, "mani"], [3, "roopali"], [4, "manika"], [5, "shivam"], [6, "divya"], [7, "bansari"], [8, "amit"]]
	print('yes1')
#	return jsonify(test())
	tt = test()
	return jsonify(tt)

@app.route('/entity/<int:entity_id>', methods=['GET'])
def get_task(entity_id):
	arr = [[1, "jugal"] , [2, "mani"], [3, "roopali"], [4, "manika"], [5, "shivam"], [6, "divya"], [7, "bansari"], [8, "amit"]]
	entity = [0, ""]
	for e in arr:
		if e[0] == entity_id:
			entity = e
	return jsonify({'entity' : entity})

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/entity', methods=['POST'])
def create_task():
    if not request.json:
        abort(400)
    entity = [request.json['id'], request.json['name']]
    return jsonify({'entity': entity}), 201

if __name__ == '__main__':
    app.run(debug=True)
