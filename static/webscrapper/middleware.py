import time
import logging

logger = logging.getLogger(__name__)

class TimeLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        total_time = end_time - start_time

        logger.info(f"View '{request.path}' executed in {total_time:.2f} seconds")

        return response
