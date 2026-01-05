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
        slug_field="name",
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Message
        fields = (
            "id",
            "created_at",
            "user",
            "text",
            "text_preview",
            "tags"
        )
        read_only_fields = (
            "id",
            "user",
            "text_preview",
            "created_at"
        )
        extra_kwargs = {"text": {"write_only": True}}


class MessageDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = ListSerializer(child=serializers.CharField(source="name"))

    class Meta:
        model = Message
        fields = ("id", "created_at", "text", "user", "tags")
