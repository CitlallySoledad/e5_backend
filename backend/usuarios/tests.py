from rest_framework import status
from rest_framework.test import APITestCase

from .models import Role, Usuario


class UsuariosApiTests(APITestCase):
    def test_crea_role_y_usuario_del_modelo_pdf(self):
        role_response = self.client.post(
            '/api/roles/',
            {'nombre_role': 'Cajero', 'descripcion': 'Registra ventas'},
            format='json',
        )

        self.assertEqual(role_response.status_code, status.HTTP_201_CREATED)

        usuario_response = self.client.post(
            '/api/usuarios/',
            {
                'username': 'cajero1',
                'password_hash': 'hash-local',
                'nombre_completo': 'Cajero Uno',
                'role': role_response.data['id_role'],
                'activo': True,
            },
            format='json',
        )

        self.assertEqual(usuario_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(usuario_response.data['role_nombre'], 'Cajero')
        self.assertEqual(Role.objects.count(), 1)
        self.assertEqual(Usuario.objects.count(), 1)
