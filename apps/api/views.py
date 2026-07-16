import logging
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import ContactSerializer
from apps.services.email_service import email_service
from apps.services.ai_service import ai_service
from apps.core.decorators import rate_limit
from django.conf import settings

logger = logging.getLogger(__name__)

class ContactView(APIView):
    @extend_schema(
        request=ContactSerializer,
        responses={
            201: OpenApiResponse(
                description='Успешно отправлено',
                response={
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'string'},
                        'request_id': {'type': 'string'},
                        'message': {'type': 'string'},
                        'sentiment': {'type': 'string'},
                        'auto_reply': {'type': 'string', 'nullable': True},
                    }
                }
            ),
            400: OpenApiResponse(description='Ошибка валидации'),
            429: OpenApiResponse(description='Слишком много запросов'),
            500: OpenApiResponse(description='Внутренняя ошибка'),
        }
    )
    @rate_limit(
        requests_limit=settings.RATE_LIMIT_REQUESTS,
        period=settings.RATE_LIMIT_PERIOD
    )
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Validation error: {serializer.errors}")
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        request_id = str(uuid.uuid4())[:8]
        
        sentiment_result = ai_service.analyze_sentiment(validated_data['comment'])
        sentiment = sentiment_result.get('sentiment', 'neutral')
        auto_reply = ai_service.generate_reply(validated_data['comment'])
        
        email_sent = email_service.send_contact_notification(validated_data)
        if not email_sent:
            logger.warning(f"Email sending failed for request {request_id}")
        
        logger.info(
            f"Contact request {request_id} from {validated_data['email']}",
            extra={
                'request_id': request_id,
                'email': validated_data['email'],
                'sentiment': sentiment,
                'ai_source': sentiment_result.get('source', 'unknown')
            }
        )
        
        return Response({
            'status': 'success',
            'request_id': request_id,
            'message': 'Ваше сообщение успешно отправлено!',
            'sentiment': sentiment,
            'auto_reply': auto_reply,
        }, status=status.HTTP_201_CREATED)