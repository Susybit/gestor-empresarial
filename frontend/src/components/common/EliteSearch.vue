<template>
  <div class="elite-search-wrapper" :class="{ 'is-focused': isFocused, 'has-content': modelValue }">
    <Search class="search-icon" />
    <input
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      @focus="isFocused = true"
      @blur="isFocused = false"
      type="text"
      :placeholder="placeholder"
      class="elite-search-input"
    />
    <button 
      v-if="modelValue" 
      class="clear-btn" 
      @click="$emit('update:modelValue', '')"
    >
      <X class="icon-tiny" />
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Search, X } from 'lucide-vue-next'

defineProps({
  modelValue: String,
  placeholder: { type: String, default: 'Buscar...' }
})

defineEmits(['update:modelValue'])

const isFocused = ref(false)
</script>

<style scoped>
.elite-search-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0px; /* Sin padding lateral para que sea camaleón total */
  background: transparent;
  border-bottom: 1px solid transparent; /* Borde invisible por defecto */
  width: 250px;
  transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
  position: relative;
}

/* Efecto Camaleón en Foco */
.elite-search-wrapper.is-focused {
  width: 320px; /* Ancho más contenido */
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(4px);
  border-radius: 99px;
  border: 1px solid rgba(30, 64, 175, 0.2);
}

.search-icon {
  width: 18px;
  height: 18px;
  color: #94A3B8;
  transition: all 0.3s;
}

.elite-search-wrapper.is-focused .search-icon {
  color: #1E40AF;
}

.elite-search-input {
  width: 100%;
  background: none;
  border: none;
  outline: none;
  font-size: 14px;
  font-weight: 500;
  color: #0F172A;
}

.elite-search-input::placeholder {
  color: #CBD5E1;
  font-weight: 400;
}

/* Botón X Minimalista SIN CÍRCULO */
.clear-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none; /* Sin círculo */
  border: none;
  padding: 0;
  cursor: pointer;
  color: #94A3B8;
  transition: 0.2s;
}

.clear-btn:hover {
  color: #0F172A;
  transform: scale(1.1);
}

.icon-tiny {
  width: 12px;
  height: 12px;
}
</style>
