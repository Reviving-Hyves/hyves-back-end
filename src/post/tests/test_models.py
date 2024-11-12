import pytest
from post.models import Post

@pytest.mark.django_db
def test_post_str(create_post):
    assert str(create_post) == f"Post by {create_post.author_id} at {create_post.created_at}"

@pytest.mark.django_db
def test_delete_post(create_post):
    create_post.delete()
    assert Post.objects.count() == 0 
