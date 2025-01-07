from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True) 

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"] 
        extra_kwargs = {"password": {"write_only": True}} 

    def validate(self, attrs):
        password = attrs["password"]
        password2 = attrs["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"]) 
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()