from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status

from base.mixins import ActionSerializerMixin
from messenger.filters import MessageFilter
from messenger.models import Message
from messenger.serializers import MessageSerializer, MessageDetailSerializer


class MessageViewSet(ActionSerializerMixin, ModelViewSet):
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["tags__name", "user__username", "text"]
    ordering_fields = ["created_at"]
    filterset_class = MessageFilter
    pagination_class = LimitOffsetPagination

    serializer_class = MessageSerializer
    action_serializers = {"retrieve": MessageDetailSerializer}

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Message.objects.all()

        match self.action:
            case "retrieve":
                queryset = queryset.select_related("user")
            case "list":
                queryset = queryset.prefetch_related("likes", "tags")

        return queryset

    @action(
        methods=["POST"],
        detail=True,
        url_path="like",
    )
    def toggle_like(self, request, pk=None):
        message = self.get_object()
        user = request.user
        if message.likes.filter(id=user.id).exists():
            message.likes.remove(user)
            liked = False
        else:
            message.likes.add(user)
            liked = True

        return Response(
            {"id": message.id, "is_liked": liked, "likes_count": message.likes.count()},
            status=status.HTTP_200_OK,
        )
