from django.core.cache import cache
from django.http import JsonResponse


# this is for limit the request of user in spesific time
from django.core.cache import cache
from django.http import JsonResponse

class RateLimitingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        key = f'rate_limit_{ip}'
        limit = 100

        # افزایش مقدار به‌صورت اتمی
        current = cache.get_or_set(key, 0, 60)
        new_value = cache.incr(key)

        if new_value > limit:
            return JsonResponse({"error": "Rate limit exceeded"}, status=429)

        return self.get_response(request)
