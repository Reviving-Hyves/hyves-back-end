from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from typing import Callable

def require_authentication(view_func: Callable) -> Callable:
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_data = getattr(request, 'user_data', None)
        
        if not user_data:
            return Response(
                {"error": "User authentication failed"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
        request.user_id = user_data.get('user_id')
        
        return view_func(request, *args, **kwargs)
    return wrapper