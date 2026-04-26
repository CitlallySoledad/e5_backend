from rest_framework import status
from rest_framework.test import APITestCase

from .models import Categoria, Color, Marca, Producto, Talla, VarianteProducto


class ProductosApiTests(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Ropa')
        self.marca = Marca.objects.create(nombre='Marca Norte')
        self.talla = Talla.objects.create(nombre='M')
        self.color = Color.objects.create(nombre='Azul', codigo_hex='#0000FF')

    def test_crea_producto_con_categoria_y_marca(self):
        response = self.client.post(
            '/api/productos/',
            {
                'nombre': 'Camisa',
                'descripcion': 'Camisa casual',
                'categoria': self.categoria.id_categoria,
                'marca': self.marca.id_marca,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['categoria_nombre'], 'Ropa')
        self.assertEqual(response.data['marca_nombre'], 'Marca Norte')

    def test_crea_variante_y_normaliza_sku(self):
        producto = Producto.objects.create(
            nombre='Camisa',
            descripcion='Camisa casual',
            categoria=self.categoria,
            marca=self.marca,
        )

        response = self.client.post(
            '/api/variantes/',
            {
                'producto': producto.id_producto,
                'talla': self.talla.id_talla,
                'color': self.color.id_color,
                'sku': ' sku-001 ',
                'codigo_barras': '750000000001',
                'precio_venta': '299.90',
                'stock_actual': 4,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sku'], 'SKU-001')
        self.assertEqual(VarianteProducto.objects.count(), 1)

    def test_rechaza_color_hex_invalido(self):
        response = self.client.post(
            '/api/colores/',
            {'nombre': 'Color raro', 'codigo_hex': '#ZZZZZZ'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
