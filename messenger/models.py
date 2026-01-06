from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages"
    )
    tags = models.ManyToManyField(Tag, related_name="messages")
    image = models.ImageField(upload_to="messages/images/", null=True, blank=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_messages",
        blank=True,
    )

    def __str__(self) -> str:
        return self.text

    @property
    def text_preview(self) -> str:
        max_length = 30

        if len(self.text) <= max_length:
            return self.text

        return f"{self.text[:max_length]}..."
