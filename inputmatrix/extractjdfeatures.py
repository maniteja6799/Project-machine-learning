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
# import spacy
import parser

parser = parser.Parser()
tokens = "Set the volume to zero when I 'm in a meeting unless John 's school calls".split()
tags, heads = parser.parse(tokens)
print(heads)



def extractfeaturescore_jd_new(config, txtfile, jd, row):
	File = open(config['txts_folder']+txtfile,'r')
	txt = File.read()
	File.close()
	# print(config['txts_folder']+txtfile)
	punctuation = list(string.punctuation)
	stop_words = set(stopwords.words('english') + punctuation)
	sents = []
	word_tokens = []
	try:
		sents = sent_tokenize(txt.decode('utf-8'))
	except Exception as e:
		print("\n\n"+txtfile+" sents ****** and error: "+str(e))
	jddict ={}
	try:
		word_tokens = word_tokenize(jd["c_feature"])
	except Exception as e:
		print("\n\n"+txtfile+" jd c ++++++ and error: "+str(e))
	c_feature = [w for w in word_tokens if not w in stop_words]
	jddict['c_feature'] = c_feature
	# print([w for w in jd])
	try:
		word_tokens = word_tokenize(jd["Technical"])
	except Exception as e:
		print("\n\n"+txtfile+" jd t ++++++ and error: "+str(e))
	
	Technical = [w for w in word_tokens if not w in stop_words]
	jddict['Technical'] = Technical
	try:
		word_tokens = word_tokenize(jd["Role"])
	except Exception as e:
		print("\n\n"+txtfile+" jd r ++++++ and error: "+str(e))
	
	Role = [w for w in word_tokens if not w in stop_words]
	jddict['Role'] = Role
	# print(jddict)
	c_count = 0
	r_count = 0
	t_count = 0
	parser = spacy.parser.Parser()
	row['c_count'] = c_count
	row['r_count'] = r_count
	row['t_count'] = t_count
	return row
