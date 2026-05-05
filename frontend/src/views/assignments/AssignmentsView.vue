<template>
  <div class="f-page-view">
    <header class="f-header">
      <div class="f-header-content">
        <h1 class="text-title">Asignaciones</h1>
      </div>
      <div class="f-header-actions">
        <button 
          class="btn-f-base btn-f-text"
          @click="$router.push('/projects')"
        >
          Volver
        </button>
      </div>
    </header>

    <div class="profile-grid">
      <!-- PANEL LATERAL DE IDENTIDAD -->
      <aside class="profile-aside">
        <div class="identity-block-minimal animate-in">
          <div class="identity-text">
            <span class="text-label text-uppercase">Resumen de Asignación</span>
          </div>
          
          <div class="aside-stats-stack">
            <div class="aside-stat-item">
              <span class="text-label">Personal Asignado</span>
              <span class="text-primary f-tabular">{{ assignedCount }}</span>
            </div>
            <div class="aside-stat-item">
              <span class="text-label">Proyecto Seleccionado</span>
              <span class="text-primary f-tabular" style="font-size: 14px; line-height: 1.2;">
                {{ selectedProjectLabel || 'Ninguno' }}
              </span>
            </div>
          </div>
        </div>
      </aside>

      <!-- ÁREA PRINCIPAL -->
      <main class="profile-main-list">
        <!-- ÁREA DE CONTROL INTEGRADA -->
        <div class="control-area-elite animate-in delay-1">
          <div class="search-group">
            <EliteSearch v-model="search" placeholder="Filtrar empleados por nombre o NIF..." />
          </div>
          
          <div class="project-selector-wrapper">
            <v-select
              v-model="selectedProject"
              :items="projects"
              item-title="description"
              item-value="idProject"
              label="Seleccionar Proyecto Estratégico"
              variant="outlined"
              density="comfortable"
              hide-details
              prepend-inner-icon="mdi-briefcase-outline"
              @update:model-value="fetchAssignments"
              class="elite-select-naked"
            />
          </div>
        </div>

        <!-- LISTA NAKED CRYSTAL (Igual que empleados) -->
        <div class="naked-list-container animate-in delay-2">
          <!-- Cabecera de la lista -->
          <div class="list-header-minimal assignment-grid px-8 pb-4">
            <div class="text-label">Información de Empleado</div>
            <div class="text-label text-right">NIF / NIE</div>
            <div class="text-label"></div>
          </div>

          <div v-if="!selectedProject" class="empty-state-elite">
            <div class="empty-icon-wrapper">
              <FileText class="empty-icon" />
            </div>
            <p>Selecciona un proyecto para gestionar el equipo</p>
          </div>

          <div v-else class="list-body">
            <div 
              v-for="item in filteredAssignments" 
              :key="item.idEmployee" 
              class="list-row-naked-crystal assignment-grid align-center px-8 py-3"
            >
              <div class="d-flex flex-column">
                <span class="text-primary">{{ item.firstName }} {{ item.lastName }} {{ item.secondLastName || '' }}</span>
                <span class="text-secondary">{{ item.email }}</span>
              </div>

              <div class="text-secondary text-right f-tabular">{{ item.nif }}</div>

              <div class="d-flex justify-center">
                <v-checkbox-btn
                  :model-value="item.assigned"
                  :loading="processingId === item.idEmployee"
                  color="primary"
                  @update:model-value="(val) => toggleAssignment(item, val)"
                />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from "vue";
import { FileText, Briefcase, Users, ChevronDown } from 'lucide-vue-next';
import EliteSearch from '@/components/common/EliteSearch.vue';
import api from "@/plugins/axios";
import { toast } from '@/services/toastService';

const loading = ref(false);
const search = ref('');
const processingId = ref(null);
const projects = ref([]);
const assignments = ref([]); 
const selectedProject = ref(null);

const assignedCount = computed(() => assignments.value.filter(a => a.assigned).length);
const selectedProjectLabel = computed(() => projects.value.find(p => p.idProject === selectedProject.value)?.description);

const filteredAssignments = computed(() => {
  if (!search.value) return assignments.value;
  const q = search.value.toLowerCase();
  return assignments.value.filter(a => 
    `${a.firstName} ${a.lastName}`.toLowerCase().includes(q) ||
    a.nif.toLowerCase().includes(q)
  );
});

const init = async () => {
  try {
    const response = await api.get("/projects");
    projects.value = response.data.content || response.data;
  } catch (e) {
    toast.error("Error al recuperar catálogo de proyectos");
  }
};

const fetchAssignments = async () => {
  if (!selectedProject.value) return;
  loading.value = true;
  try {
    const res = await api.get(`/projects/${selectedProject.value}/employees`);
    assignments.value = res.data.content || res.data;
  } catch (e) {
    toast.error("Error al sincronizar estado de asignaciones");
  } finally {
    loading.value = false;
  }
};

const toggleAssignment = async (employee, shouldAssign) => {
  processingId.value = employee.idEmployee;
  try {
    if (shouldAssign) {
      await api.put(`/projects/${selectedProject.value}/employees/${employee.idEmployee}`);
      toast.success("Asignación confirmada");
    } else {
      await api.delete(`/projects/${selectedProject.value}/employees/${employee.idEmployee}`);
      toast.success("Asignación revocada");
    }
    await fetchAssignments();
  } catch (e) {
    toast.error("Error al procesar la vinculación");
  } finally {
    processingId.value = null;
  }
};

const formatDate = (date) => {
  if (!date) return '—'
  return new Date(date).toLocaleDateString('es-ES')
}

onMounted(init);
</script>

<style scoped>
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

.control-area-elite {
  padding: 0 32px;
  margin-bottom: 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.project-selector-wrapper {
  background: rgba(255, 255, 255, 0.4);
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
  padding: 4px 16px;
  border-radius: 12px;
}

.f-tabular { font-variant-numeric: tabular-nums; }
.f-center { display: flex; justify-content: center; }

/* GRID SISTÉMICO PARA ASIGNACIONES */
.assignment-grid {
  display: grid;
  grid-template-columns: 1fr 150px 80px;
  gap: 16px;
  align-items: center;
}

/* EMPTY STATE ELITE */
.empty-state-elite {
  padding: 80px 0;
  text-align: center;
  color: rgb(var(--v-theme-on-surface));
  opacity: 0.5;
}
.empty-icon-wrapper {
  width: 64px;
  height: 64px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}
.empty-icon { width: 32px; height: 32px; color: rgb(var(--v-theme-on-surface)); opacity: 0.3; }
</style>
