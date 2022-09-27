from django_filters import rest_framework as filters

from .models import Ingredient, Recipe
from users.models import User


class RecipeFilter(filters.FilterSet):
    """Кастомный фильтр для модели Recipe"""
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'tags')

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value is True:
            return queryset.filter(favorite__user=self.request.user)
        return queryset


class IngredientFilter(filters.FilterSet):
    """Кастомный фильтр для модели Ingredient"""
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )
