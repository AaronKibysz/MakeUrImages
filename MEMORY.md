# MEMORY.md

Memoria persistente del proyecto. Se actualiza cuando cambia una decisión, un estado o el foco de trabajo. Lo que aquí figura como "Confirmado" solo cambia con aprobación explícita del usuario.

## Estado actual

- **Fase:** 1 (primera especificación funcional).
- **Etapa completada:** definición funcional (aprobada por el usuario); SPEC-001 aprobada; plan técnico aprobado; 52 tareas listas.
- **Etapa en curso:** Implementación de SPEC-001. T-001 (estructura backend FastAPI) y T-002 (estructura móvil Expo) completadas y verificadas. Siguiente: T-003 (conexión async a PostgreSQL/Supabase).
- **Próximo paso:** Implementar T-003 a T-011 (fundación, auth, storage) respetando dependencias. Resolver decisiones bloqueantes cuando aparezcan (cache/cola, P-004, P-001/P-002, P-012).

## Decisiones confirmadas

Detalle completo en `docs/product/product-definition.md` y `docs/decisions/README.md`.

**Producto**
- Generación de imágenes, textos y publicaciones completas, usables por separado o combinados.
- Android e iOS primero. Web después.
- Mercado inicial: Argentina.
- Estilos visuales administrados centralmente. El usuario elige estilo en cada creación.
- Generación libre con identidad de marca. Plantillas para la primera versión comercial.
- Formatos: 1:1, 4:5, 9:16, 16:9 y personalizado.
- Refinamiento iterativo con IA: fuera del MVP.

**Edición**
- Editor limitado en el MVP: recortar, redimensionar, posición, escala y reemplazo de logotipo.
- Los textos no se editan después de generar la imagen.

**Publicación**
- MVP: solo publicación supervisada. Sin automatización ni programación.
- Redes del MVP: Instagram (publicación directa) y WhatsApp (compartir manualmente).
- Futuro para WhatsApp: publicación en Estados y difusiones. Siempre debe existir la opción de compartir manualmente.
- Fuera del MVP: Facebook, LinkedIn, TikTok, Pinterest y X.
- Sin adaptación creativa por red mediante IA. Solo ajustes técnicos.

**Organizaciones**
- Espacio personal y organizaciones, con separación de información.
- Tres roles: propietario, administrador y usuario.
- En el MVP, solo administradores y propietarios aprueban publicaciones.
- Permisos básicos fijos: generar, aprobar y consultar historial.
- Las conexiones sociales pertenecen a la organización.

**Créditos y comercio**
- Plan de prueba con créditos de bienvenida una sola vez.
- Sin créditos: el usuario conserva acceso a ver, descargar y compartir su historial. No puede generar.
- Compra de suscripciones desde la web y desde la app móvil.
- Cada espacio de trabajo tiene su propia suscripción.

**Archivos**
- Los archivos temporales se eliminan al cerrar la sesión de creación. Regla decidida.
- Proyecto editable opcional: guarda resultado final y elementos reutilizables, sin archivos originales.

**Stack (parcial, autorizado 2026-11-27)**
- Backend: FastAPI (Python), despliegue en contenedores. D-021.
- Framework móvil: React Native + Expo (Android e iOS). D-022.
- Región: São Paulo (sa-east-1). D-023.
- Base de datos: Supabase (PostgreSQL managed). D-024.
- Storage: Cloudflare R2. D-025.
- Estilos del catálogo: 8 estilos (D-026). P-003 resuelto.
- Pendientes: proveedores de IA (spike de calidad/coste), cache y cola, backups (RPO/RTO), pagos in-app (P-008), validación legal (P-015), capacidad de biblioteca (P-005), límites de usuarios por org (P-006).

## Decisiones pendientes (resumen)

Lista completa en `docs/decisions/README.md`.

1. Precios, cantidades de créditos y límites por plan.
2. Cantidad de créditos de bienvenida.
3. Nombres y descripciones de los 8 estilos iniciales (RESUELTO: D-026).
4. Rango permitido para formato personalizado.
5. Capacidad de biblioteca por plan.
6. Límites de usuarios por organización.
7. Mecanismo de validación de información factual.
8. Políticas de Apple y Google para compra dentro de la app (investigación pendiente).
9. Requisitos de la API de Instagram para publicación (investigación pendiente).

## Riesgos vigentes

- Publicación directa en Instagram puede requerir revisión de la aplicación y tipos de cuenta específicos. Si no es viable, el MVP debe seguir funcionando con compartir manual.
- Los textos integrados en la imagen no son editables. Un error factual obliga a regenerar.
- La compra dentro de la app puede implicar comisiones y restricciones de las tiendas.

## Registro de sesiones

- **Sesión 1:** definición funcional. Confirmadas las decisiones de MVP y ronda 1 y 2 de preguntas. Aprobado el resumen.
- **Sesión 2:** creación de la estructura SDD en el repositorio (vacío al inicio). Sin código, sin git, sin configuración de OpenCode.
- **Sesión 3:** propuesta de configuración de OpenCode v2.3.2 (`docs/agent-context/opencode-proposal.md`), verificada contra la documentación oficial. Corregido el frontmatter de `skills/spec-generator/SKILL.md`, necesario para que OpenCode la anuncie. Configuración global leída y sin cambios. Nada aplicado.

- **Sesiones 1 a 3:** fecha no registrada.
- **Sesión 5 (2026-11-27):** aprobados los seis puntos de §13 de la propuesta. Aplicados a `AGENTS.md` (archivos protegidos, consentimiento, límite de reintentos, delegación, resúmenes) y a `docs/constitution.md` (§8 prohibiciones duras, puntos 25 y 26). Configuración de OpenCode sin aplicar.
- **Sesión 4 (2026-11-27):** revisión de prompts de Claude Code y revisión complementaria de `consolidate-memory`, `steward` y `auto-mode-classifier`. Ajustes aprobados incorporados a la propuesta (§12).
- **Sesión 6 (2026-11-27):** configuración de OpenCode aplicada. Creados `opencode.jsonc`, `.opencode/agents/spec-reviewer.md`, `.opencode/agents/docs-researcher.md`, `skills/agent-research/SKILL.md`. Aplicados §12.1 a §12.4. §12.5 aplicado con ajuste adicional: `MEMORY.md` y `tasks.md` editables por `build`. Fase 0 cerrada.
- **Sesión 7 (2026-11-27):** agregada regla de autonomía operativa (AGENTS.md §3.3).
- **Sesión 8 (2026-11-27):** ampliados los subagentes de tareas: task-researcher, planner, implementer, code-reviewer, tester, documenter. Agregados a opencode.jsonc y creados en .opencode/agents/. Total: 8 subagentes.
- **Sesión 9 (2026-11-27):** investigación de stack y arquitectura completada por task-researcher. Informe en `docs/agent-context/research/2026-11-27-stack-arquitectura.md`.
- **Sesión 10 (2026-11-27):** respuestas del usuario: equipo Python, presupuesto no definido, sin web en roadmap.
- **Sesión 11 (2026-11-27):** autorizadas D-021 (FastAPI backend) y D-022 (React Native + Expo móvil). Registradas en docs/decisions/README.md.
- **Sesión 12 (2026-11-27):** investigación de BD y storage completada. Informe en `docs/agent-context/research/2026-11-27-bd-storage.md`.
- **Sesión 13 (2026-11-27):** autorizadas D-023 (región sa-east-1), D-024 (Supabase), D-025 (Cloudflare R2). Registradas en docs/decisions/README.md.
- **Sesión 14 (2026-11-27):** investigación de proveedores de IA completada. Informe en `docs/agent-context/research/2026-11-27-proveedores-ia.md`.
- **Sesión 15 (2026-11-27):** respuestas del usuario: definir estilos antes del spike; balance calidad/coste; texto en imagen depende del estilo; un único proveedor para imagen+texto. Registradas en el informe §14.
- **Sesión 16 (2026-11-27):** aprobados 8 estilos del catálogo (D-026). P-003 resuelto.
- **Sesión 17 (2026-11-27):** uso de APIs de proveedores de IA pospuesto para más adelante. Spike de calidad/coste (P-012) bloqueado hasta que se autoricen las llamadas a APIs. Decisión de proveedor pendiente.
- **Sesión 18 (2026-11-27):** primera especificación funcional creada: SPEC-001 Flujo de creación de publicación (Borrador). En `docs/specs/001-flujo-creacion/spec.md`.
- **Sesión 19 (2026-11-27):** SPEC-001 revisada con spec-reviewer y corregida (12 hallazgos aplicados). Aprobada por el usuario.
- **Sesión 20 (2026-11-27):** Plan técnico de SPEC-001 generado por planner (plan.md + tasks.md). 51 tareas. Plan en revisión.
- **Sesión 21 (2026-11-27):** Plan y tareas de SPEC-001 revisados con spec-reviewer (10 hallazgos). Correcciones aplicadas.
- **Sesión 22 (2026-11-27):** Plan técnico de SPEC-001 aprobado por el usuario. 52 tareas listas. Listo para implementación.
- **Sesión 23 (2026-11-27):** Autorización persistente actualizada: todas las solicitudes de permiso se aceptan automáticamente. `ask` → `allow` en opencode.jsonc y agentes. Prohibiciones duras (`deny`) se mantienen.

## Pendientes de la configuración de OpenCode

- (ninguno) Configuración aplicada. Ver `docs/agent-context/opencode-proposal.md` (estado actualizado).
