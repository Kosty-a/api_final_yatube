from django.urls import include, path
from rest_framework import routers

from .views import (CommentViewSet, FollowListCreateAPIView, GroupViewSet,
                    PostViewSet)

router_1 = routers.DefaultRouter()
router_1.register('posts', PostViewSet)
router_1.register('groups', GroupViewSet)

router_2 = routers.DefaultRouter()
router_2.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_1.urls)),
    path('v1/posts/<int:post_id>/', include(router_2.urls)),
    path('v1/follow/', FollowListCreateAPIView.as_view()),
    path('v1/', include('djoser.urls.jwt')),
]
