# chat/views.py
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
# chat/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .serializers import *
# from django.contrib.auth import get_user_model

# user = get_user_model()


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    def post(self, request):
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')

        # Validate the input
        if not username_or_email or not password:
            return Response({"error": "Both username/email and password are required."}, status=HTTP_400_BAD_REQUEST)

        user = None
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                return Response({"error": "Invalid email or password."}, status=HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(username=username_or_email, password=password)

        if user and user.check_password(password):
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=HTTP_200_OK)

        return Response({"error": "Invalid credentials."}, status=HTTP_400_BAD_REQUEST)

# class LoginAPIView(APIView):
#     def post(self, request):
#         username_or_email = request.data.get('username_or_email')
#         password = request.data.get('password')

#         user = None
#         if '@' in username_or_email:
#             try:
#                 user = User.objects.get(email=username_or_email)
#             except User.DoesNotExist:
#                 pass
#         else:
#             user = authenticate(username=username_or_email, password=password)

#         if user and user.check_password(password):
#             from rest_framework_simplejwt.tokens import RefreshToken
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#             }, status=HTTP_200_OK)
#         return Response({"error": "Invalid credentials."}, status=HTTP_400_BAD_REQUEST)



# from .serializers import ProfileSerializer, UserSerializer


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Check if the user has a profile
        try:
            profile = user.profile  # Access the related profile
            profile_data = ProfileSerializer(profile).data
        except Profile.DoesNotExist:
            profile_data = None

        # Include username and email in the response
        data = {
            "username": user.username,
            "email": user.email,
            "profile": profile_data,  # Include profile data only if it exists
        }
        return Response(data, status=HTTP_200_OK)

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "User registered successfully."}, status=HTTP_201_CREATED)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# class LoginAPIView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = authenticate(
#                 username=serializer.validated_data['username'],
#                 password=serializer.validated_data['password']
#             )
#             if user:
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     "refresh": str(refresh),
#                     "access": str(refresh.access_token),
#                 }, status=HTTP_200_OK)
#             return Response({"error": "Invalid credentials."}, status=HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# class ProfileAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         profile = request.user.profile
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data)

#     def put(self, request):
#         profile = request.user.profile
#         serializer = ProfileSerializer(profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class MessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get(self, request):
        messages = Message.objects.filter(recipient=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
