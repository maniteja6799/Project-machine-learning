from flask import Flask, jsonify, abort, make_response, request
import sys
import json
sys.path.insert(0, 'inputmatrix')
sys.path.insert(0, 'converters')
sys.path.insert(0, 'ml-models')
import generatematrix as gm
# import converter as cnv
import mlmodels as ml
import numpy as np
import pickle

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def hello():
	return jsonify('hello')

@app.route('/genmat', methods=['GET'])
def get_tasks():
	arr = [[1, "jugal"] , [2, "mani"], [3, "roopali"], [4, "manika"], [5, "shivam"], [6, "divya"], [7, "bansari"], [8, "amit"]]
	print('yes1')
#	return jsonify(test())
	tt = gm.generatematrixanddump()
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

@app.route('/trainmodel', methods=['GET'])
def trainmodel():
	gm.generatematrixanddump()
	ml.train_nb()
	return jsonify({'status' : 'done'})

@app.route('/postresume', methods=['POST'])
def process_resume():
	if not request.json:
		abort(400)
	# resume = [request.json['id'], request.json['name']]
	# code to convert to txt 
	# ------ from here------

	# ------ to here ------
	# taking sample txt file from resources/temp/sample.txt
	# txtfile = request.json['txtfile']
	experience = request.json['experience']
	testscore = request.json['testscore']
	appliedfor = request.json['appliedfor']
	resume = {}
	resume['txtfile'] = 'sample.txt'
	resume['experience'] = experience
	resume['testscore'] = testscore
	resume['appliedfor'] = appliedfor
	config = gm.get_config('config.json')
	array_row = extractfeatures(config, resume)
	model = pickle.load(open(config['model_pickle'],"rb"))
	[op,prob] = ml.predict_one_row(model, array_row)
	cat = ''
	if op == 1:
		cat += 'java select'
	if op == 2:	
		cat+= 'android select'
	if op == 0:
		cat+= 'not select'		
	return jsonify({'class': cat, 'prob':prob[0]}), 201

def concert_to_text(file, filetype):
	txt = ''
	if filetype == 'docx':
		txt = cnv.docx_to_txt(file)
	if filetype == 'doc':
		txt = cnv.doc_to_txt(file)
	if filetype == 'pdf':
		txt = cnv.pdf_to_txt(file)
	return txt

def extractfeatures(config, resume):
	txtfile = resume['txtfile'] 
	experience = resume['experience']
	testscore = resume['testscore']
	appliedfor = resume['appliedfor']
	words = gm.getwords(config)
	jds = gm.getjds(config)
	row = {}
	row = gm.extractfeaturescore_words(config,config['sample']+txtfile, words, row)
	if appliedfor == 'java':
		row = gm.extractfeaturescore_jd(config, config['sample']+txtfile, jds[0], row)
	if appliedfor == 'android':
		row = gm.extractfeaturescore_jd(config, config['sample']+txtfile, jds[1], row)
	row = gm.extractfeaturescore_companies(config, config['sample']+txtfile, row)	
		
	row['experience'] = experience
	row['testscore'] = testscore
	file = open(config['tags_order'],'r')
	tags_order = json.load(file)
	file.close()
	array_row = np.array([row[tag] for tag in tags_order])
	return array_row

		
if __name__ == '__main__':
    app.run(debug=True)














