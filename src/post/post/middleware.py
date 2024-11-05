import logging
from django.http import JsonResponse
from .tasks import verify_token
from django.core.cache import cache

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'error': 'Token missing'}, status=401)

        token = token.replace('Bearer ', '').strip()
        cache_key = f"token_verification_{token}"

        verified_data = cache.get(cache_key)
        
        if verified_data is None:
            verification_task = verify_token.delay(token)
            try:
                verified_data = verification_task.get(timeout=15)
                if verified_data:
                    cache.set(cache_key, verified_data, timeout=300) 
            except Exception as e:
                logging.error(f"Token validation error: {str(e)}")
                return JsonResponse({'error': 'Token validation failed'}, status=401)

        if not verified_data or not verified_data.get('valid'):
            logging.error(f"Token validation failed: {verified_data}")
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)

        request.user_data = verified_data
        return self.get_response(request)