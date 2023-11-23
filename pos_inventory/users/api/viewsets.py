from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, UserResponseSerializer
from pos_inventory.utils.decorators import response_schema


@response_schema(serializer=UserResponseSerializer)
class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance

        # Generate token for the created user
        token, created = Token.objects.get_or_create(user=user)
        user_token = token.key

        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "User created", "token": user_token}, status=201, headers=headers)

    @action(detail=False, methods=["POST"])
    def login(self, request):
        # overwrote login method to return a user object together with a token
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # want to return a user and the token
            token, created = Token.objects.get_or_create(user=user)
            user_token = token.key
            user_serializer = UserSerializer(user)
            response_user_data = {"token": user_token, "user": user_serializer.data}
            return Response(response_user_data, status=200)
        else:
            return Response({"detail": "Invalid credentials"}, status=400)

    @action(detail=False, methods=["POST"])
    def logout(self, request):
        logout(request)
        return Response({"detail": "Logout successful"})
