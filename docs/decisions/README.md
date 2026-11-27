# Registro de decisiones

Todas las decisiones relevantes se registran aquí o en un ADR propio.

## Etiquetas de estado

| Etiqueta | Significado |
|---|---|
| **Confirmada** | Aprobada explícitamente por el usuario. |
| **Propuesta** | Recomendación de un agente, sin aprobación. |
| **Pendiente** | Requiere decisión del usuario o investigación previa. |
| **Hipótesis** | Supuesto que debe verificarse. |
| **Verificado** | Hecho confirmado con fuente oficial y fecha de consulta. |

## Decisiones confirmadas

| ID | Tema | Decisión | Fuente |
|---|---|---|---|
| D-001 | Plataformas | Android e iOS primero; web después. | Definición |
| D-002 | Mercado | Argentina primero. | Definición |
| D-003 | Estilos | Catálogo central, elegido por el usuario en cada creación. | Definición |
| D-004 | Formatos | 1:1, 4:5, 9:16, 16:9 y personalizado, elegidos explícitamente. | Definición |
| D-005 | Plantillas | Fuera del MVP; primera versión comercial. | Ronda 1, P3 |
| D-006 | Editor MVP | Recortar, redimensionar, posición, escala y reemplazo de logotipo. | Ronda 1, P4 |
| D-007 | Publicación | Solo supervisada en el MVP. | Ronda 1, P2 |
| D-008 | Redes MVP | Instagram (directa) y WhatsApp (manual). | Ronda 2, P1 |
| D-009 | WhatsApp futuro | Estados y difusiones, con opción manual siempre disponible. | Confirmación final |
| D-010 | Aprobación | Solo administradores y propietarios aprueban. | Ronda 1, P5 |
| D-011 | Compra | Desde web y desde app móvil. | Ronda 1, P6 |
| D-012 | Sin créditos | Ver, descargar y compartir historial; no generar. | Ronda 2, P2 |
| D-013 | Flujo de creación | Rápido, con predeterminados y opciones avanzadas plegadas. | Ronda 2, P3 |
| D-014 | Proyecto editable | Guarda resultado final y elementos reutilizables, sin originales. | Ronda 2, P4 |
| D-015 | Permisos MVP | Permisos básicos fijos: generar, aprobar, historial. | Ronda 2, P5 |
| D-016 | Estilos MVP | Entre 6 y 8 estilos. | Ronda 2, P6 |
| D-017 | Archivos temporales | Se eliminan al cerrar la sesión de creación. | Definición (fija) |
| D-018 | Programación | Fuera del MVP. | Ronda 1, P2 |
| D-019 | Refinamiento IA | Fuera del MVP. | Definición |
| D-020 | Ajustes por red | Solo técnicos; sin generación por red. | Definición |
| D-021 | Backend | FastAPI (Python) como backend principal. Ecosistema IA/ML (LangChain, LlamaIndex, HuggingFace). Despliegue en contenedores. | Investigación 2026-11-27, autorizado por el usuario |
| D-022 | Framework móvil | React Native + Expo (Android e iOS). Cloud builds, OTA updates, mayor pool de contratación. Equipo con experiencia en Python; framework móvil nuevo para el equipo. | Investigación 2026-11-27, autorizado por el usuario |
| D-023 | Región de despliegue | São Paulo (sa-east-1) como región principal. Catálogo completo GA, ~30-40 ms desde Argentina. Bedrock no disponible; usar APIs directas (OpenAI/Google) para IA. | Investigación 2026-11-27, autorizado por el usuario |
| D-024 | Base de datos | Supabase (PostgreSQL managed). Ecosistema completo (auth, storage, realtime). Considerar solapamiento con FastAPI; validar en el plan técnico. | Investigación 2026-11-27, autorizado por el usuario |
| D-025 | Storage de archivos | Cloudflare R2. Egress gratis, 0,015 USD/GB-mes, S3-compatible API, edge en Buenos Aires. | Investigación 2026-11-27, autorizado por el usuario |
| D-026 | Estilos del catálogo (P-003) | 8 estilos: Fotográfico premium, Ilustración moderna, Minimalista corporativo, Retro/vintage, Gastronómico, Inmobiliario, Lifestyle aspiracional, Geométrico/abstracto. Administrados centralmente, elegidos por el usuario en cada creación. | Propuesta del agente, aprobado por el usuario 2026-11-27 |

## Decisiones pendientes

| ID | Tema | Bloquea | Estado |
|---|---|---|---|
| P-001 | Precios, cantidades y límites de planes | Modelo comercial | Pendiente |
| P-002 | Créditos de bienvenida (cantidad) | Plan de prueba | Pendiente |
| P-003 | Nombres y descripciones de los 8 estilos | Catálogo | RESUELTO (D-026) |
| P-004 | Rango del formato personalizado | Generación | Pendiente |
| P-005 | Capacidad de biblioteca por plan | Biblioteca | Pendiente |
| P-006 | Límite de integrantes por organización | Organizaciones | Pendiente |
| P-007 | Mecanismo de validación de información factual | Generación de textos | Pendiente |
| P-008 | Políticas de Apple y Google para compra en app (Argentina) | Compra móvil | Pendiente de investigación |
| P-009 | Requisitos y permisos de la API de Instagram | Publicación Instagram | Pendiente de investigación |
| P-010 | Requisitos de WhatsApp para Estados y difusiones | Fase 2 | Pendiente de investigación |
| P-011 | Stack tecnológico | Arquitectura | RESUELTO (D-021 a D-025) |
| P-012 | Proveedores de IA y costes | Modelo de costes | Pendiente de investigación |
| P-013 | Nombre definitivo del producto | Marca | Pendiente |
| P-014 | Licencia del repositorio | Publicación del código | Pendiente |
| P-015 | Validación legal (Ley 25.326 y términos) | Lanzamiento | Pendiente de asesoramiento profesional |

## Formato de un ADR

Archivo: `docs/decisions/ADR-NNN-slug.md`

```markdown
# ADR-NNN: Título

- **Estado:** Propuesta | Confirmada | Reemplazada por ADR-XXX
- **Fecha:** AAAA-MM-DD
- **Fuentes:** enlaces oficiales y fecha de consulta

## Contexto
## Opciones consideradas
| Opción | Ventajas | Desventajas | Costes | Riesgos |
## Decisión
## Consecuencias
## Revisión futura
```
