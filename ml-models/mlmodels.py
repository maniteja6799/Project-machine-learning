# import sklearn
from sklearn.naive_bayes import GaussianNB
import numpy as np
import json
import random

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

def get_target(config, len):
	tar = []
	for i in range(len):
		tar.append(random.randint(0,1))
	return	tar

config = get_config('config.json')
matrix = get_matrix(config)
features = list()
count = 0
for file in matrix:
	# if count ==0:
	# 	print([tag for tag in matrix[file]])
	# print([matrix[file][tag] for tag in matrix[file]])
	features.append([matrix[file][tag] for tag in matrix[file]])
	count+=1

target = get_target(config, len(features))
# print(target)
# print(len(features))

array_features = np.array(features)
classifier  =  GaussianNB()
model = classifier.fit(array_features,target)
output_target = model.predict(array_features)
c = 0
for i in range(len(target)):
	if(target[i] == output_target[i]):
		c+=1
print(c,len(target))




















