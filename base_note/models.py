from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#class user(models.Model):
#	user_name = models.CharField(max_length=64)
#	pass_hash = models.CharField(max_length=128)
#
#	def __str__(self):
#		return self.user_name


class Post(models.Model):
	title = models.CharField(max_length=200)
	url = models.URLField() #using url as unique identifier, may need to use a shorter field
	site = models.CharField(max_length=64)
	from_se = models.BooleanField()
	se_activity_date = models.DateTimeField()
	entry_date = models.DateTimeField()
	text = models.TextField()

	def __str__(self):
		return self.title

	class Meta:
		indexes = [
			models.Index(fields=['url', 'entry_date'])
		]

class Bucket(models.Model):
	bucket_name = models.CharField(max_length=200)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	count = models.IntegerField()

	def __str__(self):
		return self.bucket_name

	class Meta:
		indexes = [
			models.Index(fields=['bucket_name', 'owner'])
		]

class PostBucket(models.Model):
	post_key = models.ForeignKey(Post, on_delete=models.CASCADE)
	bucket_key = models.ForeignKey(Bucket, on_delete=models.CASCADE)

	def __str__(self):
		return 'post:{} - bucket:{}'.format(self.post_key, self.bucket_key)

	class Meta:
		indexes = [
			models.Index(fields=['post_key', 'bucket_key'])
		]


class Tag(models.Model):
	tag_name = models.CharField(max_length=64)
	site = models.CharField(max_length=64)

	def __str__(self):
		return self.tag_name

	class Meta:
		indexes = [
			models.Index(fields=['tag_name', 'site'])
		]

class UserPost(models.Model):
	pair_id = models.CharField(max_length=256) #user_name-url
	user_key = models.ForeignKey(User, on_delete=models.CASCADE)
	post_key = models.ForeignKey(Post, on_delete=models.CASCADE)
	#marked_answer = models.URLField()
	#user_comment = models.CharField(max_length=1024)

	def __str__(self):
		return 'user:{} - post:{}'.format(self.user_key, self.post_key)

	class Meta:
		indexes = [
			models.Index(fields=['pair_id', 'user_key', 'post_key'])
		]

class Markedanswer(models.Model):
	user_key = models.ForeignKey(User, on_delete=models.CASCADE)
	post_key = models.ForeignKey(Post, on_delete=models.CASCADE)
	marked_answer = models.URLField()
	answer_text = models.CharField(max_length=1024)

	def __str__(self):
		return '{}-{}-{}'.format(self.user_key, self.post_key, self.marked_answer)

	class Meta:
		indexes = [
			models.Index(fields=['user_key', 'post_key'])
		]

class Usercomment(models.Model):
	user_key = models.ForeignKey(User, on_delete=models.CASCADE)
	post_key = models.ForeignKey(Post, on_delete=models.CASCADE)
	user_comment = models.CharField(max_length=1024)

	def __str__(self):
		return '{}-{}-{}'.format(self.user_key, self.post_key, self.user_comment)

	class Meta:
		indexes = [
			models.Index(fields=['user_key', 'post_key'])
		]


class PostTag(models.Model):
	pair_id = models.CharField(max_length=256) #url-tag_name
	post_key = models.ForeignKey(Post, on_delete=models.CASCADE)
	tag_key = models.ForeignKey(Tag, on_delete=models.CASCADE)

	def __str__(self):
		return 'post:{} - tag:{}'.format(self.post_key, self.tag_key)

	class Meta:
		indexes = [
			models.Index(fields=['pair_id', 'post_key', 'tag_key'])
		]


class UserTag(models.Model):
	pair_id = models.CharField(max_length=256) #user_name-tag_name
	user_key = models.ForeignKey(User, on_delete=models.CASCADE)
	tag_key = models.ForeignKey(Tag, on_delete=models.CASCADE)
	count = models.IntegerField()

	def __str__(self):
		return 'user:{} - tag:{}'.format(self.user_key, self.tag_key)

	class Meta:
		indexes = [
			models.Index(fields=['pair_id', 'user_key', 'tag_key'])
		]










































