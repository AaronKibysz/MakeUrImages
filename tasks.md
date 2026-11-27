# tasks.md

Seguimiento macro del proyecto. Las tareas de desarrollo de cada funcionalidad viven en `docs/specs/<spec>/tasks.md`.

## Fase 0: definición y metodología

- [x] Definición funcional del producto (etapa 1, aprobada).
- [x] Estructura base de documentación SDD.
- [x] Revisión de la estructura por el usuario.
- [x] Propuesta de configuración de OpenCode (agentes, subagentes, permisos, skills). Aplicada. Ver `docs/agent-context/opencode-proposal.md`.
- [x] Aprobación de la propuesta de configuración por el usuario.
- [x] Revisión de los prompts de Claude Code en `system_prompts_leaks` (prerrequisito de `agent-research`). **Solo lectura.** Ver `docs/agent-context/research/2026-11-27-claude-code-prompts.md`.
- [x] Revisión de `consolidate-memory`, `steward` y `auto-mode-classifier`. Ver `docs/agent-context/research/2026-11-27-claude-code-pending-review.md`.
- [x] Ajustes aprobados incorporados a la propuesta de configuración (`opencode-proposal.md` §12). Aplicados a `AGENTS.md`, configuración y skills.
- [x] Aprobación de los hallazgos de §13 de la propuesta. Aplicados a `AGENTS.md` y `docs/constitution.md`.
- [x] Configuración de OpenCode aplicada (`opencode.jsonc`, `.opencode/agents/*`, `skills/agent-research`).
- [x] `agent-research` creado.
- [ ] Propuesta de integración de skills de interfaz (`ui-exploration`, `ui-build`, `ui-review`). **Solo propuesta, diferida.**
- [ ] Investigación de servicios de IA, costes y márgenes. **Requiere autorización.**
- [ ] Investigación de APIs de Instagram y WhatsApp. **Requiere autorización.**
- [ ] Investigación de políticas de Apple, Google y pagos para Argentina. **Requiere autorización.**
- [x] Investigación de stack y arquitectura. Informe en `docs/agent-context/research/2026-11-27-stack-arquitectura.md`.
- [x] Decisiones D-021 (FastAPI backend) y D-022 (React Native + Expo móvil) autorizadas por el usuario.
- [x] Investigación de base de datos y storage. Informe en `docs/agent-context/research/2026-11-27-bd-storage.md`.
- [x] Decisión de región de despliegue: São Paulo (sa-east-1). D-023.
- [x] Decisión de proveedor de BD: Supabase. D-024.
- [x] Decisión de proveedor de storage: Cloudflare R2. D-025.
- [ ] Decisión de cache y cola (Upstash vs ElastiCache, RQ/Dramatiq/ARQ vs managed). **Requiere autorización.**
- [ ] Validación de latencia de R2 desde Argentina (edge en Buenos Aires). **Pendiente de prueba.**
- [x] Investigación de proveedores de IA. Informe en `docs/agent-context/research/2026-11-27-proveedores-ia.md`.
- [x] Estilos del catálogo definidos (8 estilos, D-026). P-003 resuelto.
- [ ] Spike de calidad/coste con 2-3 proveedores y 3-5 estilos. **Pospuesto por el usuario (uso de APIs para más adelante).**
- [ ] Validación profesional de pagos in-app en Argentina (P-008). **Requiere autorización.**
- [ ] Validación profesional de Ley 25.326 (P-015). **Requiere autorización.**
- [ ] Análisis de referencias en TDL, AAProject, HERRAMIENTA-DTF y DEVPulse (solo lectura).
- [ ] Aprobación de precios, planes y límites comerciales. **Requiere decisión del usuario.**

## Fase 1: primera especificación

- [x] Redactar primera especificación funcional a partir de la definición aprobada. SPEC-001 Flujo de creación de publicación.
- [x] Revisión y aprobación por el usuario. SPEC-001 Aprobada (2026-11-27).
- [x] Plan técnico de SPEC-001 generado por planner. 52 tareas creadas.
- [x] Aprobación del plan técnico por el usuario (2026-11-27).
- [x] Implementación iniciada. T-001 (estructura backend FastAPI) completada y verificada (code-reviewer + tester).
- [x] T-002 (estructura móvil Expo) completada y verificada (code-reviewer + tester).
- [x] Autorización persistente de permisos actualizada: sk → llow en opencode.jsonc y agentes; prohibiciones duras (deny) se mantienen.

Las especificaciones de desarrollo se crean una por una, con aprobación previa. Ver `docs/specs/README.md`.
