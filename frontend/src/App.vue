<template>
  <div class="app-shell">
    <header class="app-header">
      <div>
        <p class="eyebrow">Punto de venta</p>
        <h1 class="page-title">Administracion del inventario</h1>
        <p class="page-subtitle">Gestiona la estructura completa del modelo: usuarios, catalogos, productos, variantes y ventas.</p>
      </div>
      <button type="button" class="btn btn-outline-primary" @click="cargarDatos" :disabled="cargando">
        {{ cargando ? 'Actualizando...' : 'Actualizar' }}
      </button>
    </header>

    <div v-if="mensaje" class="alert alert-success" role="alert">{{ mensaje }}</div>
    <div v-if="errorCarga" class="alert alert-danger" role="alert">{{ errorCarga }}</div>

    <section class="panel mb-4">
      <div class="panel-header">
        <div>
          <h2 class="panel-title">Acceso Django</h2>
          <p class="panel-subtitle">Sesion para endpoints protegidos y administracion tecnica.</p>
        </div>
        <span class="status-pill" :class="{ active: sesionActiva }">{{ sesionActiva ? 'Sesion activa' : 'Sin sesion' }}</span>
      </div>
      <div class="panel-body login-grid">
        <form @submit.prevent="iniciarSesion" class="compact-form">
          <label class="form-label">Usuario</label>
          <input v-model="credenciales.username" type="text" class="form-control" autocomplete="username" required>
          <label class="form-label">Contrasena</label>
          <input v-model="credenciales.password" type="password" class="form-control" autocomplete="current-password" required>
          <div class="button-row">
            <button type="submit" class="btn btn-primary" :disabled="cargandoSesion">{{ cargandoSesion ? 'Entrando...' : 'Iniciar sesion' }}</button>
            <button type="button" class="btn btn-outline-secondary" @click="cerrarSesion">Cerrar</button>
          </div>
          <p v-if="errorSesion" class="form-error">{{ errorSesion }}</p>
        </form>
        <div class="session-summary">
          <strong>{{ usuarioActual?.username || 'Invitado' }}</strong>
          <span>{{ usuarioActual?.email || 'Sin correo cargado' }}</span>
          <span>Rol: {{ usuarioActual?.rol || 'sin rol' }}</span>
        </div>
      </div>
    </section>

    <section class="dashboard-grid">
      <article class="panel">
        <div class="panel-header">
          <h2 class="panel-title">Roles y usuarios</h2>
        </div>
        <div class="panel-body stacked">
          <form @submit.prevent="guardarRole" class="form-grid two">
            <input v-model="nuevoRole.nombre_role" class="form-control" placeholder="Rol" required>
            <input v-model="nuevoRole.descripcion" class="form-control" placeholder="Descripcion">
            <button class="btn btn-primary span-2" type="submit">Guardar rol</button>
          </form>
          <form @submit.prevent="guardarUsuario" class="form-grid two">
            <input v-model="nuevoUsuario.username" class="form-control" placeholder="Usuario" required>
            <select v-model="nuevoUsuario.role" class="form-select" required>
              <option value="" disabled>Rol</option>
              <option v-for="role in roles" :key="role.id_role" :value="role.id_role">{{ role.nombre_role }}</option>
            </select>
            <input v-model="nuevoUsuario.nombre_completo" class="form-control span-2" placeholder="Nombre completo" required>
            <input v-model="nuevoUsuario.password_hash" class="form-control span-2" placeholder="Password hash" required>
            <label class="check-line span-2">
              <input v-model="nuevoUsuario.activo" type="checkbox"> Activo
            </label>
            <button class="btn btn-primary span-2" type="submit">Guardar usuario</button>
          </form>
          <div class="mini-table">
            <div v-for="usuario in usuarios" :key="usuario.id_usuario" class="mini-row">
              <strong>{{ usuario.username }}</strong>
              <span>{{ usuario.nombre_completo }} · {{ usuario.role_nombre }}</span>
            </div>
            <p v-if="!usuarios.length" class="empty-state">Sin usuarios.</p>
          </div>
        </div>
      </article>

      <article class="panel">
        <div class="panel-header">
          <h2 class="panel-title">Catalogos</h2>
        </div>
        <div class="panel-body stacked">
          <form @submit.prevent="guardarCategoria" class="inline-form">
            <input v-model="nuevaCategoria.nombre" class="form-control" placeholder="Categoria" required>
            <button class="btn btn-primary" type="submit">Agregar</button>
          </form>
          <form @submit.prevent="guardarMarca" class="inline-form">
            <input v-model="nuevaMarca.nombre" class="form-control" placeholder="Marca" required>
            <button class="btn btn-primary" type="submit">Agregar</button>
          </form>
          <form @submit.prevent="guardarTalla" class="inline-form">
            <input v-model="nuevaTalla.nombre" class="form-control" placeholder="Talla" required>
            <button class="btn btn-primary" type="submit">Agregar</button>
          </form>
          <form @submit.prevent="guardarColor" class="form-grid color-grid">
            <input v-model="nuevoColor.nombre" class="form-control" placeholder="Color" required>
            <input v-model="nuevoColor.codigo_hex" type="color" class="form-control form-control-color color-input" required>
            <button class="btn btn-primary" type="submit">Agregar</button>
          </form>
          <div class="tag-cloud">
            <span v-for="categoria in categorias" :key="categoria.id_categoria">{{ categoria.nombre }}</span>
            <span v-for="marca in marcas" :key="marca.id_marca">{{ marca.nombre }}</span>
            <span v-for="talla in tallas" :key="talla.id_talla">{{ talla.nombre }}</span>
            <span v-for="color in colores" :key="color.id_color">
              <i class="color-dot" :style="{ backgroundColor: color.codigo_hex }"></i>{{ color.nombre }}
            </span>
          </div>
        </div>
      </article>

      <article class="panel wide">
        <div class="panel-header">
          <h2 class="panel-title">Productos y variantes</h2>
        </div>
        <div class="panel-body product-layout">
          <form @submit.prevent="guardarProducto" class="form-grid product-form">
            <input v-model="nuevoProducto.nombre" class="form-control" placeholder="Producto" required>
            <select v-model="nuevoProducto.categoria" class="form-select" required>
              <option value="" disabled>Categoria</option>
              <option v-for="categoria in categorias" :key="categoria.id_categoria" :value="categoria.id_categoria">{{ categoria.nombre }}</option>
            </select>
            <select v-model="nuevoProducto.marca" class="form-select" required>
              <option value="" disabled>Marca</option>
              <option v-for="marca in marcas" :key="marca.id_marca" :value="marca.id_marca">{{ marca.nombre }}</option>
            </select>
            <textarea v-model="nuevoProducto.descripcion" class="form-control span-3" rows="2" placeholder="Descripcion"></textarea>
            <button class="btn btn-primary span-3" type="submit">Guardar producto</button>
          </form>

          <form @submit.prevent="guardarVariante" class="form-grid variant-form">
            <select v-model="nuevaVariante.producto" class="form-select" required>
              <option value="" disabled>Producto</option>
              <option v-for="producto in productos" :key="producto.id_producto" :value="producto.id_producto">{{ producto.nombre }}</option>
            </select>
            <select v-model="nuevaVariante.talla" class="form-select" required>
              <option value="" disabled>Talla</option>
              <option v-for="talla in tallas" :key="talla.id_talla" :value="talla.id_talla">{{ talla.nombre }}</option>
            </select>
            <select v-model="nuevaVariante.color" class="form-select" required>
              <option value="" disabled>Color</option>
              <option v-for="color in colores" :key="color.id_color" :value="color.id_color">{{ color.nombre }}</option>
            </select>
            <input v-model="nuevaVariante.sku" class="form-control" placeholder="SKU" required>
            <input v-model="nuevaVariante.codigo_barras" class="form-control" placeholder="Codigo de barras" required>
            <input v-model.number="nuevaVariante.precio_venta" type="number" min="0.01" step="0.01" class="form-control" placeholder="Precio" required>
            <input v-model.number="nuevaVariante.stock_actual" type="number" min="0" step="1" class="form-control span-3" placeholder="Stock" required>
            <button class="btn btn-primary span-3" type="submit">Guardar variante</button>
          </form>
        </div>
      </article>

      <article class="panel wide">
        <div class="panel-header">
          <h2 class="panel-title">Registrar venta</h2>
        </div>
        <div class="panel-body">
          <form @submit.prevent="guardarVenta" class="form-grid sale-form">
            <select v-model="nuevaVenta.usuario_id" class="form-select" required>
              <option value="" disabled>Usuario</option>
              <option v-for="usuario in usuariosActivos" :key="usuario.id_usuario" :value="usuario.id_usuario">{{ usuario.nombre_completo }}</option>
            </select>
            <select v-model="nuevaVenta.variante_id" class="form-select" required>
              <option value="" disabled>Variante</option>
              <option v-for="variante in variantes" :key="variante.id_variante" :value="variante.id_variante">
                {{ variante.producto_nombre }} · {{ variante.sku }} · stock {{ variante.stock_actual }}
              </option>
            </select>
            <input v-model.number="nuevaVenta.cantidad" type="number" min="1" step="1" class="form-control" placeholder="Cantidad" required>
            <select v-model="nuevaVenta.metodo_pago" class="form-select" required>
              <option value="" disabled>Metodo de pago</option>
              <option>Efectivo</option>
              <option>Tarjeta</option>
              <option>Transferencia</option>
            </select>
            <button class="btn btn-success" type="submit">Registrar venta</button>
          </form>
        </div>
      </article>
    </section>

    <section class="panel mt-4">
      <div class="panel-header">
        <h2 class="panel-title">Inventario y ventas</h2>
      </div>
      <div class="panel-body table-wrap">
        <table class="table table-hover align-middle">
          <thead>
            <tr>
              <th>Producto</th>
              <th>Marca</th>
              <th>Categoria</th>
              <th>SKU</th>
              <th>Talla</th>
              <th>Color</th>
              <th>Precio</th>
              <th>Stock</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="variante in variantes" :key="variante.id_variante">
              <td>{{ variante.producto_nombre }}</td>
              <td>{{ productoPorId(variante.producto)?.marca_nombre || '-' }}</td>
              <td>{{ productoPorId(variante.producto)?.categoria_nombre || '-' }}</td>
              <td>{{ variante.sku }}</td>
              <td>{{ variante.talla_nombre }}</td>
              <td><i class="color-dot" :style="{ backgroundColor: variante.color_hex }"></i>{{ variante.color_nombre }}</td>
              <td>${{ variante.precio_venta }}</td>
              <td>{{ variante.stock_actual }}</td>
            </tr>
            <tr v-if="!variantes.length">
              <td colspan="8" class="empty-state">Sin variantes registradas.</td>
            </tr>
          </tbody>
        </table>
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>Venta</th>
              <th>Fecha</th>
              <th>Usuario</th>
              <th>Metodo</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="venta in ventas" :key="venta.id_venta">
              <td>#{{ venta.id_venta }}</td>
              <td>{{ formatearFecha(venta.fecha_venta) }}</td>
              <td>{{ venta.usuario_nombre }}</td>
              <td>{{ venta.metodo_pago }}</td>
              <td>${{ venta.total }}</td>
            </tr>
            <tr v-if="!ventas.length">
              <td colspan="5" class="empty-state">Sin ventas registradas.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import api from './services/api';

const roles = ref([]);
const usuarios = ref([]);
const categorias = ref([]);
const marcas = ref([]);
const tallas = ref([]);
const colores = ref([]);
const productos = ref([]);
const variantes = ref([]);
const ventas = ref([]);

const mensaje = ref('');
const errorCarga = ref('');
const errorSesion = ref('');
const cargando = ref(false);
const cargandoSesion = ref(false);
const usuarioActual = ref(api.getStoredUser());
const sesionActiva = ref(Boolean(api.getToken()));
const credenciales = ref({ username: '', password: '' });

const nuevoRole = ref({ nombre_role: '', descripcion: '' });
const nuevoUsuario = ref({ username: '', password_hash: '', nombre_completo: '', role: '', activo: true });
const nuevaCategoria = ref({ nombre: '' });
const nuevaMarca = ref({ nombre: '' });
const nuevaTalla = ref({ nombre: '' });
const nuevoColor = ref({ nombre: '', codigo_hex: '#2563eb' });
const nuevoProducto = ref({ nombre: '', descripcion: '', categoria: '', marca: '' });
const nuevaVariante = ref({ producto: '', talla: '', color: '', sku: '', codigo_barras: '', precio_venta: '', stock_actual: 0 });
const nuevaVenta = ref({ usuario_id: '', variante_id: '', cantidad: 1, metodo_pago: '' });

const usuariosActivos = computed(() => usuarios.value.filter((usuario) => usuario.activo));

const productoPorId = (id) => productos.value.find((producto) => producto.id_producto === id);

const formatearFecha = (fecha) => {
  if (!fecha) return '-';
  return new Intl.DateTimeFormat('es-MX', { dateStyle: 'short', timeStyle: 'short' }).format(new Date(fecha));
};

const mostrarMensaje = (texto) => {
  mensaje.value = texto;
  window.setTimeout(() => {
    if (mensaje.value === texto) mensaje.value = '';
  }, 3500);
};

const cargarDatos = async () => {
  cargando.value = true;
  errorCarga.value = '';
  try {
    const [rolesRes, usuariosRes, categoriasRes, marcasRes, tallasRes, coloresRes, productosRes, variantesRes, ventasRes] = await Promise.all([
      api.getRoles(),
      api.getUsuarios(),
      api.getCategorias(),
      api.getMarcas(),
      api.getTallas(),
      api.getColores(),
      api.getProductos(),
      api.getVariantes(),
      api.getVentas()
    ]);

    roles.value = rolesRes.data;
    usuarios.value = usuariosRes.data;
    categorias.value = categoriasRes.data;
    marcas.value = marcasRes.data;
    tallas.value = tallasRes.data;
    colores.value = coloresRes.data;
    productos.value = productosRes.data;
    variantes.value = variantesRes.data;
    ventas.value = ventasRes.data;
  } catch (error) {
    console.error('Error al cargar datos:', error);
    errorCarga.value = 'No se pudo cargar la informacion del backend.';
  } finally {
    cargando.value = false;
  }
};

const restaurarSesion = async () => {
  if (!api.getToken()) {
    sesionActiva.value = false;
    usuarioActual.value = null;
    return;
  }
  try {
    const response = await api.getPerfil();
    usuarioActual.value = response.data;
    sesionActiva.value = true;
  } catch (error) {
    console.error('Error al restaurar sesion:', error);
    usuarioActual.value = null;
    sesionActiva.value = false;
  }
};

const iniciarSesion = async () => {
  errorSesion.value = '';
  cargandoSesion.value = true;
  try {
    const data = await api.login(credenciales.value);
    usuarioActual.value = data.user;
    sesionActiva.value = true;
    credenciales.value = { username: '', password: '' };
  } catch (error) {
    errorSesion.value = error.message;
  } finally {
    cargandoSesion.value = false;
  }
};

const cerrarSesion = () => {
  api.logout();
  usuarioActual.value = null;
  sesionActiva.value = false;
  errorSesion.value = '';
};

const guardar = async (accion, limpiar, texto) => {
  try {
    await accion();
    limpiar();
    await cargarDatos();
    mostrarMensaje(texto);
  } catch (error) {
    errorCarga.value = error.message;
  }
};

const guardarRole = () => guardar(
  () => api.crearRole(nuevoRole.value),
  () => { nuevoRole.value = { nombre_role: '', descripcion: '' }; },
  'Rol guardado.'
);

const guardarUsuario = () => guardar(
  () => api.crearUsuario(nuevoUsuario.value),
  () => { nuevoUsuario.value = { username: '', password_hash: '', nombre_completo: '', role: '', activo: true }; },
  'Usuario guardado.'
);

const guardarCategoria = () => guardar(
  () => api.crearCategoria(nuevaCategoria.value),
  () => { nuevaCategoria.value = { nombre: '' }; },
  'Categoria guardada.'
);

const guardarMarca = () => guardar(
  () => api.crearMarca(nuevaMarca.value),
  () => { nuevaMarca.value = { nombre: '' }; },
  'Marca guardada.'
);

const guardarTalla = () => guardar(
  () => api.crearTalla(nuevaTalla.value),
  () => { nuevaTalla.value = { nombre: '' }; },
  'Talla guardada.'
);

const guardarColor = () => guardar(
  () => api.crearColor(nuevoColor.value),
  () => { nuevoColor.value = { nombre: '', codigo_hex: '#2563eb' }; },
  'Color guardado.'
);

const guardarProducto = () => guardar(
  () => api.crearProducto(nuevoProducto.value),
  () => { nuevoProducto.value = { nombre: '', descripcion: '', categoria: '', marca: '' }; },
  'Producto guardado.'
);

const guardarVariante = () => guardar(
  () => api.crearVariante(nuevaVariante.value),
  () => { nuevaVariante.value = { producto: '', talla: '', color: '', sku: '', codigo_barras: '', precio_venta: '', stock_actual: 0 }; },
  'Variante guardada.'
);

const guardarVenta = () => guardar(
  () => api.crearVenta(nuevaVenta.value),
  () => { nuevaVenta.value = { usuario_id: '', variante_id: '', cantidad: 1, metodo_pago: '' }; },
  'Venta registrada.'
);

onMounted(async () => {
  await Promise.all([restaurarSesion(), cargarDatos()]);
});
</script>
