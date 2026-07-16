import logging
import openai
from django.conf import settings
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        # Для версии 0.28.0 используем старый синтаксис
        openai.api_key = self.api_key if self.api_key else None
        
    def analyze_sentiment(self, text: str) -> Dict[str, str]:
        if not self.api_key:
            logger.warning("OpenAI API key not configured, using fallback")
            return self._fallback_analysis(text)
        
        try:
            # Старый синтаксис для openai 0.28.0
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты анализируешь тональность комментария. Ответь строго одним словом: positive, negative или neutral."},
                    {"role": "user", "content": f"Проанализируй тональность: {text}"}
                ],
                max_tokens=10,
                temperature=0.3,
                timeout=5.0
            )
            
            sentiment = response.choices[0].message.content.strip().lower()
            if sentiment not in ['positive', 'negative', 'neutral']:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'confidence': 0.8,
                'source': 'openai'
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._fallback_analysis(text)
    
    def generate_reply(self, text: str) -> Optional[str]:
        if not self.api_key:
            return None
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты - менеджер по продажам. Ответь вежливо и предложи помощь. Ответ должен быть кратким (2-3 предложения)."},
                    {"role": "user", "content": f"Пользователь написал: {text}. Напиши ответ."}
                ],
                max_tokens=100,
                temperature=0.7,
                timeout=5.0
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI reply generation error: {e}")
            return None
    
    def _fallback_analysis(self, text: str) -> Dict[str, str]:
        positive_words = ['хорош', 'отличн', 'прекрасн', 'классн', 'замечательн', 'спасиб']
        negative_words = ['плох', 'ужасн', 'отвратительн', 'негативн', 'проблем']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = 'positive'
        elif neg_count > pos_count:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'confidence': 0.5,
            'source': 'fallback'
        }

ai_service = AIService()