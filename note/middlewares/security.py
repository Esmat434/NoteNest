
# this middleware for increase scutrity with add scurity headers
class SecurityMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        response = self.get_response(request)

        # prevent from guissing mime type attack
        response['X-Content-Type-Options'] = 'nosniff'

        # prevent from clickjacking attack
        response['X-Frame-Options'] = 'DENY'

        # prevent from XSS attack
        response['X-XSS-Protection'] = '1; mode=block'
        
        #  prevent from caching the sensitive pages
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        # limit send information in header Referrer
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # prevent from sensitives ability of browser
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response