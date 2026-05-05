import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import { useAuthStore } from '@/stores/auth'

/**
 * DEFINICIÓN DE RUTAS
 * Se definen de forma estática para mantener la claridad.
 */
const routes = [
  {
    // Ruta de acceso pública
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { title: 'Acceso', requiresAuth: false }
  },
  {
    // Rutas protegidas bajo el Layout Principal
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('@/views/dashboard/DashboardView.vue'),
        meta: { title: 'Panel de Control' }
      },
      {
        path: 'employees',
        name: 'employees',
        component: () => import('@/views/employees/EmployeesView.vue'),
        meta: { title: 'Gestión de Empleados' }
      },
      {
        path: 'employees/new',
        name: 'employee-new',
        component: () => import('@/views/employees/EmployeeFormView.vue'),
        meta: { title: 'Nuevo Empleado' }
      },
      {
        path: 'employees/edit/:id',
        name: 'employee-edit',
        component: () => import('@/views/employees/EmployeeFormView.vue'),
        meta: { title: 'Editar Empleado' }
      },
      {
        path: 'projects',
        name: 'projects',
        component: () => import('@/views/projects/ProjectsView.vue'),
        meta: { title: 'Gestión de Proyectos' }
      },
      {
        path: 'projects/new',
        name: 'project-new',
        component: () => import('@/views/projects/ProjectFormView.vue'),
        meta: { title: 'Nuevo Proyecto' }
      },
      {
        path: 'projects/edit/:id',
        name: 'project-edit',
        component: () => import('@/views/projects/ProjectFormView.vue'),
        meta: { title: 'Editar Proyecto' }
      },
      {
        path: 'assignments',
        name: 'assignments',
        component: () => import('@/views/assignments/AssignmentsView.vue'),
        meta: { title: 'Asignación de Recursos' }
      },
      {
        path: 'profile',
        name: 'profile',
        component: () => import('@/views/profile/ProfileView.vue'),
        meta: { title: 'Mi Perfil' }
      }
    ]
  },
  {
    // Redirección de seguridad para rutas inexistentes
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard'
  }
]

/**
 * INSTANCIACIÓN DEL ROUTER
 */
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

/**
 * NAVIGATION GUARD (GUARDIA DE NAVEGACIÓN)
 * Protegemos las rutas verificando el estado de autenticación en Pinia.
 */
router.beforeEach((to, from, next) => {
  // Instanciamos el store DENTRO del guard para asegurarnos de que Pinia ya está inicializado
  const authStore = useAuthStore()
  
  // Caso A: La ruta requiere autenticación y el usuario NO está logueado
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } 
  // Caso B: El usuario intenta ir al Login teniendo ya una sesión activa
  else if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
  } 
  // Caso C: Navegación permitida
  else {
    next()
  }
})

// Sincronización del título de la pestaña del navegador con identidad consistente
router.afterEach((to) => {
  document.title = to.meta.title
    ? `${to.meta.title} | Manager`
    : 'Manager | Future Space';
})

export default router