from rest_framework import viewsets
from users.permissions import AdminOrReadonly

from .models import Recipe, Tag, Ingredient
from .serializers import (RecipesSerializer, TagsSerializer,
                          IngredientsSerializer)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    permission_classes = (AdminOrReadonly, )


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (AdminOrReadonly, )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = (AdminOrReadonly, )
