from django.views.generic import ListView,DetailView,UpdateView,DeleteView
from .models import Post,Category
from django.shortcuts import render
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm

class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-insertdt']
    paginate_by = 2
    # queryset = Post.objects.order_by('-insertdt')



class PostContent(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

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
class CreatePost(ListView):
    model = Post
    template_name = 'create_post.html'
    context_object_name = 'posts'
    form_class=PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']=Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

class PostUpdate(UpdateView):
    template_name = 'create_post.html'
    form_class = PostForm
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    template_name = 'delete_post.html'
    queryset = Post.objects.all()
    success_url='/posts/'