from django.http import JsonResponse

# this middlewate for management the errors and return spesific message
class ErrorHandlingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        try:
            response = self.get_response(request)
        except Exception as e:
            return JsonResponse({"error":e},status = 500)
        return response