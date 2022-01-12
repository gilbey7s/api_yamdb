from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet,
                    TitleViewSet, GenreViewSet, 
                    APIsignup, APIusers, APIgetToken
                )

router_v1 = DefaultRouter()

app_name = 'api'

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', APIusers, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', APIgetToken.as_view(), name='token'),
    path('v1/auth/signup/', APIsignup.as_view(), name='signup'),
    path('v1/', include(router_v1.urls)),
]

