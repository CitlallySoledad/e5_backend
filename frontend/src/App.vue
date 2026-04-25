<template>
  <div class="app-shell">
    <header class="mb-4">
      <h1 class="page-title">Registro de Inventario</h1>
      <p class="page-subtitle">
        Controla productos, consulta datos cargados en MySQL y prueba el flujo de autenticacion del backend.
      </p>
    </header>

    <section class="glass-card mb-4">
      <div class="panel-header">
        <h2 class="panel-title">Acceso al sistema</h2>
        <p class="panel-subtitle">Inicia sesion con un usuario de Django para probar JWT y permisos.</p>
      </div>
      <div class="panel-body">
        <div class="login-grid">
          <form @submit.prevent="iniciarSesion">
            <div class="mb-3">
              <label class="form-label">Usuario</label>
              <input v-model="credenciales.username" type="text" class="form-control" autocomplete="username" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Contrasena</label>
              <input v-model="credenciales.password" type="password" class="form-control" autocomplete="current-password" required>
            </div>
            <div class="d-flex gap-2">
              <button type="submit" class="btn btn-success" :disabled="cargandoSesion">
                {{ cargandoSesion ? 'Entrando...' : 'Iniciar sesion' }}
              </button>
              <button type="button" class="btn btn-outline-secondary" @click="cerrarSesion">
                Cerrar sesion
              </button>
            </div>
            <div v-if="errorSesion" class="alert alert-danger mt-3 mb-0">
              {{ errorSesion }}
            </div>
          </form>

          <div class="session-box">
            <div class="d-flex justify-content-between align-items-start gap-3">
              <div>
                <span class="session-tag">{{ sesionActiva ? 'Sesion activa' : 'Sin autenticar' }}</span>
                <h3 class="h4 mt-3 mb-2">{{ usuarioActual?.username || 'Invitado' }}</h3>
                <p>{{ usuarioActual?.email || 'No hay usuario autenticado.' }}</p>
              </div>
            </div>
            <hr class="border-secondary-subtle">
            <p><strong>Rol:</strong> {{ usuarioActual?.rol || 'sin rol' }}</p>
            <p><strong>Admin:</strong> {{ usuarioActual?.is_staff ? 'si' : 'no' }}</p>
            <p class="mb-0"><strong>Token cargado:</strong> {{ sesionActiva ? 'si' : 'no' }}</p>
          </div>
        </div>
      </div>
    </section>

    <div class="inventory-grid">
      <section class="glass-card">
        <div class="panel-header">
          <h2 class="panel-title">Agregar nuevo producto</h2>
          <p class="panel-subtitle">Este formulario sigue usando la API actual de productos.</p>
        </div>
        <div class="panel-body">
          <form @submit.prevent="guardarProducto">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Nombre del producto</label>
                <input v-model="nuevoProducto.nombre" type="text" class="form-control" placeholder="Ej: Camisa Slim Fit" required>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Marca</label>
                <input v-model="nuevoProducto.marca" type="text" class="form-control" placeholder="Ej: Levi's" required>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Categoria</label>
                <select v-model="nuevoProducto.categoria" class="form-select" required>
                  <option value="" disabled>Seleccione una categoria</option>
                  <option v-for="cat in categorias" :key="cat.id" :value="cat.id">
                    {{ cat.nombre }}
                  </option>
                </select>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Descripcion</label>
                <textarea v-model="nuevoProducto.descripcion" class="form-control" rows="1"></textarea>
              </div>
            </div>

            <button type="submit" class="btn btn-primary w-100">Guardar en base de datos</button>
          </form>
        </div>
      </section>

      <div v-if="errorCarga" class="alert alert-danger mb-0" role="alert">
        {{ errorCarga }}
      </div>

      <section class="glass-card">
        <div class="panel-header">
          <h2 class="panel-title">Productos en MySQL</h2>
          <p class="panel-subtitle">Consulta directa al endpoint de productos del backend.</p>
        </div>
        <div class="panel-body px-0">
          <table class="table table-hover mb-0">
            <thead>
              <tr>
                <th class="ps-4">ID</th>
                <th>Nombre</th>
                <th>Marca</th>
                <th class="pe-4">Categoria</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in productos" :key="p.id">
                <td class="ps-4">{{ p.id }}</td>
                <td>{{ p.nombre }}</td>
                <td>{{ p.marca }}</td>
                <td class="pe-4">{{ p.categoria_nombre || p.categoria }}</td>
              </tr>
              <tr v-if="!productos.length">
                <td colspan="4" class="empty-state">No hay productos registrados.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from './services/api';

const productos = ref([]);
const categorias = ref([]);
const errorCarga = ref('');
const errorSesion = ref('');
const cargandoSesion = ref(false);
const usuarioActual = ref(api.getStoredUser());
const sesionActiva = ref(Boolean(api.getToken()));
const nuevoProducto = ref({ nombre: '', marca: '', categoria: '', descripcion: '' });
const credenciales = ref({ username: '', password: '' });

const cargarDatos = async () => {
  errorCarga.value = '';
  try {
    const [resProd, resCat] = await Promise.all([
      api.getProductos(),
      api.getCategorias()
    ]);
    productos.value = resProd.data;
    categorias.value = resCat.data;
  } catch (error) {
    console.error('Error al cargar datos:', error);
    errorCarga.value = 'No se pudo conectar con la API. Verifica que el backend este encendido.';
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
    console.error('Error de autenticacion:', error);
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

const guardarProducto = async () => {
  try {
    await api.crearProducto(nuevoProducto.value);
    alert('Producto guardado exitosamente.');
    nuevoProducto.value = { nombre: '', marca: '', categoria: '', descripcion: '' };
    await cargarDatos();
  } catch (error) {
    console.error('Error al guardar:', error);
    alert(error.message);
  }
};

onMounted(async () => {
  await Promise.all([restaurarSesion(), cargarDatos()]);
});
</script>
