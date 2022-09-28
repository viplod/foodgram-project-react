from django.urls import include, path, re_path

# from users.views import SubscribeAPIView, SubscriptionsAPIView
from users.views import SubscribeViewSet

urlpatterns = [
    # path('users/', SubscribeViewSet.as_view()),
    # path('users/subscriptions/', SubscriptionsAPIView.as_view()),
    path('users/', SubscribeViewSet.as_view(
        {'get': 'list'}
        )
    ),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('users/<int:pk>/subscribe/', SubscribeAPIView.as_view()),
]
