from django.db import models
from django.core.validators import FileExtensionValidator


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
    attachment = models.FileField(
        upload_to="attachments/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "gif", "txt"]
            )
        ],
    )

    def save(self, *args, **kwargs):
        self.is_reply = bool(self.parent_comment)
        super().save(*args, **kwargs)
