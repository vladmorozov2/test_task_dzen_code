from rest_framework import serializers
from .models import Comment
from user.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import re
from .tasks import resize_comment_attachment


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
    email = serializers.EmailField(source="sender.email", read_only=True)
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
                Image.open(file)  # just validation
            except Exception:
                raise serializers.ValidationError("Invalid image file")
            return file

        else:
            raise serializers.ValidationError(
                "Invalid file format. Only JPG, PNG, GIF, or TXT allowed."
            )

    def validate_text(self, value):
        errors = []

        tag_regex = re.compile(r"</?([a-z]+)(\s[^>]*)?>", re.IGNORECASE)
        tags = tag_regex.findall(value)

        stack = []
        for tag_match in tags:
            tag_name = tag_match[0].lower()
            attrs = tag_match[1]

            if tag_name not in self.ALLOWED_TAGS:
                errors.append(f"Disallowed HTML tag: <{tag_name}>")
                continue

            if tag_name == "a":

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

                if attrs.strip():
                    errors.append(f"<{tag_name}> tag should not have attributes")

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def is_valid_url(self, url):
        if not url:
            return False

        if url.strip().lower().startswith("javascript:"):
            return False

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
        comment = Comment.objects.create(**validated_data)
        if comment.attachment and comment.attachment.name.lower().endswith(
            (".jpg", ".jpeg", ".png", ".gif")
        ):
            resize_comment_attachment.delay(comment.id)

        return comment

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        if "attachment" in validated_data:
            instance.attachment = validated_data["attachment"]
        instance.save()
        return instance
