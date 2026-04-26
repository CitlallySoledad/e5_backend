import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/'
});

const TOKEN_KEY = 'inventario_token';
const USER_KEY = 'inventario_user';

const getErrorMessage = (error, fallbackMessage) => {
    const data = error?.response?.data;
    if (data?.detail || data?.error) {
        return data.detail || data.error;
    }
    if (data && typeof data === 'object') {
        return Object.entries(data)
            .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
            .join(' | ');
    }
    return fallbackMessage;
};

const setToken = (token) => {
    if (token) {
        localStorage.setItem(TOKEN_KEY, token);
        api.defaults.headers.common.Authorization = `Bearer ${token}`;
        return;
    }
    localStorage.removeItem(TOKEN_KEY);
    delete api.defaults.headers.common.Authorization;
};

const getStoredUser = () => {
    const value = localStorage.getItem(USER_KEY);
    return value ? JSON.parse(value) : null;
};

const setStoredUser = (user) => {
    if (user) {
        localStorage.setItem(USER_KEY, JSON.stringify(user));
        return;
    }
    localStorage.removeItem(USER_KEY);
};

setToken(localStorage.getItem(TOKEN_KEY));

export default {
    getToken() {
        return localStorage.getItem(TOKEN_KEY);
    },
    getStoredUser,
    getProductos() {
        return api.get('productos/');
    },
    getCategorias() {
        return api.get('categorias/');
    },
    getMarcas() {
        return api.get('marcas/');
    },
    getTallas() {
        return api.get('tallas/');
    },
    getColores() {
        return api.get('colores/');
    },
    getVariantes() {
        return api.get('variantes/');
    },
    getRoles() {
        return api.get('roles/');
    },
    getUsuarios() {
        return api.get('usuarios/');
    },
    getVentas() {
        return api.get('ventas/');
    },
    login(credentials) {
        return api.post('auth/login/', credentials)
            .then((response) => {
                setToken(response.data.access);
                setStoredUser(response.data.user);
                return response.data;
            })
            .catch((error) => {
                throw new Error(getErrorMessage(error, 'No se pudo iniciar sesion.'));
            });
    },
    getPerfil() {
        return api.get('auth/me/')
            .then((response) => {
                setStoredUser(response.data);
                return response;
            })
            .catch((error) => {
                if (error?.response?.status === 401) {
                    setToken(null);
                    setStoredUser(null);
                }
                throw error;
            });
    },
    logout() {
        setToken(null);
        setStoredUser(null);
    },
    crearProducto(data) {
        return api.post('productos/', data).catch((error) => {
            throw new Error(getErrorMessage(error, 'No se pudo guardar el producto.'));
        });
    },
    crearCategoria(data) {
        return api.post('categorias/', data).catch((error) => {
            throw new Error(getErrorMessage(error, 'No se pudo guardar la categoria.'));
        });
    },
    crearMarca(data) {
        return api.post('marcas/', data).catch((error) => {
            throw new Error(getErrorMessage(error, 'No se pudo guardar la marca.'));
        });
    },
    crearTalla(data) {
        return api.post('tallas/', data).catch((error) => {
            throw new Error(getErrorMessage(error, 'No se pudo guardar la talla.'));
        });
    },
    crearColor(data) {
        return api.post('colores/', data).catch((error) => {
            throw new Error(getErrorMessage(error, 'No se pudo guardar el color.'));
        });
    },
    crearVariante(data) {
        return api.post('variantes/', data).catch((error) => {
            throw new Error(getErrorMessage(error, 'No se pudo guardar la variante.'));
        });
    },
    crearRole(data) {
        return api.post('roles/', data).catch((error) => {
            throw new Error(getErrorMessage(error, 'No se pudo guardar el rol.'));
        });
    },
    crearUsuario(data) {
        return api.post('usuarios/', data).catch((error) => {
            throw new Error(getErrorMessage(error, 'No se pudo guardar el usuario.'));
        });
    },
    crearVenta(data) {
        return api.post('ventas/', data).catch((error) => {
            throw new Error(getErrorMessage(error, 'No se pudo registrar la venta.'));
        });
    }
};
