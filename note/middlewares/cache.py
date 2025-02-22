from django.core.cache import cache

# this middleware cache responses for good performance
class CacheMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        cache_key = request.path
        response = cache.get(cache_key)

        if not response:
            response = self.get_response(request)
            cache.set(cache_key,response,60)
        
        return response