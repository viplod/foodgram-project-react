from djoser.serializers import(
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer)
from rest_framework import serializers, validators

from .models import User


class UserSerializer(BaseUserSerializer):
    """
    Сериализатор для работы с моделью User
    """
    class Meta(BaseUserSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name')


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'password')
