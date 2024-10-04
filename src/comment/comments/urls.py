from django.urls import path
from .views import create_comment, CommentList


urlpatterns = [
    path('comment/', create_comment, name='create_comment'),
    path('comments/', CommentList.as_view(), name='comment-list'),

]
