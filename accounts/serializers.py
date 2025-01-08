from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings

from .models import User, OtpCode

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True) 

    class Meta:
        model = User
        fields = ["email", "sur_name", "for_name", "password", "password2"] 
        extra_kwargs = {"password": {"write_only": True}} 

    def validate(self, attrs):
        password = attrs["password"]
        password2 = attrs["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return attrs

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            sur_name=validated_data["sur_name"],
            for_name=validated_data["for_name"]
        )
        user.set_password(validated_data["password"]) 
        user.save()
        return user

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value

    def save(self):
        email = self.validated_data["email"]
        # Generate OTP using model method
        otp_instance = OtpCode.generate_otp(email)
        
        # Send email
        send_mail(
            "Password Reset OTP",
            f"Your OTP code for password reset is: {otp_instance.code}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords don't match")

        try:
            otp_obj = OtpCode.objects.get(email=data["email"])
            if otp_obj.code != data["otp_code"]:
                raise serializers.ValidationError("Invalid OTP")
        except OtpCode.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP")

        return data

    def save(self):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]
        
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # Delete used OTP
        OtpCode.objects.filter(email=email).delete()