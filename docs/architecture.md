# Arquitectura

> **Estado: pendiente.** La arquitectura no se definió todavía. Se diseñará en la etapa técnica, tras la investigación autorizada. Este documento registra solo las restricciones ya conocidas, para que las especificaciones no las contradigan.

## Restricciones conocidas

**Plataformas**
- Android e iOS en la primera versión. Web en una etapa posterior.
- No sacrificar la experiencia móvil para reutilizar código.

**Seguridad y datos**
- Las llamadas a proveedores de IA, redes sociales y pagos pasan por el backend.
- Aislamiento de información entre espacios de trabajo desde el diseño.
- Tokens de redes sociales cifrados y accesibles solo al backend.
- Archivos temporales eliminados al cerrar la sesión de creación.
- Archivos originales conservados solo con consentimiento explícito.

**Procesamiento**
- La generación de imágenes y textos y la publicación pueden tardar. No deben bloquear las solicitudes del usuario.
- La arquitectura debe permitir cambiar de proveedor de IA sin reconstruir las aplicaciones.

**Pagos**
- Compra de suscripciones desde la web y desde la app móvil.
- Sistema centralizado de derechos de suscripción y créditos, independiente del proveedor de pago.

**Redes sociales**
- Módulos independientes por red. Instagram y WhatsApp en el MVP.
- La publicación directa en Instagram y la publicación en WhatsApp dependen de verificación de APIs y políticas.

**Edición**
- Editor limitado en el MVP. La arquitectura del editor debe permitir evolucionar a capas, pero no implementarlas ahora.

## Módulos previstos (sin aprobar)

La lista de dominios se toma de la definición del producto. Su división final se decidirá en la etapa técnica.

| Dominio | Responsabilidad general |
|---|---|
| Autenticación | Identidad y sesiones |
| Espacios de trabajo y membresías | Personal y organizaciones, roles y permisos |
| Identidad de marca | Logotipo, colores, tipografías y datos de contacto |
| Suscripciones y créditos | Planes, consumo y derechos |
| Administración de IA | Proveedores, modelos, costes y límites (solo plataforma) |
| Generación | Imágenes y textos |
| Validación factual | Verificación de información proporcionada por el usuario |
| Estilos | Catálogo administrado centralmente |
| Editor | Ajustes básicos sobre resultados |
| Biblioteca e historial | Recursos permanentes y resultados guardados |
| Archivos temporales | Ciclo de vida limitado a la sesión de creación |
| Publicación | Aprobación, publicación directa y compartir manual |
| Redes sociales | Conexiones y módulos por plataforma |
| Auditoría | Registro de operaciones relevantes |
| Panel de plataforma | Administración global del servicio |

## Documentos que se crearán en la etapa técnica

- Diagramas Mermaid de arquitectura general, generación, publicación, créditos, multi-tenant e integraciones.
- Decisiones de stack y proveedores como ADR.
- Modelo de datos.
