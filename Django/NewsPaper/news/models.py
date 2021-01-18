from django.db import models
from django.contrib.auth.models import User
class Author(models.Model):
    user_id =models.OneToOneField(User, on_delete=models.CASCADE)
    rating =models.IntegerField(default=0)
    def update_rating(self):
        rating = self.rating
        return rating+Post.rating*3+Comment.rating

class Category(models.Model):
    name =models.CharField(max_length=255,unique=True)
class Post(models.Model):

    author_id =models.ForeignKey(Author, on_delete=models.CASCADE)
    its_post =models.BooleanField(default=True)
    insertdt = models.DateTimeField(auto_now_add=True)
    category_id = models.ManyToManyField(Category,through='PostCategory',null=True,blank=True)
    caption =models.CharField(max_length=255)
    text = models.TextField()
    rating =models.IntegerField(default=0)
    def like(self):
        rating = self.rating
        rating += 1
        return rating

    def dislike(self):
        rating -= 1

    def preview(self):
        return text[:124]+'...'

class PostCategory(models.Model):
    post_id =models.ForeignKey(Post,on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
class Comment(models.Model):
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    insertdt = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    def like(self):
        rating += 1

    def dislike(self):
        rating -= 1

