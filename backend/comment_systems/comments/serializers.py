from rest_framework import serializers
from .models import Comment
from user.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import re


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
    ALLOWED_TAGS = ["i", "strong", "code", "a"]
    ALLOWED_ATTRS = ["href", "title"]

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

    def validate_text(self, value):
        errors = []

        # Простий парсер тегів через regex (не ідеально, але достатньо для базової валідації)
        tag_regex = re.compile(r"</?([a-z]+)(\s[^>]*)?>", re.IGNORECASE)
        tags = tag_regex.findall(value)

        stack = []
        for tag_match in tags:
            tag_name = tag_match[0].lower()
            attrs = tag_match[1]

            # Перевірка тегів
            if tag_name not in self.ALLOWED_TAGS:
                errors.append(f"Disallowed HTML tag: <{tag_name}>")
                continue

            # Перевірка атрибутів тільки для <a>
            if tag_name == "a":
                # Перевірка, що атрибути лише href і title
                if attrs:
                    attr_regex = re.compile(
                        r'([a-z-]+)\s*=\s*["\'][^"\']*["\']', re.IGNORECASE
                    )
                    for attr_match in attr_regex.findall(attrs):
                        attr_name = attr_match.lower()
                        if attr_name not in self.ALLOWED_ATTRS:
                            errors.append(
                                f"Disallowed attribute in <a> tag: {attr_name}"
                            )

                # Перевірка що href існує і є валідним посиланням
                href_match = re.search(
                    r'href\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE
                )
                if not href_match:
                    errors.append("<a> tag must have href attribute")
                else:
                    href = href_match.group(1)
                    if not self.is_valid_url(href):
                        errors.append(f"Invalid URL in href attribute: {href}")
            else:
                # Для інших тегів атрибути заборонені
                if attrs.strip():
                    errors.append(f"<{tag_name}> tag should not have attributes")

            # Для простоти — можна ігнорувати складну перевірку вкладення тегів,
            # або додати додаткову логіку стека тут, якщо потрібно.

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def is_valid_url(self, url):
        if not url:
            return False
        # Заборонити javascript: і інші небезпечні протоколи
        if url.strip().lower().startswith("javascript:"):
            return False
        # Базова перевірка через Django URLField (примітивно)
        try:
            from django.core.validators import URLValidator

            validate = URLValidator()
            validate(url)
            return True
        except:
            return False

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
