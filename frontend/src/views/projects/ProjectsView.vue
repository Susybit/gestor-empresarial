<template>
  <div class="f-page-view">
    <header class="f-header">
      <div class="f-header-content">
        <h1 class="text-title">Proyectos</h1>
      </div>
      <div class="f-header-actions">
        <button 
          class="btn-f-base btn-f-text"
          @click="router.push({ name: 'assignments' })"
        >
          <Users class="icon-sm mr-2" />
          Asignaciones
        </button>
        
        <button 
          class="btn-f-base btn-f-text"
          @click="router.push({ name: 'project-new' })"
        >
          <Plus class="icon-sm mr-2" />
          Alta Proyecto
        </button>
      </div>
    </header>

    <div class="profile-grid">
      <aside class="profile-aside">
        <div class="identity-block-minimal">
          <div class="identity-text">
            <span class="text-label text-uppercase">Cartera Operativa</span>
          </div>
          
          <div class="aside-stats-stack">
            <div class="aside-stat-item">
              <span class="text-label">Proyectos Activos</span>
              <span class="text-primary f-tabular">{{ projects.length }}</span>
            </div>
            <div class="aside-stat-item">
              <span class="text-label">Sedes Operativas</span>
              <span class="text-primary f-tabular">{{ uniqueLocationsCount }}</span>
            </div>
          </div>
        </div>
      </aside>

      <main class="profile-main-list">
        <!-- SEARCH INTEGRADO -->
        <div class="search-area-naked">
          <EliteSearch v-model="search" placeholder="Filtrar proyectos por nombre o ubicación..." />
        </div>

        <!-- NAKED LIST CONTAINER -->
        <div class="naked-list-container animate-in delay-1">
          <div class="list-header-minimal project-grid px-8 pb-4">
            <div class="text-label">Identificación de Proyecto</div>
            <div class="text-label text-right">Inicio</div>
            <div class="text-label text-right">Cierre</div>
            <div class="text-label"></div>
          </div>

          <div v-if="loading" class="empty-state-elite">
            <RefreshCw class="icon-md spin mb-4" />
            <p>Sincronizando cartera estratégica...</p>
          </div>

          <div v-else class="list-body">
            <div v-for="item in displayedProjects" :key="item.idProject" class="list-row-naked-crystal project-grid align-center px-8 py-3">
              <div class="d-flex flex-column">
                <span class="text-primary">{{ item.description }}</span>
                <span class="text-secondary">{{ item.location }}</span>
              </div>

              <div class="text-secondary text-right f-tabular">{{ formatDate(item.startDate) }}</div>
              <div class="text-secondary text-right f-tabular">{{ formatDate(item.endDate) }}</div>

              <div class="col-actions">
                <div class="row-actions-floating">
                  <button 
                    class="btn-f-base btn-f-text"
                    @click="router.push({ name: 'project-edit', params: { id: item.idProject } })"
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
                Cargar más proyectos
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
          Eliminar proyecto
        </v-card-title>

        <v-card-text class="px-0 py-4 text-body-2">
          Esta acción eliminará permanentemente <strong>{{ confirmDialog.projectName }}</strong>.
          <br><span class="font-weight-bold mt-2 d-block">Esta acción no se puede deshacer.</span>
        </v-card-text>

        <v-card-actions class="px-0 pt-4 pb-0 justify-end">
          <v-btn variant="text" class="btn-f-base" @click="confirmDialog.show = false">
            Cancelar
          </v-btn>
          <v-btn color="error" variant="flat" class="btn-f-base" @click="handleDelete">
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
import { Users, Plus, Edit3, UserMinus, ChevronUp, ChevronDown, RefreshCw } from 'lucide-vue-next'
import CrystalCard from '@/components/common/CrystalCard.vue'
import EliteSearch from '@/components/common/EliteSearch.vue'
import { projectService } from '@/services/projectService'
import { toast } from '@/services/toastService'

const router = useRouter()
const projects = ref([])
const search = ref('')
const sortBy = ref('description')
const sortDesc = ref(false)
const loading = ref(true)
const visibleCount = ref(10)

const confirmDialog = reactive({
  show: false,
  projectId: null,
  projectName: ''
})

const uniqueLocationsCount = computed(() => {
  return new Set(projects.value.map(p => p.location)).size
})

const filteredProjects = computed(() => {
  let list = projects.value
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(p => p.description.toLowerCase().includes(q) || p.location.toLowerCase().includes(q))
  }
  return list.sort((a, b) => {
    let fieldA = (a[sortBy.value] || '').toString().toLowerCase()
    let fieldB = (b[sortBy.value] || '').toString().toLowerCase()
    let mod = sortDesc.value ? -1 : 1
    return fieldA < fieldB ? -1 * mod : (fieldA > fieldB ? 1 * mod : 0)
  })
})

const displayedProjects = computed(() => {
  return filteredProjects.value.slice(0, visibleCount.value)
})

const hasMore = computed(() => {
  return visibleCount.value < filteredProjects.value.length
})

const loadMore = () => {
  visibleCount.value += 10
}

const toggleSort = (key) => {
  if (sortBy.value === key) sortDesc.value = !sortDesc.value
  else { sortBy.value = key; sortDesc.value = false }
}

const confirmDelete = (item) => {
  confirmDialog.projectId = item.idProject
  confirmDialog.projectName = item.description
  confirmDialog.show = true
}

const handleDelete = async () => {
  try {
    await projectService.delete(confirmDialog.projectId)
    confirmDialog.show = false
    projects.value = await projectService.getAll(false)
    toast.success('Proyecto eliminado correctamente')
  } catch (e) {
    confirmDialog.show = false
    toast.error('Error al eliminar el proyecto')
  }
}

const formatDate = (date) => {
  if (!date) return '—'
  return new Date(date).toLocaleDateString('es-ES')
}

onMounted(async () => {
  try {
    projects.value = await projectService.getAll(false)
  } catch (e) {
    console.error('Error:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
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

.row-actions-floating { 
  opacity: 0; 
  transform: translateX(10px); 
  transition: 0.3s; 
  display: flex; 
  gap: 8px; 
  justify-content: flex-end;
}
.list-row-naked-crystal:hover .row-actions-floating { opacity: 1; transform: translateX(0); }

/* GRID SISTÉMICO PARA PROYECTOS */
.project-grid {
  display: grid;
  grid-template-columns: 1fr 120px 120px 80px;
  gap: 16px;
  align-items: center;
}
</style>
