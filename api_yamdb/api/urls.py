from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIgetToken, APIsignup, UserViewSet, Categories,
                    CategoryDetail, CommentViewSet, GenreDetail, Genres,
                    ReviewViewSet, TitleViewSet)

router_v1 = DefaultRouter()

app_name = 'api'


router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
urlpatterns = [

    path('v1/auth/token/', APIgetToken.as_view(), name='token'),
    path('v1/auth/signup/', APIsignup.as_view(), name='signup'),
    path('v1/categories/<slug>/', CategoryDetail.as_view(), name='category'),
    path('v1/categories/', Categories.as_view(), name='categories'),
    path('v1/genres/', Genres.as_view(), name='genres'),
    path('v1/genres/<slug>/', GenreDetail.as_view(), name='genre'),
    path('v1/', include(router_v1.urls)),

]
