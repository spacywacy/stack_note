import json
import requests

#a bit hard to import this path from config
#hard coding for now
new_related_path = 'cache/new_related.json'


def post_new_items():
	#load new_related.json
	with open(new_related_path, 'r') as f:
		new_items = f.read()

	#call api
	re = requests.post('http://127.0.0.1:5000/merge', data={'new_items':new_items})
	print(re)
	print(re.json())

	#empty new_related.json
	if re.status_code == 200:
		new_items = {'header':{}, 'urls':{}, 'posts':[]}
		with open(new_related_path, 'w') as f:
			json.dump(new_items, f)


def check_new_items():
	with open(new_related_path, 'r') as f:
		new_items = json.load(f)
		print(new_items)



if __name__ == '__main__':
	post_new_items()

