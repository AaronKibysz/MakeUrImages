# MEMORY.md

Memoria persistente del proyecto. Se actualiza cuando cambia una decisión, un estado o el foco de trabajo. Lo que aquí figura como "Confirmado" solo cambia con aprobación explícita del usuario.

## Estado actual

- **Fase:** 0 (definición del producto y metodología SDD).
- **Etapa completada:** definición funcional (aprobada por el usuario).
- **Etapa en curso:** estructura de documentación SDD.
- **Próximo paso:** revisión de esta estructura por el usuario. Después, la etapa de investigación técnica y económica, que requiere autorización explícita.

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

## Decisiones pendientes (resumen)

Lista completa en `docs/decisions/README.md`.

1. Precios, cantidades de créditos y límites por plan.
2. Cantidad de créditos de bienvenida.
3. Nombres y descripciones de los 6 a 8 estilos iniciales.
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

- **Sesión 4 (2026-11-27):** revisión de prompts de Claude Code (`docs/agent-context/research/2026-11-27-claude-code-prompts.md`) y revisión complementaria de `consolidate-memory`, `steward` y `auto-mode-classifier` (`docs/agent-context/research/2026-11-27-claude-code-pending-review.md`). Ajustes aprobados incorporados a la propuesta (§12). Hallazgos nuevos en §13 pendientes de aprobación. Nada aplicado a `AGENTS.md` ni a la configuración.

## Pendientes de la configuración de OpenCode

- Aprobación de la propuesta de configuración (§3 a §9) y de los hallazgos de §13.
- Creación de `agent-research` tras la aprobación.
- Validar los puntos marcados en §3 de la propuesta.
- Revisar la regla de `build` en §12.5 antes de aplicar.
