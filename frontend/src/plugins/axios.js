import axios from 'axios';
import { toast } from '@/services/toastService';
import router from '@/router';

/**
 * Instancia de Axios configurada para el ecosistema Future Space.
 * Incluye interceptores para robustez y manejo global de estados de error.
 */
const api = axios.create({
  baseURL: 'http://localhost:8080',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Interceptor de Peticiones: Preparado para inyectar Tokens si fuera necesario
api.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
);

// Interceptor de Respuestas: El "Paracaídas" Global
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;
    const message = error.response?.data?.message || error.message;

    if (status === 401) {
      // Sesión caducada o no autorizada
      toast.error('Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.');
      router.push({ name: 'login' });
    } else if (status === 403) {
      toast.error('No tienes permisos suficientes para esta acción.');
    } else if (status >= 500) {
      // Errores críticos de servidor
      toast.error('Error crítico en el servidor. El equipo técnico ha sido notificado.');
    }

    console.error(`[API Error ${status || 'NET'}]: ${message}`);
    return Promise.reject(error);
  }
);

export default api;
