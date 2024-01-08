from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate, login, logout
from ..models import User
from .serializers import UserSerializer, UserResponseSerializer
from pos_inventory.utils.decorators import response_schema


@response_schema(serializer=UserResponseSerializer)
class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Create and register a user and create jwt tokens
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance

        # Generate token for the created user
        refresh = RefreshToken.for_user(user)
        user_token = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "User created", "token": user_token}, status=201, headers=headers)

    @action(detail=False, methods=["POST"])
    def login(self, request):
        """
        Login a user and generate jwt tokens
        """
        # overwrote login method to return a user object together with a token
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # want to return a user and the token
            # token, created = Token.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user)
            user_token = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            user_serializer = UserSerializer(user)
            response_user_data = {"token": user_token, "user": user_serializer.data}
            return Response(response_user_data, status=200)
        else:
            return Response({"detail": "Invalid credentials"}, status=400)

    @action(detail=False, methods=["POST"])
    def logout(self, request):
        """
        Logging user out
        """
        logout(request)
        return Response({"detail": "Logout successful"})

    @action(detail=False, methods=["POST"])
    def refresh_token(self, request):
        """Custom view to refresh access_token"""
        refresh_token = request.data.get("refresh", None)
        if refresh_token:
            try:
                refresh_token = RefreshToken(refresh_token)
                access_token = str(refresh_token.access_token)
                return Response({"access": access_token}, status=200)
            except Exception as e:
                return Response({"detail": f"Error refreshing token: {str(e)}"}, status=400)
        else:
            return Response({"detail": "Invalid refresh_token"}, status=400)

    @action(detail=False, methods=["POST"])
    def verify_token(self, request):
        """
        Custom view to verify access_token
        """
        access_token = request.data.get("access", None)
        if access_token:
            try:
                token = AccessToken(access_token)
                token.verify()
                return Response({"detail": "Token is valid"}, status=200)
            except Exception as e:
                return Response({"detail": f"Token verification failed: {str(e)}"}, status=400)
        else:
            return Response({"detail": "Access token not provided"}, status=400)

    @action(detail=False, methods=["GET"])
    def get_token_associated_user(self, request):
        access_token = request.data.get("access", None)
        if access_token:
            decoded_token = AccessToken(access_token)
            user_id = decoded_token.payload["user_id"]
            user = get_object_or_404(User, id=user_id)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=200)
        else:
            return Response({"detail": "Invalid token"}, status=400)
