
# this middleware for add the custom header in response
class CustomHeaderMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        response = self.get_response(request)
        response['X-API-Version'] = '1.0'
        return response