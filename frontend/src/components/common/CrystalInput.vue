<template>
  <div class="f-input-group" :class="customClass">
    <label v-if="label">{{ label }}</label>
    <div 
      class="f-input-wrapper" 
      :class="{ 
        'has-error': error,
        'is-disabled': disabled 
      }"
    >
      <component :is="icon" v-if="icon" class="input-icon" />
      <input
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :type="type"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
      />
    </div>
    <transition name="fade-glass">
      <span v-if="error" class="f-error-message mt-1">{{ error }}</span>
    </transition>
  </div>
</template>

<script setup>
/**
 * Componente de entrada de datos estandarizado.
 * Utiliza las clases globales f-input para mantener la consistencia SaaS.
 */
defineProps({
  modelValue: [String, Number],
  label: String,
  placeholder: String,
  type: { type: String, default: 'text' },
  icon: [Object, Function],
  error: String,
  disabled: Boolean,
  readonly: Boolean,
  customClass: String
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
/* Sin estilos locales: toda la estetica emana de forms.css */
.mt-1 { margin-top: 4px; }
</style>
