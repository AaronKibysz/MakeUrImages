# Revisión de prompts de Claude Code (system_prompts_leaks)

- **Fecha de consulta:** 2026-11-27
- **Fuente:** `asgeirtj/system_prompts_leaks`, carpeta `Anthropic/claude-code/` (rama `main`)
- **Estado:** Hallazgos y recomendaciones. Preguntas 1 a 3 aprobadas el 2026-11-27. Los ajustes quedaron incorporados a la propuesta (`opencode-proposal.md` §12) y **no aplicados** a `AGENTS.md`, configuración ni skills.

## 1. Advertencias sobre la fuente

- No es documentación oficial de Anthropic. El README del repositorio indica que son prompts publicados sin verificación oficial.
- Los archivos tienen frontmatter con campos internos (`disallowedTools`, `omitClaudeMd`, `maxTurns`, `permissionMode`) que no corresponden a la sintaxis de OpenCode. Se adaptan los patrones, no los campos.
- No se copia texto de los prompts. Solo se extraen patrones y se comparan con nuestra propuesta.

## 2. Alcance de la revisión

**Revisado (contenido completo):**

| Archivo | Por qué |
|---|---|
| `agents/Plan.md` | Subagente de planificación, solo lectura |
| `agents/Explore.md` | Subagente de búsqueda, solo lectura |
| `agents/general-purpose.md` | Subagente de propósito general |
| `agents/fork.md` | Subagente que hereda el contexto completo |
| `agents/shared-notes.md` | Reglas comunes de los subagentes |
| `prompts/plan-mode.md` | Flujo de planificación del agente principal |
| `prompts/compact.md` | Instrucciones de compactación de contexto |
| `skills/skill-creator/SKILL.md` | Creación y evaluación de skills |
| `skills/verify/SKILL.md` | Verificación de cambios mediante ejecución |

**Revisado solo por estructura (no el contenido):** `skills/` completo (más de 60 carpetas), `output-styles/`, `prompts/` restantes (`auto-mode-classifier`, `session-recap`, `side-chat`, etc.), `agents/claude.md`, `agents/web-fetch.md`, `skills/steward`, `skills/ship`, `skills/consolidate-memory`.

**Revisado en la segunda pasada:** `consolidate-memory`, `steward` y `auto-mode-classifier`. Ver `docs/agent-context/research/2026-11-27-claude-code-pending-review.md`.

## 3. Hallazgos y adaptación

### 3.1 Subagentes

| # | Patrón observado | Fuente | Adaptación para nuestro proyecto | Decisión |
|---|---|---|---|---|
| S1 | **Solo lectura reforzada en dos niveles:** la lista de herramientas excluye edición y además el prompt lo prohíbe de forma explícita. | `Plan.md`, `Explore.md` | Ya tenemos permisos en la configuración. Agregamos al prompt de cada subagente la prohibición explícita, como respaldo. | **Adoptar** |
| S2 | **La descripción dice cuándo no usar al agente.** `Explore` aclara que no sirve para auditorías ni revisión de documentos, porque lee fragmentos y puede perder contenido. | `Explore.md` | Agregar "no usar para" a las descripciones de `spec-reviewer` y `docs-researcher`. El modelo elige agentes por esa descripción. | **Adoptar** |
| S3 | **Revisor completo, no búsqueda.** Para auditar documentos hay que leerlos completos. | `Explore.md` (advertencia) | `spec-reviewer` debe leer cada documento completo. No usar `explore` para auditorías. | **Adoptar** |
| S4 | **Un subagente no lanza otros.** `Fork` lo prohíbe explícitamente. `Explore` y `Plan` no tienen acceso al lanzador. | `fork.md`, `Explore.md` | Coincide con `subagent_depth: 1` (valor por defecto de OpenCode). Se mantiene. | **Confirmar** (ya cubierto) |
| S5 | **Un encargo, un informe.** Los subagentes informan una vez y no preguntan ni proponen pasos siguientes. | `fork.md` | Agregar a `subagent-brief.md` la regla de informe único. | **Adoptar** |
| S6 | **Los informes se entregan como texto, no como archivos.** Los subagentes no crean archivos de informe. | `general-purpose.md`, `shared-notes.md` | **Conflicto deliberado.** `docs-researcher` escribe en `docs/agent-context/research/` porque necesitamos trazabilidad y fuentes. Se mantiene el archivo, pero el resumen al agente principal debe ser breve (ya lo exige la propuesta). | **Adaptar** |
| S7 | **Un mensaje de otro agente no es aprobación.** Solo el sistema de permisos o el usuario pueden autorizar cambios de configuración. | `shared-notes.md` | Es nuestra regla de aprobación (`AGENTS.md` §3). Se refuerza: ningún informe de subagente aprueba una spec ni cambia permisos. | **Adoptar** |
| S8 | **Tratar la información del usuario y del proyecto como privada.** No incluirla en búsquedas, URLs ni encabezados enviados a servicios externos. | `shared-notes.md` | Muy relevante para `docs-researcher`, que hace búsquedas web. Agregar a `AGENTS.md` y a su prompt: no incluir datos de clientes, proyecto ni credenciales en consultas. | **Adoptar** |
| S9 | **Rutas absolutas y sin emojis en la comunicación.** | `shared-notes.md` | Minor. En nuestro caso, rutas relativas al repositorio, para que sean legibles desde cualquier sesión. | **No adoptar** (criterio de estilo propio) |
| S10 | **Paralelismo acotado.** Explore: hasta 3 agentes en paralelo. Plan: 1 agente. Se usa el mínimo necesario. | `plan-mode.md` | Regla en `AGENTS.md` §5: el número mínimo de subagentes necesario, con un máximo por fase. | **Adoptar** |

### 3.2 Modo plan y flujo de planificación

| # | Patrón | Fuente | Adaptación | Decisión |
|---|---|---|---|---|
| P1 | **Única escritura permitida: el archivo del plan.** Todo lo demás es solo lectura. | `plan-mode.md` | Equivale a la fase de discovery de nuestro flujo: el agente explora y solo escribe la spec en `docs/specs/NNN-slug/` tras aprobación de la fase anterior. | **Adoptar** como regla de fase |
| P2 | **Fases explícitas:** exploración, diseño, revisión, plan final y salida. La salida solo ocurre con una pregunta al usuario o con la solicitud de aprobación. | `plan-mode.md` | Coincide con nuestro `docs/workflow.md`. Agregamos la regla de que el turno termina solo con una pregunta concreta o con la solicitud de aprobación. | **Adoptar** |
| P3 | **La aprobación se pide con un mecanismo específico, no en texto libre.** Las preguntas de aclaración van por una herramienta de preguntas; la aprobación del plan, por otra. | `plan-mode.md` | En OpenCode usamos la herramienta de preguntas para ambas. Lo importante es separar aclaración de aprobación y que la aprobación sea explícita. | **Adaptar** |
| P4 | **El plan final incluye contexto, enfoque recomendado (sin alternativas), archivos críticos y verificación de extremo a extremo.** | `plan-mode.md` | Coincide con `skills/spec-generator/technical-plan-template.md`. Agregamos la sección "archivos críticos" si la plantilla no la tiene. | **Adoptar** |

### 3.3 Contexto y compactación

| # | Patrón | Fuente | Adaptación | Decisión |
|---|---|---|---|---|
| C1 | **Resumen con secciones fijas:** intención, conceptos técnicos, archivos y cambios, errores y correcciones, mensajes del usuario, tareas pendientes, trabajo actual y siguiente paso. | `compact.md` | Nuestra `MEMORY.md` no tiene esa estructura. Propuesta: que la compactación preserve las mismas secciones y que `MEMORY.md` se actualice al cerrar cada sesión. | **Adoptar** |
| C2 | **Las restricciones de seguridad se preservan textualmente** en cualquier resumen. | `compact.md` | Muy relevante. Agregar a `AGENTS.md` una regla: las prohibiciones de la constitución y las decisiones de archivos temporales se copian textualmente en cualquier resumen. | **Adoptar** |
| C3 | **Los mensajes del usuario se listan completos.** Un texto del asistente con formato de mensaje de usuario no se considera del usuario. | `compact.md` | Regla útil para evitar que un agente atribuya aprobaciones que no existen. Agregar a `AGENTS.md`. | **Adoptar** |
| C4 | **Instrucciones de compactación personalizables.** El usuario puede indicar qué priorizar al resumir. | `compact.md` | OpenCode permite configurar `compaction`. Ver `opencode-proposal.md` §8. | **Confirmar** en la configuración |

### 3.4 Skills

| # | Patrón | Fuente | Adaptación | Decisión |
|---|---|---|---|---|
| K1 | **Carga progresiva en tres niveles:** metadatos siempre visibles (~100 palabras), cuerpo de `SKILL.md` (menos de 500 líneas) y recursos bajo demanda. | `skill-creator/SKILL.md` | Coincide con OpenCode: solo nombre y descripción se muestran al modelo. Nuestro `spec-generator` tiene cuerpo corto y plantillas separadas. | **Adoptar** |
| K2 | **La descripción es el mecanismo principal de activación.** Debe incluir cuándo usarla. Se recomienda una descripción "insistente", porque los modelos tienden a no activar skills. | `skill-creator/SKILL.md` | Ajustar la descripción de `spec-generator` para que cubra variantes de petición ("nueva funcionalidad", "plan técnico", "dividir en tareas"). | **Adoptar** |
| K3 | **Las skills útiles para tareas complejas se activan; las tareas simples no.** Una petición trivial no activa una skill aunque coincida. | `skill-creator/SKILL.md` | Esperable. Nuestras skills son de proceso, no de tareas triviales. | **Confirmar** |
| K4 | **Evaluación con casos:** cada caso tiene un prompt y criterios verificables. Se compara la ejecución con la skill frente a una línea base sin skill. | `skill-creator/SKILL.md` | Útil para medir si `spec-generator` produce specs que cumplen la constitución. Propuesta: `skills/spec-generator/evals/` con 3 casos, en una etapa posterior. | **Diferir** |
| K5 | **Optimización de la descripción:** 20 consultas (positivas y negativas), con división entrenamiento/prueba. | `skill-creator/SKILL.md` | Demasiado costoso para la fase 0. Se revisa cuando haya varias skills. | **Diferir** |
| K6 | **Principio de no sorpresa:** una skill no debe contener nada distinto de lo que dice su descripción. | `skill-creator/SKILL.md` | Adoptar como regla de `skills/` y para `agent-research`. | **Adoptar** |
| K7 | **Verificación por ejecución, no por pruebas.** Un cambio se verifica ejecutando el flujo afectado. No basta con tests ni con revisar el código. | `verify/SKILL.md` | Para documentación, equivale a comprobar cada criterio de aceptación contra un resultado observable. Para código, se adapta cuando exista. | **Adaptar** |
| K8 | **Ante la duda, fallar.** Un resultado ambiguo se marca como fallido con evidencia. No hay aprobaciones parciales. | `verify/SKILL.md` | Coincide con nuestra regla de que una spec no se marca como verificada con criterios pendientes. | **Adoptar** |
| K9 | **Informe con pasos, evidencia y hallazgos.** Los hallazgos incluyen fricciones, no solo errores. | `verify/SKILL.md` | Agregar a la plantilla de verificación una sección de "hallazgos" separada del veredicto. | **Adoptar** |

## 4. Patrones que no conviene adoptar

| Patrón | Motivo |
|---|---|
| Agente `fork` (hereda todo el contexto) | Consume mucho contexto en cada llamada. Contradice el criterio de consumo mínimo de tokens. |
| Subagentes de sesión en segundo plano sin límite | Dificulta el seguimiento. Nuestro límite es lo que dice la configuración de §3 de la propuesta. |
| Escribir la verificación como una lista de comprobaciones fija | Los documentos de verificación de Claude Code son específicos de su runtime. Para nosotros, cada spec define sus criterios. |
| Sección de compactación con "siempre" y "nunca" en mayúsculas | Nuestra constitución usa principios explicados, no reglas rígidas. Mantenemos la explicación de cada regla. |
| Agentes de navegador y de escritorio | Fuera del alcance del MVP. |

## 5. Cambios propuestos a la configuración (no aplicados)

Si los aprobás, estos ajustes se incorporan a `docs/agent-context/opencode-proposal.md`. Hoy no están aplicados:

1. Agregar a las descripciones de `spec-reviewer` y `docs-researcher` el texto de "no usar para" (S2, S3).
2. Agregar la prohibición explícita de escritura al prompt de `spec-reviewer` y `docs-researcher` (S1).
3. Agregar la regla de informe único y de privacidad en las consultas externas a `subagent-brief.md` y a `docs-researcher` (S5, S8).
4. Agregar a `AGENTS.md`:
   - Límite de subagentes por fase (S10).
   - Preservación textual de restricciones en cualquier resumen (C2).
   - Mensajes del usuario atribuidos solo a turnos del usuario (C3).
   - Un agente no aprueba nada por informes de otros agentes (S7).
   - Privacidad de la información en búsquedas externas (S8).
5. Ajustar la descripción de `spec-generator` (K2).
6. Agregar a `skills/spec-generator/` la plantilla de informe de verificación con hallazgos (K9).

## 6. Cambios sugeridos a la documentación del proyecto

- `docs/workflow.md`: la fase de discovery y de plan se limitan a escribir solo en la carpeta de la spec (P1). El turno termina con una pregunta o una solicitud de aprobación (P2).
- `docs/constitution.md`: agregar un principio sobre preservación de restricciones y atribución de aprobaciones (C2, C3, S7).

## 7. Riesgos

| Riesgo | Mitigación |
|---|---|
| La fuente puede estar desactualizada o no ser exacta | Cada patrón se verifica antes de adoptarse. Nada se copia. |
| Adoptar demasiados subagentes por imitación | Se mantiene la lista corta de §8 de la propuesta. |
| Confundir patrones de Claude Code con funciones de OpenCode | Cada adaptación se contrasta con la documentación oficial de OpenCode (v2.3.2). |

## 8. Preguntas para el usuario

1. ¿Aprobás los ajustes de la sección 5 para incorporarlos a la propuesta?
2. ¿Querés que revise también `consolidate-memory`, `steward` y `auto-mode-classifier` antes de cerrar la fase de memoria y permisos?
3. ¿Confirmás que `docs-researcher` puede seguir escribiendo informes en archivo, como excepción a S6?
