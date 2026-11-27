# SPEC-001: Flujo de creación de publicación

- **Estado:** Aprobada
- **Fecha:** 2026-11-27
- **Módulo:** Creación de contenido
- **Relacionada con:** D-003, D-004, D-006, D-007, D-008, D-009, D-012, D-013, D-014, D-016, D-017, D-019, D-020, D-026, P-001, P-002, P-004, P-005, P-007, P-012
- **Aprobación de spec:** aprobada por el usuario (2026-11-27)
- **Aprobación de plan:** aprobada por el usuario (2026-11-27)

## 1. Objetivo

Permitir a un usuario crear una publicación (imagen + texto) eligiendo estilo, formato y redes de destino, con edición limitada, guardado y opción de publicar o compartir. El flujo debe ser rápido, con predeterminados y opciones avanzadas plegadas (D-013).

## 2. Alcance

**Incluye:**
- Sesión de creación con archivos temporales.
- Adjuntar archivos temporales (fotografías, logotipos).
- Introducir información factual (precios, ubicación, características, etc.).
- Introducir instrucciones adicionales (texto libre).
- Seleccionar estilo del catálogo (D-026).
- Seleccionar formato (1:1, 4:5, 9:16, 16:9, personalizado).
- Seleccionar redes de destino (Instagram y/o WhatsApp).
- Elegir cantidad de variantes (1 o varias) con consumo estimado de créditos.
- Generar imagen(es) y texto(s) con IA.
- Editar de forma limitada (recortar, redimensionar, posición, escala, reemplazar logotipo).
- Guardar el resultado (historial, biblioteca).
- Guardar como proyecto editable (opcional).
- Iniciar publicación (Instagram directa) o compartir manual (WhatsApp).
- Eliminación de archivos temporales al cerrar la sesión.

**Excluye:**
- Flujo completo de publicación supervisada (aprobación por administrador/propietario, push a Instagram, compartir en WhatsApp). Es una funcionalidad separada (SPEC-002 o posterior). Esta spec solo cubre la intención de publicar/compartir.
- Integración con APIs de Instagram/WhatsApp (publicación directa). Depende de verificación de API (P-009).
- Proyecto editable completo (capas, movimiento, deshacer/rehacer). Fase 2. Esta spec cubre solo el guardado básico (resultado final + elementos reutilizables).
- Refinamiento iterativo con IA (fuera del MVP, D-019).
- Generación de variantes por red (fuera del MVP, D-020).
- Edición de textos generados (se regenera, D-006).
- Editor avanzado (capas, formas, tipografías, deshacer/rehacer).
- Gestión de identidad de marca (se asume configurada previamente).
- Gestión de créditos y planes (SPEC posterior).
- Organizaciones y roles (SPEC posterior, pero se respetan permisos).

## 3. Actores

| Actor | Rol en esta funcionalidad |
|---|---|
| Usuario individual | Crea publicaciones en su espacio personal. Genera, edita, guarda y comparte/publica. |
| Usuario de organización | Crea publicaciones para la organización. Genera, edita y guarda. Publicar requiere aprobación de administrador/propietario. |
| Administrador de organización | Igual que usuario de organización, más puede aprobar publicaciones (fuera de esta spec). |
| Propietario de organización | Igual que administrador. |

## 4. Requisitos

Usar EARS cuando sea apropiado.

| ID | Requisito | Tipo EARS |
|---|---|---|
| REQ-001 | El sistema debe permitir al usuario iniciar una sesión de creación en su espacio personal o en una organización a la que pertenece, siempre que tenga permiso de generar en ese espacio. | Ubiquitous |
| REQ-002 | El sistema debe permitir adjuntar archivos (fotografías, logotipos) a la sesión de creación. Los archivos adjuntos son temporales y se eliminan al cerrar la sesión (D-017). Si el usuario guarda un logotipo en la biblioteca, se convierte en activo permanente. | Ubiquitous |
| REQ-003 | El sistema debe eliminar los archivos temporales de la sesión cuando el usuario la cierra. | Event-driven |
| REQ-004 | El sistema debe permitir al usuario introducir información factual (precios, ubicación, características, datos de contacto, fechas). | Ubiquitous |
| REQ-005 | El sistema debe conservar la información factual exactamente como fue introducida, sin alteración por la IA. | Ubiquitous |
| REQ-006 | El sistema debe permitir al usuario introducir instrucciones adicionales en texto libre. | Ubiquitous |
| REQ-007 | El sistema debe permitir al usuario seleccionar un estilo del catálogo (D-026). | Ubiquitous |
| REQ-008 | El sistema debe permitir al usuario seleccionar un formato entre 1:1, 4:5, 9:16, 16:9 y personalizado. | Ubiquitous |
| REQ-009 | Si el usuario selecciona formato personalizado, el sistema debe validar que las dimensiones estén dentro del rango permitido (P-004 pendiente). | Ubiquitous |
| REQ-010 | El sistema debe permitir al usuario seleccionar una o varias redes de destino entre Instagram y WhatsApp. | Ubiquitous |
| REQ-011 | El sistema debe permitir al usuario elegir la cantidad de variantes a generar (1 o varias). | Ubiquitous |
| REQ-012 | Antes de generar, el sistema debe mostrar el consumo estimado de créditos según la cantidad de variantes elegidas. | Event-driven |
| REQ-013 | Mientras el espacio de trabajo no tenga créditos disponibles, el sistema no debe iniciar nuevas generaciones. | State-driven |
| REQ-014 | Cuando el usuario solicite generar, el sistema debe generar imagen(es) y texto(s) usando el estilo, formato e información proporcionados. | Event-driven |
| REQ-015 | El sistema debe generar los textos distinguiendo información factual (conservada exactamente) de contenido creativo (títulos, descripciones, promociones, hashtags, CTAs). | Ubiquitous |
| REQ-016 | El sistema debe informar al usuario del consumo de créditos realizado tras cada generación. | Event-driven |
| REQ-017 | El sistema debe permitir al usuario editar el resultado de forma limitada: recortar, redimensionar, ajustar posición y escala, reemplazar logotipo. | Ubiquitous |
| REQ-018 | El sistema no debe permitir editar los textos generados; si el usuario desea cambiarlos, debe regenerar. | Ubiquitous |
| REQ-019 | El sistema debe permitir al usuario guardar el resultado generado en su historial y biblioteca. | Ubiquitous |
| REQ-020 | El sistema debe permitir al usuario guardar el resultado como proyecto editable (resultado final y elementos reutilizables, sin archivos originales). | Optional |
| REQ-021 | El sistema debe permitir al usuario indicar la intención de publicar el resultado en Instagram o compartirlo manualmente (incluido WhatsApp), sujeta a la aprobación correspondiente según el espacio de trabajo. | Ubiquitous |
| REQ-022 | El sistema debe guardar metadatos de cada resultado: imagen, textos, datos de la creación, estilo, modelo utilizado, fecha, referencias de consumo y publicación vinculada. | Ubiquitous |
| REQ-023 | Si la generación falla, el sistema no debe consumir créditos y debe informar el error al usuario. | Unwanted behavior |
| REQ-024 | El sistema debe eliminar los archivos temporales al cerrar la sesión de creación (regla fija, D-017). Si la sesión se abandona, una política de ciclo de vida de respaldo debe eliminar los archivos huérfanos transcurrido el tiempo configurado. | Event-driven |
| REQ-025 | Antes de iniciar la publicación o el compartido, el sistema debe mostrar al usuario el contenido final para su revisión. | Ubiquitous |
| REQ-026 | Al cambiar el formato de un resultado ya generado, el sistema debe aplicar ajustes técnicos sin nueva generación de IA y advertir incompatibilidades si las hubiera. | Ubiquitous |

## 5. Criterios de aceptación

Cada criterio debe poder comprobarse.

| ID | Criterio | Requisito relacionado |
|---|---|---|
| CA-001 | Dado un usuario con créditos disponibles, cuando inicia una sesión de creación y completa los campos requeridos (información factual, estilo, formato), entonces el sistema genera al menos una variante de imagen y texto. | REQ-001, REQ-014 |
| CA-002 | Dado un usuario sin créditos, cuando intenta generar, entonces el sistema bloquea la generación e informa que no hay créditos disponibles. | REQ-013 |
| CA-003 | Dado una sesión de creación, cuando el usuario la cierra, entonces todos los archivos temporales adjuntos se eliminan. | REQ-003 |
| CA-004 | Dado un resultado generado, cuando el usuario edita posición y escala del logotipo, entonces el cambio se refleja en la vista previa y en el resultado guardado. | REQ-017 |
| CA-005 | Dado un resultado generado, cuando el usuario intenta editar un texto, entonces el sistema no lo permite e indica que debe regenerar. | REQ-018 |
| CA-006 | Dado una generación exitosa, cuando el usuario consulta su historial, entonces aparece el resultado con imagen, textos, estilo, formato y fecha. | REQ-019, REQ-022 |
| CA-007 | Dado una generación fallida, cuando el usuario consulta su saldo de créditos, entonces no se dedujeron créditos. | REQ-023 |
| CA-008 | Dado información factual introducida (ej. precio "USD 150.000"), cuando se genera el texto, entonces el precio aparece idéntico en el resultado. | REQ-005 |
| CA-009 | Dado una sesión abandonada (sin cierre explícito), cuando transcurre el tiempo de expiración configurado, entonces los archivos temporales se eliminan. | REQ-024 |
| CA-010 | Dado un usuario sin permiso de generar, cuando intenta iniciar una sesión de creación, entonces el sistema rechaza la operación. | REQ-001, sección 7 |
| CA-011 | Dado una generación exitosa, cuando el usuario consulta el resultado, entonces se muestra el consumo de créditos realizado. | REQ-016 |
| CA-012 | Dado un resultado guardado, cuando el usuario elige guardar como proyecto editable, entonces se conserva el resultado final y los elementos reutilizables, sin archivos originales. | REQ-020 |
| CA-013 | Dado un resultado listo para publicar, cuando el usuario inicia la publicación, entonces el sistema muestra el contenido final para revisión antes de proceder. | REQ-025 |

## 6. Casos de error y casos límite

| Situación | Comportamiento esperado |
|---|---|
| Sin créditos disponibles | El sistema bloquea la generación y muestra mensaje de créditos insuficientes. El usuario puede ver, descargar y compartir su historial. |
| Usuario sin permiso de generar | El sistema rechaza la operación de inicio de sesión de creación. |
| Información factual incompleta | El sistema permite generar con la información proporcionada. La validación de información factual es responsabilidad del usuario (P-007 pendiente). |
| Generación fallida (error del proveedor de IA) | El sistema informa el error, no consume créditos, y permite reintentar. |
| Formato personalizado con dimensiones inválidas | El sistema rechaza las dimensiones y solicita valores válidos (P-004 pendiente). |
| Archivo temporal demasiado grande | El sistema rechaza el archivo y muestra el límite permitido. |
| Sesión abandonada | Los archivos temporales se eliminan según la política de ciclo de vida (lifecycle policy + borrado explícito). |
| Usuario de organización sin permiso de publicar | El usuario puede generar y guardar, pero no puede publicar directamente; la publicación requiere aprobación (fuera de esta spec). |
| Generación de varias variantes | El sistema genera todas las variantes solicitadas y muestra el consumo total estimado antes de confirmar. |

## 7. Permisos y roles

Indicar qué roles y permisos básicos pueden realizar cada acción.

| Acción | Usuario individual | Usuario de org | Administrador de org | Propietario de org |
|---|---|---|---|---|
| Iniciar sesión de creación | Sí | Sí | Sí | Sí |
| Adjuntar archivos temporales | Sí | Sí | Sí | Sí |
| Generar (con créditos) | Sí | Sí (si tiene permiso de generar) | Sí | Sí |
| Editar resultado limitado | Sí | Sí | Sí | Sí |
| Guardar resultado | Sí | Sí | Sí | Sí |
| Guardar como proyecto editable | Sí | Sí | Sí | Sí |
| Iniciar publicación/sharing | Sí | Sí | Sí | Sí |
| Aprobar publicación | N/A (publica directo) | No | Sí | Sí |

Nota: los permisos de publicación supervisada (aprobación) se definen en la spec de publicación (SPEC-002 o posterior). En espacio personal, el usuario es propietario y puede iniciar la publicación tras revisar el contenido (REQ-025). En organización, la publicación requiere aprobación de un administrador o propietario.

## 8. Información factual y contenido

La funcionalidad maneja información factual (precios, teléfonos, direcciones, nombres, fechas, características). Se conserva exactamente como fue introducida (REQ-005). El mecanismo de validación de información factual (P-007) es pendiente y se resolverá en el plan técnico o en una spec posterior.

El contenido creativo (títulos, descripciones, promociones, hashtags, CTAs) puede ser del usuario o generado por IA.

## 9. Privacidad y datos

- **Datos personales tratados:** información factual introducida por el usuario (precios, teléfonos, direcciones, nombres, fechas, características). Estos datos pueden incluir información de clientes o terceros.
- **Archivos temporales involucrados:** fotografías y logotipos adjuntos por el usuario.
- **Conservación y eliminación:** los archivos temporales se eliminan al cerrar la sesión. Los resultados generados se conservan hasta que el usuario los elimine. El proyecto editable (opcional) guarda el resultado final y elementos reutilizables, sin archivos originales.
- **Consentimiento requerido:** el usuario debe aceptar los términos de uso y la política de privacidad. El tratamiento de datos personales de terceros (ej. datos de una propiedad) es responsabilidad del usuario.
- **Transferencias internacionales:** los datos se procesan en servidores en São Paulo (sa-east-1) y pueden transferirse a proveedores de IA en US/EU. Requiere validación profesional (P-015).

## 10. Consumo de créditos

La operación consume créditos por cada generación. La cantidad de créditos por generación y los planes disponibles son pendientes (P-001, P-002). El sistema debe:
- Mostrar el consumo estimado antes de generar (REQ-012).
- Informar el consumo realizado tras cada generación (REQ-016).
- No consumir créditos si la generación falla (REQ-023).
- Bloquear la generación si no hay créditos disponibles (REQ-013).

El sistema transaccional de créditos (reservas, reembolsos, concurrencia) no se diseña en esta spec (va en el plan o en una spec posterior).

## 11. Dependencias y decisiones pendientes

- **Decisiones pendientes que afectan esta spec:**
  - P-001: precios, cantidades y límites de planes (afecta consumo de créditos).
  - P-002: créditos de bienvenida.
  - P-004: rango permitido para formato personalizado.
  - P-005: capacidad de biblioteca por plan.
  - P-007: mecanismo de validación de información factual.
  - P-012: proveedores de IA (pospuesto por el usuario).
  - P-015: validación legal (Ley 25.326).
- **Specs de las que depende:** ninguna (es la primera spec).
- **Specs que dependen de esta:** SPEC-002 (publicación supervisada), gestión de identidad de marca, gestión de créditos.

## 12. Preguntas abiertas

1. ¿El usuario puede guardar un resultado sin generar (borrador)? ¿O solo se guarda tras generar?
2. ¿El sistema debe permitir regenerar solo la imagen o solo el texto, o siempre ambos juntos?
3. ¿El proyecto editable (opcional) se crea automáticamente o el usuario elige guardarlo?
4. ¿Los archivos temporales tienen un límite de tamaño o cantidad por sesión?
5. ¿El usuario puede reutilizar archivos temporales de una sesión anterior en una nueva sesión?

## 13. Historial de cambios

| Fecha | Cambio | Motivo | Aprobado por |
|---|---|---|---|
| 2026-11-27 | Creación | — | — |