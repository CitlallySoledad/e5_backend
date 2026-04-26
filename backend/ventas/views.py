from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .exceptions import DomainError, InsufficientStockError
from .models import Venta
from .serializers import VentaCreateSerializer, VentaSerializer
from .services import VentaService


class VentaViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Venta.objects.select_related('usuario').prefetch_related('detalles__variante__producto').all()
    serializer_class = VentaSerializer

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
