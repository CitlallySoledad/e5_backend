from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ProductoService
from .serializers import ProductoSerializer

class ProductoListCreateView(APIView):
    def get(self, request):
        productos = ProductoService.listar_productos()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            producto = ProductoService.crear_producto(serializer.validated_data)
            return Response(ProductoSerializer(producto).data,
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoDetailView(APIView):
    def get(self, request, pk):
        try:
            producto = ProductoService.obtener_producto(pk)
            return Response(ProductoSerializer(producto).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            producto = ProductoService.actualizar_producto(pk, serializer.validated_data)
            return Response(ProductoSerializer(producto).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ProductoService.eliminar_producto(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
