from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Role, Usuario


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id_role', 'nombre_role', 'descripcion']

    def validate_nombre_role(self, value):
        nombre_role = value.strip()
        if not nombre_role:
            raise serializers.ValidationError('El nombre del rol es obligatorio.')
        return nombre_role


class UsuarioPdfSerializer(serializers.ModelSerializer):
    role_nombre = serializers.ReadOnlyField(source='role.nombre_role')

    class Meta:
        model = Usuario
        fields = [
            'id_usuario',
            'username',
            'password_hash',
            'nombre_completo',
            'role',
            'role_nombre',
            'activo',
        ]

    def validate_username(self, value):
        username = value.strip()
        if not username:
            raise serializers.ValidationError('El usuario es obligatorio.')
        return username

    def validate_nombre_completo(self, value):
        nombre_completo = value.strip()
        if not nombre_completo:
            raise serializers.ValidationError('El nombre completo es obligatorio.')
        return nombre_completo

    def validate_password_hash(self, value):
        password_hash = value.strip()
        if not password_hash:
            raise serializers.ValidationError('El password_hash es obligatorio.')
        return password_hash


class UserSerializer(serializers.ModelSerializer):
    rol = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'rol']

    def get_rol(self, obj):
        if obj.is_superuser or obj.is_staff:
            return 'admin'
        return 'usuario'


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_staff']

    def validate_username(self, value):
        username = value.strip()
        if not username:
            raise serializers.ValidationError('El nombre de usuario es obligatorio.')
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError('Ese nombre de usuario ya existe.')
        return username

    def validate_email(self, value):
        email = value.strip().lower()
        if not email:
            raise serializers.ValidationError('El correo es obligatorio.')
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('Ese correo ya existe.')
        return email


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff']

    def validate_email(self, value):
        email = value.strip().lower()
        queryset = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Ese correo ya existe.')
        return email


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
