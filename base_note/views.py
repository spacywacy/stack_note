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
from .model_utils import get_post_info
from .model_utils import add_answer_comment
from .model_utils import get_answer_comment
from .model_utils import query_buckets
from .model_utils import add_post_to_bucket
from .model_utils import if_clear_search
from .model_utils import if_clear_dates
from .model_utils import get_post_fields
from .model_utils import show_post
from .documents import PostDocument
from .related_api import get_related
from config import api_key
from config import se_sites_path
from datetime import datetime
#from .test_models import test




def posts(request, posts_to_show=-1):
	print('GET:', request.GET)
	print('POST:', request.POST)
	context = {'page_title':'Posts', 'nav_posts':'bg-info'}
	
	#redirects
	for k, v in redirect_mapping.items():
		if k in request.GET:
			return redirect(v)

	#filtering posts
	if 'clear' in request.GET:
		selected_sites = None
		selected_tags = None
		entry_dates = None
		cache.delete('selected_sites')
		cache.delete('selected_tags')
		cache.delete('search_re_ids')
		cache.delete('search_term')
		cache.delete('entry_dates')
	else:
		#get filters
		form_sites = get_checkbox(request.GET, 'sitefilter')
		form_tags = get_checkbox(request.GET, 'tagfilter')
		selected_sites = cache.get('selected_sites', default=set())
		selected_tags = cache.get('selected_tags', default=set())
		selected_sites = selected_sites.union(set(form_sites))
		selected_tags = selected_tags.union(set(form_tags))
		
		if request.GET.get('sdate') or request.GET.get('edate'):
			entry_dates = {'sdate':request.GET.get('sdate'), 'edate':request.GET.get('edate')}
			cache.set('entry_dates', entry_dates)
		else:
			entry_dates = cache.get('entry_dates')

		#clear filters
		clear_form_filters = get_checkbox(request.GET, 'clearfilter')
		selected_sites = set([x for x in selected_sites if x not in clear_form_filters])
		selected_tags = set([x for x in selected_tags if x not in clear_form_filters])
		if if_clear_dates(request.GET):
			entry_dates = None

		#cache selected
		cache.set('selected_sites', selected_sites)
		cache.set('selected_tags', selected_tags)

	#searching posts
	if 'search' in request.GET:
		search_term = request.GET.get('search')
		search_results = PostDocument.search().query('multi_match', query=search_term, fields=['title', 'text'])
		search_re_ids = [x.id for x in search_results]
		cache.set('search_re_ids', search_re_ids)
		cache.set('search_term', search_term)
	elif if_clear_search(request.GET):
		search_re_ids = None
		search_term = None
	elif cache.get('search_re_ids', None):
		search_re_ids = cache.get('search_re_ids')
		search_term = cache.get('search_term')
	else:
		search_re_ids = None
		search_term = None


	#combine selected filters
	context['selected_fields'] = []
	if selected_sites:
		context['selected_fields'] += selected_sites
	if selected_tags:
		context['selected_fields'] += selected_tags
	#if 'search' in request.GET:
	if search_re_ids and search_term:
		context['selected_fields'] += ['search:{}'.format(search_term)]
	if entry_dates:
		context['selected_fields'] += ['dates']
	

	#query user posts
	userposts = query_user_posts(str(request.user))

	#query tags/sites/buckets
	context['sites'] = query_sites(userposts, selected_sites, request.GET.get('sites_sort_by',None))
	context['tags'] = query_user_tags(str(request.user), selected_tags, request.GET.get('tags_sort_by',None))

	#get order
	post_order = request.GET.get('postorder', None)
	if not post_order:
		post_order = '-entry_date'

	post_desc = request.GET.get('post_desc', None)
	if post_desc:
		post_order = '-' + post_order

	#apply filter fields & search result to queried posts
	#also get date range
	post_package, has_filter, date_range = filter_posts(userposts,
											tags=selected_tags,
											sites=selected_sites,
											entry_dates=entry_dates,
											ids=search_re_ids,
											order_by=post_order)
	get_post_info(post_package, str(request.user))
	show_post(post_package, posts_to_show)
	context['posts'] = post_package
	if post_package:
		context['n_posts'] = len(post_package)
	if date_range:
		context['sdate'] = datetime.strftime(date_range[0], '%Y-%m-%d')
		context['edate'] = datetime.strftime(date_range[1], '%Y-%m-%d')

	#query post fields
	context['post_fields'] = get_post_fields()


	#method==post
	#add answer url & comment
	posted_id = add_answer_comment(request.POST, str(request.user))

	#add post to bucket


	#redirect & show previous view
	if posted_id:
		print('redirecting')
		return redirect(posts, posts_to_show=posted_id)

	#debug
	#print('\nselected_sites')
	#print(selected_sites)
	#print('\nselected_tags')
	#print(selected_tags)
	#print(context['tags'])
	#print(search_term)
	#print(entry_dates)
	#print(date_range)
	#print(get_post_fields())

	return render(request, 'posts.html', context)


def buckets(request):
	print('GET:', request.GET)
	print('POST:', request.POST)
	context = {'page_title':'Buckets', 'nav_buckets':'bg-info'}

	#redirects
	for k, v in redirect_mapping.items():
		if k in request.GET:
			return redirect(v)

	return render(request, 'buckets.html', context)



def recommend(request):
	print('GET:', request.GET)
	print('POST:', request.POST)
	context = {'page_title':'Recommend', 'nav_recommend':'bg-info'}

	#redirects
	for k, v in redirect_mapping.items():
		if k in request.GET:
			return redirect(v)

	return render(request, 'recommend.html', context)



def account(request):
	print('GET:', request.GET)
	print('POST:', request.POST)
	context = {'page_title':'Account', 'nav_account':'bg-info'}

	#redirects
	for k, v in redirect_mapping.items():
		if k in request.GET:
			return redirect(v)

	return render(request, 'account.html', context)










#redirects
redirect_mapping = {
	'posts':posts,
	'buckets':buckets,
	'recommend':recommend,
	'account':account
}
















