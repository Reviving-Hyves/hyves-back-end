from django.urls import path
from .views import create_post, delete_post

urlpatterns = [
    path('post/create/', create_post, name='create_post'),
    path('post/delete/<int:post_id>', delete_post, name='delete_post'),
]