<template>
  <div class="f-page-view">
    <header class="f-header">
      <div class="f-header-content">
        <h1 class="text-title">Empleados</h1>
      </div>
      <div class="f-header-actions">
        <button 
          class="btn-f-base btn-f-text"
          @click="router.push({ name: 'employee-new' })"
        >
          <UserPlus class="icon-sm mr-2" />
          Alta Empleado
        </button>
      </div>
    </header>

    <div class="profile-grid">
      <aside class="profile-aside">
        <div class="identity-block-minimal">
          <div class="identity-text">
            <span class="text-label text-uppercase">Resumen de Plantilla</span>
          </div>
          
          <div class="aside-stats-stack">
            <div class="aside-stat-item">
              <span class="text-label">Personal Activo</span>
              <span class="text-primary f-tabular">{{ employees.length }}</span>
            </div>
            <div class="aside-stat-item">
              <span class="text-label">Proyectos Activos</span>
              <span class="text-primary f-tabular">{{ activeProjectsCount }}</span>
            </div>
          </div>
        </div>
      </aside>

      <main class="profile-main-list">
        <!-- SEARCH INTEGRADO -->
        <div class="search-area-naked">
          <EliteSearch v-model="search" placeholder="Buscar empleado..." />
        </div>

        <!-- NAKED LIST CONTAINER -->
        <div class="naked-list-container animate-in delay-1">
          <div class="list-header-minimal employee-grid px-8 pb-4">
            <div class="text-label">Información de Empleado</div>
            <div class="text-label text-right">NIF / NIE</div>
            <div class="text-label text-right">F. Nacimiento</div>
            <div class="text-label text-right">Teléfono</div>
            <div class="text-label text-center">Est. Civil</div>
            <div class="text-label text-center">Formación</div>
            <div class="text-label"></div>
          </div>

          <div v-if="loadingInitial" class="empty-state-elite">
            <RefreshCw class="icon-md spin mb-4" />
            <p>Sincronizando base de datos de capital humano...</p>
          </div>

          <div v-else class="list-body">
            <div v-for="item in displayedEmployees" :key="item.idEmployee" class="list-row-naked-crystal employee-grid align-center px-8 py-3">
              <!-- IZQUIERDA -->
              <div class="d-flex flex-column">
                <span class="text-primary">{{ item.firstName }} {{ item.lastName }} {{ item.secondLastName || '' }}</span>
                <span class="text-secondary">{{ item.email }}</span>
              </div>

              <!-- DERECHA -->
              <div class="text-secondary text-right f-tabular">{{ item.nif }}</div>
              <div class="text-secondary text-right f-tabular">{{ formatDate(item.birthDate) }}</div>
              <div class="text-secondary text-right f-tabular">{{ item.phone1 || '—' }}</div>
              <div class="text-secondary text-center">{{ item.maritalStatus === 'S' ? 'Soltero' : 'Casado' }}</div>
              <div class="text-secondary text-center">{{ item.hasUniversityEducation === 'S' ? 'Univ.' : 'Básico' }}</div>

              <div class="col-actions">
                <div class="row-actions-floating">
                  <button 
                    class="btn-f-base btn-f-text"
                    @click="router.push({ name: 'employee-edit', params: { id: item.idEmployee } })"
                  >
                    <Edit3 class="icon-xs" />
                  </button>
                  
                  <button 
                    class="btn-f-base btn-f-text"
                    style="color: #DC2626 !important;"
                    @click="confirmDelete(item)"
                  >
                    <UserMinus class="icon-xs" />
                  </button>
                </div>
              </div>
            </div>

            <!-- CARGADOR ELITE -->
            <div v-if="hasMore" class="text-center py-8">
              <button 
                class="btn-f-base btn-f-text"
                @click="loadMore"
              >
                Cargar más empleados
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- DIÁLOGO DE CESE ELITE -->
    <v-dialog v-model="confirmDialog.show" max-width="440" persistent scrim="rgba(15, 23, 42, 0.4)">
      <v-card class="pa-6" rounded="xl">
        <v-card-title class="px-0 pt-0 pb-2 font-weight-bold text-h6">
          Eliminar empleado
        </v-card-title>

        <v-card-text class="px-0 py-4 text-body-2">
          Esta acción eliminará permanentemente a <strong>{{ confirmDialog.employeeName }}</strong>.
          <br><span class="font-weight-bold mt-2 d-block">Esta acción no se puede deshacer.</span>
        </v-card-text>

        <v-card-actions class="px-0 pt-4 pb-0 justify-end">
          <v-btn variant="text" class="btn-f-base" @click="confirmDialog.show = false">
            Cancelar
          </v-btn>
          <v-btn color="error" variant="flat" class="btn-f-base" @click="handleTerminate">
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { UserPlus, Edit3, UserMinus, ChevronUp, ChevronDown, RefreshCw, Plus } from 'lucide-vue-next'
import CrystalCard from '@/components/common/CrystalCard.vue'
import EliteSearch from '@/components/common/EliteSearch.vue'
import { employeeService } from '@/services/employeeService'
import { projectService } from '@/services/projectService'
import { toast } from '@/services/toastService'

const router = useRouter()
const employees = ref([])
const activeProjectsCount = ref(0)
const search = ref('')
const sortBy = ref('firstName')
const sortDesc = ref(false)
const loadingInitial = ref(true)
const visibleCount = ref(10)

// Estado del Diálogo de Confirmación
const confirmDialog = reactive({
  show: false,
  employeeId: null,
  employeeName: ''
})

/**
 * Lógica de filtrado y ordenación alfabética humana (A-Z por Nombre completo)
 */
const filteredEmployees = computed(() => {
  let list = employees.value
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(e => 
      `${e.firstName} ${e.lastName}`.toLowerCase().includes(q) ||
      e.nif.toLowerCase().includes(q)
    )
  }
  return list.sort((a, b) => {
    let fieldA = (a[sortBy.value] || '').toString().toLowerCase()
    let fieldB = (b[sortBy.value] || '').toString().toLowerCase()
    
    if (sortBy.value === 'firstName') {
      fieldA = `${a.firstName} ${a.lastName}`.toLowerCase()
      fieldB = `${b.firstName} ${b.lastName}`.toLowerCase()
    }
    
    let mod = sortDesc.value ? -1 : 1
    return fieldA < fieldB ? -1 * mod : (fieldA > fieldB ? 1 * mod : 0)
  })
})

// Solo mostramos un trozo para no saturar la UI
const displayedEmployees = computed(() => {
  return filteredEmployees.value.slice(0, visibleCount.value)
})

const hasMore = computed(() => {
  return visibleCount.value < filteredEmployees.value.length
})

const loadMore = () => {
  visibleCount.value += 10
}

const toggleSort = (key) => {
  if (sortBy.value === key) sortDesc.value = !sortDesc.value
  else { sortBy.value = key; sortDesc.value = false }
}

const confirmDelete = (item) => {
  confirmDialog.employeeId = item.idEmployee
  confirmDialog.employeeName = `${item.firstName} ${item.lastName}`
  confirmDialog.show = true
}

const handleTerminate = async () => {
  try {
    await employeeService.delete(confirmDialog.employeeId)
    confirmDialog.show = false
    employees.value = await employeeService.getAll(false)
    toast.success('Cese tramitado correctamente')
  } catch (e) {
    confirmDialog.show = false
    toast.error(e.response?.data?.message || 'Error al procesar el cese')
  }
}

const formatDate = (date) => {
  if (!date) return '—'
  return new Date(date).toLocaleDateString('es-ES')
}

onMounted(async () => {
  try {
    // Solo cargamos activos por defecto como se pide
    const [empData, projData] = await Promise.all([
      employeeService.getAll(false),
      projectService.getAll(false)
    ])
    employees.value = empData
    activeProjectsCount.value = projData.length
  } catch (e) {
    console.error('Error al cargar datos:', e)
  } finally {
    loadingInitial.value = false
  }
})
</script>

<style scoped>
/* Layout estandarizado vía f-page-view */
.header-stats-minimal { display: flex; align-items: center; gap: 12px; margin-top: 8px; }
.stat-pill { background: #F1F5F9; padding: 2px 10px; border-radius: 99px; font-weight: 800; font-size: 12px; color: #64748B; }

/* Botón "Nuevo empleado" CLONADO EXACTO de ProfileView */
.btn-elite-outline {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none !important;
  color: rgb(var(--v-theme-primary));
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  transition: opacity 0.2s ease;
}

.btn-elite-outline:hover {
  opacity: 0.65;
}

.btn-elite-outline .icon-sm {
  width: 14px; /* Ajustado al estándar de icono de botón de texto */
  height: 14px;
  stroke-width: 1.75px;
}


.identity-text h2 {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: #1E293B;
  letter-spacing: -0.04em;
  line-height: 1;
}

.identity-text .role-text {
  font-size: 10px;
  color: #64748B;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 4px;
  display: block;
}

.aside-stats-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-top: 20px;
  border-top: 1px solid rgba(15, 23, 42, 0.05);
}

.aside-stat-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.stat-label {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  font-weight: 500;
  color: #64748B;
  letter-spacing: -0.03em;
  line-height: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1E293B;
  font-family: var(--font-display);
  letter-spacing: -0.02em;
}

.f-tabular { font-variant-numeric: tabular-nums; }

.profile-main-list { display: flex; flex-direction: column; }

.search-area-naked { margin-bottom: 24px; padding: 0 32px; }

.list-row-naked-crystal {
  position: relative;
  transition: all 0.2s ease; 
  border-left: 3px solid transparent;
  border-bottom: 1px solid #E2E8F0;
}

.list-row-naked-crystal:hover { 
  background: #F8FAFC;
  border-left-color: rgb(var(--v-theme-primary));
}

.f-center { display: flex; justify-content: center; text-align: center; }

.row-actions-floating { 
  opacity: 0; 
  transform: translateX(10px); 
  transition: 0.3s; 
  display: flex; 
  gap: 8px; 
  justify-content: flex-end;
}
.list-row-naked-crystal:hover .row-actions-floating { opacity: 1; transform: translateX(0); }

/* GRID SISTÉMICO PARA EMPLEADOS */
.employee-grid {
  display: grid;
  grid-template-columns: 1fr 100px 120px 110px 90px 90px 80px;
  gap: 16px;
  align-items: center;
}
</style>
