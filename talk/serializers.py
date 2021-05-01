from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Messages
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
