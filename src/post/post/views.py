from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Post
from rest_framework.response import Response
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@api_view(['POST'])
def create_post(request):
    if not request.data:
        return Response({'error': 'No data provided.'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data.copy()
    serializer = PostSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({**serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_200_OK)