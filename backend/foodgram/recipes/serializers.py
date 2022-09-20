import base64
from django.core.files.base import ContentFile
# from django.shortcuts import get_object_or_404

from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Ingredient, Recipe, Tag, IngredientInRecipe


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagsSerializer(serializers.ModelSerializer):
    """Сериалиатор для упаковки тегов"""
    # name = serializers.CharField(source='name')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериалиатор для упаковки ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для упаковки рецептов"""
    tags = TagsSerializer(many=True, read_only=True)
    ingredients = IngredientsSerializer(many=True, read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name',
                  'image', 'text', 'cooking_time')

    def create(self, validated_data):
        print(self.initial_data)
        tags = self.initial_data['tags']
        recipe = Recipe.objects.create(**validated_data)
        if tags:
            for tag in tags:
                recipe.tags.add(tag)
        recipe.save()
        return recipe


class IngredientsInRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью IngredientsInRecipes"""
    class Meta:
        fields = ('recipe', 'ingredient', 'amount')
        model = IngredientInRecipe
