import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/'
});

const TOKEN_KEY = 'inventario_token';
const USER_KEY = 'inventario_user';

const getErrorMessage = (error, fallbackMessage) => {
    return error?.response?.data?.detail || error?.response?.data?.error || fallbackMessage;
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
    }
};
