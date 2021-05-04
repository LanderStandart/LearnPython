from celery import shared_task
import time
from .models import Post,Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import datetime,timedelta

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def send_post_sub(cid,pid):
    post = Post.objects.get(pk=pid)
    cat = Category.objects.get(pk=cid)
    q = cat.subscribers.all()

    for mail in q:
        html_content = render_to_string(
            'newpost_mail.html', {
                'post': post,
                'user': mail.username
            }
        )

        msg = EmailMultiAlternatives(
            subject=post.caption,
            body=post.text,
            from_email='landerneo@yandex.ru',
            to=[mail.email]
        )
        msg.attach_alternative(html_content, "text/html")
        print(html_content)
        # msg.send()

@shared_task
def send_news_review():
    sub = Category.objects.all()
    for cat in sub:
        post = Post.objects.filter(category_id=cat.id, insertdt__gt=datetime.now() - timedelta(days=7))
        if post.count() > 0:
            q = cat.subscribers.all()
            for mail in q:

                print(mail.email)
                for postn in post:
                    print(postn.id, postn.caption)
                html_content = render_to_string(
                    'week_news.html', {
                        'post': post,
                        'user': mail.username,
                        'category': cat.name
                    }
                )
                msg = EmailMultiAlternatives(
                    subject='Django NewsPortal WeekNews',
                    body='d',
                    from_email='landerneo@yandex.ru',
                    to=[mail.email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
    # print(datetime.now()-timedelta(days=7),'hello from job',sub)
    print(html_content)
    print('------------')
