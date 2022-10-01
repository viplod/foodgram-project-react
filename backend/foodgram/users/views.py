from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from users.permissions import AuthorOrReadonly
from .models import Follow, User
from .serializers import FollowingSerializer, FollowSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    """Вье сет для отображения подписок, для подписки и отписки от авторов"""
    serializer_class = FollowingSerializer
    permission_classes = (AuthorOrReadonly, )

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    @action(detail=True,
            permission_classes=[AuthorOrReadonly],
            )
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            data = {'user': request.user.id, 'author': author.id}
            serializer = FollowSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        follow = get_object_or_404(
            Follow, user=request.user, author=author
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
