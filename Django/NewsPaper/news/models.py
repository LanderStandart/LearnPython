from django.db import models
from django.contrib.auth.models import User
class Author(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=255,null=True)
    rating =models.IntegerField(default=0)

    def update_raiting(self):
        posts = Post.objects.filter(author_id=self.id)  # все посты автора
        post_raiting = sum([r.rating * 3 for r in posts])  # рейтинг каждого поста автора умножен на 3
        comment_raiting = sum([r.rating for r in
                               Comment.objects.filter(user_id=self.user_id)])  # сумма лайков/дислайков к комментам автора
        all_to_post_comment_raiting = sum([r.rating for r in Comment.objects.filter(
            post_id__in=posts)])  # сумма лайков/дислайков всех комментов к постам автора
        self.rating = post_raiting + comment_raiting + all_to_post_comment_raiting
        self.save()

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
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124]+'...'
    def __str__(self):
        return f'{self.caption.title()}:{self.text[:20]}...'

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
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

