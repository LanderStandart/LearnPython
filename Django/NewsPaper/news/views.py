from django.views.generic import ListView,DetailView,UpdateView,DeleteView,TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .models import Post,Category,PostCategory
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.core.mail import EmailMultiAlternatives,send_mail
from django.db.models.signals import m2m_changed,pre_save
from django.dispatch import receiver
from django.db import models
from datetime import date
from .tasks import send_post_sub,send_news_review
from django.core.cache import cache
today = date.today()

# @receiver(m2m_changed, sender=Post.category_id.through)
# def notify_new_post(sender,instance,action, **kwargs):
#     #cat = Category.objects.get(category=instance.category_id)
#     cat = Category.objects.get(id=list(kwargs['pk_set'])[0])
#     q = cat.subscribers.all()
#
#     if not q:
#         return
#     mail_reseiv=[]
#     for mail in q:
#         mail_reseiv.append(mail.email)
#
#
#     html_content = render_to_string(
#         'newpost_mail.html', {
#             'post': instance,
#             'user': mail.username
#         }
#     )
#     msg = EmailMultiAlternatives(
#         subject=instance.caption,
#         body=instance.text,
#         from_email='landerneo@yandex.ru',
#         to=mail_reseiv
#     )
#     msg.attach_alternative(html_content, "text/html")
#     #msg.send()
#
# @receiver(pre_save,sender=Post)
# def limit_post(sender,instance,**kwargs):
#     date=models.DateTimeField(auto_now_add=True)
#     #p= sender.objects.filter(author_id=1,insertdt=models.DateTimeField(auto_now_add=True))
#     print(date)
#
#


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-insertdt']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['sub']=Category.objects.filter().values('subscribers')

        return context


# class PostContent(DetailView):
#     model = Post
#     template_name = 'post.html'
#     context_object_name = 'post'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

class PostContent(DetailView):
    template_name = 'post.html'
    queryset = Post.objects.all()

    def get_object(self, *args,**kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}',obj)
        return obj



class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-insertdt']
    paginate_by = 1
    # queryset = Post.objects.order_by('-insertdt')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,queryset=self.get_queryset())
        return context
class CreatePost(PermissionRequiredMixin,CreateView):
    model = Post
    template_name = 'create_post.html'
    context_object_name = 'posts'
    form_class=PostForm
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']=Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            tas =form.save()

        post = request.POST
        #sendmail
        allPOST = Post.objects.filter(insertdt__contains=today,author_id=request.POST['author_id']).count()
        if allPOST>10:
            print('Hvatit')
            return redirect(f'/posts/stopadd')
        send_post_sub(request.POST['category_id'],tas.pk)
        #print(tas.pk)
        # cat = Category.objects.get(id=request.POST['category_id'])
        # q = cat.subscribers.all()
        #
        # for mail in q:
        #     html_content = render_to_string(
        #         'newpost_mail.html', {
        #             'post': post,
        #             'user':mail.username
        #         }
        #     )
        #
        #     msg = EmailMultiAlternatives(
        #         subject=post['caption'],
        #         body=post['text'],
        #         from_email='landerneo@yandex.ru',
        #         to=[mail.email]
        #     )
        #     msg.attach_alternative(html_content,"text/html")
            #msg.send()
            # send_mail(
            #     subject=request.POST['caption'],
            #     message=request.POST['text'],
            #     from_email='landerneo@yandex.ru',
            #     recipient_list=[mail.email]
            # )

        return super().get(request, *args, **kwargs)

class PostUpdate(PermissionRequiredMixin,UpdateView):
    template_name = 'create_post.html'
    form_class = PostForm
    permission_required = ('news.change_post',)
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    template_name = 'delete_post.html'
    queryset = Post.objects.all()
    success_url='/posts/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

class StopADDViev(TemplateView):
    template_name = 'stop_add.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class CategoryList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        cat = Category.objects.get(id=self.kwargs['category'])
        myuser = self.request.user
        context['user']=myuser
        q = cat.subscribers.filter().values('email')
        context['cuser'] = q.values('email')
        if myuser in q:
            context['categoryidbed'] = Category.objects.get(id=self.kwargs['category'])
        else:
            context['categoryid'] = Category.objects.get(id=self.kwargs['category'])
        return context

    def get_queryset(self):
        return Post.objects.filter(category_id=self.kwargs['category'])


def subscribe(request, category):
    # getemail = request.user.email
    # print('наш полученный емаил', getemail)

    myuser = request.user
    cat = Category.objects.get(id=category)
    # print('наша категория', dir(cat))
    cat.subscribers.add(myuser)
    return redirect(f'/news/category/{category}')


def subscribebed(request, category):
    # getemail = request.user.email
    # print('наш полученный емаил', getemail)
    myuser = request.user
    cat = Category.objects.get(id=category)
    cat.subscribers.remove(myuser)
    cat.save()
    print('fffffffffffffffffff')
    return redirect(f'/news/category/{category}')