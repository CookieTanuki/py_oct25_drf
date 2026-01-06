from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ListSerializer

from base.serializers import CreatableSlugRelatedField
from messenger.models import Message, Tag

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
        read_only_fields = fields


class MessageSerializer(serializers.ModelSerializer):
    tags = CreatableSlugRelatedField(
        slug_field="name", many=True, queryset=Tag.objects.all()
    )
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "created_at",
            "user",
            "text",
            "text_preview",
            "tags",
            "image",
            "likes_count",
            "is_liked",
        )
        read_only_fields = ("id", "user", "text_preview", "created_at")
        extra_kwargs = {"text": {"write_only": True}}

    def get_is_liked(self, obj):
        user = self.context["request"].user

        if user.is_authenticated:
            return user in obj.likes.all()

        return False


class MessageDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = ListSerializer(child=serializers.CharField(source="name"))
    likes = UserSerializer(many=True)

    class Meta:
        model = Message
        fields = ("id", "created_at", "text", "user", "tags", "likes")
