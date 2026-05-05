<template>
  <!-- Contenedor raíz obligatorio de Vuetify -->
  <v-app class="fsm-app">
    <router-view />
    <!-- SISTEMA DE NOTIFICACIONES GLOBAL CRYSTAL -->
    <CrystalToast 
      v-model="toast.show" 
      :message="toast.message" 
      :type="toast.type" 
    />
  </v-app>
</template>

<script setup>
import CrystalToast from '@/components/common/CrystalToast.vue'
import { toast } from '@/services/toastService'
</script>

<style>
/* Inyección de los estilos globales */
@import "@/assets/styles/main.css";

/* Fuerza el fondo corporativo en el canvas general de Vuetify */
.fsm-app {
  background-color: var(--v-theme-background) !important;
}
</style>
