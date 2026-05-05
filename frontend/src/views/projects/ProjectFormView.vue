<template>
  <div class="f-page-view animate-in">
    <header class="f-header">
      <div class="f-header-content">
        <h1 class="text-title">{{ isEdit ? 'Editar Proyecto' : 'Nuevo Proyecto' }}</h1>
      </div>
      <div class="f-header-actions">
        <button class="btn-f-base btn-f-text" @click="router.back()">
          Cancelar
        </button>
        <button class="btn-f-base btn-f-text" @click="save">
          <Check class="icon-xs mr-2" />
          Guardar proyecto
        </button>
      </div>
    </header>

    <div class="profile-grid">
      <aside class="profile-aside">
        <div class="identity-block-minimal">
          <div class="avatar-minimal">
            <span class="initials">{{ projectInitials }}</span>
          </div>
          <div class="identity-text">
            <h2 class="text-primary font-weight-bold">{{ form.description || 'Nuevo Proyecto' }}</h2>
            <span class="text-label text-uppercase">Ficha de Proyecto Operativo</span>
          </div>
        </div>
      </aside>

      <main class="profile-main f-card animate-in delay-1">
        <div class="settings-section">
          <div class="section-header">
            <h3 class="text-primary font-weight-bold mb-4">Datos Maestros</h3>
          </div>

          <div class="f-form-grid">
            <div class="f-span-2">
              <CrystalInput v-model="form.description" label="Nombre del Proyecto" :icon="Briefcase" :error="errors.description" maxlength="125" />
            </div>
            
            <CrystalInput 
              v-model="form.location" 
              label="Sede / Ubicación" 
              :icon="MapPin" 
              :error="errors.location" 
              maxlength="30"
            />

            <div class="f-input-group">
              <label class="text-label mb-1 d-block">Fecha de Inicio</label>
              <div class="f-input-wrapper" :class="{ 'has-error': errors.startDate }" @click="showStartPicker = !showStartPicker" v-click-outside="() => showStartPicker = false">
                <Calendar class="input-icon" />
                <div class="f-select-display">{{ formatDisplayDate(form.startDate) || 'Seleccionar fecha' }}</div>
                <transition name="fade-glass">
                  <div v-if="showStartPicker" class="f-dropdown-glass p-4" @click.stop>
                    <v-date-picker v-model="form.startDate" color="primary" flat hide-header />
                  </div>
                </transition>
              </div>
              <span v-if="errors.startDate" class="f-error-message">{{ errors.startDate }}</span>
            </div>

            <div class="f-input-group f-span-2">
              <label class="text-label mb-1 d-block">Fecha de Cierre (Prevista)</label>
              <div class="f-input-wrapper" :class="{ 'has-error': errors.endDate }" @click="showEndPicker = !showEndPicker" v-click-outside="() => showEndPicker = false">
                <Calendar class="input-icon" />
                <div class="f-select-display">{{ formatDisplayDate(form.endDate) || 'Seleccionar fecha' }}</div>
                <transition name="fade-glass">
                  <div v-if="showEndPicker" class="f-dropdown-glass p-4" @click.stop>
                    <v-date-picker v-model="form.endDate" color="primary" flat hide-header />
                  </div>
                </transition>
              </div>
              <span v-if="errors.endDate" class="f-error-message">{{ errors.endDate }}</span>
            </div>
          </div>
        </div>

        <div class="section-divider"></div>

        <div class="settings-section">
          <div class="section-header">
            <h3 class="text-primary font-weight-bold mb-4">Memorándum Operativo</h3>
          </div>
          <div class="f-form-grid">
            <div class="f-span-2">
              <label class="text-label mb-1 d-block">Observaciones Estratégicas</label>
              <v-textarea
                v-model="form.observations"
                variant="plain"
                maxlength="300"
                counter
                :error-messages="errors.observations"
                hide-details="auto"
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Check, RefreshCw, Briefcase, MapPin, Calendar } from 'lucide-vue-next'
import { projectService } from '@/services/projectService'
import { toast } from '@/services/toastService'
import CrystalInput from '@/components/common/CrystalInput.vue'

const route = useRoute()
const router = useRouter()
const isEdit = Boolean(route.params.id)
const isSaving = ref(false)
const showStartPicker = ref(false)
const showEndPicker = ref(false)
const errors = reactive({})

const form = reactive({ idProject: null, description: '', startDate: '', endDate: '', location: '', observations: '' })

const validateForm = () => {
  errors.description = !form.description ? 'Obligatorio' : form.description.length > 125 ? 'Máximo 125 caracteres' : ''
  errors.location = !form.location ? 'Obligatorio' : form.location.length > 30 ? 'Máximo 30 caracteres' : ''
  errors.startDate = !form.startDate ? 'Obligatorio' : ''
  errors.observations = !form.observations ? 'Obligatorio' : form.observations.length > 300 ? 'Máximo 300 caracteres' : ''
  if (form.startDate && form.endDate && new Date(form.endDate) <= new Date(form.startDate)) {
    errors.endDate = 'Debe ser posterior al inicio'
  } else { errors.endDate = '' }
  return !Object.values(errors).some(v => v !== '')
}

const formatDisplayDate = (date) => date ? new Date(date).toLocaleDateString('es-ES') : ''
const projectInitials = computed(() => form.description ? form.description.substring(0, 2).toUpperCase() : 'P')

const save = async () => {
  if (!validateForm()) return toast.error('Completa los campos obligatorios')
  isSaving.value = true
  try {
    if (isEdit) await projectService.update(form.idProject, form)
    else await projectService.create(form)
    toast.success('Proyecto guardado')
    router.push({ name: 'projects' })
  } catch (e) {
    const msg = e.response?.data?.message || 'Error al guardar el proyecto';
    toast.error(msg);
  } finally { isSaving.value = false }
}

onMounted(async () => {
  if (isEdit) Object.assign(form, await projectService.getById(route.params.id))
})
</script>

<style scoped>
.avatar-minimal {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #F8FAFC;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  border: 1px solid #E2E8F0;
}

.initials { font-family: 'Outfit'; font-size: 22px; color: #1E293B; font-weight: 700; }
.settings-section { padding: 12px 0; }
.section-divider { height: 1px; background: #E2E8F0; margin: 12px 0; }
.f-label-minimal { font-size: 11px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; }
.elite-textarea-minimal { background: rgba(255, 255, 255, 0.4); border: 1px solid rgba(15, 23, 42, 0.08); border-radius: 16px; padding: 12px; backdrop-filter: blur(8px); }
.p-4 { padding: 16px; }

.spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.icon-xs { width: 14px; height: 14px; }
</style>
