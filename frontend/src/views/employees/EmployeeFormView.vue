<template>
  <div class="f-page-view animate-in">
    <header class="f-header">
      <div class="f-header-content">
        <h1 class="text-title">{{ isEdit ? 'Editar Empleado' : 'Nuevo Empleado' }}</h1>
      </div>
      <div class="f-header-actions">
        <button class="btn-f-base btn-f-text" @click="router.back()">
          Cancelar
        </button>
        <button class="btn-f-base btn-f-text" @click="save">
          <Check class="icon-xs mr-2" />
          Guardar empleado
        </button>
      </div>
    </header>

    <div class="profile-grid">
      <aside class="profile-aside">
        <div class="identity-block-minimal">
          <div class="avatar-minimal">
            <span class="initials">{{ userInitials }}</span>
          </div>
          <div class="identity-text">
            <h2 class="text-primary font-weight-bold">{{ form.firstName || 'Nuevo' }} {{ form.lastName || 'Empleado' }}</h2>
            <span class="text-label text-uppercase">Ficha de empleado</span>
          </div>
        </div>
      </aside>

      <main class="profile-main f-card animate-in delay-1">
        <!-- SECCIÓN 1: DATOS PERSONALES -->
        <div class="settings-section">
          <div class="section-header">
            <h3 class="text-primary font-weight-bold mb-4">Datos Personales</h3>
          </div>

          <div class="f-form-grid">
            <CrystalInput v-model="form.firstName" label="Nombre" :icon="User" :error="errors.firstName" />
            <CrystalInput v-model="form.lastName" label="Primer Apellido" :icon="User" :error="errors.lastName" />
            <CrystalInput v-model="form.secondLastName" label="Segundo Apellido" :icon="User" :error="errors.secondLastName" />
            <CrystalInput 
              v-model="form.nif"
              label="NIF / NIE"
              placeholder="01234567J"
              :icon="CreditCard"
              :error="errors.nif"
              maxlength="9"
            />
            
            <!-- Selector de Fecha Estandarizado -->
            <div class="f-input-group">
              <label class="text-label mb-1 d-block">Fecha de Nacimiento</label>
              <div class="f-input-wrapper" :class="{ 'has-error': errors.birthDate }" @click="showDatePicker = !showDatePicker" v-click-outside="() => showDatePicker = false">
                <Calendar class="input-icon" />
                <div class="f-select-display">{{ formatDisplayDate(form.birthDate) || 'Seleccionar fecha' }}</div>
                <transition name="fade-glass">
                  <div v-if="showDatePicker" class="f-dropdown-glass p-4" @click.stop>
                    <v-date-picker v-model="form.birthDate" color="primary" flat hide-header />
                  </div>
                </transition>
              </div>
              <span v-if="errors.birthDate" class="f-error-message">{{ errors.birthDate }}</span>
            </div>

            <!-- Selector de Estado Civil Estandarizado -->
            <div class="f-input-group">
              <label class="text-label mb-1 d-block">Estado Civil</label>
              <div class="f-input-wrapper" @click="toggleSelect('marital')" v-click-outside="() => closeSelect('marital')">
                <Users class="input-icon" />
                <div class="f-select-display">{{ getLabel(form.maritalStatus, maritalOptions) }}</div>
                <transition name="fade-glass">
                  <div v-if="activeSelect === 'marital'" class="f-dropdown-glass">
                    <div v-for="opt in maritalOptions" :key="opt.value" class="select-option" @click.stop="selectOpt('marital', opt.value)">
                      {{ opt.label }}
                    </div>
                  </div>
                </transition>
              </div>
            </div>
          </div>
        </div>

        <div class="section-divider"></div>

        <!-- SECCIÓN 2: INFORMACIÓN CORPORATIVA -->
        <div class="settings-section">
          <div class="section-header">
            <h3 class="text-primary font-weight-bold mb-4">Información Corporativa</h3>
          </div>
          <div class="f-form-grid">
            <CrystalInput v-model="form.email" label="Email Corporativo" type="email" :icon="Mail" :error="errors.email" />
            <CrystalInput v-model="form.phone1" label="Teléfono Principal" :icon="Phone" :error="errors.phone1" />
            <CrystalInput v-model="form.phone2" label="Teléfono Secundario" :icon="Phone" :error="errors.phone2" />
            <CrystalInput :modelValue="form.hireDate" label="Fecha de Alta" :icon="Lock" disabled readonly />
          </div>
        </div>

        <div class="section-divider"></div>

        <!-- SECCIÓN 3: NIVEL ACADÉMICO -->
        <div class="settings-section">
          <div class="section-header">
            <h3 class="text-primary font-weight-bold mb-4">Nivel Académico</h3>
          </div>
          <div class="f-form-grid">
            <div class="f-input-group f-span-2">
              <label class="text-label mb-1 d-block">Formación</label>
              <div class="f-input-wrapper" @click="toggleSelect('education')" v-click-outside="() => closeSelect('education')">
                <GraduationCap class="input-icon" />
                <div class="f-select-display">{{ getLabel(form.hasUniversityEducation, educationOptions) }}</div>
                <transition name="fade-glass">
                  <div v-if="activeSelect === 'education'" class="f-dropdown-glass">
                    <div v-for="opt in educationOptions" :key="opt.value" class="select-option" @click.stop="selectOpt('education', opt.value)">
                      {{ opt.label }}
                    </div>
                  </div>
                </transition>
              </div>
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
import { User, Mail, Phone, Calendar, GraduationCap, CreditCard, Lock, Users, ArrowLeft, Check, RefreshCw } from 'lucide-vue-next'
import { employeeService } from '@/services/employeeService'
import { toast } from '@/services/toastService'
import CrystalInput from '@/components/common/CrystalInput.vue'

const route = useRoute()
const router = useRouter()
const isEdit = Boolean(route.params.id)
const isSaving = ref(false)
const showDatePicker = ref(false)
const activeSelect = ref(null)
const errors = reactive({})

const form = reactive({
  idEmployee: null, nif: '', firstName: '', lastName: '', secondLastName: '',
  birthDate: '', phone1: '', phone2: '', email: '',
  hireDate: new Date().toISOString().split('T')[0],
  hasUniversityEducation: 'N', maritalStatus: 'S'
})

const maritalOptions = [{ label: 'Soltero / a', value: 'S' }, { label: 'Casado / a', value: 'C' }]
const educationOptions = [{ label: 'Título Universitario / Grado Superior', value: 'S' }, { label: 'No tiene título universitario', value: 'N' }]

const validateForm = () => {
  errors.firstName = !form.firstName ? 'Obligatorio' : form.firstName.length < 2 ? 'Mínimo 2 caracteres' : form.firstName.length > 30 ? 'Máximo 30' : ''
  errors.lastName = !form.lastName ? 'Obligatorio' : form.lastName.length < 2 ? 'Mínimo 2 caracteres' : form.lastName.length > 40 ? 'Máximo 40' : ''
  errors.nif = !form.nif ? 'Obligatorio' : !/^[0-9]{8}[A-Za-z]$/.test(form.nif) ? 'Formato: 8 números + letra' : ''
  errors.email = !form.email ? 'Obligatorio' : !/.+@.+\..+/.test(form.email) ? 'Email inválido' : form.email.length > 40 ? 'Máximo 40' : ''
  errors.phone1 = !form.phone1 ? 'Obligatorio' : !/^[0-9]{9,12}$/.test(form.phone1) ? 'De 9 a 12 dígitos' : ''
  errors.birthDate = !form.birthDate ? 'Obligatorio' : ''
  return !Object.values(errors).some(v => v !== '')
}

const formatDisplayDate = (date) => date ? new Date(date).toLocaleDateString('es-ES') : ''
const toggleSelect = (type) => activeSelect.value = activeSelect.value === type ? null : type
const closeSelect = (type) => { if (activeSelect.value === type) activeSelect.value = null }
const selectOpt = (type, val) => {
  if (type === 'marital') form.maritalStatus = val
  else form.hasUniversityEducation = val
  activeSelect.value = null
}
const getLabel = (val, opts) => opts.find(o => o.value === val)?.label || ''

const userInitials = computed(() => (form.firstName?.charAt(0) || '') + (form.lastName?.charAt(0) || ''))

const save = async () => {
  if (!validateForm()) return toast.error('Revisa los campos obligatorios')
  isSaving.value = true
  try {
    if (isEdit) await employeeService.update(form.idEmployee, form)
    else await employeeService.create(form)
    toast.success('Empleado guardado')
    router.push({ name: 'employees' })
  } catch (e) {
    const msg = e.response?.data?.message || 'Error al guardar el empleado';
    toast.error(msg);
  } finally { isSaving.value = false }
}

onMounted(async () => {
  if (isEdit) Object.assign(form, await employeeService.getById(route.params.id))
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
.role-text { font-size: 10px; color: #64748B; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
.settings-section { padding: 12px 0; }
.section-divider { height: 1px; background: #E2E8F0; margin: 12px 0; }
.select-option { padding: 12px 16px; font-size: 13px; font-weight: 500; color: #475569; cursor: pointer; transition: 0.2s; }
.select-option:hover { background: rgba(var(--v-theme-primary), 0.05); color: rgb(var(--v-theme-primary)); }
.p-4 { padding: 16px; }

.spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.icon-xs { width: 14px; height: 14px; }
</style>
