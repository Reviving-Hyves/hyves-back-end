import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from post.models import Post
from django.contrib.auth.models import User
from django.test import override_settings

class MockTokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user_data = {'user_id': 1, 'valid': True}
        return self.get_response(request)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(username='nickw', password='testtest')

@pytest.fixture(autouse=True)
def mock_middleware_setting():
    with override_settings(
        MIDDLEWARE=[
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'tests.integration_tests.MockTokenAuthMiddleware',
        ]
    ):
        yield

@pytest.fixture
def authenticated_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer fake-token')
    return api_client

@pytest.mark.django_db
class TestPostAPI:
    def test_create_post_success(self, authenticated_client):
        url = reverse('create_post')
        data = {'content': 'Integration test post'}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1
        post = Post.objects.first()
        assert post.content == 'Integration test post'
        assert post.author_id == 1

    def test_create_post_empty_content(self, authenticated_client):
        url = reverse('create_post')
        data = {'content': ''}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Post.objects.count() == 0

    def test_delete_post_success(self, authenticated_client, test_user):
        post = Post.objects.create(author_id=1, content='Test post content')
        url = reverse('delete_post', args=[post.id])
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert Post.objects.count() == 0

    def test_delete_nonexistent_post(self, authenticated_client):
        url = reverse('delete_post', args=[99999])
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_posts(self, authenticated_client):
        Post.objects.create(author_id=1, content='Test post content')
        url = reverse('list_posts')
        
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['content'] == 'Test post content'