from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Contact Service API",
        "endpoints": {
            "POST /api/contact": "Отправка сообщения"
        },
        "docs": "Смотри README.md"
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]