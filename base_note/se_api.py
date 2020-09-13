import sys
sys.path.append('../')

import os
import requests
import json
from time import sleep
from datetime import datetime
import utils
from bs4 import BeautifulSoup


def call_api(url, params, raw=False):
	res = requests.get(url, params=params)
	url_obj = res.content.decode('utf-8')
	if raw:
		return url_obj
	else:
		try:
			return json.loads(url_obj)['items']
		except:
			print(url_obj)


def cache_sites(se_sites_path, api_key):
	url = 'https://api.stackexchange.com/2.2/sites'
	params = {'pagesize':100}
	json_items = call_api(url, params)
	sites = []
	for item in json_items:
		api_name = item.get('api_site_parameter')
		sites.append(api_name)
	utils.pickle_dump(se_sites_path, sites)
	print('cached se site list to file')


def get_acct_id(inname, se_sites_path, api_key):
	se_sites = utils.pickle_load(se_sites_path)
	for site in se_sites:
		url = 'https://api.stackexchange.com/2.2/users'
		params = {
			'order':'desc',
			'sort':'name',
			'site':site,
			'key':api_key,
			'inname':inname
		}
		json_items = call_api(url, params)

		if json_items:
			for item in json_items:
				if inname == item.get('display_name'):
					return item.get('account_id')


def get_site_uids(acct_id, api_key):
	'''given a inname, find all associated sites and corresponding user_ids'''
	url = 'https://api.stackexchange.com/2.2/users/{}/associated'.format(acct_id)
	params = {}
	json_items = call_api(url, params)
	site_uids = []
	for item in json_items:
		user_id = item.get('user_id')
		site_url = item.get('site_url')
		site_name = site_url.split('//')[1].split('.')[0]
		site_uids.append((site_name, user_id))

	return site_uids


def get_fav_ques(site_uids, api_key):
	favs = []
	for site, user_id in site_uids:

		#api call
		url = 'https://api.stackexchange.com/2.2/users/{}/favorites'.format(user_id)
		params = {
			'order':'desc',
			'sort':'added',
			'site':site,
			'key':api_key
		}
		json_items = call_api(url, params)

		#extract favs
		for item in json_items:
			title = item.get('title')
			url = item.get('link')
			tags = item.get('tags')
			se_activity_date = int(item.get('last_activity_date'))
			se_activity_date = datetime.utcfromtimestamp(se_activity_date)
			text = get_post_text(url)
			item_dict = {
				'site':site,
				'title':title,
				'url':url,
				'tags':tags,
				'se_activity_date':se_activity_date,
				'text':text
			}
			favs.append(item_dict)

	return favs

def get_post_text(url, top=5):
	print('getting text for:', url)
	re = requests.get(url)
	soup = BeautifulSoup(re.content, 'html.parser')
	post_content = soup.find_all(class_='s-prose js-post-body')
	if len(post_content)<=top:
		return '\n'.join([x.text for x in post_content])
	else:
		return '\n'.join([x.text for x in post_content[:top]])








if __name__ == '__main__':
	'''
	api_key = 'EfszLp6dWEhyCHQ8fxGpWA(('
	se_sites_path = 'cache/se_sites.pickle'
	inname = 'spacy_'
	
	#cache_sites(se_sites_path, api_key)
	acct_id = get_acct_id(inname, se_sites_path, api_key)
	site_uids = get_site_uids(acct_id, api_key)
	favs = get_fav_ques(site_uids, api_key)
	for item in favs:
		print(item)
	'''

	x = get_post_text('https://stackoverflow.com/questions/947215/how-to-get-a-list-of-column-names-on-sqlite3-database')
	print(x)





