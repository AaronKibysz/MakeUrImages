# Definición del producto

Resumen de las decisiones confirmadas en la etapa de definición. Es la fuente de referencia para las especificaciones funcionales.

Estado de cada punto: **Confirmado** por el usuario. Lo que no figura aquí está pendiente en `docs/decisions/README.md`.

## 1. Propuesta de valor

Personas y empresas necesitan producir imágenes y publicaciones con frecuencia. El flujo habitual exige preparar información, redactar instrucciones para una IA, generar imágenes, corregirlas y publicar manualmente. La plataforma centraliza ese flujo.

Es un producto generalista: inmobiliarias, gastronomía, comercio, profesionales, servicios y emprendimientos.

## 2. Usuarios

| Perfil | Descripción |
|---|---|
| Usuario individual | Persona que crea contenido para su propia marca o actividad. |
| Usuario de organización | Empleado que genera contenido para una empresa, con permisos configurados. |
| Propietario de organización | Controla la suscripción, los integrantes y las conexiones sociales. |
| Administrador de organización | Gestiona integrantes, conexiones y configuración. Aprueba publicaciones. |
| Administrador de plataforma | Gestiona catálogo de estilos, planes y configuración global, según permisos. |
| Propietario de plataforma | Responsable del servicio. Gestiona proveedores de IA, claves y costes. |

El propietario y los administradores de la plataforma son perfiles distintos de los de las organizaciones. Sus permisos están separados.

## 3. Caso de uso principal (ejemplo inmobiliario)

1. Adjuntar fotografías de la propiedad (archivos temporales).
2. Introducir precio, ubicación y características.
3. Seleccionar estilo visual.
4. Indicar instrucciones adicionales.
5. Seleccionar formato.
6. Seleccionar redes (Instagram y/o WhatsApp en el MVP).
7. Elegir una o varias variantes, con consumo estimado previo.
8. Generar, revisar y ajustar de forma limitada.
9. Guardar, publicar en Instagram o compartir manualmente.

## 4. Capacidades

1. Generación y edición de imágenes con IA.
2. Generación de textos, propios o redactados por IA.
3. Publicaciones completas que combinan imagen, información y texto.

Pueden usarse por separado o combinadas.

**Textos.** Se distinguen dos tipos:
- *Información factual* (precios, teléfonos, direcciones, nombres, fechas, características): se conserva exactamente. Requiere mecanismo de verificación.
- *Contenido creativo* (títulos, descripciones, promociones, hashtags, llamadas a la acción): puede ser del usuario o generado por IA.

## 5. Identidad de marca

Nombre comercial, logotipo, colores, tipografías, datos de contacto, material institucional y recursos reutilizables. Es independiente del estilo visual de cada publicación.

## 6. Estilos visuales

- Catálogo predefinido, administrado centralmente.
- El usuario elige estilo en cada creación.
- No hay estilo obligatorio por organización.
- MVP: 8 estilos (D-026): Fotográfico premium, Ilustración moderna, Minimalista corporativo, Retro/vintage, Gastronómico, Inmobiliario, Lifestyle aspiracional, Geométrico/abstracto. Nombres y descripciones aprobados el 2026-11-27.

## 7. Formatos

1:1, 4:5, 9:16, 16:9 y personalizado. El usuario elige formato explícitamente. El sistema no lo elige por la red de destino. Puede hacer ajustes técnicos sin nueva generación de IA, y debe advertir incompatibilidades.

## 8. Generación y variantes

- Una propuesta o varias variantes.
- Consumo estimado de créditos antes de generar.
- Más variantes implican mayor consumo.
- Refinamiento iterativo con IA: fuera del MVP.

## 9. Editor

**MVP:** recortar, redimensionar, ajustar posición y escala, reemplazar logotipo.
**No incluido en MVP:** edición de textos (se regenera), capas, formas, tipografías, deshacer/rehacer.

## 10. Publicación

- **Supervisada:** única modalidad en el MVP. El contenido se revisa y aprueba antes de publicar.
- **Aprobación:** la realizan administradores y propietarios.
- **Automatizada y programada:** fuera del MVP.

## 11. Redes sociales

| Red | Estado en MVP | Modo |
|---|---|---|
| Instagram | Incluida | Publicación directa, sujeta a verificación de API |
| WhatsApp | Incluida | Compartir manualmente |
| Facebook | Fuera | — |
| LinkedIn | Fuera | — |
| TikTok | Fuera | — |
| Pinterest | Fuera | — |
| X | Fuera | — |

- Las conexiones sociales pertenecen a la organización.
- Retirar a un empleado no elimina las conexiones.
- WhatsApp: en el futuro, publicación en Estados y difusiones (B y C). Siempre debe existir la opción de compartir manualmente.
- No se generan variantes de IA por red. Solo ajustes técnicos.

## 12. Archivos

| Tipo | Ubicación | Ciclo de vida |
|---|---|---|
| Biblioteca permanente | Logotipos, imágenes, recursos, plantillas | Hasta que el usuario lo elimine. Capacidad según plan. |
| Archivos temporales | Adjuntos de una sesión de creación | Eliminados al cerrar la sesión. Regla fija. |
| Resultados generados | Imágenes, textos y metadatos | Hasta que el usuario los elimine. Capacidad según plan. |
| Proyecto editable (opcional) | Resultado final y elementos reutilizables | Guardado por elección del usuario. No incluye archivos originales. |

Historial de cada resultado: imagen, textos, datos de la creación, estilo, modelo utilizado, fecha, referencias de consumo y publicación vinculada.

## 13. Organizaciones y permisos

- Espacio personal y organizaciones. Un usuario puede pertenecer a varias organizaciones.
- Cada espacio tiene su suscripción, créditos, biblioteca, historial y conexiones.
- Roles: propietario, administrador, usuario.
- MVP: permisos básicos fijos (generar, aprobar, consultar historial).
- Ningún permiso puede superar el rol al que pertenece.
- Los permisos de publicación son independientes de los administrativos.

## 14. Créditos y planes

- Planes: Prueba, Usuario, Pequeña empresa, Empresa.
- Prueba: créditos de bienvenida una sola vez, sin renovación.
- Planes pagos: créditos mensuales y paquetes adicionales.
- Empresas: bolsa compartida, límites individuales opcionales, registro de consumo individual y general.
- Sin créditos: el usuario puede ver, descargar y compartir su historial, pero no generar.
- Precios, cantidades y límites: **pendientes**.
- El sistema transaccional de créditos (reservas, reembolsos, concurrencia) no se diseña en esta etapa.

## 15. Suscripción y tiendas

- Compra desde web y desde app móvil.
- Políticas de Apple y Google, y alternativas de pago para Argentina: **pendientes de investigación**.

## 16. Administración de IA

Exclusivamente de la plataforma: proveedores, claves, modelos, operaciones, calidad, costes, límites y márgenes. Los usuarios no ven claves ni eligen proveedor. Los usuarios solo eligen estilos del catálogo.

## 17. Mercado

Argentina primero. Diseño preparado para monedas, idiomas, países y zonas horarias, sin implementación completa en el MVP.

## 18. Fuera del MVP

- Facebook, LinkedIn, TikTok, Pinterest, X.
- Publicación programada y automatizada.
- Refinamiento iterativo con IA.
- Plantillas (van en la primera versión comercial).
- Editor por capas y edición de textos.
- Adaptación creativa por red mediante IA.
- Aplicación web.
- Internacionalización completa.
