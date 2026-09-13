from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    is_staff = serializers.BooleanField()


class CsrfView(APIView):
    """
    GET /api/auth/csrf/
    Sets the CSRF cookie so the SPA can include X-CSRFToken on unsafe requests.
    """
    permission_classes = [AllowAny]
    serializer_class = None

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({'detail': 'CSRF cookie set'})


class LoginView(APIView):
    """
    POST /api/auth/login/
    Body: {"username": "...", "password": "..."}
    Creates a Django session on success.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {'detail': 'Invalid username or password'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login(request, user)
        return Response({
            'username': user.username,
            'is_staff': user.is_staff,
        })


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Ends the Django session.
    """
    permission_classes = [AllowAny]
    serializer_class = None

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out'})


class MeView(APIView):
    """
    GET /api/auth/me/
    Returns the current authenticated user, or 401.
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'username': request.user.username,
                'is_staff': request.user.is_staff,
            })
        return Response(
            {'detail': 'Not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED,
        )