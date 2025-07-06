# comments/tasks.py
from celery import shared_task
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from .models import Comment


@shared_task
def resize_comment_attachment(comment_id):

    try:
        comment = Comment.objects.get(id=comment_id)
        if not comment.attachment:
            return

        image = Image.open(comment.attachment)
        if image.width > 320 or image.height > 240:
            image.thumbnail((320, 240))
            buffer = BytesIO()
            image_format = image.format or "PNG"
            image.save(buffer, format=image_format)

            comment.attachment.save(
                comment.attachment.name, ContentFile(buffer.getvalue()), save=True
            )
    except Exception as e:
  
        print(f"[resize_comment_attachment] Failed: {e}")
