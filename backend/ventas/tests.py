from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .exceptions import DomainError, InsufficientStockError
from .models import Categoria, Producto, VarianteProducto, Venta
from .services import InventarioService, VentaService


class InventarioServiceTests(APITestCase):
    def test_no_permite_categorias_duplicadas(self):
        InventarioService.crear_categoria('Ropa')

        with self.assertRaisesMessage(DomainError, 'La categoria ya existe.'):
            InventarioService.crear_categoria('ropa')

    def test_registra_venta_y_descuenta_stock(self):
        categoria = Categoria.objects.create(nombre='Ropa')
        producto = Producto.objects.create(nombre='Playera', marca='Marca', categoria=categoria)
        variante = VarianteProducto.objects.create(
            producto=producto,
            talla='M',
            color='Azul',
            sku='SKU-1',
            precio_venta='150.00',
            stock_actual=10,
        )

        venta = VentaService.registrar_venta(variante.id, 2, 'tarjeta')

        variante.refresh_from_db()
        self.assertEqual(variante.stock_actual, 8)
        self.assertEqual(Venta.objects.count(), 1)
        self.assertEqual(str(venta.total), '300.00')

    def test_no_permite_vender_sin_stock(self):
        categoria = Categoria.objects.create(nombre='Calzado')
        producto = Producto.objects.create(nombre='Tenis', marca='Marca', categoria=categoria)
        variante = VarianteProducto.objects.create(
            producto=producto,
            talla='28',
            color='Negro',
            sku='SKU-2',
            precio_venta='999.00',
            stock_actual=1,
        )

        with self.assertRaises(InsufficientStockError):
            VentaService.registrar_venta(variante.id, 3, 'efectivo')


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
