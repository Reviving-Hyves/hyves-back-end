from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Comments
from .serializers import CommentSerializer

@api_view(['POST'])
def create_comment(request):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentList(generics.ListAPIView):
    queryset = Comments.objects.all() 
    serializer_class = CommentSerializer  