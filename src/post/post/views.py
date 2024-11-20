from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostSerializer
from .decorators import require_authentication

@api_view(['POST'])
@require_authentication
def create_post(request) -> Response:
    if not request.data:
        return Response(
            {'error': 'No data provided.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
        
    post_data = {
        **request.data,
        'author_id': request.user_id
    }
    
    serializer = PostSerializer(data=post_data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@require_authentication
def delete_post(request, post_id: int) -> Response:
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    post.delete()
    return Response(status=status.HTTP_200_OK)
    
@api_view(['GET'])
@require_authentication
def list_posts(request) -> Response:
    posts = Post.objects.all().order_by('-created_at')
    paginator = PageNumberPagination()
    paginator.page_size = 30
    
    result_page = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
