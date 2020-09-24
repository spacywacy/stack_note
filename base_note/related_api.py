import os
import json
import requests
from datetime import datetime
from time import time
from django.contrib.auth.models import User
from .models import Post
from .models import Tag
from .models import PostTag
from .models import UserTag
from .models import UserPost
from config import new_related_path
from django.db.models import Q


def get_related(posts):
	#call api
	urls = [x.url for x in posts]
	urls = json.dumps(urls)
	re = requests.get('http://127.0.0.1:5000/related', data={'urls':urls}).json()


	#load new_related.json
	with open(new_related_path, 'r') as f:
		new_items = json.load(f)


	#record posts not seen by the related system
	'''
	'posts':
	[
		{
		'title':'',
		'source':'',
		'url':'',
		'tags'['tag_name']
		}
	]
	'''
	posts_package = []
	for post in posts:
		related = re.get(post.url)
		posts_package.append({'post':post, 'related':related})
		
		if not related and post.url not in new_items['urls']:
			tags = PostTag.objects.filter(post_key=post)
			tags = [x.tag_key.tag_name for x in tags]
			new_item = {
				'title': post.title,
				'source': 'user_se',
				'url': post.url,
				'tags':tags
			}
			new_items['posts'].append(new_item)
			new_items['urls'][post.url] = 1

	#dump new_related.json
	with open(new_related_path, 'w') as f:
		json.dump(new_items, f)


	#return related_items
	return posts_package













