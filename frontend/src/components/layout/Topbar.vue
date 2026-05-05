<template>
  <header class="topbar">
    <div class="topbar-left">
      <!-- Mantenemos limpio para no interferir con los títulos de las vistas -->
    </div>
    <div class="topbar-right">
      <!-- Espacio reservado para perfil o acciones futuras -->
    </div>
  </header>
</template>

<script setup>
/**
 * TOPBAR - VERSIÓN MINIMALISTA
 * Se han eliminado los buscadores globales para evitar duplicidad visual.
 */
</script>

<style scoped>
.topbar {
  height: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 64px;
  background-color: transparent;
  position: relative;
  z-index: 50;
}
</style>
