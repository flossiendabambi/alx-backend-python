from datetime import datetime, time
from django.http import HttpResponseForbidden

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
