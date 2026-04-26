from rest_framework import viewsets

from .models import Categoria, Color, Marca, Producto, Talla, VarianteProducto
from .serializers import (
    CategoriaSerializer,
    ColorSerializer,
    MarcaSerializer,
    ProductoSerializer,
    TallaSerializer,
    VarianteProductoSerializer,
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer


class TallaViewSet(viewsets.ModelViewSet):
    queryset = Talla.objects.all()
    serializer_class = TallaSerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('categoria', 'marca').all()
    serializer_class = ProductoSerializer


class VarianteProductoViewSet(viewsets.ModelViewSet):
    queryset = VarianteProducto.objects.select_related('producto', 'talla', 'color').all()
    serializer_class = VarianteProductoSerializer
