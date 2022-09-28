from django.contrib import admin

from .models import (
    FavoriteRecipe, Ingredient, IngredientInRecipe, Recipe, ShoppingRecipe,
    Tag, TagRecipe,
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройка отображенения модели Recipe в админ-панели"""
    list_display = ('name', 'author', 'image', 'text',
                    'cooking_time', 'count_favorited',)
    list_filter = ('name', 'author', 'tags')

    readonly_fields = ('count_favorited',)

    def count_favorited(self, obj):
        return obj.favorite.count()

    count_favorited.short_description = 'Добавлен в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка отображенения модели Ingredient в админ-панели"""
    list_filter = ('name',)
    list_display = ('name', 'measurement_unit',)


@admin.register(Tag, IngredientInRecipe, TagRecipe, FavoriteRecipe,
                ShoppingRecipe)
class PersonAdmin(admin.ModelAdmin):
    pass
