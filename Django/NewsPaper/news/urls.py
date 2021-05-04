from django.urls import path
from .views import StopADDViev,PostList,PostContent,SearchList,CreatePost,PostUpdate,PostDeleteView,CategoryList,subscribe,subscribebed
from django.views.decorators.cache import cache_page
urlpatterns = [
    path('',cache_page(60)(PostList.as_view())),
    path('<int:pk>',cache_page(60*5)(PostContent.as_view()),name='post_detail'),
    path('search/',SearchList.as_view()),
    path('add/',CreatePost.as_view(),name='create_post'),
    path('<int:pk>/edit',PostUpdate.as_view(),name='edit_post'),
    path('<int:pk>/delete',PostDeleteView.as_view(),name='delete_post'),
    path('category/<int:category>/',cache_page(60*5) (CategoryList.as_view()), name='category'),
    path('subscribe/<int:category>/', subscribe, name='subscribe'),
    path('subscribebed/<int:category>/', subscribebed, name='subscribebed'),
    path('stopadd/', StopADDViev.as_view(), name='stop_add'),

]