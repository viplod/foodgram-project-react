from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.serializers import UserSerializer
from .models import (
    FavoriteRecipe, Ingredient, IngredientInRecipe, Recipe, ShoppingRecipe,
    Tag,
)
from .fields import Base64ImageField


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

        validators = (
            UniqueTogetherValidator(
                queryset=IngredientInRecipe.objects.all(),
                fields=('ingredient', 'recipe')
            ),
            MinValueValidator(
                1,
                'Количество ингредиента должно быть больше 1'
            )
        )


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

    @staticmethod
    def __create_ingredient(recipe, ingredients):
        list_obj = []
        if ingredients:
            for ingredient in ingredients:
                list_obj.append(IngredientInRecipe(
                    recipe=recipe,
                    ingredient_id=ingredient['id'],
                    amount=ingredient['amount']
                ))
            IngredientInRecipe.objects.bulk_create(list_obj)

    def create(self, validated_data):
        tags = self.initial_data['tags']
        recipe = Recipe.objects.create(**validated_data)
        if tags:
            for tag in tags:
                recipe.tags.add(tag)
        ingredients = self.initial_data['ingredients']
        result = self.__create_ingredient(recipe, ingredients)
        raise ValueError(f'Результат {result}')
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        tags = self.initial_data['tags']
        if tags:
            for tag in tags:
                instance.tags.add(tag)
        ingredients = self.initial_data['ingredients']
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        self.__create_ingredient(instance, ingredients)
        return super().update(instance, validated_data)
