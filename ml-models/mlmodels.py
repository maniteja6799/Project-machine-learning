# import sklearn
from sklearn.naive_bayes import GaussianNB
import numpy as np
import json
import random
import re
import string
import pickle

def get_config(configfile):
	config = []
	try:
		File = open(configfile,'r')
		config = json.load(File)
	except Exception as e:
		print(str(e))
	else:
		File.close()
	return config

def get_matrix(config):
	matrix = {}
	try:
		File = open(config['matrix'],'r')
		matrix = json.load(File)
	except Exception as e:
		print(str(e))
	else:
		File.close()
	return matrix


def get_feature_array(matrix):
	features = []
	tags_order = []
	count = 0
	for file in matrix:
		# if count ==0:
		# 	print([tag for tag in matrix[file]])
		# print([matrix[file][tag] for tag in matrix[file]])
		f = []
		for tag in matrix[file]:
			if tag != 'target':
				if count == 0:
					tags_order.append(tag)
				f.append(matrix[file][tag])
		if len(f) == 16:
			features.append((f,matrix[file]['target']))
		count+=1
	return(features,tags_order)	

def trainandfit_NB(array_features,target):
	classifier  =  GaussianNB()
	model = classifier.fit(array_features,target)
	return model

def predictandanalyse(model,test_features,target):
	output_target = model.predict_proba(test_features)
	c = 0
	# for i in range(len(target)):
	# 	if(target[i] == output_target[i]):
	# 		c+=1
	# print(c,len(target))
	print(output_target)
	return 

def predict_one_row(model, row):
	op = model.predict(row.reshape(1,-1))
	prob = model.predict_proba(row.reshape(1,-1))[0][op]
	return[op,prob] 

def train_nb():
	global matrix
	config = get_config('config.json')
	matrix = get_matrix(config)
	tmp = get_feature_array(matrix)
	features = tmp[0]
	tags_order = tmp[1]
	file = open(config['tags_order'],'w')
	json.dump(tags_order,file)
	file.close()

	array_features = np.array([f[0] for f in features])
	target = [f[1] for f in features]
	# print(array_features)
	# for f in matrix:
	# 	if 'experience' in matrix[f].keys():
	# 		print(matrix[f]['experience'],f)
	# 	else:
	# 		print('no exp ',f)	
	# print(target)
	# print(array_features)
	# print(len(array_features),len(array_features[1]))
	naive_bayes_model = trainandfit_NB(array_features, target)
	pickle.dump(naive_bayes_model, open(config['model_pickle'], "wb"))
	return (naive_bayes_model, array_features, target)


# (model, array_features, target) = train_nb()	
# predictandanalyse(model, array_features[2].reshape(1,-1), target)




















