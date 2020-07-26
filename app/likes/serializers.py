from rest_framework import serializers
from core.models import Like


class LikeSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source="user.id")
    post = serializers.ReadOnlyField(source="post.id")

    class Meta:
        model = Like
        fields = (
            "user",
            "post",
            "created",
        )
        read_only_fields = ("id",)
