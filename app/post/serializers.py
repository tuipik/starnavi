from rest_framework import serializers
from core.models import Post


class PostSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Post
        fields = (
            "id",
            "text",
            "user",
            "created",
            "likes_count",
        )
        read_only_fields = ("id",)
