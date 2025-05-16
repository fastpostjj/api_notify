from django.urls import path
from rest_framework.routers import DefaultRouter
from api_notify.views import MessageCreateAPIView

router = DefaultRouter()

urlpatterns = [
    path('notify/', MessageCreateAPIView.as_view(), name='message_create'),
] + router.urls
