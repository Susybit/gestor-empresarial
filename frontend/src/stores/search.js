import { defineStore } from 'pinia'

/**
 * Store global para la gestión de búsquedas en toda la plataforma.
 * Permite que el buscador del Topbar controle el filtrado de cualquier vista activa.
 */
export const useSearchStore = defineStore('search', {
  state: () => ({
    query: ''
  }),
  actions: {
    setQuery(val) {
      this.query = val
    },
    clear() {
      this.query = ''
    }
  }
})
