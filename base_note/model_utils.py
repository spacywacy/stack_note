from datetime import datetime
from time import time
from django.contrib.auth.models import User
from .models import Post
from .models import Tag
from .models import PostTag
from .models import UserTag
from .models import UserPost
from django.db.models import Q
from django.db.models import Min
from django.db.models import Max



def bookmark_pull(django_user, post_items, from_se=True):
	t0 = time()

	for item_dict in post_items:

		#get user
		user_name = str(django_user)
		user = User.objects.get(username=user_name)

		#get post_item
		title = item_dict.get('title')
		url = item_dict.get('url')
		site = item_dict.get('site')
		se_activity_date = item_dict.get('se_activity_date')
		entry_date = datetime.now()

		#save post
		re_post = Post.objects.filter(url=url)
		if re_post:
			post = re_post[0]
		else:
			post = Post(title=title,
						url=url,
						site=site,
						from_se=from_se,
						se_activity_date=se_activity_date,
						entry_date=entry_date)
			post.save()

		#save UserPost
		user_post_pair_id = '{}-{}'.format(user_name, url)
		re_user_post = UserPost.objects.filter(pair_id=user_post_pair_id)
		if not re_user_post:
			user_post = UserPost(pair_id=user_post_pair_id, user_key=user, post_key=post)
			user_post.save()
		
		#loop tags
		tag_names = item_dict.get('tags')
		for tag_name in tag_names:

			#save tag
			re_tag = Tag.objects.filter(tag_name=tag_name)
			if re_tag:
				tag = re_tag[0]
			else:
				tag = Tag(tag_name=tag_name, site=site)
				tag.save()

			#save post_tag
			post_tag_pair_id = '{}-{}'.format(url, tag_name)
			re_post_tag = PostTag.objects.filter(pair_id=post_tag_pair_id)
			if not re_post_tag:
				post_tag = PostTag(pair_id=post_tag_pair_id, post_key=post, tag_key=tag)
				post_tag.save()

			#save user_tag
			user_tag_pair_id = '{}-{}'.format(user_name, tag_name)
			re_user_tag = UserTag.objects.filter(pair_id=user_tag_pair_id)
			if not re_user_tag:
				user_tag = UserTag(pair_id=user_tag_pair_id, user_key=user, tag_key=tag, count=1)
				user_tag.save()
			else:
				user_tag = re_user_tag[0]
				user_tag.count += 1
				user_tag.save()

	print('pull time: {0:.2f}'.format(time()-t0))


def query_user_posts(django_user):
	#get all post_items belong to the user
	user_name = str(django_user)
	userposts = Post.objects.filter(userpost__user_key__username=user_name)
	has_results = bool(userposts)
	if has_results:
		return userposts

		
def filter_posts(userposts, tags=None, sites=None, sdate_entry=None, edate_entry=None):
	#tag: or condition
	#site: or condition
	#dates: and condition
	#everything put together using and condition

	filtered = userposts

	if tags:
		filtered = filtered.filter(userpost__post_key__posttag__tag_key__tag_name__in=tags)

	if sites:
		filtered = filtered.filter(site__in=sites)

	if sdate_entry:
		filtered = filtered.filter(entry_date__gte=sdate_entry)

	if edate_entry:
		filtered = filtered.filter(entry_date__lte=edate_entry)

	return filtered.distinct()


def query_user_tags_(django_user):
	user_name = str(django_user)
	usertags = Tag.objects.filter(usertag__user_key__username=user_name)
	has_results = bool(usertags)
	if has_results:
		return usertags

def query_user_tags(django_user):
	user_name = str(django_user)
	usertags = UserTag.objects.filter(user_key__username=user_name)
	has_results = bool(usertags)
	if has_results:
		return usertags

def query_sites(userposts):
	sites = set()
	for item in userposts:
		sites.add(item.site)
	return list(sites)

def query_date_range(filtered):
	min_date = filtered.aggregate(Min('entry_date'))['entry_date__min']
	max_date = filtered.aggregate(Max('entry_date'))['entry_date__max']

	return min_date, max_date

def get_checkbox(get_obj, checkbox_name):
	results = []
	for k, v in get_obj.items():
		form_item = k.split('_')
		if len(form_item) > 1:
			item_prefix = form_item[0]
			item_name = form_item[1]
			if item_prefix == checkbox_name and bool(v):
				results.append(item_name)

	return results


def test(django_user):
	tags = ['git', 'python']
	sites = ['stackoverflow']
	sdate_entry = '2020-01-01'
	userposts = query_user_posts(django_user)
	filtered = filter_posts(userposts, tags=tags, sites=sites, sdate_entry=sdate_entry)
	print(filtered)




if __name__ == '__main__':
	pass











