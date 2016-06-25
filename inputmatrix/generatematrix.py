try:
    import json
except ImportError:
    import simplejson as json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import string
from pprint import pprint


matrix = {}

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

def genMatrix(filenames):
	global matrix
	for file in filenames:
		matrix[file]=[]

def get_features(config, txtfile, words, jd):
	row = extractfeaturescore_words(config,txtfile,words)
	row = extractfeaturescore_jd(config, txtfile, jd, row)
	row = extractfeaturescore_companies(config,row)
	return row

def update_matrix(config,features, txtfile):
	global matrix
	matrix[txtfile] = features
	return

def process_txts(config, words, jd):
	filenames = []
	try:
		File = open(config['txts_filename'],'r')
		filenames = File.read().split('\n')
		genMatrix(filenames)
		if len(filenames)>0:
			for txtfile in filenames:
				# print(txtfile)
				features = get_features(config, txtfile, words, jd)
				# print([features[fat] for fat in features])
				update_matrix(config, features, txtfile)
			print('** all files processed **')
		else:
			print('** no txt files in txts_filename **')
	except Exception as e:
		print('** ads file error **\n'+str(e))
	else:
		File.close()
		return filenames

def getwords(config):
	words = {}
	try:
		File = open(config["words"],'r')
		words = json.load(File)
	except Exception as e:
		print(str(e))
	else:
		File.close()
	return words

def getjds(config):
	jds =[]
	for jd in config["jds"]:
		try:
			File = open(jd,'r')
			jds.append(json.load(File))
		except Exception as e:
			print("hi "+str(e))
		else:
			File.close()
	return jds

def extractfeaturescore_words(config,txtfile,words):
	row = {}
	File = open(config['txts_folder']+txtfile , 'r')
	txt = File.read()
	# print(config['txts_folder']+txtfile)
	punctuation = list(string.punctuation)
	stop_words = set(stopwords.words('english') + punctuation)
	word_tokens = word_tokenize(txt)
	filtered_txt = [w for w in word_tokens if not w in stop_words]
	# print(filtered_txt)
	for cat in words:
		acc = 0
		for word in words[cat]:
			if word in filtered_txt:
				acc +=1
		row[cat] = acc
	return row

def extractfeaturescore_jd(config, txtfile, jd, row):
	File = open(config['txts_folder']+txtfile , 'r')
	txt = File.read()
	# print(config['txts_folder']+txtfile)
	punctuation = list(string.punctuation)
	stop_words = set(stopwords.words('english') + punctuation)
	sents = sent_tokenize(txt)
	jddict ={}
	word_tokens = word_tokenize(jd["c_feature"])
	c_feature = [w for w in word_tokens if not w in stop_words]
	jddict['c_feature'] = c_feature
	# print([w for w in jd])
	word_tokens = word_tokenize(jd["Technical"])
	Technical = [w for w in word_tokens if not w in stop_words]
	jddict['Technical'] = Technical
	word_tokens = word_tokenize(jd["Role"])
	Role = [w for w in word_tokens if not w in stop_words]
	jddict['Role'] = Role
	# print(jddict)
	c_count = 0
	r_count = 0
	t_count = 0
	for sent in sents:
		words = word_tokenize(sent)
		for word in words:
			for wrd in jddict['c_feature']:
				if wrd == word:
					c_count +=1
			for wrd in jddict['Role']:
				if wrd == word:
					r_count +=1
			for wrd in jddict['Technical']:
				if wrd == word:
					t_count +=1				
	# print((c_count,r_count,t_count))
	row['c_count'] = c_count
	row['r_count'] = r_count
	row['t_count'] = t_count
	return row

config = get_config('config.json')
words = getwords(config)
jds = getjds(config)
# print(words)
# pprint(jds)
filenames = process_txts(config,words,jds[0])

count = 0
for file in matrix:
	if count ==0:
		print([tag for tag in matrix[file]])
	print([matrix[file][tag] for tag in matrix[file]])
	count+=1

print(count+1)












