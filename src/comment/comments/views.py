from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Comments
from .serializers import CommentSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Comments
from .serializers import CommentSerializer

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

class CommentList(generics.ListAPIView):
    queryset = Comments.objects.all() 
    serializer_class = CommentSerializer  