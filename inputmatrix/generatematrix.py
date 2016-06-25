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

def getwords(config):
	words = {}
	try:
		File = open(config["words"],'r')
		words = json.load(File)
	except Exception as e:
		print("config catch : "+str(e))
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
			print("jds catch : "+str(e))
		else:
			File.close()
	return jds

def process_txts(config, words, jd):
	filenames = []
	try:
		File = open(config['txts_filename'],'r')
		filenames = File.read().split('\n')
		genMatrix(filenames)
		if len(filenames)>0:	
			for txtfile in filenames:
				# print(config['txts_folder']+txtfile)
				# print(txt)
				features = get_features(config, txtfile, words, jd)
				# print([features[fat] for fat in features])
				update_matrix(config, features, txtfile)
				
			print('** all files processed **')
		else:
			print('** no txt files in txts_filename **')
	except Exception as e:
		print('** Process catch **'+str(e))
		# print(e.)
	else:
		File.close()
		return filenames

def get_features(config, txtfile, words, jd):
	row = {}
	row = extractfeaturescore_words(config,txtfile,words, row)
	row = extractfeaturescore_jd(config, txtfile, jd, row)
	# row = extractfeaturescore_companies(config,row)
	return row

def extractfeaturescore_words(config,txtfile,words, row):
	File = open(config['txts_folder']+txtfile,'r')
	txt = File.read()
	File.close()
	# print(config['txts_folder']+txtfile)
	punctuation = list(string.punctuation)
	stop_words = set(stopwords.words('english') + punctuation)
	word_tokens = []

	try:
		word_tokens = word_tokenize(txt.decode('utf-8'))
	except Exception as e:
		print("\n\n"+txtfile+" and error: "+str(e))

	filtered_txt = [w for w in word_tokens if not w in stop_words]
	# print(filtered_txt)
	for cat in words:
		acc = 0
		for word in words[cat]:
			if word in filtered_txt:
				acc +=1
		row[cat] = acc
	return row

def wordtokenize(jd):
	word_tokens = []
	try:
		word_tokens = word_tokenize(jd)
	except Exception as e:
		print("\n\n"+txtfile+" jd c ++++++ and error: "+str(e))
	return word_tokens

def senttokenize(txt):
	sents = []
	try:
		sents = sent_tokenize(txt)
	except Exception as e:
		print("\n\n"+txtfile+" sents ****** and error: "+str(e))
	return sents

def counter(jddict, word):
	count = 0
	for wrd in jddict:
				if wrd == word:
					count +=1
	return count

def extractfeaturescore_jd(config, txtfile, jd, row):
	File = open(config['txts_folder']+txtfile,'r')
	txt = File.read()
	File.close()

	punctuation = list(string.punctuation)
	stop_words = set(stopwords.words('english') + punctuation)
	
	sents = []
	sents = senttokenize(txt.decode('utf-8'))

	word_tokens = []
	jddict ={}

	word_tokens = wordtokenize(jd["c_feature"])
	c_feature = [w for w in word_tokens if not w in stop_words]
	jddict['c_feature'] = c_feature

	word_tokens = wordtokenize(jd["Technical"])
	Technical = [w for w in word_tokens if not w in stop_words]
	jddict['Technical'] = Technical

	word_tokens = wordtokenize(jd["Role"])
	Role = [w for w in word_tokens if not w in stop_words]
	jddict['Role'] = Role

	c_count = 0
	r_count = 0
	t_count = 0
	for sent in sents:
		words = word_tokenize(sent)
		for word in words:
			c_count += counter(jddict['c_feature'], word)
			r_count += counter(jddict['Role'], word)
			t_count += counter(jddict['Technical'], word)

	row['c_count'] = c_count
	row['r_count'] = r_count
	row['t_count'] = t_count
	return row

def extractfeaturescore_companies(config, txtfile, row):
	companies = []
	words = []
	with open(config['companies'], 'r') as f:
		for line in f:
			for word in line.split():
				companies.append(word.lower())

	file = open(config['txts_folder']+txtfile, 'r')
	text = file.read().lower()
	file.close()
	text = re.sub('[^a-z\ \']+', " ", text)
	words = list(text.split())

	cmpscore = 0.0
	cmplen = len(companies)
	for i in range(cmplen):
		if companies[i] in words:
			print(companies[i])
			cmpscore += cmplen-i+1
			print(cmplen-i+1)
	row['cmp_score'] = cmpscore/cmplen
	return row

def genMatrix(filenames):
	global matrix
	for file in filenames:
		matrix[file]=[]

def update_matrix(config,features, txtfile):
	global matrix
	matrix[txtfile] = features
	return

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

# print(count+1)












