from .repository import ProductoRepository

class ProductoService:
    @staticmethod
    def listar_productos():
        return ProductoRepository.get_all()

    @staticmethod
    def obtener_producto(id):
        try:
            return ProductoRepository.get_by_id(id)
        except Exception:
            raise ValueError(f"Producto con id {id} no encontrado")

    @staticmethod
    def crear_producto(data):
        tallas = data.pop('tallas', [])
        colores = data.pop('colores', [])
        producto = ProductoRepository.create(data)
        if tallas:
            producto.tallas.set(tallas)
        if colores:
            producto.colores.set(colores)
        return producto

    @staticmethod
    def actualizar_producto(id, data):
        producto = ProductoRepository.get_by_id(id)
        tallas = data.pop('tallas', None)
        colores = data.pop('colores', None)
        producto = ProductoRepository.update(producto, data)
        if tallas is not None:
            producto.tallas.set(tallas)
        if colores is not None:
            producto.colores.set(colores)
        return producto

    @staticmethod
    def eliminar_producto(id):
        producto = ProductoRepository.get_by_id(id)
        ProductoRepository.delete(producto)