<template>
  <Transition name="toast-slide">
    <div v-if="modelValue" class="crystal-toast-elite">
      <div class="toast-glass-content" :class="type">
        <component :is="currentIcon" class="toast-icon-mini" />
        <span class="toast-text-mini">{{ message }}</span>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed, watch } from 'vue'
import { CheckCircle, AlertCircle, Info } from 'lucide-vue-next'

const props = defineProps({
  modelValue: Boolean,
  message: String,
  type: {
    type: String,
    default: 'success' // success, error, info
  },
  duration: {
    type: Number,
    default: 3000
  }
})

const emit = defineEmits(['update:modelValue'])

const currentIcon = computed(() => {
  if (props.type === 'error') return AlertCircle
  if (props.type === 'info') return Info
  return CheckCircle
})

watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    setTimeout(() => {
      emit('update:modelValue', false)
    }, props.duration)
  }
})
</script>

<style scoped>
.crystal-toast-elite {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  pointer-events: none;
}

.toast-glass-content {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  padding: 8px 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  border: 0.5px solid rgba(255, 255, 255, 0.2);
  box-shadow: none;
}

.toast-icon-mini {
  width: 12px;
  height: 12px;
  stroke-width: 1.5px;
}

/* Colores dinámicos solo en iconos */
.toast-glass-content.success .toast-icon-mini { color: #1E40AF; }
.toast-glass-content.error .toast-icon-mini { color: #EF4444; }
.toast-glass-content.info .toast-icon-mini { color: #64748B; }

.toast-text-mini {
  font-size: 12px;
  font-weight: 500;
  color: #475569;
  letter-spacing: -0.01em;
}

/* Animación de Caída Minimalista */
.toast-slide-enter-active { transition: all 0.4s cubic-bezier(0.2, 1, 0.3, 1); }
.toast-slide-leave-active { transition: all 0.3s ease; }
.toast-slide-enter-from { opacity: 0; transform: translateY(-10px); }
.toast-slide-leave-to { opacity: 0; transform: translateY(-5px); }
</style>
