from time import time
from django.contrib.auth.models import User
from .models import Post
from .models import Tag
from .models import PostTag
from .models import UserTag
from .models import UserPost
from django.db.models import Q



def test():
	print('test is working')

	#chained lazy filters
	t0 = time()
	re_post = Post.objects.filter(userpost__user_key__username='spacy_').filter(userpost__post_key__posttag__tag_key__tag_name='git')
	print(re_post)
	print('time took:', time()-t0)

	#


