try:
    import json
except ImportError:
    import simplejson as json


def get_config(configfile):
	configs = []
	try:
		File = open(configfile,'r')
		lines = File.readlines()
		if len(lines)>0:
			for line in lines:
				configs.append(json.loads(line))
			print('** appended jsons **')
		else:
			print('** no jsons **')
	except (FileNotFoundError, IOError):
		print('** file error **')
	finally:
		File.close()
	return configs[0]

def process_txts(config):
	try:
		File = open(config['txts_filename'],'r')
		filenames = File.readlines();
		if len(filenames)>0:
			for txtfile in filenames:
				print(txtfile)
				features = get_features(txtfile)
				update_matrix(features,txtfile)
			print('** all files processed **')
		else:
			print('** no txt files in txts_filename **')
	except (FileNotFoundError, IOError):
		print('** file error **')
	finally:
		File.close()
		return

def get_features(txtfile):
	return 'nothing'

def update_matrix(features,usertxtfile):
	return ''

config = get_config('config.txt')
process_txts(config)
