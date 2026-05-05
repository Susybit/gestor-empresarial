<template>
  <div class="stat-card-elite">
    <div class="stat-header">
      <div class="stat-icon-box" :style="{ backgroundColor: accent + '10', color: accent }">
        <component :is="icon" class="icon-stat" />
      </div>
      <span class="stat-label">{{ label }}</span>
    </div>
    
    <div class="stat-content">
      <div class="stat-value-group">
        <span class="stat-value f-tabular">{{ value }}</span>
        <span v-if="suffix" class="stat-suffix">{{ suffix }}</span>
      </div>
      <div class="stat-trend" v-if="trendLabel">
        <span class="trend-text">{{ trendLabel }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [Number, String],
  suffix: String,
  icon: [Object, Function],
  accent: { type: String, default: '#64748B' },
  trendLabel: String
})
</script>

<style scoped>
.stat-card-elite {
  background: white;
  padding: 24px;
  border-radius: 24px;
  border: 1px solid rgba(15, 23, 42, 0.05);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
  transition: transform 0.3s ease;
}

.stat-card-elite:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.04);
}

.stat-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }

.stat-icon-box {
  width: 40px; height: 40px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
}

.icon-stat { width: 20px; height: 20px; stroke-width: 2.25px; }

.stat-label { font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; }

.stat-value-group { display: flex; align-items: baseline; gap: 4px; }
.stat-value { font-family: var(--font-display); font-size: 32px; font-weight: 800; color: #1E293B; letter-spacing: -0.04em; }
.stat-suffix { font-size: 16px; font-weight: 700; color: #94A3B8; }

.stat-trend { margin-top: 8px; }
.trend-text { font-size: 11px; font-weight: 600; color: #94A3B8; }

.f-tabular { font-variant-numeric: tabular-nums; }
</style>
