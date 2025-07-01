from rest_framework import serializers
from .models import Comment
from user.models import User
from django.core.files.base import ContentFile

class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=500)
    created_at = serializers.DateTimeField(read_only=True)
    parent_comment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), required=False, allow_null=True
    )
    is_reply = serializers.BooleanField(read_only=True)
    sender = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    username = serializers.CharField(source='sender.username', read_only=True)
    
    # Attachment fields
    attachment = serializers.FileField(required=False, allow_null=True, write_only=True)
    attachment_type = serializers.CharField(read_only=True)
    attachment_name = serializers.CharField(read_only=True)
    attachment_size = serializers.IntegerField(read_only=True)
    attachment_url = serializers.SerializerMethodField()

    def get_attachment_url(self, obj):
        if obj.attachment:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.attachment.url)
        return None

    def create(self, validated_data):
        # Extract attachment separately
        attachment = validated_data.pop('attachment', None)
        
        # Handle parent comment and is_reply
        parent_comment = validated_data.get("parent_comment")
        if parent_comment:
            validated_data["is_reply"] = True
        else:
            validated_data["is_reply"] = False
        
        # Create comment instance
        comment = Comment.objects.create(**validated_data)
        
        # Add attachment if exists
        if attachment:
            comment.attachment.save(attachment.name, attachment)
            comment.save()  # This will trigger the save() method with processing
        
        return comment

    def update(self, instance, validated_data):
        # Currently only updating text
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance