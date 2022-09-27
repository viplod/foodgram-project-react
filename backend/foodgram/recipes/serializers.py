import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import (FavoriteRecipe, Ingredient,
                     IngredientInRecipe, Recipe, Tag,
                     ShoppingRecipe)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagsSerializer(serializers.ModelSerializer):
    """Сериалиатор для упаковки тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsInRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью IngredientsInRecipes"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериалиатор для упаковки ингредиентов"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для упаковки рецептов"""
    tags = TagsSerializer(many=True, read_only=True)
    ingredients = IngredientsInRecipesSerializer(
        many=True,
        source='ingredientinrecipe',
        read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name',
                  'image', 'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingRecipe.objects.filter(
            recipe=obj, user=request.user).exists()

    def create(self, validated_data):
        tags = self.initial_data['tags']
        recipe = Recipe.objects.create(**validated_data)
        if tags:
            for tag in tags:
                recipe.tags.add(tag)
        ingredients = self.initial_data['ingredients']
        if ingredients:
            for ingredient in ingredients:
                IngredientInRecipe.objects.create(
                    recipe=recipe,
                    ingredient_id=ingredient['id'],
                    amount=ingredient['amount']
                )
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        tags = self.initial_data['tags']
        if tags:
            for tag in tags:
                instance.tags.add(tag)
        ingredients = self.initial_data['ingredients']
        if ingredients:
            for ingredient in ingredients:
                IngredientInRecipe.objects.create(
                    recipe=instance,
                    ingredient_id=ingredient['id'],
                    amount=ingredient['amount']
                )
        return super().update(instance, validated_data)


class FollowRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для упаковки рецептов в Follow"""
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
