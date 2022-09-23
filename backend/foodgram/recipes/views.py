from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import AdminOrReadonly

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
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True, url_path='favorite', methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        print(request)
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
            serializer = RecipesSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)
        FavoriteRecipe.objects.filter(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = (AdminOrReadonly, )
