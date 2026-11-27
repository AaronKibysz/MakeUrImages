# Flujo de trabajo SDD

## 1. Proceso

```
Discovery → Spec → Revisión → Aprobación de spec → Plan técnico → Aprobación del plan
→ Tareas → Implementación → Testing → Revisión → Verificación → Cierre
```

| Etapa | Entrada | Salida | Responsable |
|---|---|---|---|
| Discovery | Idea, necesidad o cambio | Notas de contexto y preguntas abiertas | Usuario y agente principal |
| Spec | Discovery aprobado | `docs/specs/<id>/spec.md` | Agente principal con skill `spec-generator` |
| Revisión | Spec en borrador | Comentarios y correcciones | Usuario |
| Aprobación de spec | Spec revisada | Spec aprobada | **Usuario** |
| Plan técnico | Spec aprobada | `docs/specs/<id>/plan.md` | Agente principal (investigación previa si aplica) |
| Aprobación del plan | Plan completo | Plan aprobado | **Usuario** |
| Tareas | Plan aprobado | `docs/specs/<id>/tasks.md` | Agente principal |
| Implementación | Tareas aprobadas | Código y pruebas | Agentes autorizados |
| Testing | Implementación completa | Resultados de pruebas | Agentes y usuario |
| Revisión | Tests en verde | Hallazgos registrados | Agente revisor y usuario |
| Verificación | Revisión aceptada | Criterios de aceptación cumplidos | Usuario |
| Cierre | Verificación aceptada | Estado `Cerrada` y actualización de `MEMORY.md` | Agente principal |

No se avanza automáticamente de una etapa a otra. Cada aprobación se registra en la especificación.

## 2. Estados de una especificación

| Estado | Significado |
|---|---|
| `Borrador` | En redacción. No se implementa. |
| `En revisión` | Enviada al usuario para revisión. |
| `Aprobada` | Comportamiento aceptado. Se puede planificar. |
| `Plan en revisión` | Plan técnico enviado para revisión. |
| `Plan aprobado` | Puede generar tareas. |
| `En implementación` | Tareas en curso. |
| `En testing` | Implementación completa, pruebas en curso. |
| `En revisión de código` | Revisión técnica. |
| `Verificada` | Criterios de aceptación cumplidos. Pendiente de cierre. |
| `Cerrada` | Completada y registrada. |
| `Rechazada` | No se implementará. Motivo registrado. |
| `Obsoleta` | Reemplazada por otra especificación. Referencia registrada. |

## 3. Transiciones permitidas

```
Borrador → En revisión → Aprobada → Plan en revisión → Plan aprobado
→ En implementación → En testing → En revisión de código → Verificada → Cerrada

En revisión → Borrador            (el usuario solicita cambios)
Plan en revisión → Aprobada       (el plan requiere cambios de alcance o comportamiento)
Plan aprobado → Plan en revisión  (el plan debe modificarse)
En testing / En revisión de código → En implementación  (fallos detectados)
Cualquiera → Rechazada            (decisión del usuario)
Aprobada / Cerrada → Obsoleta     (reemplazo por nueva especificación)
```

Un cambio de comportamiento sobre una especificación `Aprobada` o posterior exige volver a `Borrador`. No se edita en silencio.

## 4. Identificadores

- Especificaciones: `SPEC-NNN-slug`, por ejemplo `SPEC-001-autenticacion-y-espacios`.
- Carpeta: `docs/specs/NNN-slug/` con `spec.md`, `plan.md`, `tasks.md`.
- Decisiones: `ADR-NNN-slug` en `docs/decisions/`.
- Tareas: `T-NNN` dentro de cada `tasks.md`.

## 5. Niveles de cambio

| Nivel | Ejemplo | Requiere |
|---|---|---|
| Menor | Corregir un texto, un enlace o un error tipográfico | Registro en la especificación |
| Comportamiento | Cambiar una regla de negocio o un criterio de aceptación | Nueva revisión de la spec |
| Arquitectura | Cambiar módulos, stack, proveedores o modelo de datos | Nuevo ADR y aprobación del plan |
| Alcance | Agregar o quitar funcionalidades del MVP | Aprobación del usuario y actualización de `docs/roadmap.md` |

## 6. Investigación

La investigación técnica o económica se hace solo después de la autorización del usuario y se registra en `docs/agent-context/research/` o en el ADR correspondiente, con fuentes y fecha de consulta.

## 7. Revisión y verificación

- Revisión: se comprueba que el código cumple la spec y el plan, y que no hay cambios fuera de alcance.
- Verificación: el usuario comprueba los criterios de aceptación de la spec.
- Ninguna tarea se marca como completada sin pruebas que la respalden, salvo que la spec indique lo contrario.
