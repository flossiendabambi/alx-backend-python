from datetime import datetime

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
