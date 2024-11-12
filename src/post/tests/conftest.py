import pytest
from post.models import Post

@pytest.fixture
def create_post():
    return Post.objects.create(author_id=1, content="Sample Content")
