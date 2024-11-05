import logging
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Comments
from .serializers import CommentSerializer

@api_view(['POST'])
def create_comment(request, post_id):
    user_data = getattr(request, 'user_data', None)
    if not user_data:
        return Response(
            {"error": "User authentication failed"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    comment_data = {
        **request.data,
        'post_id': post_id,
        'user_id': user_data.get('user_id')
    }

    serializer = CommentSerializer(data=comment_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
    user_data = getattr(request, 'user_data', None)
    if not user_data:
        return Response(
            {"error": "User authentication failed"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
        
    comments = Comments.objects.filter(post_id=post_id)
    
    if not comments.exists():
            return Response([], status=status.HTTP_200_OK)
    try:
        serializer = CommentSerializer(comments, many=True)
        
        return Response({
            'post_id': post_id,
            'comments': serializer.data,
            'total_comments': len(serializer.data)
        }, status=status.HTTP_200_OK)

    except Comments.DoesNotExist:
        return Response(
            {"error": f"No comments found for post {post_id}"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logging.error(f"Error fetching comments for post {post_id}: {str(e)}")
        return Response(
            {"error": "An error occurred while fetching comments"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# List all comments
class CommentList(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer  