# Especificaciones

Cada funcionalidad tiene una carpeta con tres documentos:

```
docs/specs/NNN-slug/
├── spec.md    → qué debe hacer el sistema (comportamiento y criterios de aceptación)
├── plan.md    → cómo se implementa (arquitectura, datos, endpoints, riesgos)
└── tasks.md   → tareas ordenadas y verificables
```

## Reglas

1. Una especificación describe **comportamiento**, no implementación.
2. Usar EARS cuando sea apropiado. Ejemplos:
   - Ubiquitous: `El sistema debe conservar la información factual exactamente como fue introducida.`
   - Event-driven: `Cuando el usuario cierre una sesión de creación, el sistema debe eliminar sus archivos temporales.`
   - State-driven: `Mientras el espacio de trabajo no tenga créditos disponibles, el sistema no debe iniciar nuevas generaciones.`
   - Unwanted: `Si un usuario sin permiso de aprobación intenta aprobar una publicación, el sistema debe rechazar la operación.`
   - Optional: `Donde la organización tenga conexiones de Instagram, el sistema debe ofrecer la publicación directa.`
3. Cada requisito tiene identificador (`REQ-NNN`) y criterio de aceptación verificable.
4. No se implementa nada sin spec `Aprobada` y plan `Plan aprobado`.
5. Los cambios de comportamiento sobre una spec aprobada vuelven a `Borrador`.

## Índice

| ID | Carpeta | Título | Estado |
|---|---|---|---|
| SPEC-001 | 001-flujo-creacion | Flujo de creación de publicación | Aprobada |

Plantillas: `skills/spec-generator/spec-template.md`, `skills/spec-generator/technical-plan-template.md` y `skills/spec-generator/tasks-template.md`.
