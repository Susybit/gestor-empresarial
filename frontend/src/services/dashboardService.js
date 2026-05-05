import api from '@/plugins/axios'

/**
 * Cliente del cuadro de mando.
 *
 * Resuelve las tres lecturas que necesita el dashboard contra el
 * backend real: empleados activos, proyectos activos y el grafo
 * plano de asignaciones. Se encarga de:
 *
 *   - desempaquetar las respuestas paginadas de Spring Data,
 *   - pedir un tamaño suficiente para no fragmentar la consulta,
 *   - lanzar las tres lecturas en paralelo.
 *
 * Devuelve datos crudos. Toda la lógica de derivación de
 * indicadores vive en la vista, lo que mantiene este módulo
 * trivialmente testeable y reusable desde otros sitios.
 */

const PAGE_SIZE = 2000

const unwrapPage = (res) => {
  const body = res?.data
  if (Array.isArray(body)) return body
  if (Array.isArray(body?.content)) return body.content
  return []
}

export async function fetchDashboardData() {
  const [employeesRes, projectsRes, assignmentsRes] = await Promise.all([
    api.get('/employees', { params: { size: PAGE_SIZE, includeInactive: true } }),
    api.get('/projects', { params: { size: PAGE_SIZE } }),
    api.get('/assignments')
  ])

  return {
    employees: unwrapPage(employeesRes),
    projects: unwrapPage(projectsRes),
    assignments: unwrapPage(assignmentsRes)
  }
}
