from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404


class UsuarioService:
    @staticmethod
    def listar():
        return User.objects.order_by('id')

    @staticmethod
    def obtener(user_id):
        return get_object_or_404(User, pk=user_id)

    @staticmethod
    @transaction.atomic
    def crear_usuario(validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.email = user.email.lower()
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    @transaction.atomic
    def actualizar_usuario(user_id, validated_data):
        user = UsuarioService.obtener(user_id)
        for field, value in validated_data.items():
            setattr(user, field, value.lower() if field == 'email' else value)
        user.save()
        return user

    @staticmethod
    @transaction.atomic
    def desactivar_usuario(user_id):
        user = UsuarioService.obtener(user_id)
        user.is_active = False
        user.save(update_fields=['is_active'])
        return user
