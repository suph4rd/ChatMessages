from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from . import models
from . import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action


class MessagesViewSet(viewsets.ModelViewSet):
    queryset = models.Messages.objects.all()
    serializer_class = serializers.MessagesSerializer

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(123)
        return super().list(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def all_from_me(self, request):
        user = self.request.user
        serializer = self.serializer_class(self.queryset.filter(author=user), many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def all_for_me(self, request):
        user = self.request.user
        serializer = self.serializer_class(self.queryset.filter(target=user), many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def from_me_to(self, request, pk):
        user = self.request.user
        serializer = self.serializer_class(self.queryset.filter(author=user, target=pk), many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def for_me_from(self, request, pk):
        user = self.request.user
        serializer = self.serializer_class(self.queryset.filter(target=user, author=pk), many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
