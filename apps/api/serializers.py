from rest_framework import serializers
import re

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=100)
    phone = serializers.CharField(min_length=10, max_length=20)
    email = serializers.EmailField()
    comment = serializers.CharField(min_length=1, max_length=1000)
    
    def validate_phone(self, value):
        cleaned = re.sub(r'[\s\-\(\)]', '', value)
        if not re.match(r'^\+?\d{10,15}$', cleaned):
            raise serializers.ValidationError(
                'Неверный формат телефона. Используйте +7XXXXXXXXXX'
            )
        return value
    
    def validate(self, data):
        data['name'] = data['name'].strip()
        data['comment'] = data['comment'].strip()
        return data