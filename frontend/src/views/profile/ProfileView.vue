<template>
  <div class="f-page-view animate-in">
    <header class="f-header">
      <div class="f-header-content">
        <h1 class="text-title">Mi Perfil</h1>
      </div>
      <div class="f-header-actions">
        <button 
          class="btn-f-base btn-f-text"
          @click="router.push({ name: 'dashboard' })"
        >
          Cancelar
        </button>
        <button 
          class="btn-f-base btn-f-text"
          @click="handleSave"
        >
          <Check class="icon-xs mr-2" />
          Guardar cambios
        </button>
      </div>
    </header>

    <div class="profile-grid">
      <aside class="profile-aside">
        <div class="identity-block-minimal">
          <div class="avatar-container">
            <div class="avatar-main">
              <img v-if="avatarUrl" :src="avatarUrl" alt="Avatar" />
              <span v-else class="initials">{{ userInitials }}</span>
            </div>
            <div class="avatar-buttons">
              <v-btn icon variant="text" size="small" color="primary" @click="triggerFileInput">
                <Camera class="icon-xs" />
              </v-btn>
              <v-btn v-if="avatarUrl" icon variant="text" size="small" color="error" @click="removePhoto">
                <Trash2 class="icon-xs" />
              </v-btn>
            </div>
          </div>
          <div class="identity-text text-center">
            <span class="text-label text-uppercase">Configuración de Perfil</span>
          </div>
        </div>
      </aside>

      <main class="profile-main f-card animate-in delay-1">
        <div class="settings-section">
          <div class="section-header">
            <h3 class="text-primary font-weight-bold mb-4">Información de Cuenta</h3>
          </div>
          <div class="f-form-grid">
            <CrystalInput v-model="fullNameDisplay" label="Nombre Completo" :icon="User" />
            <CrystalInput :modelValue="fullEmployeeData.email" label="Email Corporativo" :icon="Lock" disabled readonly />
          </div>
        </div>
      </main>
    </div>
    <input type="file" ref="fileInput" style="display: none" accept="image/*" @change="handleFileChange" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/plugins/axios'
import { Camera, RefreshCw, Trash2, ArrowLeft, Check, User, Mail, Lock } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { toast } from '@/services/toastService'
import CrystalInput from '@/components/common/CrystalInput.vue'

const router = useRouter()
const authStore = useAuthStore()
const isSaving = ref(false)
const avatarUrl = ref(localStorage.getItem('fsm_user_avatar') || '')
const fileInput = ref(null)

const fullEmployeeData = ref({ firstName: '', lastName: '', email: '' })

const fullNameDisplay = computed({
  get: () => `${fullEmployeeData.value.firstName} ${fullEmployeeData.value.lastName}`.trim(),
  set: (val) => {
    const parts = val.trim().split(' ')
    fullEmployeeData.value.firstName = parts[0] || ''
    fullEmployeeData.value.lastName = parts.slice(1).join(' ') || ''
  }
})

const userInitials = computed(() => (fullEmployeeData.value.firstName?.charAt(0) || '') + (fullEmployeeData.value.lastName?.charAt(0) || ''))

const triggerFileInput = () => fileInput.value.click()
const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (event) => { avatarUrl.value = event.target.result }
    reader.readAsDataURL(file)
  }
}
const removePhoto = () => avatarUrl.value = ''

const handleSave = async () => {
  isSaving.value = true
  try {
    const dataToSave = { ...fullEmployeeData.value, imageUrl: avatarUrl.value || '' }
    await api.put(`/employees/${fullEmployeeData.value.idEmployee}`, dataToSave)
    localStorage.setItem('fsm_user_name', fullNameDisplay.value)
    if (avatarUrl.value) localStorage.setItem('fsm_user_avatar', avatarUrl.value)
    else localStorage.removeItem('fsm_user_avatar')
    window.dispatchEvent(new CustomEvent('profile-updated'))
    toast.success('Perfil actualizado')
    router.push({ name: 'dashboard' })
  } catch (error) { toast.error('Error al guardar') }
  finally { isSaving.value = false }
}

onMounted(async () => {
  try {
    const res = await api.get('/employees')
    const employees = res.data.content || res.data
    const me = employees.find(e => e.email === authStore.user?.email) || employees[0]
    if (me) {
      fullEmployeeData.value = { ...me }
      if (!avatarUrl.value && me.imageUrl) avatarUrl.value = me.imageUrl
    }
  } catch (e) { toast.error('Error al cargar perfil') }
})
</script>

<style scoped>
.profile-header { display: none; }
.identity-block-minimal { align-items: center; }
.avatar-container { position: relative; margin-bottom: 20px; }
.avatar-main { 
  width: 80px; 
  height: 80px; 
  border-radius: 50%; 
  background: #F8FAFC; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  overflow: hidden; 
  border: 1px solid #E2E8F0;
}
.avatar-main img { width: 100%; height: 100%; object-fit: cover; }
.initials { font-family: 'Outfit'; font-size: 22px; color: #1E293B; font-weight: 700; }
.avatar-buttons { display: flex; gap: 8px; margin-top: 12px; justify-content: center; }
.settings-section { padding: 8px 0; }
.text-center { text-align: center; }

.spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.icon-xs { width: 14px; height: 14px; }
</style>
