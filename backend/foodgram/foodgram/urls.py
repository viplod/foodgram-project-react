from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
# from recipes.views import IngredientsViewSet, RecipesViewSet, TagsViewSet
# from rest_framework import routers


# router = routers.DefaultRouter()
# router.register(r'recipes', RecipesViewSet)
# router.register(r'tags', TagsViewSet)
# router.register(r'ingredients', IngredientsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    re_path(r'^api/auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
