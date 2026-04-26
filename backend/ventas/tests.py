from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from productos.models import Categoria, Color, Marca, Producto, Talla, VarianteProducto
from usuarios.models import Role, Usuario

from .exceptions import InsufficientStockError
from .models import Venta
from .services import VentaService


class VentaServiceTests(APITestCase):
    def setUp(self):
        self.role = Role.objects.create(nombre_role='Vendedor', descripcion='Registra ventas')
        self.usuario = Usuario.objects.create(
            username='cajero',
            password_hash='hash',
            nombre_completo='Cajero Principal',
            role=self.role,
        )
        categoria = Categoria.objects.create(nombre='Ropa')
        marca = Marca.objects.create(nombre='Marca')
        talla = Talla.objects.create(nombre='M')
        color = Color.objects.create(nombre='Azul', codigo_hex='#0000FF')
        producto = Producto.objects.create(
            nombre='Playera',
            descripcion='Playera basica',
            categoria=categoria,
            marca=marca,
        )
        self.variante = VarianteProducto.objects.create(
            producto=producto,
            talla=talla,
            color=color,
            sku='SKU-1',
            codigo_barras='750000000001',
            precio_venta='150.00',
            stock_actual=10,
        )

    def test_registra_venta_y_descuenta_stock(self):
        venta = VentaService.registrar_venta(self.usuario.id_usuario, self.variante.id_variante, 2, 'tarjeta')

        self.variante.refresh_from_db()
        self.assertEqual(self.variante.stock_actual, 8)
        self.assertEqual(Venta.objects.count(), 1)
        self.assertEqual(str(venta.total), '300.00')
        self.assertEqual(venta.usuario, self.usuario)

    def test_no_permite_vender_sin_stock(self):
        with self.assertRaises(InsufficientStockError):
            VentaService.registrar_venta(self.usuario.id_usuario, self.variante.id_variante, 30, 'efectivo')


class AuthApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='secret123',
            is_staff=True,
        )

    def test_login_devuelve_tokens(self):
        response = self.client.post(
            reverse('auth_login'),
            {'username': 'admin', 'password': 'secret123'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], 'admin')

    def test_me_requiere_autenticacion(self):
        response = self.client.get(reverse('auth_me'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
