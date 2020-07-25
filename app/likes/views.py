from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.models import Like, Post


class LikeView(APIView):
    authentication_class = JSONWebTokenAuthentication
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = self.request.user
        post = Post.objects.filter(id=pk).first()
        Like.objects.get_or_create(user=user, post=post)

        return Response(200)

    def delete(self, request, pk):
        user = self.request.user
        post = Post.objects.filter(id=pk).first()
        Like.objects.filter(user=user, post=post).delete()

        return Response(200)
