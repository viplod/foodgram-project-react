from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer)
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

import recipes
from recipes.models import Recipe
from .models import Follow, User


class UserSerializer(BaseUserSerializer):
    """
    Изменение сериализатора djoser работы с моделью User
    для отображение дополнительных полей.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj).exists()


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Изменение сериализатора djoser работы с моделью User
    при создании нового пользователя для отображение дополнительных полей.
    """
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'password')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор модели Follow"""
    class Meta:
        model = Follow
        fields = ('user', 'author')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = FollowingSerializer(
            instance,
            context=context
        )
        print(serializer.data)
        return serializer.data


class FollowingSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Follow с рецептами"""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta():
        model = Follow
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Follow.objects.filter(
            user=request.user, author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        if recipes_limit:
            queryset = Recipe.objects.filter(
                author=obj.author)[:int(recipes_limit)]
        else:
            queryset = Recipe.objects.filter(author=obj.author)
        recipes_serializer = recipes.serializers.FollowRecipeSerializer(
            queryset, many=True, read_only=True)
        return recipes_serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
