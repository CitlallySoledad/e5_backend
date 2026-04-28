from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .exceptions import DomainError, InsufficientStockError
from .models import Categoria, Producto, VarianteProducto, Venta
from .serializers import (
    CategoriaSerializer,
    ProductoSerializer,
    VarianteSerializer,
    VentaCreateSerializer,
    VentaSerializer,
)
from .services import InventarioService, VentaService

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            categoria = InventarioService.crear_categoria(serializer.validated_data['nombre'])
        except DomainError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(categoria).data, status=status.HTTP_201_CREATED)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('categoria').all()
    serializer_class = ProductoSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            producto = InventarioService.crear_producto_con_categoria(
                nombre=serializer.validated_data['nombre'],
                marca=serializer.validated_data['marca'],
                categoria_id=serializer.validated_data['categoria'].id,
                descripcion=serializer.validated_data.get('descripcion', ''),
            )
        except DomainError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(producto).data, status=status.HTTP_201_CREATED)


class VarianteViewSet(viewsets.ModelViewSet):
    queryset = VarianteProducto.objects.all()
    serializer_class = VarianteSerializer
    permission_classes = [IsAdminUser]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            variante = InventarioService.crear_variante(
                producto_id=serializer.validated_data['producto'].id,
                talla=serializer.validated_data['talla'],
                color=serializer.validated_data['color'],
                sku=serializer.validated_data['sku'],
                precio_venta=serializer.validated_data['precio_venta'],
                stock_actual=serializer.validated_data['stock_actual'],
            )
        except DomainError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(variante).data, status=status.HTTP_201_CREATED)


class VentaViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Venta.objects.prefetch_related('detalles__variante__producto').all().order_by('-fecha_venta')
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = VentaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            venta = VentaService.registrar_venta(**serializer.validated_data)
        except InsufficientStockError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except DomainError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(VentaSerializer(venta).data, status=status.HTTP_201_CREATED)
