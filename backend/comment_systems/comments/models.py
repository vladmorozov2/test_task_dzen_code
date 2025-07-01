from django.db import models
from django.core.validators import URLValidator, RegexValidator
from django.core.files.storage import FileSystemStorage
from PIL import Image
from io import BytesIO
import sys
import os
import uuid


def attachment_directory_path(instance, filename):
    # Generate unique filename to prevent conflicts
    ext = os.path.splitext(filename)[1]
    unique_name = f"{uuid.uuid4()}{ext}"
    return f"attachments/{instance.id}/{unique_name}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
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
    # Attachment fields
    attachment = models.FileField(
        upload_to=attachment_directory_path, null=True, blank=True
    )
    attachment_type = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=[
            ("image", "Image"),
            ("text", "Text File"),
        ],
    )
    attachment_name = models.CharField(max_length=255, null=True, blank=True)
    attachment_size = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.sender.username} at {self.created_at}"

    def save(self, *args, **kwargs):
        # If this is a new comment (not updating existing)
        is_new = self.pk is None

        # Save first to get an ID (needed for attachment path)
        if is_new:
            super().save(*args, **kwargs)

        # Process attachment if exists
        if self.attachment:
            # Get file extension
            filename = self.attachment.name
            ext = os.path.splitext(filename)[1].lower()

            # Process images
            if ext in [".jpg", ".jpeg", ".png", ".gif"]:
                self.attachment_type = "image"

                try:
                    # Open image
                    img = Image.open(self.attachment)

                    # Convert to RGB if necessary
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")

                    # Resize if needed
                    max_width, max_height = 320, 240
                    if img.width > max_width or img.height > max_height:
                        # Calculate new size maintaining aspect ratio
                        ratio = min(max_width / img.width, max_height / img.height)
                        new_width = int(img.width * ratio)
                        new_height = int(img.height * ratio)

                        # Resize image
                        img = img.resize((new_width, new_height), Image.LANCZOS)

                        # Save resized image to BytesIO
                        output = BytesIO()

                        # Determine format
                        if ext in [".jpg", ".jpeg"]:
                            format = "JPEG"
                        elif ext == ".png":
                            format = "PNG"
                        else:  # .gif
                            format = "GIF"

                        img.save(output, format=format, quality=90)
                        output.seek(0)

                        # Create new filename with same extension
                        new_filename = f"{os.path.splitext(filename)[0]}{ext}"

                        # Replace the file with resized version
                        self.attachment.save(new_filename, content=output, save=False)

                except Exception as e:
                    # Log error but don't break
                    print(f"Error processing image: {e}")

            # Process text files
            elif ext == ".txt":
                self.attachment_type = "text"

                # Check size
                if self.attachment.size > 100 * 1024:  # 100KB
                    # Delete the invalid attachment
                    self.attachment.delete(save=False)
                    self.attachment = None
                    self.attachment_type = None
                    print("Text file size exceeds 100KB limit")

        # Save attachment metadata
        if self.attachment:
            self.attachment_name = os.path.basename(self.attachment.name)
            self.attachment_size = self.attachment.size

        # Save again to store processed attachment and metadata
        super().save(*args, **kwargs)
