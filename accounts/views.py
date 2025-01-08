import random
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from .serializers import (UserSerializer,
    OTPVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
    PasswordResetSerializer,
    ChangePasswordSerializer)
from .authentication import authenticate
from .models import User, OtpCode

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser_data = UserSerializer(data=request.data)

        if ser_data.is_valid():
            user = ser_data.save()
            otp_code = random.randint(10000, 99999)
            OtpCode.objects.create(email=user.email, code=otp_code)
            send_mail(
                "Your OTP Code",
                f"Your OTP code for account activation is {otp_code}.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Please check your email for the OTP."}, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser_data = OTPVerificationSerializer(data=request.data)
        
        if ser_data.is_valid():
            email = ser_data.validated_data["email"]
            code_instance = OtpCode.objects.get(email=email)
            otp = int(ser_data.validated_data["otp_code"])
            user = User.objects.get(email=email)

            if otp == code_instance.code:
                user.is_active = True
                user.save()
                code_instance.delete()
                return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser_data = LoginSerializer(data=request.data)
        if ser_data.is_valid():
            username = ser_data.data.get("username")
            password = ser_data.data.get("password")
            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                })
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = LogoutSerializer(data=request.data)
        if ser_data.is_valid():
            refresh_token = ser_data.validated_data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "you logged out successfully!!"}, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPasswordRestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "OTP has been sent to your email"}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password has been reset successfully"}, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)