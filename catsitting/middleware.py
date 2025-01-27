from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class CustomCORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Request received: {request.method} {request.path}")
        if request.method == "OPTIONS":
            print("CORS Preflight request detected")
        response = self.get_response(request)
        return response

    def process_request(self, request):
        if request.method == "OPTIONS":
            response = JsonResponse({"detail": "CORS preflight passed"})
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            return response
