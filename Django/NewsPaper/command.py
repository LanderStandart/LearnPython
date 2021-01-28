from news.models import  *

User.objects.create_user(username='user1')
User.objects.create_user(username='user2')

Author.objects.create(user_id=User.objects.get(username='user1'), username='FirstUser')
Author.objects.create(user_id=User.objects.get(username='user2'), username='SecondUser')

Category.objects.create(name='Политика')
Category.objects.create(name='Здоровье')
Category.objects.create(name='Шоубизнес')
Category.objects.create(name='Финансы')

Post.objects.create(author_id=Author.objects.get(username='FirstUser'),its_post=True,caption='Вопросы о Ковид',text='Что говорит ВОЗ о Пандемии')
Post.objects.create(author_id=Author.objects.get(username='SecondUser'),its_post=True,caption='Ситуация на рынке',text='Грозит ли кризис?')
Post.objects.create(author_id=Author.objects.get(username='SecondUser'),its_post=False,caption='Новости недели',text='Что нового в России ? Вернется ли Навальный')

p1 = Post.objects.get(caption='Вопросы о Ковид')
c1 = Category.objects.get(name='Здоровье')
p1.category_id.add(c1)

p2 = Post.objects.get(caption='Ситуация на рынке')
c2 = Category.objects.get(name='Политика')
p2.category_id.add(c1,c2)

p3 = Post.objects.get(caption='Новости недели')
c3 = Category.objects.get(name='Финансы')
p3.category_id.add(c1,c2,c3)

Comment.objects.create(post_id=Post.objects.get(caption='Вопросы о Ковид'),user_id=User.objects.get(username='user1'),text='Поддерживаю полностью')
Comment.objects.create(post_id=Post.objects.get(caption='Новости недели'),user_id=User.objects.get(username='user2'),text='Ой опять про него')
Comment.objects.create(post_id=Post.objects.get(caption='Ситуация на рынке'),user_id=User.objects.get(username='user1'),text='У меня кафе в минусе')
Comment.objects.create(post_id=Post.objects.get(caption='Новости недели'),user_id=User.objects.get(username='user1'),text='Красавчик верю в него')

Post.objects.get(caption='Новости недели').like()
Post.objects.get(caption='Вопросы о Ковид').like()
Post.objects.get(caption='Ситуация на рынке').like()
Post.objects.get(caption='Ситуация на рынке').like()
Post.objects.get(caption='Ситуация на рынке').like()

Post.objects.get(caption='Ситуация на рынке').dislike()
Post.objects.get(caption='Вопросы о Ковид').dislike()

Comment.objects.get(post_id=Post.objects.get(caption='Новости недели')).like()

for auth in Author.objects.all():
    auth.update_raiting()

Author.objects.all().order_by('-rating').values('username','rating')[0]

best = Post.objects.all().order_by('-rating')[0]
Post.objects.all().order_by('-rating').values('insertdt','username','caption','rating','text')[0]
best.preview()

Comment.objects.filter(post_id=best).values('user_id__username', 'insertdt', 'text')





