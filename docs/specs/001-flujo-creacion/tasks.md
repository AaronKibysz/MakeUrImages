# Tareas: SPEC-001 Flujo de creación de publicación

- **Estado:** Plan aprobado
- **Plan:** `docs/specs/001-flujo-creacion/plan.md`
- **Aprobación de tareas:** aprobada por el usuario (2026-11-27)

## Reglas

- Cada tarea es pequeña y verificable.
- Cada tarea referencia los requisitos o criterios que cubre.
- Las dependencias se declaran explícitamente.
- Una tarea se marca como completada solo con evidencia (prueba, revisión o verificación).
- Una tarea que requiere cambiar la spec o el plan se detiene y se consulta al usuario.

## Tareas

| ID | Tarea | Cubre | Depende de | Delegable | Alcance de archivos | Finalización | Estado |
|---|---|---|---|---|---|---|---|
| T-001 | Crear estructura de proyecto backend FastAPI (carpetas, pyproject.toml, settings, .env.example) | Infra | — | Sí (implementer) | backend/** | Proyecto arranca con uvicorn y `/health` responde 200 | Completada |
| T-002 | Crear estructura de proyecto móvil Expo (app, screens, api client) | Infra | — | Sí (implementer) | mobile/** | App compila y ejecuta en emulador | Completada |
| T-003 | Configurar conexión async a PostgreSQL/Supabase (engine, session, settings) | REQ-001 | T-001 | Sí (implementer) | backend/app/db/** | Conexión exitosa a BD de prueba | Pendiente |
| T-004 | Migración: tablas `workspaces`, `users`, `workspace_members` | Multi-tenancy | T-003 | Sí (implementer) | backend/migrations/** | Migración aplica sin error | Pendiente |
| T-005 | Migración: tablas `creation_sessions`, `session_temp_files`, `creation_inputs`, `styles` | REQ-001..REQ-010 | T-004 | Sí (implementer) | backend/migrations/** | Migración aplica sin error | Pendiente |
| T-006 | Migración: tablas `generation_jobs`, `generation_results`, `saved_results`, `editable_projects`, `publication_intents`, `library_assets` | REQ-014..REQ-022 | T-005 | Sí (implementer) | backend/migrations/** | Migración aplica sin error | Pendiente |
| T-007 | Implementar RLS policies en todas las tablas tenant-scoped + `FORCE RLS` | Aislamiento | T-004, T-005, T-006 | Sí (implementer) con revisión code-reviewer | backend/migrations/** | Policies aplicadas; test de aislamiento pasa | Pendiente |
| T-008 | Middleware FastAPI: establecer `app.current_workspace_id` por request tras validar membresía | Multi-tenancy | T-003, T-004 | Sí (implementer) | backend/app/middleware/** | Workspace context disponible en handlers | Pendiente |
| T-009 | Autenticación JWT (integración con Supabase Auth o propio) | Seguridad | T-001 | Sí (implementer) | backend/app/auth/** | Endpoints protegidos rechazan sin token | Pendiente |
| T-010 | Autorización: permisos por rol (generate, approve, history) en workspace | REQ-001, §7 | T-004, T-009 | Sí (implementer) | backend/app/auth/** | Tests de permisos pasan | Pendiente |
| T-011 | `StorageService` para R2 (presign upload/download, delete, public url) | REQ-002, REQ-003 | T-001 | Sí (implementer) | backend/app/services/storage.py | Operaciones contra R2 de prueba exitosas | Pendiente |
| T-012 | Lifecycle policy en bucket R2 para temporales (7 días) | REQ-024, CA-009 | T-011 | No (configuración de infra, requiere credenciales) | Cloudflare R2 (config) | Policy visible en consola; CA-009 verificable parcialmente con tests unitarios del policy (mock) | Pendiente (bloqueada por credenciales) |
| T-013 | Endpoints de sesión de creación (POST/GET/close) | REQ-001, REQ-003 | T-005, T-008, T-010 | Sí (implementer) | backend/app/api/sessions.py | Tests API pasan | Pendiente |
| T-014 | Endpoints de archivos temporales (presign, confirm, list, delete) | REQ-002, REQ-003 | T-011, T-013 | Sí (implementer) | backend/app/api/temp_files.py | Tests API pasan | Pendiente |
| T-015 | Cierre de sesión con borrado explícito de temporales en R2 | REQ-003, REQ-024 | T-014 | Sí (implementer) | backend/app/api/sessions.py, services/ | CA-003 pasa | Pendiente |
| T-016 | Endpoint guardar inputs (factual, instrucciones, estilo, formato, redes, variantes) | REQ-004, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011 | T-005, T-013 | Sí (implementer) | backend/app/api/inputs.py | Tests API pasan | Pendiente |
| T-017 | Validación de formato personalizado (rango) | REQ-009 | T-016 + P-004 | Sí (implementer) | backend/app/api/inputs.py | Rechaza dimensiones inválidas | Pendiente (bloqueada por P-004) |
| T-018 | Endpoint listar estilos | REQ-007 | T-005 | Sí (implementer) | backend/app/api/styles.py | Tests API pasan | Pendiente |
| T-019 | Seed de los 8 estilos (D-026) en BD | REQ-007 | T-005, T-018 | Sí (implementer/documenter) | backend/seeds/** | Estilos disponibles vía API | Pendiente |
| T-020 | `CreditService` interfaz + stub (get_balance, estimate, reserve, commit, release) | REQ-012, REQ-013, REQ-016, REQ-023 | T-001 | Sí (implementer) | backend/app/services/credit.py | Interfaz definida; stub respeta saldo (0 créditos → bloqueo) para que CA-002 sea verificable | Pendiente (implementación real bloqueada por P-001/P-002) |
| T-021 | Endpoint estimar créditos | REQ-012 | T-020, T-016 | Sí (implementer) | backend/app/api/credits.py | Tests API pasan | Pendiente |
| T-022 | `AIProvider` interfaz (generate_image, generate_text) + adapter base + mock | REQ-014, REQ-015 | T-001 | Sí (implementer) | backend/app/services/ai_provider.py | Mock provider pasa tests | Pendiente (implementación concreta bloqueada por P-012) |
| T-023 | Job queue + worker base (enqueue, get_status, cancel) | Procesamiento async | T-001 + decisión de cola | Sí (implementer) | backend/app/queue/**, workers/ | Job encolado y consumido por worker de prueba | Pendiente (bloqueada parcialmente por decisión de cola/cache) |
| T-024 | Worker de generación: llama AIProvider, almacena en R2, crea results, actualiza job, consume créditos | REQ-014, REQ-015, REQ-016, REQ-022 | T-022, T-023, T-011, T-020 | Sí (implementer) | backend/app/workers/generation.py | CA-001, CA-011 pasan | Pendiente |
| T-025 | Conservación de info factual: inyección en prompt + validación post-generación (substring exacto) | REQ-005, REQ-015 | T-024 + P-007 | Sí (implementer) | backend/app/services/factual.py | CA-008 pasa | Pendiente (bloqueada parcialmente por P-007) |
| T-026 | Endpoint iniciar generación (valida créditos, inputs, encola job) | REQ-013, REQ-014 | T-016, T-020, T-023 | Sí (implementer) | backend/app/api/generation.py | CA-002 pasa | Pendiente |
| T-027 | Endpoint estado de job (polling) | CA-011 | T-024 | Sí (implementer) | backend/app/api/generation.py | Tests API pasan | Pendiente |
| T-028 | Endpoint cancelar job | Procesamiento async | T-023, T-024 | Sí (implementer) | backend/app/api/generation.py | Tests API pasan | Pendiente |
| T-029 | Reintentos con backoff en worker (max 3) | REQ-023 | T-024 | Sí (implementer) | backend/app/workers/generation.py | CA-007 pasa | Pendiente |
| T-030 | Edición limitada: endpoint aplicar edición (crop/resize/position/scale) sobre imagen | REQ-017, CA-004 | T-011, T-024 | Sí (implementer) | backend/app/api/edits.py, services/image_edit.py | CA-004 pasa | Pendiente (hipótesis: server-side Pillow; alcance puede cambiar si se elige client-side) |
| T-031 | Reemplazo de logotipo (temp file o asset de biblioteca) | REQ-017 | T-030, T-014 | Sí (implementer) | backend/app/api/edits.py | Tests API pasan | Pendiente |
| T-032 | Cambio de formato con ajuste técnico + advertencia de incompatibilidades | REQ-026 | T-030 | Sí (implementer) | backend/app/api/edits.py | Tests API pasan | Pendiente |
| T-033 | Guardado en historial/biblioteca | REQ-019, REQ-022, CA-006 | T-024, T-006 | Sí (implementer) | backend/app/api/results.py | CA-006 pasa | Pendiente |
| T-034 | Guardar como proyecto editable (resultado final + reusable elements, sin originales) | REQ-020, CA-012 | T-033 | Sí (implementer) | backend/app/api/results.py | CA-012 pasa | Pendiente |
| T-035 | Endpoint listar historial | CA-006 | T-033 | Sí (implementer) | backend/app/api/results.py | Tests API pasan | Pendiente |
| T-036 | Intención de publicar/compartir + preview de contenido final | REQ-021, REQ-025, CA-013 | T-024, T-033 | Sí (implementer) | backend/app/api/publication_intents.py | CA-013 pasa | Pendiente |
| T-037 | Tests unitarios de servicios (session, storage, credit interface, provider adapter) | Calidad | T-013..T-022 | Sí (tester) | backend/tests/unit/** | Suite verde | Pendiente |
| T-038 | Tests de integración end-to-end (sesión → generación → guardado) | CA-001, CA-006, CA-007, CA-011 | T-024, T-033 | Sí (tester) | backend/tests/integration/** | Suite verde | Pendiente |
| T-039 | Tests de aislamiento RLS (tenant no lee datos de otro) | Constitución §2.5 | T-007, T-008 | Sí (tester) | backend/tests/isolation/** | Suite verde | Pendiente |
| T-040 | Tests de permisos (sin permiso → 403) | CA-010 | T-010, T-013 | Sí (tester) | backend/tests/api/** | Suite verde | Pendiente |
| T-041 | Tests de archivos temporales (cierre elimina; abandono lifecycle) | CA-003, CA-009 | T-015, T-012 | Sí (tester) | backend/tests/integration/** | Suite verde | Pendiente |
| T-042 | Tests de info factual (substring exacto) | CA-008 | T-025 | Sí (tester) | backend/tests/unit/** | Suite verde | Pendiente |
| T-043 | Tests de edición (CA-004, CA-005) | CA-004, CA-005 | T-030, T-031 | Sí (tester) | backend/tests/api/** | Suite verde | Pendiente |
| T-044 | Tests de guardado (CA-012, CA-013) | CA-012, CA-013 | T-034, T-036 | Sí (tester) | backend/tests/api/** | Suite verde | Pendiente |
| T-045 | Móvil: pantallas de creación (inputs, estilo, formato, redes, variantes) | REQ-004..REQ-011 | T-002, T-016, T-018, T-021 | Sí (implementer) | mobile/src/screens/create/** | Flujo navegable en emulador | Pendiente |
| T-046 | Móvil: adjuntar archivos temporales (upload presignado) | REQ-002 | T-014, T-045 | Sí (implementer) | mobile/src/screens/create/** | Upload exitoso a R2 | Pendiente |
| T-047 | Móvil: generar y mostrar progreso (polling) | REQ-014 | T-026, T-027, T-045 | Sí (implementer) | mobile/src/screens/create/** | Generación visible en app | Pendiente |
| T-048 | Móvil: editor limitado (crop/resize/position/scale/logo replace) | REQ-017 | T-030, T-031, T-047 | Sí (implementer) | mobile/src/screens/editor/** | Edición funcional | Pendiente |
| T-049 | Móvil: guardar y publicar intent | REQ-019, REQ-020, REQ-021 | T-033, T-034, T-036, T-047 | Sí (implementer) | mobile/src/screens/** | Guardado e intención visibles | Pendiente |
| T-050 | Documentación: actualizar spec/plan si cambia comportamiento; README de módulos | Constitución §5.18 | Implementación | Sí (documenter) | docs/**, READMEs | Docs sincronizadas | Pendiente |
| T-051 | Revisión de código de módulos backend y móvil | Calidad | Implementación | Sí (code-reviewer) | backend/**, mobile/** | Revisión aprobada | Pendiente |
| T-052 | Endpoint listar y registrar activos de biblioteca (logotipos, imágenes, recursos) | REQ-017 (reemplazo de logotipo) | T-005, T-011 | Sí (implementer) | backend/app/api/library_assets.py | Tests API pasan | Pendiente |

## Notas para subagentes

Para cada tarea delegable, usar la plantilla de `docs/agent-context/subagent-brief.md`. Indicar en el encargo: objetivo, archivos permitidos, contexto necesario, formato de entrega y condición de finalización. Un subagente no modifica archivos que pertenezcan a otra tarea en curso. El agente principal sintetiza y verifica los informes antes de escribir en `docs/`.

### Tareas bloqueadas por decisiones pendientes

- **T-017:** bloqueada por P-004 (rango de formato personalizado).
- **T-020 (implementación real):** bloqueada por P-001/P-002 (créditos).
- **T-022 (implementación concreta):** bloqueada por P-012 (proveedor de IA).
- **T-023:** bloqueada parcialmente por la decisión de cola/cache.
- **T-025:** bloqueada parcialmente por P-007 (validación de info factual).
- **T-012:** bloqueada por credenciales de Cloudflare (configuración de infra).

### Orden sugerido de ejecución

1. Fundación: T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008.
2. Auth y storage: T-009 → T-010 → T-011 → T-012.
3. Sesión e inputs: T-013 → T-014 → T-015 → T-016 → T-017 → T-018 → T-019.
4. Créditos e IA (interfaces): T-020 → T-021 → T-022.
5. Generación async: T-023 → T-024 → T-025 → T-026 → T-027 → T-028 → T-029.
6. Edición y guardado: T-030 → T-031 → T-032 → T-033 → T-034 → T-035 → T-036 → T-052.
7. Pruebas: T-037 → T-038 → T-039 → T-040 → T-041 → T-042 → T-043 → T-044.
8. Móvil: T-045 → T-046 → T-047 → T-048 → T-049.
9. Cierre: T-050 → T-051.
