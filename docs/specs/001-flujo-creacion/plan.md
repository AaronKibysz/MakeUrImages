# Plan técnico: SPEC-001 Flujo de creación de publicación

- **Estado:** Plan aprobado
- **Fecha:** 2026-11-27
- **Spec aprobada:** `docs/specs/001-flujo-creacion/spec.md` (2026-11-27)
- **Aprobación del plan:** aprobada por el usuario (2026-11-27)

## 1. Resumen

Se implementará el flujo de creación de publicación (imagen + texto) sobre el stack autorizado: backend FastAPI (Python) en contenedores, app móvil React Native + Expo, base de datos Supabase (PostgreSQL) con multi-tenancy por RLS, archivos en Cloudflare R2 y generación asíncrona mediante cola de trabajos + worker. El proveedor de IA queda detrás de una abstracción (adapter), sin decisión tomada (P-012 pospuesto). La spec cubre REQ-001 a REQ-026 y CA-001 a CA-013. No se implementa publicación real (SPEC-002) ni gestión de créditos (SPEC posterior); se definen interfaces para integrarlas.

## 2. Alcance técnico

- **Requisitos cubiertos:** REQ-001 a REQ-026.
- **Criterios de aceptación cubiertos:** CA-001 a CA-013.
- **Fuera de alcance técnico:**
  - Publicación real en Instagram/WhatsApp (SPEC-002). Solo se registra la intención y se expone preview.
  - Gestión de créditos y planes (SPEC posterior). Se define la interfaz `CreditService`; la implementación real queda bloqueada por P-001/P-002.
  - Editor avanzado, capas, deshacer/rehacer (Fase 2).
  - Refinamiento iterativo con IA (fuera del MVP, D-019).
  - Variantes por red (fuera del MVP, D-020).
  - Edición de textos generados (se regenera, D-006).
  - Gestión de identidad de marca (se asume configurada previamente).
  - Organizaciones y roles completos (solo se respetan permisos básicos fijos).

## 3. Decisiones técnicas

| Decisión | Opciones consideradas | Elegida | ADR / Fuente |
|---|---|---|---|
| Backend | FastAPI vs Node.js | FastAPI (Python) | D-021 |
| Framework móvil | React Native + Expo vs Flutter vs nativo | React Native + Expo | D-022 |
| Región | sa-east-1 vs AWS Chile (GA fines 2026) | sa-east-1 (São Paulo) | D-023 |
| Base de datos | Supabase vs Neon vs RDS/Aurora | Supabase (PostgreSQL managed) | D-024 |
| Storage | S3 vs Cloudflare R2 vs Backblaze B2 | Cloudflare R2 | D-025 |
| Multi-tenancy | pool (shared schema + tenant_id + RLS) vs silo/schema por tenant | pool + RLS | Hipótesis H-10 (requiere validación) |
| Cache | Upstash Redis vs ElastiCache Valkey | Pendiente (recomendación: Upstash Redis) | Pendiente |
| Cola de trabajos | Dramatiq/ARQ/RQ/Celery/Cloud Tasks/SQS | Pendiente (recomendación: Dramatiq o ARQ sobre Redis) | Pendiente |
| Proveedor de IA | OpenAI/Google/alternativas | Abstracción (adapter); decisión pospuesta | P-012 (pospuesto) |
| Formato personalizado (rango) | TBD | Pendiente | P-004 |
| Validación de info factual | TBD | Pendiente | P-007 |
| Créditos (precios/cantidades) | TBD | Interfaz definida; implementación pendiente | P-001, P-002 |
| Autenticación | Supabase Auth vs JWT propio en FastAPI | Pendiente (recomendación: JWT propio validado por FastAPI, Supabase como BD) | Hipótesis |
| Edición de imagen | Server-side (Pillow) vs client-side | Pendiente (recomendación: server-side para persistir resultado final) | Hipótesis |
| Notificación de progreso | Polling vs WebSocket vs push | Pendiente (recomendación: polling en MVP) | Hipótesis |
| Migraciones | Alembic vs Supabase migrations | Pendiente (recomendación: Alembic en repo) | Hipótesis |

> Las decisiones que cambian arquitectura, stack o proveedores requieren un ADR aprobado por el usuario. Las marcadas como pendiente o hipótesis no se implementan hasta autorización.

## 4. Impacto en arquitectura

- **Módulos afectados:**
  - `backend/app/api/` (rutas FastAPI)
  - `backend/app/services/` (session, generation, credit, storage, provider adapter)
  - `backend/app/models/` (SQLAlchemy + Pydantic)
  - `backend/app/workers/` (consumidor de cola)
  - `mobile/src/screens/create/` (flujo de creación)
  - `mobile/src/api/` (cliente HTTP)
  - Supabase: migraciones SQL (tablas + RLS)
  - R2: buckets temporales y permanentes
- **Dependencias nuevas (justificadas):**
  - FastAPI, Pydantic v2, SQLAlchemy (async), asyncpg
  - Cliente S3-compatible para R2 (boto3/aiobotocore)
  - Cola y Redis: según decisión pendiente (Dramatiq/ARQ/RQ + redis-py)
  - SDKs de IA (`openai`, `google-genai`, `anthropic`): solo se instala el elegido tras P-012; hasta entonces, un mock provider para tests
  - Pillow (si edición server-side) — hipótesis
- **Cambios en contratos entre módulos:**
  - `CreditService`: `get_balance`, `estimate`, `reserve`, `commit`, `release`
  - `AIProvider`: `generate_image`, `generate_text`
  - `StorageService`: `presign_upload`, `presign_download`, `delete`, `get_public_url`
  - `JobQueue`: `enqueue`, `get_status`, `cancel`

## 5. Modelo de datos

Entidades en PostgreSQL (schema compartido `public`), multi-tenant por `workspace_id`:

- `workspaces` (id uuid PK, type enum('personal','organization'), owner_user_id, created_at)
- `users` (id uuid PK, email, created_at)
- `workspace_members` (workspace_id, user_id, role enum('owner','admin','user'), permissions jsonb, created_at)
- `creation_sessions` (id uuid PK, workspace_id FK, user_id FK, status enum('open','closed','abandoned'), created_at, closed_at, expires_at)
- `session_temp_files` (id uuid PK, session_id FK, r2_key, original_filename, content_type, size_bytes, created_at)
- `creation_inputs` (id uuid PK, session_id FK, factual_info jsonb, additional_instructions text, style_id FK, format enum, custom_width int, custom_height int, target_networks text[], variants_count int, created_at, updated_at)
- `styles` (id uuid PK, name, description, prompt_template text, is_active bool, created_at) — catálogo central, administrado por la plataforma
- `generation_jobs` (id uuid PK, session_id FK, workspace_id FK, user_id FK, status enum('queued','running','succeeded','failed','cancelled'), variants_requested int, credits_estimated int, credits_consumed int, model_used text, style_id FK, format, error_code text, created_at, started_at, finished_at)
- `generation_results` (id uuid PK, job_id FK, variant_index int, image_r2_key, image_public_url, text_factual jsonb, text_creative jsonb, edited_image_r2_key text nullable, edit_params jsonb, created_at)
- `saved_results` (id uuid PK, workspace_id FK, user_id FK, result_id FK, saved_at)
- `editable_projects` (id uuid PK, workspace_id FK, user_id FK, result_id FK, reusable_elements jsonb, created_at)
- `library_assets` (id uuid PK, workspace_id FK, user_id FK, r2_key, original_filename, content_type, size_bytes, asset_type enum('logo','image','resource'), created_at) — activos permanentes de biblioteca (logotipos, imágenes, recursos reutilizables)
- `publication_intents` (id uuid PK, result_id FK, workspace_id FK, user_id FK, network enum('instagram','whatsapp'), status enum('pending_review','approved','rejected','cancelled'), created_at) — solo intención; publicación real en SPEC-002. Los estados `published`/`shared` se agregan en SPEC-002.

**Aislamiento por espacio de trabajo:**

- Toda tabla con datos de usuario incluye `workspace_id`.
- RLS policies: `USING (workspace_id = current_setting('app.current_workspace_id', true)::uuid)` y `WITH CHECK` equivalente.
- `FORCE ROW LEVEL SECURITY` en todas las tablas tenant-scoped.
- FastAPI establece `app.current_workspace_id` por request (en la transacción) tras validar membresía y permisos.
- Tests de aislamiento en CI: un tenant no lee datos de otro.

**Datos sensibles y cifrado:**

- `factual_info` puede contener datos personales de terceros (precios, teléfonos, direcciones). Almacenar cifrado a nivel de columna (pgcrypto) o en aplicación (AES-256 con clave en secret manager). Hipótesis: cifrado en aplicación. Decisión final pendiente de validación legal (P-015).
- Tokens de redes sociales no se manejan en esta spec (SPEC-002).
- Archivos en R2 con keys por workspace (`ws/{workspace_id}/...`) y acceso mediante presigned URLs.

**Migraciones:** Alembic en el repositorio (recomendación), aplicadas sobre Supabase. Pendiente de confirmación de tooling.

## 6. Contratos de interfaz (API)

Base: `/api/v1`. Autenticación: Bearer JWT. Toda operación valida autenticación y permisos en el servidor.

### Sesión de creación

| Operación | Método/Ruta | Entrada | Salida | Permisos | Errores |
|---|---|---|---|---|---|
| Iniciar sesión | POST /workspaces/{ws_id}/creation-sessions | {} | { session_id, expires_at } | generate en ws | 403 sin permiso |
| Obtener sesión | GET /creation-sessions/{id} | — | session + inputs + temp files | owner de sesión | 404 |
| Cerrar sesión | POST /creation-sessions/{id}/close | {} | { deleted_files } | owner de sesión | 404, 409 si ya cerrada |

### Archivos temporales

| Operación | Método/Ruta | Entrada | Salida | Permisos | Errores |
|---|---|---|---|---|---|
| Presign upload | POST /creation-sessions/{id}/temp-files/presign | { filename, content_type, size_bytes } | { upload_url, r2_key, expires_in } | owner | 413 si excede límite |
| Confirmar archivo | POST /creation-sessions/{id}/temp-files | { r2_key, original_filename, content_type, size_bytes } | { file_id } | owner | 400 si no existe en R2 |
| Listar temporales | GET /creation-sessions/{id}/temp-files | — | [ { file_id, r2_key, url } ] | owner | — |
| Eliminar temporal | DELETE /creation-sessions/{id}/temp-files/{file_id} | — | 204 | owner | 404 |

> Límites de tamaño/cantidad por sesión: pendiente (pregunta abierta #4 de la spec). Hipótesis: 20 MB por archivo, 20 archivos por sesión. Validar con el usuario.

### Inputs

| Operación | Método/Ruta | Entrada | Salida | Permisos | Errores |
|---|---|---|---|---|---|
| Guardar inputs | PUT /creation-sessions/{id}/inputs | { factual_info, additional_instructions, style_id, format, custom_width?, custom_height?, target_networks, variants_count } | { inputs } | owner | 400 validación |
| Listar estilos | GET /styles | — | [ { id, name, description } ] | autenticado | — |

### Generación

| Operación | Método/Ruta | Entrada | Salida | Permisos | Errores |
|---|---|---|---|---|---|
| Estimar créditos | POST /creation-sessions/{id}/estimate | { variants_count } | { credits_estimated, balance_available } | owner | — |
| Iniciar generación | POST /creation-sessions/{id}/generate | {} (usa inputs guardados) | { job_id, status: "queued" } | owner + créditos disponibles | 402 sin créditos, 400 inputs incompletos, 409 job en curso |
| Estado del job | GET /generation-jobs/{job_id} | — | { status, progress?, results?, credits_consumed?, error? } | owner del job | 404 |
| Cancelar job | POST /generation-jobs/{job_id}/cancel | — | { status } | owner | 409 si ya terminó |

### Edición limitada

| Operación | Método/Ruta | Entrada | Salida | Permisos | Errores |
|---|---|---|---|---|---|
| Aplicar edición | POST /generation-results/{id}/edits | { edit_type, params } | { result } | owner | 400 params inválidos |
| Reemplazar logotipo | POST /generation-results/{id}/logo | { temp_file_id o library_asset_id } | { result } | owner | 404 recurso |
| Cambiar formato (ajuste técnico) | POST /generation-results/{id}/format | { format, custom_width?, custom_height? } | { result, warnings? } | owner | 400, 409 incompatibilidad |

> La edición de textos no está permitida (REQ-018); no existe endpoint para ello. El reemplazo de logotipo acepta archivo temporal de la sesión o activo de biblioteca.

### Guardado

| Operación | Método/Ruta | Entrada | Salida | Permisos | Errores |
|---|---|---|---|---|---|
| Guardar en historial/biblioteca | POST /generation-results/{id}/save | {} | { saved_result_id } | owner | 409 ya guardado |
| Guardar como proyecto editable | POST /generation-results/{id}/save-project | { reusable_elements? } | { project_id } | owner | — |
| Listar historial | GET /workspaces/{ws_id}/results | query params | [ saved_result ] | read | — |
| Listar activos de biblioteca | GET /workspaces/{ws_id}/library-assets | query params (asset_type?) | [ library_asset ] | read | — |

### Intención de publicar/compartir

| Operación | Método/Ruta | Entrada | Salida | Permisos | Errores |
|---|---|---|---|---|---|
| Iniciar publicación/compartido | POST /generation-results/{id}/publish-intent | { network, review_confirmed } | { intent_id, status: "pending_review", preview_url } | generate en ws | 400 si no review_confirmed, 403 sin permiso |
| Preview de contenido final | GET /publication-intents/{id}/preview | — | { image_url, texts, metadata } | owner | — |

> La publicación real queda fuera de esta spec (SPEC-002).

## 7. Procesamiento asíncrono

- La generación puede tardar 5 a 30 segundos por imagen (Hipótesis H-01 del informe de proveedores). Es asíncrona.
- Estados del job: `queued` → `running` → (`succeeded` | `failed` | `cancelled`).
- El cliente envía `POST /generate`, recibe `job_id` y hace polling a `GET /generation-jobs/{id}` con backoff (recomendación MVP). WebSocket/push quedan como opción futura (decisión pendiente).
- El worker consume la cola, llama al `AIProvider` (imagen + texto), almacena el resultado en R2, crea `generation_results`, actualiza el job y consume créditos.
- Reintentos: backoff exponencial ante errores transitorios del proveedor (`RateLimitError`, timeout, 5xx). Máximo 3 intentos por job (constitución: máximo 3 intentos para una misma causa de fallo). Tras 3 fallos, el job queda `failed` y no se consumen créditos (REQ-023).
- Cancelación: el worker verifica el flag de cancelación entre variantes; si se cancela, no genera las restantes y libera los créditos reservados de las no generadas.
- Concurrencia: limitar workers por proveedor según sus rate limits (configurable).
- El consumo de créditos se informa al usuario tras cada generación (REQ-016) vía el estado del job.

## 8. Seguridad

- **Autenticación y autorización:** toda operación valida JWT y membresía/rol en el servidor. Permisos básicos fijos (generar, aprobar, historial) por rol y espacio de trabajo.
- **Secretos y tokens:** las claves de IA y de storage solo existen en el backend (variables de entorno / secret manager). Nunca en la app móvil. Las presigned URLs de R2 tienen expiración corta (ej. 15 min para upload, 1 h para download).
- **Validación de entrada:** Pydantic v2 en todos los payloads; validación de dimensiones de formato personalizado (P-004); validación de tamaño y cantidad de archivos; la información factual se conserva sin alteración (REQ-005) pero se valida su estructura.
- **Aislamiento:** RLS + `workspace_id` en todas las consultas; tests de aislamiento.
- **Registro de auditoría:** log de generaciones (job_id, workspace_id, user_id, modelo, créditos, fecha) para verificabilidad (constitución §6.20). Logs sin datos personales sensibles (minimización).
- **Archivos temporales:** borrado explícito al cerrar la sesión + lifecycle policy de respaldo (7 días). No se persisten originales sin consentimiento del usuario (constitución §2.8).
- **Información factual:** se conserva exactamente (REQ-005). El mecanismo de validación (P-007) está pendiente; mientras, se almacena y se inyecta en el prompt con instrucción de conservación, más validación post-generación (comparación de substrings exactos de los datos factuales en el texto generado). Hipótesis hasta que se resuelva P-007.

## 9. Pruebas

| Tipo | Qué se prueba | Herramienta propuesta |
|---|---|---|
| Unitarias | Servicios (session, storage, credit interface, provider adapter), validación de formato, conservación de info factual | pytest |
| Integración | Flujos end-to-end con BD de prueba (RLS, aislamiento), cola, worker | pytest + Supabase local / testcontainers |
| API | Endpoints (auth, permisos, payloads, errores) | pytest + httpx (TestClient) |
| Aislamiento | Un tenant no lee datos de otro (RLS) | pytest (tests dedicados en CI) |
| Interfaz | Flujo móvil (creación, generación, edición, guardado) | Detox o Maestro (pendiente de decisión) |

Prioridad: permisos, aislamiento, créditos (cuando se implemente), generación.

## 10. Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Proveedor de IA no decidido (P-012) | Alta | Alto | Abstracción de proveedor (adapter); spike de calidad/coste antes de decidir |
| Generación falla o timeout | Media | Medio | Reintentos con backoff (max 3), job failed, sin consumo de créditos, mensaje al usuario |
| Archivos temporales huérfanos | Media | Bajo | Borrado explícito + lifecycle policy de 7 días |
| Fuga de datos entre tenants (RLS mal configurado) | Baja | Alto | `FORCE RLS`, tests de aislamiento en CI, revisión de policies |
| Créditos: race conditions en reserva/consumo | Media | Alto | Interfaz con locks (Redis) cuando se implemente; stub en esta etapa |
| Info factual alterada por IA | Media | Alto | Validación post-generación (substring exacto); P-007 pendiente |
| Formato personalizado inválido | Media | Bajo | Validación en backend (P-004) |
| API de Instagram no viable | Media | Medio | Solo intención en esta spec; publicación real en SPEC-002 con fallback manual |
| Latencia de generación (5-30 s) | Alta | Medio | Async + polling; UX con spinner/preview |
| Coste de egress/storage | Media | Medio | R2 con egress gratis; lifecycle para temporales |

## 11. Fuentes

- `docs/decisions/README.md` (D-001 a D-026, P-001 a P-015)
- `docs/product/product-definition.md`
- `docs/constitution.md`
- `docs/agent-context/research/2026-11-27-stack-arquitectura.md`
- `docs/agent-context/research/2026-11-27-bd-storage.md`
- `docs/agent-context/research/2026-11-27-proveedores-ia.md`
- `docs/specs/001-flujo-creacion/spec.md`

## 12. Plan de verificación

Cómo se comprobará cada criterio de aceptación:

- **CA-001:** test de integración: usuario con créditos → sesión → inputs → generate → job `succeeded` → al menos 1 result con imagen + texto.
- **CA-002:** test API: sin créditos → `POST /generate` → 402, job no creado.
- **CA-003:** test de integración: cerrar sesión → verificar que R2 no tiene objetos bajo el prefijo `tmp/{session_id}/`.
- **CA-004:** test de integración: aplicar edición de posición/escala → `edited_image_url` refleja el cambio y los params quedan guardados.
- **CA-005:** test API: intentar editar un texto → operación rechazada (no existe endpoint o retorna error).
- **CA-006:** test de integración: tras generación exitosa → historial incluye el result con imagen, textos, estilo, formato y fecha.
- **CA-007:** test de integración: generación fallida → saldo de créditos sin cambios.
- **CA-008:** test unitario: info factual "USD 150.000" → el texto generado contiene el substring exacto.
- **CA-009:** test: sesión abandonada → la lifecycle policy elimina los archivos tras la expiración configurada.
- **CA-010:** test API: usuario sin permiso de generar → `POST /creation-sessions` → 403.
- **CA-011:** test API: tras generación → `GET /generation-jobs/{id}` → `credits_consumed` presente.
- **CA-012:** test de integración: `save-project` → proyecto con resultado final + elementos reutilizables, sin archivos originales.
- **CA-013:** test API: `publish-intent` → respuesta incluye `preview_url`; `GET /preview` → contenido final.

## Dependencias y decisiones pendientes que afectan el plan

- **P-001, P-002:** créditos (precios, cantidades, bienvenida). Bloquea: implementación real de `CreditService`, estimación de consumo, bloqueo por saldo.
- **P-004:** rango de formato personalizado. Bloquea: validación de dimensiones.
- **P-005:** capacidad de biblioteca por plan. Bloquea: límites de guardado y cuotas de storage.
- **P-007:** mecanismo de validación de información factual. Bloquea: validación post-generación.
- **P-012:** proveedores de IA. Bloquea: instalación de SDK, implementación del adapter, spike de calidad/coste.
- **P-015:** validación legal. Bloquea: cifrado de datos sensibles, transferencias internacionales, consentimiento.

Además, pendientes no numerados: elección de cache, cola, tooling de migraciones, notificación (polling vs WebSocket), límites de archivos temporales, definición de estilos (D-026 ya resuelto: 8 estilos).
