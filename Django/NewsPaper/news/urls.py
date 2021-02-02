from django.urls import path
from .views import PostList,PostContent

urlpatterns = [
    path('',PostList.as_view()),
    path('<int:pk>',PostContent.as_view())
]