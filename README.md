# MakeUrImages (nombre de trabajo)

> Nombre provisional tomado de la carpeta del repositorio. El nombre definitivo del producto está pendiente de decisión.

Plataforma SaaS para crear imágenes y textos promocionales con inteligencia artificial y publicarlos en redes sociales. Primera versión para Android e iOS, con mercado inicial en Argentina.

## Estado actual

Fase 1: primera especificación funcional (SPEC-001 Flujo de creación de publicación), aprobada con plan técnico y 52 tareas. Implementación en curso: estructura base del backend (FastAPI) y de la app móvil (Expo) completadas y verificadas. Stack tecnológico aprobado (D-021 a D-026).

- Backend: ackend/ (FastAPI, Python). Arranca con uvicorn; endpoint /health responde 200.
- Móvil: mobile/ (React Native + Expo). Typecheck y bundle Android pasan.
- Ver comandos de instalación y ejecución en ackend/pyproject.toml y mobile/package.json.
- Decisiones pendientes: P-001, P-002, P-004, P-005, P-006, P-007, P-008, P-009, P-010, P-012 (ver docs/decisions/README.md).

## Alcance del MVP (aprobado en la etapa de definición)

Recorrido principal: configurar cuenta → configurar identidad de marca → cargar contenido → seleccionar estilo y formato → generar imagen y texto → revisar y editar de forma limitada → guardar → publicar (Instagram) o compartir manualmente (WhatsApp).

Detalle en `docs/product/product-definition.md`.

## Documentación

- `AGENTS.md`: reglas operativas para agentes de IA.
- `MEMORY.md`: memoria persistente del proyecto (decisiones y estado vigente).
- `tasks.md`: seguimiento macro de la planificación y el desarrollo.
- `docs/constitution.md`: principios no negociables del proyecto.
- `docs/workflow.md`: proceso SDD, estados y aprobaciones.
- `docs/product/product-definition.md`: definición funcional del producto.
- `docs/architecture.md`: arquitectura de alto nivel (pendiente de la etapa técnica).
- `docs/roadmap.md`: fases del producto.
- `docs/decisions/`: decisiones registradas (confirmadas, propuestas y pendientes).
- `docs/specs/`: especificaciones funcionales y sus planes técnicos.
- `docs/agent-context/`: contexto modular para agentes y referencias de investigación.
- `skills/spec-generator/`: procedimiento y plantillas para especificaciones, planes y tareas.

## Metodología

Desarrollo guiado por especificaciones (SDD). Ninguna funcionalidad se implementa sin una especificación aprobada y un plan técnico aprobado. Ver `docs/workflow.md`.

## Licencia

Pendiente de decidir.
