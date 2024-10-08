from django.urls import path
from .views import create_comment, CommentList


urlpatterns = [
    path('comment/comment/<int:post_id>', create_comment, name='create_comment'),
    path('comment/comments/', CommentList.as_view(), name='comment-list'),

]
