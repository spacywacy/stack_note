from django_elasticsearch_dsl import Document, Index
from .models import Post

posts = Index('posts')

@posts.doc_type
class PostDocument(Document):
	class Django:
		model = Post

		fields = [
			'id',
			'title',
			'url'
		]

















