from rest_framework import serializers
from core.models import Post


class PostSerializer(serializers.ModelSerializer):

    total_likes = serializers.SerializerMethodField(read_only=True)
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Post
        fields = (
            "id",
            "text",
            "user",
            "created",
            "total_likes",
            "likes",
        )
        read_only_fields = ("id", "likes",)

    def get_total_likes(self, obj):
        return obj.likes.count()
