from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register('posts', PostViewSet, basename='post')
router_v1.register('groups', GroupViewSet, basename='group')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
)

urlpatterns = [
    path('v1/api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('v1/', include(router_v1.urls)),
]
