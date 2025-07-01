from rest_framework import serializers
from .models import Comment
from user.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=500)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    parent_comment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), required=False, allow_null=True
    )
    is_reply = serializers.BooleanField(read_only=True)
    sender = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )
    username = serializers.CharField(source="sender.username", read_only=True)
    attachment = serializers.FileField(required=False, allow_null=True)

    def validate_attachment(self, file):
        filename = file.name.lower()

        if filename.endswith(".txt"):
            if file.size > 100 * 1024:
                raise serializers.ValidationError("Text file must be ≤ 100KB")
            return file

        elif filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
            try:
                image = Image.open(file)
                if image.width > 320 or image.height > 240:
                    image.thumbnail((320, 240))
                    buffer = BytesIO()
                    image_format = image.format or "PNG"
                    image.save(buffer, format=image_format)
                    file = ContentFile(buffer.getvalue(), name=file.name)
            except Exception:
                raise serializers.ValidationError("Invalid image file")
            return file

        else:
            raise serializers.ValidationError(
                "Invalid file format. Only JPG, PNG, GIF, or TXT allowed."
            )

    def create(self, validated_data):
        parent_comment = validated_data.get("parent_comment")
        validated_data["is_reply"] = bool(parent_comment)
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        if "attachment" in validated_data:
            instance.attachment = validated_data["attachment"]
        instance.save()
        return instance
