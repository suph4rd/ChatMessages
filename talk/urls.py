from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from . import views

router = DefaultRouter()
router.register(r'messages', views.MessagesViewSet, basename='messages-watch')
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    url(r'', include(router.urls)),
]
