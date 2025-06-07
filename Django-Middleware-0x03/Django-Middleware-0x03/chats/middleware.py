from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.http import JsonResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Open the log file in append mode
        self.log_file = "requests.log"

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        
        with open(self.log_file, "a") as f:
            f.write(log_message)

        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = {}  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/messages/'):
            ip = self.get_client_ip(request)
            now = datetime.now()
            window_start = now - timedelta(minutes=1)

            # Initialize if not existing
            if ip not in self.message_counts:
                self.message_counts[ip] = []

            # Remove messages outside the 1-minute window
            self.message_counts[ip] = [
                timestamp for timestamp in self.message_counts[ip]
                if timestamp > window_start
            ]

            if len(self.message_counts[ip]) >= 5:
                return JsonResponse(
                    {'error': 'Rate limit exceeded: Max 5 messages per minute.'},
                    status=429
                )

            self.message_counts[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Try headers first in case of reverse proxy
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check authenticated users
        if request.user.is_authenticated:
            # You can adjust path checking to match protected routes
            if request.path.startswith('/api/messages/') and request.method in ['POST', 'PUT', 'DELETE']:
                user_role = getattr(request.user, 'role', 'user')
                if user_role not in ['admin', 'moderator']:
                    return JsonResponse(
                        {"error": "You do not have permission to perform this action."},
                        status=403
                    )

        return self.get_response(request)