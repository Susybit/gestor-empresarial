# 📘 Decisiones Técnicas y Arquitectura — Future Space | Manager

Este documento detalla el ecosistema técnico del proyecto **Future Space | Manager**. Mi objetivo ha sido construir una herramienta de gestión empresarial que no solo cumpla los requisitos funcionales exigidos en el plan del curso de la beca, sino que siga los estándares de la industria SaaS en 2026: seguridad robusta, UX fluida y código limpio y mantenible.

---

# PARTE I: BACKEND (Java 17 & Spring Boot 3.2)

## 1. Filosofía de Arquitectura
He implementado una **Arquitectura en Capas** con separación estricta de responsabilidades. Esto permite que el sistema sea fácil de testear y escalar:

- **Controller:** La puerta de entrada. Solo gestiona peticiones HTTP y delega la lógica.
- **Service:** El "cerebro". Aquí vive la lógica de negocio y las reglas de validación complejas.
- **Repository:** La conexión con MySQL mediante Spring Data JPA.
- **DTO (Data Transfer Objects):** Vital para la seguridad. Nunca expongo las entidades de la base de datos directamente al exterior; solo envío y recibo contratos de datos controlados.

## 2. Modelo de Datos Avanzado
He aplicado técnicas de mapeo objeto-relacional (ORM) avanzadas:
- **Dualidad de Idioma:** Los campos en Java están en inglés (`firstName`, `hireDate`) para seguir las convenciones de Clean Code internacional, pero mapeados mediante `@Column` a la base de datos en español (`NB_NOMBRE`, `F_ALTA`).
- **Claves Compuestas (@EmbeddedId):** Para la tabla de asignaciones (`PR_EMPLEADOS_PROYECTO`), he gestionado la relación mediante una clase `EmployeeProjectId`. Esto garantiza que la integridad referencial sea perfecta a nivel de código.

## 3. Lógica de Negocio Blindada
No me he limitado a un CRUD básico. El sistema incluye reglas de protección de datos:
- **Inmutabilidad de Campos Críticos:** Una vez creado un empleado, el NIF y la Fecha de Alta quedan bloqueados. El sistema rechaza cualquier intento de modificarlos para evitar corrupciones de histórico.
- **Borrado Lógico (Soft Delete):** No eliminamos registros físicamente. El sistema gestiona el campo `F_BAJA`. Un empleado "borrado" simplemente deja de estar activo, permitiendo mantener la trazabilidad histórica.
- **Idempotencia en Asignaciones:** He diseñado el servicio de asignación para que sea "seguro". Si un usuario intenta asignar un empleado a un proyecto donde ya está, el sistema lo detecta y lo gestiona sin lanzar errores técnicos.

## 4. Seguridad, Cifrado y Errores
- **Hashes BCrypt:** Las contraseñas se almacenan siempre como hashes irreversibles.
- **Global Exception Handler:** Centralizo todos los errores. Si algo falla, el cliente recibe un JSON estandarizado con un mensaje legible, ocultando detalles técnicos internos por seguridad.
- **Endpoints Extra Pro:** He añadido `/auth/register` y `/auth/reset-password` con validaciones de complejidad (mayúsculas, símbolos) para que la gestión de administradores sea 100% autónoma.

---

# PARTE II: FRONTEND (Vue 3, Pinia & Vuetify)

## 5. Diseño Visual de Alto Rendimiento
La interfaz busca transmitir el estándar de una herramienta SaaS moderna:

- **Layout "Seamless Split":** Un login dividido que combina profundidad técnica (panel oscuro con auras de luz y Dot Grid) con claridad operativa (panel de formulario limpio).
- **Tipografía "Inter" & Clamp:** Uso de fuentes modernas con espaciado compacto (`-0.03em`) y tamaños fluidos mediante la función CSS `clamp()`. El diseño "respira" igual de bien en un portátil de 13" que en un monitor 4K de 32".
- **Fondo Anti-Fatiga:** El área de trabajo usa `#F8FAFC` (gris perla neutro), un tono que reduce el cansancio visual en jornadas largas de uso.

## 6. UX de Próxima Generación
- **Smart CTA:** Botones que reaccionan al estado de validación del formulario en tiempo real.
- **Validation @blur:** Los errores no interrumpen al usuario mientras escribe; solo aparecen cuando el usuario termina de interactuar con el campo, siguiendo las guías de Nielsen Norman Group.
- **Anulación de Autofill:** He inyectado sombras internas para "limpiar" el estilo intrusivo de autocompletado de Chrome, manteniendo la integridad visual de la marca.
- **Avatar Dinámico:** El sistema calcula las iniciales del administrador logueado en tiempo real para personalizar el dashboard.

## 7. Gestión de Estado y Navegación
- **Pinia & Persistencia:** El estado de autenticación sobrevive a la recarga de página (F5) mediante una sincronización inteligente con `localStorage`.
- **Navigation Guards:** El router está blindado. Nadie puede saltarse el login introduciendo la URL manualmente; el sistema los intercepta y redirige automáticamente.

---

# PARTE III: ANALÍTICA DE DATOS (Python & Pandas)

## 8. Procesamiento de Inteligencia de Negocio
*(En desarrollo)*
Uso de **Pandas** para conectar con la base de datos MySQL y transformar datos crudos en KPIs estratégicos:
- Distribución demográfica de la plantilla.
- Ratio de rotación (Altas vs Bajas).
- Saturación de carga por proyectos.

---

# Conclusión
Future Space | Manager es el resultado de aplicar ingeniería de software rigurosa sobre un enunciado académico. Desde el uso de `@EmbeddedId` en el backend hasta los gradientes dinámicos en el frontend, cada decisión ha sido tomada para demostrar que una aplicación corporativa puede ser, al mismo tiempo, **segura, potente y estéticamente impecable.**
