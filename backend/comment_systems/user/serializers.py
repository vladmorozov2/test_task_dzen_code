from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_repeat = serializers.CharField(write_only=True, required=True)
    homepage_url = serializers.URLField(required=False, allow_blank=True)

    def validate(self, data):
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_repeat')  
        password = validated_data.pop('password')
        
    
        user = User(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            homepage=validated_data.get('homepage_url', '')
        )
        user.set_password(password)  
        user.save()
        return user
