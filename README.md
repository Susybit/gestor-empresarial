# Future Space Manager: Fullstack Enterprise Ecosystem

Este repositorio centraliza el ecosistema **Future Space Manager**, una solución integral para la gestión estratégica de capital humano y proyectos empresariales. El proyecto combina una interfaz de usuario minimalista, una API REST robusta y un motor de analítica avanzada, formando un ciclo completo de **gestión → persistencia → análisis**.

---

## Módulos del Repositorio

### [Enterprise UI: Frontend Engine](frontend/)
Interfaz SPA desarrollada con **Vue 3** y **Vite**, bajo un estándar de diseño **Fine-Line Minimalist**. 
* **Arquitectura Reactiva:** Uso de Composition API y Pinia para una gestión de estado predecible.
* **UX/UI:** Estética premium con Vuetify, micro-animaciones dinámicas y diseño totalmente responsive.

### [Business Core: Backend API](backend/)
Núcleo de servicios construido con **Java 17** y **Spring Boot**, encargado de la lógica de negocio y la integridad referencial.
* **Arquitectura de 3 Capas:** Flujo desacoplado (Controller -> Service -> Repository) que garantiza la mantenibilidad.
* **Persistencia Avanzada:** Uso de Spring Data JPA con validaciones Jakarta y manejo global de excepciones.

### [Business Intelligence: Analytics Module](analytics/)
Motor de procesamiento de datos en **Python** para la generación de informes estratégicos y detección de anomalías.
* **Data Engine:** Sistema híbrido capaz de consumir datos reales de MySQL o activar un modo demo con datos sintéticos.
* **Insights Visuales:** Generación automática de reportes en PNG/PDF mediante Pandas y Seaborn.

---

## Stack Tecnológico

* **Frontend:** Vue 3, Vite, Pinia, Vuetify, Axios, Lucide Icons.
* **Backend:** Java 17, Spring Boot, Spring Data JPA, MySQL, Spring Security.
* **Analítica:** Python 3.11, Pandas, Seaborn, Matplotlib, Jupyter.
* **Metodologías:** Clean Code, SOLID, OOP avanzada, Documentación JSDoc/JavaDoc.

---

## Arquitectura Global

```
gestor-empresarial/
├── frontend/        # Cliente SPA (Vue 3)
├── backend/         # API REST (Spring Boot)
├── analytics/       # Motor de inteligencia (Python)
├── docs/            # Documentación técnica adicional
└── README.md        # Orquestador de documentación
```

---

## Puesta en Marcha

El sistema requiere **Node.js 18+**, **Java 17** y **Python 3.11+**.

1. **Backend:** Configurar `application.properties` y ejecutar con `./mvnw spring-boot:run`.
2. **Frontend:** Ejecutar `npm install` y `npm run dev`.
3. **Analytics:** Instalar `requirements.txt` y ejecutar `python generate_report.py`.

---
**Desarrollado por:** Susana Bitar
