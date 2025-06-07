from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden
from django.http import JsonResponse

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define allowed access hours
        start_time = time(18, 0)  # 6 PM
        end_time = time(21, 0)    # 9 PM
        now = datetime.now().time()

        # Restrict access to URLs starting with "/api/chats" (you can adjust this path)
        if request.path.startswith('/api/') and not (start_time <= now <= end_time):
            return HttpResponseForbidden("Chat access is only allowed between 6 PM and 9 PM.")

        return self.get_response(request)

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
