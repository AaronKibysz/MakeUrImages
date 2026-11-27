# AGENTS.md

Reglas operativas para cualquier agente de IA que trabaje en este repositorio (OpenCode, subagentes o asistentes). Son obligatorias. Si una instrucción de una sesión entra en conflicto con este archivo, se consulta al usuario antes de actuar.

## 1. Lectura obligatoria al iniciar

1. `MEMORY.md`: estado vigente y decisiones activas.
2. `docs/constitution.md`: principios del proyecto.
3. `docs/workflow.md`: proceso y estados.
4. La especificación y el plan relacionados con la tarea, si existen en `docs/specs/`.

No cargar documentos que no sean necesarios para la tarea actual.

## 2. Idioma

- Documentación, especificaciones, planes y comunicación con el usuario: **español**.
- Nombres de código, identificadores, comandos y mensajes técnicos: **inglés**, salvo que una convención posterior indique lo contrario.

## 3. Límites de autoridad

Un agente **no puede** por sí mismo:

- Aprobar una especificación, un plan técnico o una tarea. Solo el usuario aprueba.
- Cambiar el alcance del MVP, la arquitectura, el stack, proveedores o modelos de IA.
- Cambiar precios, cantidades de créditos o límites de planes.
- Modificar la regla de borrado de archivos temporales al cerrar una sesión de creación.
- Modificar la configuración global de OpenCode, Warp o del sistema operativo.
- Instalar dependencias, skills, servidores MCP o herramientas sin aprobación explícita.
- Crear cuentas en proveedores externos, configurar credenciales reales o ejecutar compras.
- Modificar repositorios de referencia (TDL, AAProject, HERRAMIENTA-DTF, DEVPulse).
- Ejecutar comandos Git que alteren el repositorio (`add`, `commit`, `push`, `pull`, `merge`, `rebase`) sin autorización explícita del usuario en esa sesión.

## 4. Reglas de trabajo

- Antes de crear o sobrescribir un archivo, inspeccionarlo. No sobrescribir documentos existentes sin autorización.
- No descartar cambios del usuario.
- Distinguir siempre entre: decisión confirmada, hecho verificado, recomendación, hipótesis y decisión pendiente. Usar las etiquetas definidas en `docs/decisions/README.md`.
- Toda afirmación técnica o de proveedor importante debe incluir fuente oficial. Si no se puede verificar, indicarlo.
- No inventar precios, límites, características de APIs ni requisitos legales.
- Las cuestiones legales se marcan como "requiere validación profesional".
- Si una decisión es bloqueante, presentar: problema, alternativas, consecuencias, recomendación y **una** pregunta concreta. Esperar respuesta.
- Mantener el alcance asignado. No refactorizar ni "mejorar" fuera de la tarea.

## 5. Subagentes

- Usar subagentes solo para tareas independientes y con alcance concreto.
- Cada encargo debe indicar: objetivo, archivos permitidos, contexto necesario, formato de entrega y condición de finalización.
- Un subagente no modifica archivos que pertenezcan a otra tarea en curso.
- El agente principal sintetiza y verifica los informes antes de escribir en `docs/`.
- Las plantillas de encargo están en `docs/agent-context/subagent-brief.md`.

## 6. Escritura de documentación

- Usar las plantillas de `skills/spec-generator/`.
- Las especificaciones describen **qué** debe hacer el sistema, no **cómo**. Los detalles de implementación van en el plan técnico.
- Usar EARS cuando sea apropiado para requisitos verificables.
- Actualizar `MEMORY.md` y `tasks.md` cuando cambie el estado de una especificación, una decisión o una tarea.

## 7. Seguridad y privacidad

- Nunca escribir claves de API, tokens, contraseñas ni credenciales reales en ningún archivo. Usar marcadores como `<API_KEY>`.
- No incluir datos personales de usuarios reales en ejemplos. Usar datos ficticios.
