from django.urls import path
from .views import create_comment, delete_comment, comment_by_post_id, CommentList


urlpatterns = [
    path('comment/list/', CommentList.as_view(), name='comment_list'),
    path('comment/<int:post_id>/comments/', comment_by_post_id, name='comment_by_post_id'),
    path('comment/create/<int:post_id>', create_comment, name='create_comment'),
    path('comment/delete/<int:comment_id>', delete_comment, name='delete_comment'),
]
