<template>
  <v-app class="elite-light-app">
    <div class="layout-container">
      
      <!-- Sidebar Fijo (Sticky) -->
      <aside class="sidebar-wrapper">
        <Sidebar v-model:collapsed="isCollapsed" />
      </aside>

      <!-- Contenido Principal con Margen Dinámico -->
      <div class="main-area" :style="{ paddingLeft: isCollapsed ? '100px' : '270px' }">
        <Topbar />
        
        <main class="f-view-layout">
          <router-view v-slot="{ Component }">
            <Transition name="fade" mode="out-in">
              <component :is="Component" />
            </Transition>
          </router-view>
        </main>
      </div>

    </div>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import Topbar from '@/components/layout/Topbar.vue'

const isCollapsed = ref(false)
</script>

<style scoped>
.elite-light-app {
  background-color: #F4F4F5 !important;
}

.layout-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

.sidebar-wrapper {
  position: sticky;
  top: 16px;
  height: calc(100vh - 32px);
  padding: 16px;
  z-index: 100;
}

.main-area {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  transition: padding-left 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Transición suave entre páginas */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
