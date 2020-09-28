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




def posts(request):
	print('GET:', request.GET)
	print('POST:', request.POST)
	context = {'page_title':'Posts', 'nav_posts':'bg-info'}

	#redirects
	for k, v in redirect_mapping.items():
		if k in request.GET:
			return redirect(v)

	#filtering posts
	#if 'clear' in request.GET:
		#selected filter fields = None
		#clear cached filter fields
	#else:
		#get filter fields from form
		#cache filter fields
		#remove select filter fields & clear cache for unselected field items

	#searching posts
		#get a list of post ids from search

	#query models
		#query tags/sites/dates/buckets
		#query posts
		#apply filter fields & search result to queried posts

	#method==post
		#add answer url & comment
		#add post to bucket
		#redirect & show previous view

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
















