import time


class StatsMiddleware:
    # Middleware to add header that shows execution time
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        response["X-Data-Generation-Duration-ms"] = int(duration * 1000)
        return response

# Source: https://stackoverflow.com/questions/47937566/how-to-calculate-response-time-in-django-python
