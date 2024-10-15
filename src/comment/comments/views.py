from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Comments
from .serializers import CommentSerializer

# Create comment
@api_view(['POST'])
def create_comment(request, post_id):
    if request.method == 'POST':
        if post_id is None:
            return Response({'error': 'Please provide post_id'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['post_id'] = post_id

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'post_id': post_id, **serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
# Delete comment 
@api_view(['DELETE'])
def delete_comment(request, comment_id):
    try:
        comment = Comments.objects.get(pk=comment_id)
    except Comments.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_200_OK)

# Get comments by post_id
@api_view(['GET'])
def comment_by_post_id(request, post_id):
    comments = Comments.objects.filter(post_id=post_id)
    serializer = CommentSerializer(comments, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
        

# List all comments
class CommentList(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer  