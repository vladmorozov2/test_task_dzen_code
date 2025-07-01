from django.db import models
from django.core.validators import URLValidator, RegexValidator


class Comment(models.Model):
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )
    is_reply = models.BooleanField(default=False)
    sender = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    
