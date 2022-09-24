from django.urls import include, path, re_path
from users.views import SubscriptionsAPIView, SubscribeAPIView

urlpatterns = [
    path('users/subscriptions/', SubscriptionsAPIView.as_view()),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/', SubscribeAPIView.as_view()),
]
