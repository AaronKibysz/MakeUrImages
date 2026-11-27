---
name: spec-generator
description: Crea y revisa especificaciones SDD, planes técnicos y listas de tareas del proyecto siguiendo el flujo aprobado y las plantillas de este directorio. Usar cuando se pida una nueva funcionalidad, un plan o tareas.
---

# Skill: spec-generator

Procedimiento para crear especificaciones, planes técnicos y tareas en este proyecto.

> Esta skill es documentación del proceso. No se instala ni se activa en OpenCode hasta que el usuario lo apruebe.

## Cuándo usarla

- El usuario pide una nueva funcionalidad o un cambio de comportamiento.
- Hay que transformar una spec aprobada en plan técnico.
- Hay que dividir un plan aprobado en tareas.

## Procedimiento

### Paso 1: Discovery

1. Leer `MEMORY.md`, `docs/product/product-definition.md` y `docs/decisions/README.md`.
2. Identificar si la funcionalidad está en el MVP (`docs/roadmap.md`).
3. Listar preguntas abiertas. Si una pregunta es bloqueante, detenerse y consultar al usuario con una única pregunta concreta.

### Paso 2: Spec

1. Crear `docs/specs/NNN-slug/spec.md` con `spec-template.md`.
2. Usar el siguiente número libre en `docs/specs/README.md`.
3. Estado inicial: `Borrador`.
4. Describir comportamiento, requisitos EARS, criterios de aceptación y casos límite.
5. No incluir implementación, endpoints, tablas ni librerías.
6. Cambiar a `En revisión` y pedir aprobación.

### Paso 3: Plan técnico

Solo después de `Aprobada`.

1. Crear `plan.md` con `technical-plan-template.md`.
2. Investigar alternativas si son necesarias. Registrar fuentes y fecha de consulta.
3. Si la decisión cambia arquitectura, stack o proveedores, proponer un ADR.
4. Cambiar a `Plan en revisión` y pedir aprobación.

### Paso 4: Tareas

Solo después de `Plan aprobado`.

1. Crear `tasks.md` con `tasks-template.md`.
2. Cada tarea debe ser pequeña, verificable y tener criterio de finalización.
3. Indicar dependencias entre tareas.
4. Marcar qué tareas pueden delegarse a subagentes y con qué alcance de archivos.

### Paso 5: Cierre

1. Verificar que todos los criterios de aceptación de la spec tienen prueba o evidencia.
2. Actualizar el estado de la spec, `docs/specs/README.md`, `tasks.md` y `MEMORY.md`.

## Checklist de calidad de una spec

- [ ] Describe qué hace el sistema, no cómo.
- [ ] Cada requisito tiene ID y criterio verificable.
- [ ] Incluye casos de error y casos límite.
- [ ] Respeta la constitución (seguridad, aislamiento, información factual, aprobaciones).
- [ ] No contradice decisiones confirmadas en `docs/decisions/README.md`.
- [ ] Las decisiones pendientes que la afectan están marcadas como `Pendiente`.
- [ ] Está en español.

## Prohibiciones

- No marcar una spec como `Aprobada`. Solo lo hace el usuario.
- No crear tareas de una spec que no tenga plan aprobado.
- No inventar precios, límites ni capacidades de APIs.
