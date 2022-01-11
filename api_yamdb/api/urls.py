from django.urls import include, path
<<<<<<< HEAD
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TitleViewSet, GenreViewSet

router_v1 = DefaultRouter()

app_name = 'api'

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
=======
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

from .views import APIsignup, APIusers, APIgetToken


router_v1_users = SimpleRouter()
app_name = 'api'
router_v1_users.register('users', APIusers, basename='users')

urlpatterns = [
    path('v1/auth/token/', APIgetToken.as_view(), name='token'),
    path('v1/auth/signup/', APIsignup.as_view(), name='signup'),
    path('v1/', include(router_v1_users.urls)),
]
>>>>>>> feature/users
