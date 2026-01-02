from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from messenger.filters import MessageFilter
from messenger.models import Message
from messenger.serializers import MessageSerializer, MessageDetailSerializer


class MessageViewSet(ModelViewSet):
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    search_fields = ["tags__name", "user__username", "text"]
    ordering_fields = ["created_at"]
    filterset_class = MessageFilter

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return MessageDetailSerializer

        return MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all()

        match self.action:
            case "retrieve":
                queryset = queryset.select_related("user")

        return queryset
