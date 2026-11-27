# tasks.md

Seguimiento macro del proyecto. Las tareas de desarrollo de cada funcionalidad viven en `docs/specs/<spec>/tasks.md`.

## Fase 0: definición y metodología

- [x] Definición funcional del producto (etapa 1, aprobada).
- [x] Estructura base de documentación SDD.
- [ ] Revisión de la estructura por el usuario.
- [x] Propuesta de configuración de OpenCode (agentes, subagentes, permisos, skills). **Solo propuesta, sin aplicar.** Ver `docs/agent-context/opencode-proposal.md`.
- [ ] Aprobación de la propuesta de configuración por el usuario.
- [x] Revisión de los prompts de Claude Code en `system_prompts_leaks` (prerrequisito de `agent-research`). **Solo lectura.** Ver `docs/agent-context/research/2026-11-27-claude-code-prompts.md`.
- [x] Revisión de `consolidate-memory`, `steward` y `auto-mode-classifier`. Ver `docs/agent-context/research/2026-11-27-claude-code-pending-review.md`.
- [x] Ajustes aprobados incorporados a la propuesta de configuración (`opencode-proposal.md` §12). Pendiente aplicar a `AGENTS.md` y configuración.
- [ ] Aprobación de los hallazgos de §13 de la propuesta (archivos protegidos, prohibiciones duras, consentimiento específico, límite de reintentos, memoria, revisión de delegación).
- [ ] Propuesta de integración de `agent-research` y skills de interfaz (`ui-exploration`, `ui-build`, `ui-review`). **Solo propuesta.**
- [ ] Investigación de servicios de IA, costes y márgenes. **Requiere autorización.**
- [ ] Investigación de APIs de Instagram y WhatsApp. **Requiere autorización.**
- [ ] Investigación de políticas de Apple, Google y pagos para Argentina. **Requiere autorización.**
- [ ] Investigación de stack y arquitectura. **Requiere autorización.**
- [ ] Análisis de referencias en TDL, AAProject, HERRAMIENTA-DTF y DEVPulse (solo lectura).
- [ ] Aprobación de precios, planes y límites comerciales. **Requiere decisión del usuario.**

## Fase 1: primera especificación

- [ ] Redactar primera especificación funcional a partir de la definición aprobada.
- [ ] Revisión y aprobación por el usuario.

Las especificaciones de desarrollo se crean una por una, con aprobación previa. Ver `docs/specs/README.md`.
