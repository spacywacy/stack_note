from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.cache import cache
from .se_api import cache_sites
from .se_api import get_acct_id
from .se_api import get_site_uids
from .se_api import get_fav_ques
from .model_utils import bookmark_pull
from .model_utils import test
from .model_utils import query_user_posts
from .model_utils import filter_posts
from .model_utils import query_user_tags
from .model_utils import query_sites
from .model_utils import query_date_range
from .model_utils import get_checkbox
from .model_utils import get_post_boxes
from .model_utils import get_tags_of_post
from .model_utils import add_answer_comment
from .model_utils import get_answer_comment
from .model_utils import query_buckets
from .model_utils import add_post_to_bucket
from .documents import PostDocument
from .related_api import get_related
from config import api_key
from config import se_sites_path
#from .test_models import test



def index(request):
	#<current process>
	#if need_api_call:
		#do api call
		#store in db
	#query from db & cache
		#user posts
		#user tags
		#user sites
	#read filter fields from form
	#apply filter fields
	#pass filtered user posts to context

	#<new process>
	#if need_api_call:
		#do api call
		#store in db
	#query from db & cache
		#user posts
		#user tags
		#user sites
	#read filter fields from form & cache in view
	#if clear selection
		#clear filter field cache
	#apply filter fields
	#pass filtered user posts to context


	#test(request.user)
	print(request.GET)
	print(request.POST)

	context = {}

	#cache all se sites
	#cache_sites(se_sites_path, api_key)

	#query api for bookmarked post_items of the user
	#acct_id = get_acct_id(str(request.user), se_sites_path, api_key)
	#site_uids = get_site_uids(acct_id, api_key)
	#post_items = get_fav_ques(site_uids, api_key)

	#store post_items in db
	#bookmark_pull(request.user, post_items, True)

	#get post items for the frontend
	#stuff needed
		#a list of all tags the user has
		#a list of post_items from query result

	#tags = ['git', 'python']
	#sites = ['stackoverflow']
	#sdate_entry = '2020-01-01'
	#endate_entry = '2020-12-31'

	#filtering
	if 'clear' in request.GET:
		selected_tags = None
		selected_sites = None
		selected_buckets = None
		sdate = None
		edate = None
		cache.delete('selected_tags')
		cache.delete('selected_sites')
		cache.delete('selected_sdate')
		cache.delete('selected_edate')
		cache.delete('selected_buckets')
	else:
		#filter fields
		form_tags = get_checkbox(request.GET, 'Tags')
		form_sites = get_checkbox(request.GET, 'Sites')
		form_buckets = get_checkbox(request.GET, 'Buckets')
		#selected_tags = cache.get('selected_tags', default=[]) + form_tags
		#selected_sites = cache.get('selected_sites', default=[]) + form_sites
		selected_tags = cache.get('selected_tags', default=set())
		selected_sites = cache.get('selected_sites', default=set())
		selected_buckets = cache.get('selected_buckets', default=set())
		selected_tags = selected_tags.union(set(form_tags))
		selected_sites = selected_sites.union(set(form_sites))
		selected_buckets = selected_buckets.union(set(form_buckets))

		
		if request.GET.get('sdate', None):
			sdate = request.GET.get('sdate')
			cache.set('selected_sdate', sdate)
		elif cache.get('selected_sdate', None):
			sdate = cache.get('selected_sdate')
		else:
			sdate = None

		if request.GET.get('edate', None):
			edate = request.GET.get('edate')
			cache.set('selected_edate', edate)
		elif cache.get('selected_edate', None):
			edate = cache.get('selected_edate')
		else:
			edate = None

		#clear filters
		clear_form_filters = get_checkbox(request.GET, 'clearfilter')
		selected_tags = set([x for x in selected_tags if x not in clear_form_filters])
		selected_sites = set([x for x in selected_sites if x not in clear_form_filters])
		selected_buckets = set([x for x in selected_buckets if x not in clear_form_filters])

		#cache selected
		cache.set('selected_tags', selected_tags)
		cache.set('selected_sites', selected_sites)
		cache.set('selected_buckets', selected_buckets)

	#searching
	if 'search' in request.GET:
		query_str = request.GET.get('search')
		search_results = PostDocument.search().query('multi_match', query=query_str, fields=['title', 'text'])
		search_re_ids = [x.id for x in search_results]
	else:
		search_re_ids = None



	userposts = query_user_posts(str(request.user))
	usertags = query_user_tags(str(request.user), selected_tags, request.GET.get('sort_by',None))
	posts, has_filter = filter_posts(userposts,
						 tags=selected_tags,
						 sites=selected_sites,
						 sdate_entry=sdate,
						 edate_entry=edate,
						 ids=search_re_ids,
						 buckets=selected_buckets)
	
	if 'Tags' in request.GET:
		filter_on = request.GET.get('Tags')
	elif 'Sites' in request.GET:
		filter_on = request.GET.get('Sites')
	elif 'Dates' in request.GET:
		filter_on = request.GET.get('Dates')
	elif 'Buckets' in request.GET:
		filter_on = request.GET.get('Buckets')
	elif cache.get('filter_on', None):
		filter_on = cache.get('filter_on')
	else:
		filter_on = None

	if filter_on == 'Tags':
		context['filter_items'] = usertags
		filter_field = 'Tags'
		menu_tags = 'bg-info'
		menu_sites = menu_buckets = menu_dates = ''
		cache.set('filter_on', 'Tags')
	elif filter_on == 'Sites':
		context['filter_items'] = query_sites(userposts, selected_sites, request.GET.get('sort_by',None))
		filter_field = 'Sites'
		menu_sites = 'bg-info'
		menu_tags = menu_buckets = menu_dates = ''
		cache.set('filter_on', 'Sites')
	elif filter_on == 'Dates':
		context['filter_items'] = None
		filter_field = 'Dates'
		menu_dates = 'bg-info'
		menu_tags = menu_sites = menu_buckets = ''
		cache.set('filter_on', 'Dates')
	elif filter_on == 'Buckets':
		context['filter_items'] = query_buckets(str(request.user), [], request.GET.get('sort_by',None))
		filter_field = 'Buckets'
		menu_buckets = 'bg-info'
		menu_tags = menu_sites = menu_dates = ''
		cache.set('filter_on', 'Buckets')
	else:
		filter_on = cache.get('filter_on')
		context['filter_items'] = usertags
		filter_field = 'Tags'
		menu_tags = 'bg-info'
		menu_sites = menu_buckets = menu_dates = ''
		cache.set('filter_on', 'Tags')

	#call related api
	#not sure if I should call api for related posts when loading page
	#or get related posts in batch and store in db
	if posts:
		posts_package = get_related(posts)

		#get answer url & comment
		get_answer_comment(posts_package, str(request.user))

		#context['posts'] = posts
		context['posts'] = posts_package

		#get text summary & tags
		for item in posts_package:
			item['summary'] = item['post'].text[:350]
			item['posttag'] = get_tags_of_post(item['post'])

		#dates & n_posts
		context['min_date'], context['max_date'] = query_date_range(posts)
		context['n_posts'] = len(posts)


	context['selected_fields'] = []
	if selected_tags:
		context['selected_fields'] += selected_tags
	if selected_sites:
		context['selected_fields'] += selected_sites
	if selected_buckets:
		context['selected_fields'] += selected_buckets
	if 'search' in request.GET:
		context['selected_fields'] += ['search:{}'.format(request.GET.get('search'))]
	context['has_filter'] = has_filter
	context['filter_field'] = filter_field
	context['menu_tags'] = menu_tags
	context['menu_sites'] = menu_sites
	context['menu_buckets'] = menu_buckets
	context['menu_dates'] = menu_dates
	context['buckets'] = query_buckets(str(request.user), [], request.GET.get('sort_by',None))


	#add answer url & comment
	posted = add_answer_comment(request.POST, str(request.user))
	
	#add post to bucket
	posted = add_post_to_bucket(request.POST, str(request.user))


	if posted:
		print('redirecting')
		return redirect(index)

	return render(request, 'index.html', context)














