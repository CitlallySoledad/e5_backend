from .models import Producto, VarianteProducto

class ProductoRepository:
    @staticmethod
    def get_all():
        return Producto.objects.filter(activo=True).prefetch_related(
            'tallas', 'colores', 'variantes'
        ).select_related('categoria', 'marca')

    @staticmethod
    def get_by_id(id):
        return Producto.objects.get(pk=id, activo=True)

    @staticmethod
    def create(data):
        return Producto.objects.create(**data)

    @staticmethod
    def update(instance, data):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @staticmethod
    def delete(instance):
        instance.activo = False
        instance.save()