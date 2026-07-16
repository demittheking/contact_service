from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class RateLimitExceeded(Exception):
    pass

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is None:
        if isinstance(exc, RateLimitExceeded):
            return Response(
                {'error': 'Слишком много запросов. Попробуйте позже.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return Response(
            {'error': 'Внутренняя ошибка сервера'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response