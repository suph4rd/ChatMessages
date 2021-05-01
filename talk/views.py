from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Messages
from .serializers import MessagesSerializer, UserSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action


class MessagesSendViewSet(viewsets.ModelViewSet):
    serializer_class = MessagesSerializer
    queryset = Messages.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['author'] = self.request.user
        super().create(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    filterset_fields = ['target', 'author']

    @action(methods=['get'], detail=False)
    def all_from_me(self, request):
        user = self.request.user
        serializer = MessagesSerializer(self.queryset.filter(author=user), many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def all_for_me(self, request):
        user = self.request.user
        serializer = MessagesSerializer(self.queryset.filter(target=user), many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def from_me_to(self, request, pk):
        user = self.request.user
        # target = self.request.query_params.get('user')
        serializer = MessagesSerializer(self.queryset.filter(author=user, target=pk), many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def for_me_from(self, request, pk):
        user = self.request.user
        # author = self.request.query_params.get('author')
        serializer = MessagesSerializer(self.queryset.filter(target=user, author=pk), many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
