from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import AdminOrReadonly
from .pagination import RecipePagination

from .filters import RecipeFilter, IngredientFilter
from .models import Ingredient, FavoriteRecipe, Recipe, Tag
from .serializers import (IngredientsSerializer,
                          RecipesSerializer,
                          TagsSerializer)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    permission_classes = (AdminOrReadonly, )


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (AdminOrReadonly, )
    pagination_class = RecipePagination
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True,
            url_path='favorite',
            methods=['post', 'delete'],
            # permission_classes=[is_authenticated],
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


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = (AdminOrReadonly, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = IngredientFilter