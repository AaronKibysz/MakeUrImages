# Plan técnico: SPEC-NNN <Título>

- **Estado:** Plan en revisión
- **Fecha:** AAAA-MM-DD
- **Spec aprobada:** `docs/specs/NNN-slug/spec.md` (fecha de aprobación)
- **Aprobación del plan:** pendiente (usuario)

## 1. Resumen

Qué se implementará y en qué módulos.

## 2. Alcance técnico

- Requisitos cubiertos: REQ-XXX
- Fuera de alcance técnico:

## 3. Decisiones técnicas

| Decisión | Opciones consideradas | Elegida | ADR |
|---|---|---|---|
| ... | ... | ... | ADR-NNN |

Si una decisión cambia arquitectura, stack o proveedores, debe existir un ADR aprobado.

## 4. Impacto en arquitectura

- Módulos afectados:
- Dependencias nuevas (justificadas, con licencia y fuente):
- Cambios en contratos entre módulos:

## 5. Modelo de datos

- Entidades nuevas o modificadas:
- Aislamiento por espacio de trabajo: cómo se garantiza en cada consulta.
- Datos sensibles y cifrado:
- Migraciones:

## 6. Contratos de interfaz

Descripción de las operaciones necesarias, sin implementación. Ejemplo:

| Operación | Entrada | Salida | Permisos requeridos | Errores |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## 7. Procesamiento asíncrono

- ¿La operación puede tardar?
- ¿Qué estados intermedios tiene?
- ¿Cómo se informa al usuario?
- ¿Cómo se reintenta o se cancela?

## 8. Seguridad

- Autenticación y autorización:
- Secretos y tokens:
- Validación de entrada:
- Registro de auditoría:

## 9. Pruebas

| Tipo | Qué se prueba | Herramienta propuesta |
|---|---|---|
| Unitarias | ... | ... |
| Integración | ... | ... |
| API | ... | ... |
| Interfaz | ... | ... |

Las pruebas de permisos, aislamiento, créditos y publicación tienen prioridad.

## 10. Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| ... | ... | ... | ... |

## 11. Fuentes

- Fuente oficial, URL, fecha de consulta.

## 12. Plan de verificación

Cómo se comprobará cada criterio de aceptación (CA-XXX).
