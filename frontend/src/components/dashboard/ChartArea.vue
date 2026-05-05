<template>
  <div class="f-card">
    <div class="card-head">
      <div class="title-group">
        <h3 class="f-card-title">{{ title }}</h3>
        <p class="f-card-subtitle">{{ subtitle }}</p>
      </div>
    </div>
    
    <div class="chart-viewport" v-if="hasData">
      <Line :data="chartData" :options="chartOptions" />
    </div>
    
    <div v-else class="empty-state">
      <div class="empty-icon-box">
        <BarChart3 class="empty-icon" />
      </div>
      <p class="empty-text">Sin registros históricos suficientes</p>
      <p class="empty-sub">Comienza a registrar proyectos para ver la evolución.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { BarChart3 } from 'lucide-vue-next'
import 'chart.js/auto'

const props = defineProps({
  title: { type: String, default: 'Tendencia' },
  subtitle: { type: String, default: 'Análisis de datos' },
  data: { type: Array, default: () => [] }
})

const hasData = computed(() => {
  const values = props.data || []
  return values.length > 0 && values.some(v => Number(v) > 0)
})

const chartData = computed(() => ({
  labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
  datasets: [{
    label: 'Crecimiento',
    data: props.data.map(v => Number(v)),
    borderColor: '#4F46E5',
    backgroundColor: 'rgba(79, 70, 229, 0.1)',
    fill: true,
    tension: 0.4,
    pointRadius: 4,
    pointBackgroundColor: '#FFF',
    borderWidth: 3
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { grid: { display: false }, ticks: { font: { size: 10 }, color: '#94A3B8' } },
    y: { grid: { color: 'rgba(0,0,0,0.03)' }, ticks: { display: false } }
  }
}
</script>

<style scoped>
.card-head { margin-bottom: 24px; }
.chart-viewport { height: 280px; }
.empty-state { height: 280px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.empty-icon-box { width: 60px; height: 60px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 20px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; }
.empty-icon { color: #64748B; width: 24px; height: 24px; }
.empty-text { font-weight: 700; color: #1E293B; font-size: 14px; }
.empty-sub { font-size: 12px; color: #64748B; margin-top: 4px; }
</style>
