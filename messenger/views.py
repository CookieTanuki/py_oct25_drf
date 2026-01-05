from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from base.mixins import ActionSerializerMixin
from messenger.filters import MessageFilter
from messenger.models import Message
from messenger.serializers import MessageSerializer, MessageDetailSerializer


class MessageViewSet(
    ActionSerializerMixin,
    ModelViewSet
):
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    search_fields = ["tags__name", "user__username", "text"]
    ordering_fields = ["created_at"]
    filterset_class = MessageFilter
    pagination_class = LimitOffsetPagination

    serializer_class = MessageSerializer
    action_serializers = {
        "retrieve": MessageDetailSerializer
    }

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Message.objects.all()

        match self.action:
            case "retrieve":
                queryset = queryset.select_related("user")

        return queryset
