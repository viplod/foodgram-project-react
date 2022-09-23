from django.contrib import admin

from .models import (Ingredient, Recipe, Tag,
                     IngredientInRecipe, TagRecipe,
                     FavoriteRecipe)


admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(IngredientInRecipe)
admin.site.register(TagRecipe)
admin.site.register(FavoriteRecipe)
