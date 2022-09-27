from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from users.permissions import AuthorOrReadonly
from .models import Follow, User
from .serializers import FollowSerializer, FollowingSerializer


class SubscriptionsAPIView(ListAPIView):
    """API вью для работы с подпиской на авторов"""
    serializer_class = FollowingSerializer
    permission_classes = (AuthorOrReadonly, )

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class SubscribeAPIView(APIView):
    """API вью для подписки и отписки от авторов"""
    permission_classes = (AuthorOrReadonly, )

    def post(self, request, pk=None):
        author = get_object_or_404(User, pk=pk)
        data = {'user': request.user.id, 'author': author.id}
        serializer = FollowSerializer(
            data=data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        follow = get_object_or_404(
            Follow, user=request.user, author=author
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
