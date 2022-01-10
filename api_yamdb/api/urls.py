from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

from .views import APIsignup, APIusers, APIgetToken


router_v1_users = SimpleRouter()
app_name = 'api'
router_v1_users.register('users', APIusers, basename='users')

urlpatterns = [
    path('v1/auth/token/', APIgetToken.as_view(), name='token'),
    path('v1/auth/signup/', APIsignup.as_view(),  name='signup'),
    path('v1/', include(router_v1_users.urls)),
]
