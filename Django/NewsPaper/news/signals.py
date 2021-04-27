from django.core.mail import EmailMultiAlternatives,send_mail
from django.db.models.signals import m2m_changed,pre_save
from django.dispatch import receiver
from django.db import models
from datetime import date
today = date.today()

@receiver(m2m_changed, sender=Post.category_id.through)
def notify_new_post(sender,instance,action, **kwargs):
    #cat = Category.objects.get(category=instance.category_id)
    cat = Category.objects.get(id=list(kwargs['pk_set'])[0])
    q = cat.subscribers.all()

    if not q:
        return
    mail_reseiv=[]
    for mail in q:
        mail_reseiv.append(mail.email)


    html_content = render_to_string(
        'newpost_mail.html', {
            'post': instance,
            'user': mail.username
        }
    )
    msg = EmailMultiAlternatives(
        subject=instance.caption,
        body=instance.text,
        from_email='landerneo@yandex.ru',
        to=mail_reseiv
    )
    msg.attach_alternative(html_content, "text/html")
    #msg.send()

@receiver(pre_save,sender=Post)
def limit_post(sender,instance,**kwargs):
    date=models.DateTimeField(auto_now_add=True)
    #p= sender.objects.filter(author_id=1,insertdt=models.DateTimeField(auto_now_add=True))
    print(date)