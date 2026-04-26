from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Role, Usuario
from .serializers import (
    CustomTokenObtainPairSerializer,
    RoleSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UsuarioPdfSerializer,
)
from .services import UsuarioService


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    def list(self, request):
        serializer = UserSerializer(UsuarioService.listar(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer = UserSerializer(UsuarioService.obtener(pk))
        return Response(serializer.data)

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UsuarioService.crear_usuario(serializer.validated_data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = UsuarioService.obtener(pk)
        serializer = UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_user = UsuarioService.actualizar_usuario(pk, serializer.validated_data)
        return Response(UserSerializer(updated_user).data)

    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        user = UsuarioService.desactivar_usuario(pk)
        return Response(UserSerializer(user).data)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UsuarioPdfViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.select_related('role').all()
    serializer_class = UsuarioPdfSerializer
