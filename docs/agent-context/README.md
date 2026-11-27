# Contexto para agentes

Módulos de contexto que los agentes cargan según la tarea. Mantener cada módulo corto. No cargar todo el contexto en cada sesión.

## Mapa de contexto

| Tarea | Cargar |
|---|---|
| Cualquier tarea | `AGENTS.md`, `MEMORY.md`, `docs/constitution.md` |
| Definir o revisar una especificación | `docs/product/product-definition.md`, `docs/specs/README.md`, `skills/spec-generator/` |
| Planificar una funcionalidad | Spec aprobada, `docs/architecture.md`, `docs/decisions/README.md` |
| Crear tareas | Plan aprobado y `skills/spec-generator/tasks-template.md` |
| Investigar proveedores o APIs | `docs/decisions/README.md` (pendientes P-008 a P-012) y `docs/agent-context/research/` |
| Revisar estilos o interfaz | Spec de interfaz y `docs/agent-context/design-system.md` (cuando exista) |
| Revisar seguridad | `docs/constitution.md` (secciones 1 y 2) y el plan de la spec |

## Archivos de este directorio

- `subagent-brief.md`: plantilla para encargar trabajo a subagentes.
- `references.md`: referencias externas y patrones que se están evaluando.
- `research/`: informes de investigación con fuentes y fecha de consulta. Se crea cuando se autorice una investigación.

## Principios de contexto

1. **Modular:** cada módulo responde a una pregunta.
2. **Verificable:** cada afirmación importante tiene fuente o se marca como hipótesis.
3. **Vigente:** si un módulo se contradice con `MEMORY.md` o con una spec aprobada, prevalece la spec aprobada y el módulo se corrige.
4. **Mínimo:** cargar solo lo necesario para la tarea actual.
