from django.urls import path
from .views import PostList,PostContent,SearchList,CreatePost,PostUpdate,PostDeleteView
urlpatterns = [
    path('',PostList.as_view()),
    path('<int:pk>',PostContent.as_view(),name='post_detail'),
    path('search/',SearchList.as_view()),
    path('add/',CreatePost.as_view(),name='create_post'),
    path('<int:pk>/edit',PostUpdate.as_view(),name='edit_post'),
    path('<int:pk>/delete',PostDeleteView.as_view(),name='delete_post')
]