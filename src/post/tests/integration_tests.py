import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from post.models import Post
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_post():
    user = User.objects.create_user(username='nickw', password='testtest')
    
    client = APIClient()
    client.force_authenticate(user=user)
    
    url = reverse('create_post')
    data = {
        'content': 'Integration test post'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 401
    assert Post.objects.count() == 0

@pytest.mark.django_db
def test_delete_post():
    user = User.objects.create_user(username='nickw', password='testtest')
    
    post = Post.objects.create(author_id=user.id, content='Test post content')
    
    client = APIClient()
    client.force_authenticate(user=user)
    
    url = reverse('delete_post', args=[post.id])
    
    response = client.delete(url)
    
    assert response.status_code == 401
    assert Post.objects.count() == 1