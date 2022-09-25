from django.contrib import admin

from .models import (Ingredient, Recipe, Tag,
                     IngredientInRecipe, TagRecipe,
                     FavoriteRecipe)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'image', 'text',
                    'cooking_time', 'count_favorited',)
    list_filter = ('name', 'author', 'tags')

    readonly_fields = ('count_favorited',)

    def count_favorited(self, obj):
        return obj.favorite.count()


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name', 'measurement_unit',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientInRecipe)
admin.site.register(TagRecipe)
admin.site.register(FavoriteRecipe)
