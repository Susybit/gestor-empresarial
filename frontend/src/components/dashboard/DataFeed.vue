<template>
  <div class="f-card data-feed-container">
    <div class="card-head">
      <div class="title-group">
        <h3 class="f-card-title">{{ title }}</h3>
        <p class="f-card-subtitle">{{ subtitle }}</p>
      </div>
    </div>

    <!-- LISTADO DE SEDES -->
    <div class="feed-body">
      <div class="location-stack">
        <div v-for="loc in locations" :key="loc.name" class="location-row">
          <div class="loc-info">
            <span class="loc-name">{{ loc.name }}</span>
            <span class="loc-pct f-tabular">{{ loc.pct }}%</span>
          </div>
          <div class="loc-bar-bg">
            <div class="loc-bar-fill" :style="{ width: loc.pct + '%' }"></div>
          </div>
        </div>
      </div>

      <div class="divider"></div>

      <!-- ÚLTIMOS PROYECTOS -->
      <div class="recent-projects">
        <h4 class="mini-title">Altas Recientes</h4>
        <div class="project-mini-list">
          <div v-for="p in latestProjects" :key="p.idProject" class="project-mini-item">
            <div class="p-dot"></div>
            <div class="p-text">
              <span class="p-name">{{ p.projectName }}</span>
              <span class="p-loc">{{ p.location }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  subtitle: String,
  locations: Array,
  latestProjects: Array
})
</script>

<style scoped>
.data-feed-container { display: flex; flex-direction: column; gap: 24px; }
.location-stack { display: flex; flex-direction: column; gap: 16px; }
.location-row { display: flex; flex-direction: column; gap: 6px; }
.loc-info { display: flex; justify-content: space-between; align-items: center; }
.loc-name { font-size: 13px; font-weight: 600; color: #1E293B; }
.loc-pct { font-size: 12px; font-weight: 700; color: #64748B; }
.loc-bar-bg { width: 100%; height: 6px; background: rgba(15, 23, 42, 0.04); border-radius: 99px; overflow: hidden; }
.loc-bar-fill { height: 100%; background: #4F46E5; border-radius: 99px; }

.divider { height: 1px; background: rgba(15, 23, 42, 0.05); margin: 8px 0; }

.mini-title { font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 16px; }
.project-mini-list { display: flex; flex-direction: column; gap: 14px; }
.project-mini-item { display: flex; align-items: center; gap: 12px; }
.p-dot { width: 6px; height: 6px; border-radius: 50%; background: #1E40AF; flex-shrink: 0; }
.p-text { display: flex; flex-direction: column; }
.p-name { font-size: 13px; font-weight: 600; color: #1E293B; line-height: 1.2; }
.p-loc { font-size: 11px; color: #64748B; font-weight: 500; }

.f-tabular { font-variant-numeric: tabular-nums; }
</style>
