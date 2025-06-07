from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        return super().authenticate(request)
