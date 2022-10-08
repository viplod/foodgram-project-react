from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import AuthorOrReadonly
from .filters import IngredientFilter, RecipeFilter
from .models import (
    FavoriteRecipe, Ingredient, IngredientInRecipe, Recipe, ShoppingRecipe,
    Tag,
)
from .pagination import RecipePagination
from .serializers import (
    IngredientsSerializer, RecipesSerializer, TagsSerializer
)
from .services import get_text_on_print


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вью сет для работы с тегами"""
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    permission_classes = (AuthorOrReadonly, )


class RecipesViewSet(viewsets.ModelViewSet):
    """Вью сет для работы с рецептами"""
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (AuthorOrReadonly, )
    pagination_class = RecipePagination
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @staticmethod
    def __add_or_delete_record(model, user, method, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        if method == 'POST':
            model.objects.create(user=user, recipe=recipe)
            serializer = RecipesSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)
        model.objects.filter(
            user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            url_path='favorite',
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated],
            )
    def favorite(self, request, pk=None):
        user = request.user
        method = request.method
        return RecipesViewSet.__add_or_delete_record(
            FavoriteRecipe, user, method, pk
        )

    @action(detail=True,
            url_path='shopping_cart',
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated],
            )
    def shopping_cart(self, request, pk=None):
        user = request.user
        method = request.method
        return RecipesViewSet.__add_or_delete_record(
            ShoppingRecipe, user, method, pk)

    @action(detail=False,
            url_path='download_shopping_cart',
            methods=['get'],
            permission_classes=[IsAuthenticated],
            )
    def download_shopping_cart(self, request):
        ingredient_all = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(sum_amount=Sum('amount'))
        text_on_print = get_text_on_print(ingredient_all)
        response = HttpResponse(text_on_print, 'Content-type: text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.txt"')
        return response


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вью сет для работы с ингредиентами"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = (AuthorOrReadonly, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = IngredientFilter
