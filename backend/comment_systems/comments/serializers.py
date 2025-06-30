from rest_framework import serializers
from .models import Comment
from user.models import User


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
    username = serializers.CharField(source='sender.username', read_only=True)

    def create(self, validated_data):
        parent_comment = validated_data.get("parent_comment")
        if parent_comment:
            validated_data["is_reply"] = True
        else:
            validated_data["is_reply"] = False
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance
