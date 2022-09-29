from django.urls import include, path, re_path

from users.views import SubscribeViewSet

urlpatterns = [
    path('users/subscriptions/', SubscribeViewSet.as_view(
        {'get': 'list'}
        )
    ),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/', SubscribeViewSet.as_view(
        {
            'post': 'subscribe',
            'delete': 'subscribe'
        }
    )),
]
