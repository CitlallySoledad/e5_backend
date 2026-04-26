from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriaViewSet,
    ColorViewSet,
    MarcaViewSet,
    ProductoViewSet,
    TallaViewSet,
    VarianteProductoViewSet,
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'tallas', TallaViewSet)
router.register(r'colores', ColorViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'variantes', VarianteProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
