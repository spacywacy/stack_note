from datetime import datetime
from time import time
from django.contrib.auth.models import User
from .models import Post
from .models import Tag
from .models import PostTag
from .models import UserTag
from .models import UserPost
from .models import Usercomment
from .models import Markedanswer
from .models import Bucket
from .models import PostBucket
from .se_api import get_answer_text
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
		text = item_dict.get('text')

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
						entry_date=entry_date,
						text=text)
			#print(post.text)
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

		
def filter_posts(userposts, tags=None, sites=None, sdate_entry=None, edate_entry=None, ids=None, buckets=None):
	#tag: or condition
	#site: or condition
	#dates: and condition
	#everything put together using and condition

	filtered = userposts
	has_filter = False

	if tags:
		filtered = filtered.filter(userpost__post_key__posttag__tag_key__tag_name__in=tags)
		has_filter = True

	if sites:
		filtered = filtered.filter(site__in=sites)
		has_filter = True

	if sdate_entry:
		filtered = filtered.filter(entry_date__gte=sdate_entry)
		has_filter = True

	if edate_entry:
		filtered = filtered.filter(entry_date__lte=edate_entry)
		has_filter = True

	if ids:
		filtered = filtered.filter(userpost__post_key__id__in=ids)
		has_filter = True

	if buckets:
		filtered = filtered.filter(userpost__post_key__postbucket__bucket_key__bucket_name__in=buckets)
		has_filter = True

	if filtered:
		return filtered.distinct(), has_filter
	else:
		return None, None


def query_user_tags_(django_user):
	user_name = str(django_user)
	usertags = Tag.objects.filter(usertag__user_key__username=user_name)
	has_results = bool(usertags)
	if has_results:
		return usertags

def query_user_tags(django_user, selected_tags, sort_by=None):
	user_name = str(django_user)
	usertags = UserTag.objects.filter(user_key__username=user_name)
	has_results = bool(usertags)
	
	if has_results:
		results = []
		for item in usertags:
			item_dict = {}
			item_dict['name'] = item.tag_key.tag_name
			item_dict['count'] = item.count
			if selected_tags and item.tag_key.tag_name in selected_tags:
				item_dict['bg_color'] = 'bg-primary'
				item_dict['text_color'] = 'text-white'
			else:
				item_dict['bg_color'] = ''
				item_dict['text_color'] = ''
			results.append(item_dict)

		if sort_by == 'name':
			results = sorted(results, key=lambda x: x[sort_by], reverse=False)
		elif sort_by == 'count':
			results = sorted(results, key=lambda x: x[sort_by], reverse=True)

		return results

def get_tags_of_post(post):
	return PostTag.objects.filter(post_key=post)



def query_sites(userposts, selected_sites, sort_by=None):
	counts = {}
	for item in userposts:
		counts[item.site] = counts.get(item.site, 0) + 1

	#return [{'name':site_name, 'count':count,} for site_name, count in counts.items()]
	results = []
	for site, count in counts.items():
		item_dict = {}
		item_dict['name'] = site
		item_dict['count'] = count
		if selected_sites and site in selected_sites:
			item_dict['bg_color'] = 'bg-primary'
			item_dict['text_color'] = 'text-white'
		else:
			item_dict['bg_color'] = ''
			item_dict['text_color'] = ''
		results.append(item_dict)

	if sort_by == 'name':
		results = sorted(results, key=lambda x: x[sort_by], reverse=False)
	elif sort_by == 'count':
		results = sorted(results, key=lambda x: x[sort_by], reverse=True)

	return results


def query_date_range(filtered):
	min_date = filtered.aggregate(Min('entry_date'))['entry_date__min']
	max_date = filtered.aggregate(Max('entry_date'))['entry_date__max']

	return min_date, max_date


def query_buckets(user_name, selected_buckets, sort_by=None):
	user = User.objects.get(username=user_name)
	user_buckets = Bucket.objects.filter(owner=user)
	results = []
	for bucket in user_buckets:
		item_dict = {}
		item_dict['name'] = bucket.bucket_name
		item_dict['count'] = bucket.count
		if selected_buckets and bucket.bucket_name in selected_buckets:
			item_dict['bg_color'] = 'bg-primary'
			item_dict['text_color'] = 'text_white'
		else:
			item_dict['bg_color'] = ''
			item_dict['text_color'] = ''
		results.append(item_dict)

	if sort_by == 'name':
		results = sorted(results, key=lambda x: x[sort_by], reverse=False)
	elif sort_by == 'count':
		results = sorted(results, key=lambda x: x[sort_by], reverse=True)

	return results


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

def get_post_boxes(post_obj, box_name):
	results = []
	for k, v in post_obj.items():
		form_item = k.split('_')
		#print(form_item)
		if len(form_item) > 1:
			item_prefix = form_item[0]
			item_name = form_item[1]
			#print(item_prefix, item_name)
			if item_prefix == box_name and bool(v):
				results.append((item_name, v))

	return results

def add_answer_comment(post_obj, user_name):
	#get user
	user = User.objects.get(username=user_name)

	#get form data
	answer_urls = get_post_boxes(post_obj, 'answerbox')
	user_comments = get_post_boxes(post_obj, 'commentbox')

	posted = False

	#loop answer_urls
	for item in answer_urls:
		post_id = int(item[0])
		answer_url = item[1]
		post = Post.objects.get(id=post_id)
		answer_text = get_answer_text(answer_url)
		comment_obj = Markedanswer(
			user_key=user,
			post_key=post,
			marked_answer=answer_url,
			answer_text=answer_text
		)
		posted = True
		comment_obj.save()

	#loop user_comments
	for item in user_comments:
		post_id = int(item[0])
		user_comment = item[1]
		post = Post.objects.get(id=post_id)
		comment_obj = Usercomment.objects.filter(post_key=post).filter(user_key=user)
		if comment_obj:
			comment_obj = comment_obj[0]
			comment_obj.user_comment = user_comment
		else:
			comment_obj = Usercomment(
				user_key=user,
				post_key=post,
				user_comment=user_comment
			)
		posted = True
		comment_obj.save()

	if posted:
		print('added answer comment')
		return True

def add_post_to_bucket(post_obj, user_name):
	bucket_pairs = get_post_boxes(post_obj, 'add2bucket')
	posted = False

	#loop bucket pairs
	for item in bucket_pairs:
		#add post bucket pair
		post_key = Post.objects.filter(id=item[1])[0]
		bucket_key = Bucket.objects.filter(bucket_name=item[0])[0]
		print(item[0])
		print(bucket_key)
		post_bucket = PostBucket(
			post_key = post_key,
			bucket_key = bucket_key
		)
		post_bucket.save()

		#update bucket post count
		bucket_key.count += 1
		bucket_key.save()

		posted = True


	return posted




def get_answer_comment(posts_package, user_name):
	#get user
	user = User.objects.get(username=user_name)

	for i in range(len(posts_package)):

		post = posts_package[i]['post']
		answers = Markedanswer.objects.filter(post_key=post).filter(user_key=user)
		#print('answers')
		#print(answers)
		if answers:
			posts_package[i]['answers'] = answers
		else:
			posts_package[i]['answers'] = None

		comment = Usercomment.objects.filter(post_key=post).filter(user_key=user)
		if comment:
			posts_package[i]['comment'] = comment[0]
		else:
			posts_package[i]['comment'] = None



def test(django_user):
	tags = ['git', 'python']
	sites = ['stackoverflow']
	sdate_entry = '2020-01-01'
	userposts = query_user_posts(django_user)
	filtered = filter_posts(userposts, tags=tags, sites=sites, sdate_entry=sdate_entry)
	print(filtered)




if __name__ == '__main__':
	pass











