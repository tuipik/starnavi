from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet
from likes.views import LikeView

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")

app_name = "post"

urlpatterns = [
    path("posts/<int:pk>/like/", LikeView.as_view()),
    path("", include(router.urls)),
]
