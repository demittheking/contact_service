import logging
import uuid
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request_id = str(uuid.uuid4())[:8]
        request.request_id = request_id
        logger.info(f"Request {request_id}: {request.method} {request.path}")
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'request_id'):
            logger.info(f"Response {request.request_id}: {response.status_code}")
        return response