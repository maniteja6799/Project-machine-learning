from flask import Flask, jsonify, abort, make_response, request
import sys
sys.path.insert(0, 'inputmatrix')
sys.path.insert(0, 'converters')
sys.path.insert(0, 'ml-models')
import generatematrix as gm
# import converter as cnv
import mlmodels as model

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

@app.route('/postresume', methods=['POST'])
def process_resume():
    if not request.json:
        abort(400)
    

    entity = [request.json['id'], request.json['name']]
    return jsonify({'entity': entity}), 201

def concert_to_text(file, filetype):
	txt = ''
	if filetype == 'docx':
		txt = cnv.docx_to_txt(file)
	if filetype == 'doc':
		txt = cnv.doc_to_txt(file)
	if filetype == 'pdf':
		txt = cnv.pdf_to_txt(file)
	return txt

def extractfeatures(txt):
	config = gm.get_config('config.json')
	words = gm.getwords(config)
	jds = gm.getjds(config)
	gm.getdetail(config)
	filenames = process_txts(config,words,jds[0])
	row = gm.get_features()
		
if __name__ == '__main__':
    app.run(debug=True)














