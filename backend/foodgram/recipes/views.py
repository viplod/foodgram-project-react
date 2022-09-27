from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import AuthorOrReadonly
from .pagination import RecipePagination
from django.http.response import HttpResponse
from rest_framework.permissions import IsAuthenticated

from .filters import RecipeFilter, IngredientFilter
from .models import (Ingredient, IngredientInRecipe, FavoriteRecipe,
                     Recipe, ShoppingRecipe, Tag)
from .serializers import (IngredientsSerializer,
                          RecipesSerializer,
                          TagsSerializer)


class TagsViewSet(viewsets.ModelViewSet):
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

    @action(detail=True,
            url_path='favorite',
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated],
            )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
            serializer = RecipesSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)
        FavoriteRecipe.objects.filter(
            user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            url_path='shopping_cart',
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated],
            )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            ShoppingRecipe.objects.create(user=request.user, recipe=recipe)
            serializer = RecipesSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)
        ShoppingRecipe.objects.filter(
            user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            url_path='download_shopping_cart',
            methods=['get'],
            permission_classes=[IsAuthenticated],
            )
    def download_shopping_cart(self, request):
        recipes_all = request.user.shopping_cart.all()
        list_ingredients = {}
        for recipe_one in recipes_all:
            ingredients = IngredientInRecipe.objects.filter(
                recipe=recipe_one.recipe
            )
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                amount = ingredient.amount
                measuerment_unit = ingredient.ingredient.measurement_unit
                if name not in list_ingredients:
                    list_ingredients[name] = {
                        'amount': amount,
                        'measurement_unit': measuerment_unit
                    }
                else:
                    list_ingredients[name]['amount'] += amount
        on_print = []
        for elem in list_ingredients:
            on_print.append(f'{elem.capitalize()} '
                            f'({list_ingredients[elem]["measurement_unit"]}) '
                            f'- {list_ingredients[elem]["amount"]} \n')
        response = HttpResponse(on_print, 'Content-type: text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.txt"')

        return response


class IngredientsViewSet(viewsets.ModelViewSet):
    """Вью сет для работы с ингредиентами"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = (AuthorOrReadonly, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = IngredientFilter
