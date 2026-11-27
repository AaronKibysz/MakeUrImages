# Investigación de stack y arquitectura para el MVP

- **Fecha de creación:** 2026-11-27
- **Autor:** subagente de investigación (encargo de investigación)
- **Estado:** Borrador de investigación (no es una decisión ni una especificación aprobada)
- **Alcance:** Recopilar y comparar opciones para los 7 temas listados en el encargo. No toma decisiones de stack, arquitectura ni proveedores.
- **Fuentes:** documentación oficial de proveedores, páginas de tarifas y guías técnicas (URLs y fechas de consulta al pie de cada dato).

> **Advertencia:** Este informe es material de investigación. Ninguna opción queda elegida. Las decisiones de stack, arquitectura y proveedores requieren autorización explícita del usuario (constitución §4.13, §6.21). Los precios y límites marcados como "requiere verificación" deben confirmarse antes de tomar decisiones de costes.

---

## 1. Resumen (máximo 10 líneas)

1. El equipo de desarrollo es desconocido; ese dato es bloqueante para elegir framework móvil (Pendiente).
2. Para un app móvil Android/iOS de negocio con generación de imágenes y publicación, React Native + Expo y Flutter son las dos opciones cross-platform serias; nativo (Swift/Kotlin) es la opción de mayor coste y tiempo (Verificado, fuentes oficiales de Expo y comparativas 2026).
3. En backend, FastAPI (Python) lidera cuando hay componente de IA/ML por ecosistema (LangChain, LlamaIndex, HuggingFace); Node.js lidera en streaming/UI y equipos full-TypeScript. El patrón híbrido (Node en el borde, Python en IA) es el más citado para productos AI-first (Verificado).
4. PostgreSQL con esquema compartido y Row-Level Security (RLS) es el patrón recomendado por la literatura para multi-tenant B2B SaaS; MongoDB exige aislamiento a nivel de aplicación (Verificado).
5. La publicación directa en Instagram solo es posible sobre cuentas profesionales (Business/Creator), requiere App Review y Business Verification para cuentas ajenas, y el media debe estar en una URL pública al momento de publicar; el tope es ~100 publicaciones por 24 h por cuenta (Verificado, Meta).
6. WhatsApp no ofrece API pública para publicar en Estados de terceros desde una app; la vía soportada es el "Share to Status" mediante intents/URL schemes, con el usuario confirmando la publicación (Verificado, WhatsApp Help Center).
7. Para Argentina, la región de nube más cercana es São Paulo (sa-east-1, ~30-40 ms desde Buenos Aires); AWS Chile (Santiago) está en early access y GA esperada a fines de 2026, con Bedrock/SageMaker dentro del primer año (Verificado).
8. Pagos digitales en app en Argentina deben pasar por el sistema de facturación de la tienda (Apple IAP / Google Play Billing) por regla general; Mercado Pago ofrece SDK nativo para Android/iOS, pero su uso para bienes digitales en app está sujeto a las políticas de las tiendas (Verificado, políticas oficiales; la aplicabilidad exacta requiere validación profesional).
9. Los proveedores de IA de imágenes vigentes son OpenAI (GPT Image 2/2.5, DALL·E retirado del API el 12/05/2026) y Google (Imagen 4 retirado en Gemini API el 17/08/2026 y en Vertex el 30/06/2026; vigente Nano Banana / Nano Banana 2.1). Precios publicados en USD por imagen (Verificado, fuentes oficiales).
10. Las regulaciones argentinas (Ley 25.326) exigen consentimiento informado, inscripción de bases de datos ante la AAIP, medidas de seguridad y restricciones a transferencias internacionales; requiere validación profesional (Verificado parcialmente; ver sección 6).

---

## 2. Framework móvil (tema 1)

### 2.1 Alternativas

| Opción | Lenguaje | Plataformas | Coste relativo | Tiempo a mercado | OTA updates | Ecosistema | Fuente |
|---|---|---|---|---|---|---|---|
| React Native + Expo | TypeScript/JavaScript | Android, iOS, Web | Bajo-medio | Rápido | Sí (Expo Update) | npm completo; mayor pool de contratación | expo.dev (consultado 2026-11-27) |
| Flutter | Dart | Android, iOS, Web, Desktop, Embedded | Bajo-medio | Rápido | Limitado (Shorebird) | Paquetes Dart; pool menor | flutter.dev / comparativas 2026 |
| Nativo (Swift + Kotlin) | Swift, Kotlin | Una plataforma cada uno | Alto (dos codebases) | Lento | No | SDKs completos de plataforma | comparativas 2026 |

### 2.2 Hechos verificados

- Expo y el Expo SDK son gratuitos y open source (MIT). Los servicios de Expo (build, submit, update, CI/CD) tienen planes Free/Starter/Production/Enterprise con cuotas y uso medido (fuente: expo.dev/pricing, consultado 2026-11-27).
- Plan Free de Expo: 15 builds Android + 15 builds iOS (baja prioridad), 60 min CI/CD, 1.000 MAU de updates. Starter: 19 USD/mes + uso, 45 USD de crédito de builds, 3.000 MAU. Production: 199 USD/mes + uso, 225 USD de crédito, 50.000 MAU (fuente: expo.dev/pricing, consultado 2026-11-27).
- Coste por build (usage-based): Android medium 1 USD, large 2 USD; iOS medium 2 USD, large 4 USD (fuente: expo.dev/pricing, consultado 2026-11-27).
- OTA updates en Expo se facturan por MAU actualizado (0,005 USD hasta 200.000) y bandwidth (0,10 USD/GiB extra) (fuente: docs.expo.dev/billing/usage-based-pricing, consultado 2026-11-27).
- React Native 0.88 (octubre 2026) tiene New Architecture como única arquitectura desde 0.82. Flutter 3.50 (noviembre 2026) con Dart 3.13 (fuente: upengroup.com, consultado 2026-11-27).
- React Native renderiza componentes nativos reales; Flutter dibuja sus propios widgets (Impeller) (fuente: múltiples comparativas 2026).
- La documentación oficial de Expo afirma que Meta recomienda empezar apps nuevas con un framework como Expo (fuente: expo.dev/blog, consultado 2026-11-27).

### 2.3 Notas y pendientes

- **Pendiente:** experiencia y preferencia del equipo (desconocida). Es el factor decisivo según las fuentes ("el más rápido es el que el desarrollador conoce bien"). Requiere validación con el usuario.
- **Hipótesis:** si el proyecto también tendrá web (fuera del MVP pero en roadmap), React Native/Expo comparte más código con React web. Marcar como hipótesis hasta confirmar roadmap web.
- **Pendiente:** soporte de IA en cliente. Las fuentes no cubren librerías de IA on-device de forma comparativa para este caso; marcar como pendiente de investigación si se requiere generación en el dispositivo.

---

## 3. Backend (tema 2)

### 3.1 Alternativas

| Opción | Fortalezas | Debilidades | Coste de hosting (entrada) | Fuente |
|---|---|---|---|---|
| FastAPI (Python) + Uvicorn/Gunicorn | Ecosistema IA/ML (LangChain, LlamaIndex, HuggingFace, Pandas/Polars); Pydantic v2; docs OpenAPI automáticas; async | Menor throughput bruto que Node (22k vs 35k req/s simple); cold start más alto en serverless | Render desde 7 USD/mes; Railway desde 5 USD/mes + uso; Fly.io ~2 USD/mes; Cloud Run con free tier | pandastack.io, granite.so, render.com, fly.io (consultado 2026-11-27) |
| Node.js (Fastify/NestJS) | Full-stack TypeScript; streaming/WebSockets; cold start menor; ecosistema npm | Ecosistema IA secundario (LangChain.js con lag 3-12 meses); sin HuggingFace nativo | Render desde 7 USD/mes; Railway desde 5 USD/mes | codelli.tech, ryrlabs (consultado 2026-11-27) |
| Híbrido (Node en el borde + Python/FastAPI para IA) | Combina fortalezas; patrón más citado para productos AI-first | Dos runtimes, dos pipelines, contrato entre servicios a versionar | Suma de ambos | dev.to, fively.dev (consultado 2026-11-27) |

### 3.2 Modelo de despliegue: serverless vs contenedores

| Modelo | Cold starts | WebSockets | Background tasks | Coste en idle | Mejor para |
|---|---|---|---|---|---|
| Contenedor long-lived (PaaS: Render, Railway, Fly.io) | Mínimos una vez warm | Nativos | Fáciles | Pago por contenedor corriendo (o scale-to-zero) | APIs con DB, realtime, jobs largos |
| Serverless (Lambda, Cloud Functions) | Por invocación | A menudo no soportado | Limitados por tiempo | Pago por request | Endpoints stateless y bursty |
| Serverless-contenedor (Cloud Run, Koyeb) | Posibles | Soportados (Cloud Run) | Configurables | Scale-to-zero | Middle ground |

Fuente: pandastack.io (consultado 2026-11-27). Para FastAPI con DB y trabajos de fondo, el modelo contenedor es el "fit más limpio"; serverless brilla en endpoints stateless/bursty.

### 3.3 Hechos verificados

- Para productos con componente de IA sustancial, FastAPI es la mejor opción según varias fuentes (LangChain se posiciona "Python first, JS second"; HuggingFace Transformers no está disponible nativamente en Node; Pandas/Polars sin equivalentes comparables en JS) (fuente: codelli.tech, marsdevs.com, consultado 2026-11-27).
- El patrón híbrido (Node en el borde para auth/sesiones/WebSockets, Python/FastAPI para IA/RAG/agentes) es el más citado para productos AI-first en escala (fuente: dev.to, fively.dev, consultado 2026-11-27).
- Cloud Run (GCP) soporta WebSockets, requests hasta 60 min, scale-to-zero, y no requiere adapter para ASGI (fuente: makeanapplike.com, consultado 2026-11-27).
- AWS Lambda con Mangum permite FastAPI en Lambda pero con límite de 15 min de ejecución, cold starts con dependencias pesadas y WebSockets en servicio separado (fuente: pandastack.ai, consultado 2026-11-27).

### 3.4 Pendientes

- **Pendiente:** tamaño y experiencia del equipo (desconocido). Es factor decisivo (constitución: no cambiar stack sin autorización).
- **Hipótesis:** dado que el producto es AI-first (generación de imágenes/textos con IA), el ecosistema Python es estructuralmente ventajoso. Marcar como hipótesis hasta validar con el usuario.
- **Pendiente:** si se requiere streaming de LLM en tiempo real al cliente, Node.js tiene ventaja; si la generación es asíncrona (jobs en background), Python es suficiente.

---

## 4. Base de datos y almacenamiento de archivos (tema 3)

### 4.1 Base de datos: PostgreSQL vs MongoDB

| Aspecto | PostgreSQL | MongoDB |
|---|---|---|
| Aislamiento multi-tenant | RLS (row-level security) a nivel de BD; schema por tenant; DB por tenant | Campo tenantId en colecciones compartidas; aislamiento a nivel de aplicación |
| Quién hace cumplir | La base de datos (RLS policies) | Código de aplicación |
| Joins/reporting | SQL joins nativos entre tablas/esquemas | $lookup, mismo DB |
| Transacciones | ACID nativo | Transacciones soportadas (más recientes) |
| Flexibilidad de esquema | JSONB con índices GIN | Nativo (cada doc puede diferir) |
| Escalado horizontal | Cloud-managed (Supabase, Neon, RDS Aurora) | Sharding de primera clase |
| Coste hosted | Supabase Free 500 MB, Pro desde 25 USD/mes; Neon Free 1 GB/proyecto, Launch 0,106 USD/CU-hora | Atlas Free 512 MB; Flex 8-30 USD/mes; Dedicated desde 56,94 USD/mes |
| Recomendación de la literatura | Default para B2B SaaS | Solo si datos genuinamente document-shaped |

Fuente: eltherion.com, techpuvi.com, pineido.com (consultado 2026-11-27).

### 4.2 Multi-tenancy: patrones de aislamiento

Patrones principales (fuente: AWS Prescriptive Guidance, clickhouse.com, consultado 2026-11-27):

| Patrón | Aislamiento | Coste/operación | Onboarding de tenants | Cuándo usar |
|---|---|---|---|---|
| Silo (DB/instancia por tenant) | Máximo | Alto | Lento | Clientes grandes/regulados, white-label |
| Bridge (DB por tenant en instancia compartida) | Alto | Medio | Moderado | Aislamiento de datos clave, sin cross-reference |
| Bridge (schema por tenant) | Alto (lógico) | Medio-alto | Moderado | Moderado número de tenants |
| Pool (tablas compartidas + tenant_id + RLS) | Lógico (RLS) | Bajo | Rápido | Muchos tenants con poco dato cada uno (default B2B SaaS) |

Recomendación de la literatura para B2B SaaS en 2026: **pool (shared schema + tenant_id + RLS)** como default, con tiering (silo para clientes premium/regulados) a escala. Fuente: clickhouse.com (consultado 2026-11-27). Nota: schema-per-tenant es considerado "trampa" por overhead de migraciones y connection pool.

Implementación RLS en PostgreSQL (fuente: clickhouse.com, consultado 2026-11-27):

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_select ON orders
  FOR SELECT USING (tenant_id = current_setting('app.current_tenant_id', true)::uuid);
CREATE POLICY tenant_isolation_insert ON orders
  FOR INSERT WITH CHECK (tenant_id = current_setting('app.current_tenant_id', true)::uuid);
```

Caveats verificados:
- Superusers y roles con BYPASSRLS saltan RLS; los owners de tabla también, salvo FORCE RLS (fuente: postgresql.org docs, citado en eltherion.com).
- RLS es una garantía a nivel de BD, pero el cache y el storage de archivos no se protegen automáticamente (fuente: pineido.com).
- Requiere tests automatizados en CI que verifiquen que un tenant no lee datos de otro (fuente: pineido.com).

### 4.3 Almacenamiento de archivos (imágenes)

| Servicio | Storage (USD/GB-mes, región US East) | Requests PUT/GET | Egress | Notas |
|---|---|---|---|---|
| Amazon S3 Standard | 0,023 (primeros 50 TB) | 0,005/1000 PUT; 0,0004/1000 GET | 0,09/GB (primeros 10 TB, tras 100 GB gratis) | Free tier: hasta 200 USD créditos para cuentas nuevas (desde 15/07/2025) |
| Cloudflare R2 (no verificado en esta investigación) | — | — | — | Marcado como pendiente; no se incluyó fuente verificada |
| Backblaze B2 (no verificado) | — | — | — | Marcado como pendiente |

Fuente: aws.amazon.com/s3/pricing (consultado 2026-11-27); upstash.com/blog/aws-s3-pricing-explained-2026; nubbo.app.

**Consideraciones para Argentina (ver sección 6):** sa-east-1 (São Paulo) es la región AWS más cercana; el pricing de S3 en sa-east-1 puede diferir del de US East. Verificar antes de presupuestar. AWS Chile (Santiago) en early access (GA esperada fines 2026) puede ofrecer menor latencia para Argentina (fuente: aboutamazon.com, 2026-11-11).

**Patrón para archivos temporales (decisión D-017):** los archivos temporales se eliminan al cerrar la sesión de creación. Implementación típica: bucket con lifecycle policy + borrado explícito al cerrar sesión; URLs pre-firmadas para upload/download; no persistir originales sin consentimiento (constitución §2.8).

**Patrón para imágenes generadas:** almacenar en S3 (o compatible) con URL pública para que Instagram pueda hacer cURL del media al publicar (requisito de Meta, ver sección 5). Considerar CDN (CloudFront) para servir imágenes a usuarios; el egress es el componente dominante del coste (~87% en el ejemplo de upstash).

### 4.4 Pendientes

- **Pendiente:** elección de proveedor de storage (S3 vs R2 vs B2) y región. Requiere verificación de precios en sa-east-1/Chile.
- **Pendiente:** capacidad de biblioteca por plan (P-005) y límites de usuarios por org (P-006) afectan el dimensionamiento.

---

## 5. Integración con IA (tema 4)

### 5.1 Dónde se ejecuta la generación

Recomendación de la literatura (no decisión): la generación de imágenes con IA se ejecuta en el **backend** (no en el cliente), porque:
- Las claves de API nunca se envían a la app móvil ni a la web (constitución §1.1).
- El consumo de IA debe ser verificable y registrado en el backend (constitución §6.20).
- El backend permite control de cuotas, costes y reintentos.

El cliente (app móvil) envía el prompt y parámetros; el backend llama al proveedor, almacena el resultado en storage y devuelve la URL. Esto es consistente con la constitución.

### 5.2 Proveedores candidatos (solo listar, no elegir)

#### OpenAI (imagen)

- Modelos vigentes (noviembre 2026): GPT Image 2, GPT Image 2.5 (Sunburst = calidad, Flare = rápido). DALL·E 2 y DALL·E 3 retirados del API el 12/05/2026. gpt-image-1 retirado el 23/10/2026; gpt-image-1-mini y gpt-image-1.5 retirados el 01/12/2026 (fuente: developers.openai.com, openai.com, consultado 2026-11-27).
- Tarifa: 5 USD/1M tokens de texto input, 8 USD/1M tokens de imagen input, 30 USD/1M tokens de imagen output (fuente: developers.openai.com/api/docs/pricing, consultado 2026-11-27).
- Coste por imagen (GPT Image 2, 1024×1024): ~0,006 USD low, ~0,053 USD medium, ~0,211 USD high. GPT Image 2.5 no publica tabla por imagen; se factura por tokens (fuente: costgoat.com, growth-hacker.fr, consultado 2026-11-27).
- Batch API: mitad de precio (4 USD/1M image input, 15 USD/1M image output) (fuente: growth-hacker.fr, consultado 2026-11-27).
- Rate limits: Build 2.500 img/min, Launch 7.500 img/min, Grow 10.000 img/min (fuente: developers.openai.com/models/dall-e-3, consultado 2026-11-27).

**Requiere verificación:** los precios exactos por imagen de GPT Image 2.5 deben medirse sobre muestra real; la tabla por imagen solo está publicada para GPT Image 2.

#### Google (imagen)

- Imagen 4 (Fast/Standard/Ultra) retirado de Gemini API el 17/08/2026 y de Vertex AI el 30/06/2026. Vigente: Nano Banana (Gemini 2.5 Flash Image) y Nano Banana 2.1/Pro (fuente: ai.google.dev/gemini-api/docs/imagen, consultado 2026-11-27).
- Tarifa Nano Banana 2.1: 0,0336 USD por imagen 1K, 0,0504 USD por 2K, 0,113 USD por 4K. Pro: 0,134 USD (1K/2K), 0,24 USD (4K) (fuente: hiapi.ai, consultado 2026-11-27).
- Tarifa histórica Imagen 4 (solo referencia, modelos retirados): Fast 0,02 USD, Standard 0,04 USD, Ultra 0,06 USD por imagen (fuente: cloud.google.com/model-garden/pricing, consultado 2026-11-27).
- Imagen 4 en Vertex AI sigue listado en la página de pricing pero los endpoints están descontinuados (fuente: genspend.io, consultado 2026-11-27). **Hipótesis:** la página de pricing de Google Cloud no se ha actualizado; verificar disponibilidad real antes de integrar.

**Requiere verificación:** disponibilidad actual de Imagen 4 en Vertex AI; si está descontinuado, usar Nano Banana.

#### Otros proveedores candidatos (solo listar, sin fuente verificada en esta investigación)

- Black Forest Labs (FLUX.2) — precios desde 0,001-0,015 USD/imagen según variante (fuente: hiapi.ai, consultado 2026-11-27).
- Recraft, Seedream (BytePlus), Ideogram — listados en hiapi.ai con precios aproximados (fuente: hiapi.ai, consultado 2026-11-27).
- Estos proveedores no tienen documentación oficial verificada en esta investigación; marcar como **pendiente de verificación**.

### 5.3 Texto (LLM)

- OpenAI: GPT-5.x, precios por 1M tokens (fuente: developers.openai.com/api/docs/pricing, consultado 2026-11-27). **Requiere verificación:** modelo específico y tarifa para generación de textos de marketing.
- Google Gemini: precios por token (fuente: cloud.google.com/model-garden/pricing, consultado 2026-11-27).
- Anthropic Claude: no investigado en esta ronda; marcar como pendiente.

### 5.4 Pendientes

- **Pendiente:** selección de proveedor(es) de IA (P-012). Requiere autorización del usuario y validación de costes reales.
- **Pendiente:** mecanismo de validación de información factual (P-007) — afecta la generación de textos.
- **Hipótesis:** el coste dominante será la generación de imágenes (no el texto). Validar con prototipo.

---

## 6. Publicación en redes sociales (tema 5)

### 6.1 Instagram: Content Publishing API (Graph API)

Hechos verificados (fuente: developers.facebook.com, consultado 2026-11-27):

- Solo publica en **cuentas profesionales** (Business o Creator). Las cuentas personales no son elegibles.
- Dos rutas de login: **Instagram Login** (host graph.instagram.com, scopes `instagram_business_basic`, `instagram_business_content_publish`, no requiere Facebook Page) y **Facebook Login for Business** (host graph.facebook.com, scopes `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`, requiere Facebook Page vinculada).
- Flujo de publicación: crear media container desde una **URL pública** → esperar status FINISHED → llamar a `media_publish`. Tres llamadas por post.
- Formatos soportados: imagen única, video, Reel, carrusel (hasta 10 items). Imágenes solo JPEG.
- Tope: ~100 publicaciones por API en 24 h por cuenta (moving window). Meta documenta también 50/día en otra sección; verificar con el endpoint `content_publishing_limit`.
- El media debe estar en un servidor público accesible al momento del intento (Meta hace cURL). URLs firmadas que expiran rápido fallan.
- Standard Access suficiente para cuentas propias/gestionadas (sin revisión). Advanced Access (para cuentas de terceros) requiere App Review + Business Verification.
- Business Verification obligatoria si la app sirve a usuarios sin rol en la app.
- Page Publishing Authorization (PPA): una cuenta vinculada a una Page que requiera PPA no puede publicar hasta completar PPA; no se puede detectar anticipadamente.
- Container expira si no se publica en 24 h.

**Riesgo vigente (MEMORY.md):** la publicación directa puede requerir revisión de la app y tipos de cuenta específicos. Si no es viable, el MVP funciona con compartir manual.

### 6.2 WhatsApp: compartir manual

Hechos verificados (fuente: faq.whatsapp.com, consultado 2026-11-27):

- WhatsApp ofrece **Share to Status API** para compartir fotos/videos/stickers a Estados mediante intents (Android) y URL schemes (iOS). El usuario edita y publica en el compositor de WhatsApp. No es publicación automática.
- Para compartir a un chat: deep link `wa.me/<número>?text=...` o `whatsapp://send?text=...`. En iOS se recomienda UIActivityViewController (Share Extension). Límites: hasta 30 archivos mixtos; imágenes hasta 16 MB; videos hasta 200 MB; todos los archivos hasta 2 GB.
- No hay API pública para publicar en Estados de terceros sin interacción del usuario. La opción manual siempre debe existir (decisión D-009).

**Conclusión para el MVP:** la publicación en WhatsApp es compartición manual (decisión D-008), consistente con lo que las APIs soportan. La publicación en Estados/difusiones queda para Fase 2 (P-010).

### 6.3 Viabilidad de publicación directa (resumen)

| Red | Directa en MVP | Condiciones | Riesgo |
|---|---|---|---|
| Instagram | Sí, sujeta a verificación | Cuenta profesional; App Review + Business Verification para terceros; media en URL pública; tope ~100/24h | Alto (revisión, PPA, cuenta profesional) |
| WhatsApp | No (manual) | Share to Status / deep links con confirmación del usuario | Bajo (siempre funciona) |

---

## 7. Consideraciones para Argentina (tema 6)

### 7.1 Latencia y regiones de nube

Hechos verificados (fuentes: pingcloud.io, aboutamazon.com, datametricgroup.com, consultado 2026-11-27):

- La región más cercana a Argentina es **São Paulo (sa-east-1)**: ~30-40 ms de mediana desde Buenos Aires (AWS, Azure, GCP, Oracle).
- AWS South America (Chile, Santiago) está en early access para clientes selectos; GA esperada a fines de 2026. AWS afirma que reducirá latencia para Argentina, Paraguay, Uruguay, Bolivia y Perú. Bedrock y SageMaker AI se añadirán dentro del primer año.
- GCP tiene región en Santiago (southamerica-west1) desde 2021; Azure tiene Chile Central desde 2025.
- São Paulo cuesta entre 54% y 62% más que Virginia para instancias EC2 (fuente: datametricgroup.com, consultado 2026-11-27).
- AWS tiene Local Zones en Buenos Aires (no es una región completa; servicios limitados: EC2, ECS/EKS, EBS, VPC, ElastiCache; S3 y DynamoDB siguen en la región).

**Implicación:** para baja latencia en Argentina, usar sa-east-1 (São Paulo) o, cuando esté GA, Santiago (Chile). Para servicios de IA (Bedrock), verificar disponibilidad regional; puede requerir otra región.

### 7.2 Pagos

Hechos verificados (fuentes: developer.apple.com, support.google.com, mercadopago.com.ar, consultado 2026-11-27):

- Apple: In-App Purchase obligatorio para bienes digitales/suscripciones usadas dentro de la app (App Review Guidelines 3.1.1). Comisión 30% (15% Small Business Program y suscripciones tras el primer año). Apple Developer Program 99 USD/año (fuente: developer.apple.com, mobiloud.com).
- Google: Google Play Billing obligatorio para bienes digitales/suscripciones (Payments policy). Comisión 20-25% + 5% en algunos casos; 10%+5% primeros 1M USD y suscripciones (fuente: support.google.com, appside.build).
- Mercado Pago: ofrece SDK nativo para Android/iOS (Core Methods) con tokenización de tarjetas, y Checkout Pro/API/Subscriptions. Disponible en Argentina. Tiene SDKs para iOS, Android y Flutter (fuente: mercadopago.com.ar/developers, consultado 2026-11-27).
- **Hipótesis/Pendiente:** Mercado Pago puede usarse para pagos de suscripciones en web y posiblemente como alternativa de pago en app en ciertas jurisdicciones, pero las políticas de Apple/Google para bienes digitales en app son restrictivas. La aplicabilidad exacta en Argentina requiere validación profesional (P-008). **No inventar** una solución de pagos; marcar como pendiente.

### 7.3 Regulaciones (Ley 25.326)

Hechos verificados (fuentes: argentina.gob.ar, theargentinethread.com, pentestingteam.com, consultado 2026-11-27):

- Ley 25.326 de Protección de los Datos Personales (vigente desde 2000), reglamentada por Decreto 1558/2001. Autoridad: AAIP (Agencia de Acceso a la Información Pública).
- Obligaciones clave: consentimiento libre, expreso e informado (art. 5); información al recabar datos (art. 6); inscripción de bases de datos ante la AAIP (art. 21); medidas de seguridad y confidencialidad (art. 9); secreto profesional (art. 10); restricciones a transferencias internacionales (art. 12); derechos ARCO (arts. 14-16).
- Sanciones: apercibimiento, suspensión, multa (ARS 1.000 a 100.000 por la ley; el régimen sancionatorio actualizado por Res. AAIP 126/2024), clausura/cancelación de la base (art. 31). Régimen sancionatorio de la Res. 126/2024 vigente desde 01/06/2024.
- La AAIP ha sancionado a empresas (incluyendo una investigación de oficio contra Mercado Pago) en noviembre 2026 (fuente: argentina.gob.ar, 2026-11-02).
- **Requiere validación profesional:** aplicabilidad exacta a un SaaS con proveedores en la nube fuera de Argentina (transferencias internacionales), registro de bases de datos, consentimiento para uso de IA generativa, y tratamiento de datos de empresas (personas jurídicas también son sujetos). Marcar como P-015.

### 7.4 Tiendas (Apple/Google) en Argentina

Hechos verificados (fuente: mobiloud.com, consultado 2026-11-27):

- Apple Developer Program: 99 USD/año. Google Play Console: 25 USD una vez.
- Apple requiere Xcode 26 e iOS 26 SDK para builds; Google requiere target Android 16 (API 36).
- Apple: 50% de las apps revisadas en <24 h, 90% en <48 h. Google: hasta 7 días.
- Cuenta de desarrollador: individual u organización (ambas requieren D-U-N-S para empresas).

**Pendiente (P-008):** políticas específicas para Argentina (comisiones, alternativas de pago, IAP vs pagos externos) requieren validación profesional y consulta de las reglas vigentes por país (las reglas cambian y varían por jurisdicción).

---

## 8. Multi-tenancy y organizaciones (tema 7)

Ver sección 4.2 para los patrones de aislamiento de datos en PostgreSQL.

### 8.1 Requisitos del producto (de product-definition.md)

- Espacio personal + organizaciones; un usuario puede pertenecer a varias organizaciones.
- Cada espacio tiene su suscripción, créditos, biblioteca, historial y conexiones sociales.
- Roles: propietario, administrador, usuario. Permisos básicos fijos: generar, aprobar, consultar historial.
- Las conexiones sociales pertenecen a la organización.
- Aislamiento desde el diseño: ninguna consulta devuelve datos de otro espacio sin autorización (constitución §2.5).

### 8.2 Recomendación de la literatura (no decisión)

- Patrón **pool (shared schema + tenant_id + RLS)** como default para B2B SaaS con muchos tenants y poco dato por tenant (fuente: AWS Prescriptive Guidance, clickhouse.com, consultado 2026-11-27).
- El tenant_id debe propagarse en todas las capas: API, cache, storage (object keys por tenant), background jobs, audit logs, analytics (fuente: clickhouse.com).
- Para clientes premium/regulados, considerar tiering con silo (DB dedicada) (fuente: AWS Prescriptive Guidance).
- MongoDB no tiene RLS nativo; el aislamiento es a nivel de aplicación (más débil, más difícil de auditar para SOC 2/HIPAA) (fuente: pineido.com).

### 8.3 Pendientes

- **Pendiente (P-006):** límite de integrantes por organización (afecta dimensionamiento y planes).
- **Pendiente:** estrategia de tiering (cuándo promover un tenant a silo) — decisión de negocio, no técnica.
- **Pendiente:** auditoría de aislamiento (tests automatizados en CI) — requiere especificación.

---

## 9. Tabla comparativa de frameworks móviles (resumen)

| Factor | React Native + Expo | Flutter | Nativo (Swift/Kotlin) |
|---|---|---|---|
| Lenguaje | TypeScript/JS | Dart | Swift/Kotlin |
| Codebases | 1 (+ native modules) | 1 (+ platform channels) | 2 |
| UI | Componentes nativos reales | Engine propio (Impeller) | Nativo |
| Performance (apps de negocio) | Excelente | Excelente | Mejor posible |
| OTA updates | Sí (Expo Update) | Limitado (Shorebird) | No |
| Cloud builds | Sí (Expo Build) | Third-party | Third-party |
| Pool de contratación | Mayor (JS/TS/React) | Menor (Dart) | Dos pools especializados |
| Compartir código con web | Alto (TS) | Limitado | Ninguno |
| Coste relativo | Bajo-medio | Bajo-medio | Alto |
| Tiempo a mercado | Rápido | Rápido | Lento |
| Tiendas | iOS + Android | iOS + Android (+ web/desktop/embedded) | Una plataforma |

Fuente: expo.dev, arvucore.com, pyalm.com, upengroup.com (consultado 2026-11-27).

---

## 10. Recomendación (no decisión)

> **Importante:** Esta sección es una recomendación del subagente de investigación, no una decisión. Requiere autorización explícita del usuario (constitución §3, §4.13).

### 10.1 Framework móvil

**Recomendación:** React Native + Expo, **si** el equipo tiene experiencia en JavaScript/TypeScript o React, o si se prevé compartir código con una futura web. **Alternativa:** Flutter si el equipo prefiere Dart o se necesita UI pixel-idéntica multiplataforma incluyendo desktop/embedded. **Nativo** solo si la app depende de hardware/OS profundo.

**Justificación:** Expo ofrece cloud builds, OTA updates, file-based routing y el mayor pool de contratación; Meta recomienda empezar con un framework como Expo. El coste y tiempo a mercado son menores que nativo.

**Bloqueo:** experiencia del equipo desconocida (Pendiente).

### 10.2 Backend

**Recomendación:** FastAPI (Python) como backend principal si el componente de IA es sustancial (este producto lo es), por el ecosistema LangChain/LlamaIndex/HuggingFace/Pandas. **Alternativa:** Node.js (Fastify) si el equipo es full-TypeScript y la IA se externaliza vía API. **Patrón híbrido** (Node en el borde + FastAPI para IA) para escala, a costa de complejidad operativa.

**Justificación:** el producto es AI-first; el ecosistema Python es estructuralmente ventajoso. El despliegue en contenedores (Render/Railway/Fly.io o Cloud Run) es el "fit más limpio" para FastAPI con DB y jobs en background.

**Bloqueo:** experiencia del equipo y preferencia de despliegue (serverless vs contenedor).

### 10.3 Base de datos y storage

**Recomendación:** PostgreSQL (managed: Supabase, Neon o RDS) con patrón pool (shared schema + tenant_id + RLS) para multi-tenancy. Almacenamiento de archivos en S3 (o compatible) con lifecycle policies para temporales y URLs públicas para media de Instagram.

**Justificación:** RLS da aislamiento a nivel de BD (auditable, defendible para SOC 2); JSONB cubre flexibilidad de esquema; el ecosistema de hosting managed es maduro y económico.

**Bloqueo:** región de storage (sa-east-1 vs Chile) y costes de egress (dominante).

### 10.4 Proveedores de IA

**Recomendación:** no se recomienda un proveedor único. Listar OpenAI (GPT Image 2/2.5) y Google (Nano Banana) como candidatos principales, con FLUX/Recraft/Seedream como alternativas de bajo coste. Ejecutar un spike de calidad/coste con los estilos del catálogo antes de decidir.

**Justificación:** los modelos y precios cambian rápidamente (DALL·E e Imagen 4 retirados en 2026); la decisión debe basarse en calidad para los estilos del producto y coste real verificado.

**Bloqueo:** P-012 (proveedores de IA y costes) requiere autorización del usuario.

### 10.5 Publicación en redes

**Recomendación:** implementar Instagram directa con la ruta Instagram Login (más simple, sin Facebook Page) y Advanced Access solo si se sirve a cuentas de terceros; mantener WhatsApp como compartición manual. Preparar fallback a manual si la revisión de Meta falla.

**Justificación:** consistente con las decisiones D-007 y D-008; las APIs soportan esta modalidad.

**Bloqueo:** P-009 (requisitos y permisos de la API de Instagram) requiere validación.

### 10.6 Argentina

**Recomendación:** desplegar en sa-east-1 (São Paulo) para baja latencia; evaluar AWS Chile cuando esté GA. Usar Mercado Pago para pagos web; para in-app, cumplir las políticas de Apple/Google (IAP) salvo que se valide una alternativa. Cumplir Ley 25.326 (consentimiento, registro de bases, seguridad, transferencias).

**Justificación:** sa-east-1 es la región más cercana con catálogo completo; Mercado Pago es el procesador dominante en Argentina.

**Bloqueo:** P-008 (políticas de tiendas en Argentina) y P-015 (validación legal) requieren validación profesional.

---

## 11. Preguntas y bloqueos para el agente principal

1. **Equipo:** ¿Qué experiencia tiene el equipo en JS/TS, React, Python, Dart? Es el factor decisivo para framework móvil y backend.
2. **Presupuesto:** ¿Hay un tope de coste mensual de infraestructura para el MVP? Afecta la elección de planes (Expo, hosting, storage, IA).
3. **Web en roadmap:** ¿Se confirma que habrá web después del MVP? Afecta la elección de framework móvil (compartir código).
4. **IA en cliente:** ¿Se requiere generación de imágenes en el dispositivo? Afecta framework y proveedores.
5. **Streaming:** ¿La generación de textos debe ser streaming en tiempo real al cliente?
6. **Tiering de tenants:** ¿Se prevén clientes enterprise que requieran aislamiento dedicado (silo) en el MVP o solo en fases posteriores?
7. **Pagos:** ¿Se valida con asesoramiento profesional el uso de Mercado Pago para suscripciones in-app en Argentina?
8. **Legal:** ¿Se contrata validación profesional de Ley 25.326 antes del lanzamiento?

---

## 12. Lista de datos marcados como "Hipótesis" o "Pendiente"

### Hipótesis

- H-01: Si el proyecto tendrá web, React Native/Expo comparte más código con React web (pendiente de confirmar roadmap web).
- H-02: El coste dominante será la generación de imágenes (no el texto). Validar con prototipo.
- H-03: La página de pricing de Google Cloud lista Imagen 4 pero los endpoints están descontinuados; verificar disponibilidad real.
- H-04: El ecosistema Python es estructuralmente ventajoso para este producto AI-first (pendiente de validación con el usuario).
- H-05: Mercado Pago puede usarse como alternativa de pago in-app en ciertas jurisdicciones (pendiente de validación profesional).

### Pendiente (requiere investigación o autorización)

- P-001 a P-007, P-009 a P-012, P-015 (de docs/decisions/README.md).
- P-008: políticas de Apple/Google para compra in-app en Argentina.
- P-010: requisitos de WhatsApp para Estados y difusiones (Fase 2).
- P-011: stack tecnológico (este informe es insumo, no decisión).
- Equipo de desarrollo: experiencia y preferencias (desconocido).
- Costes de storage en sa-east-1/Chile (verificar pricing regional).
- Disponibilidad de servicios de IA (Bedrock, etc.) en regiones cercanas a Argentina.
- Proveedores de IA adicionales (Anthropic, Black Forest Labs, Recraft, Seedream, Ideogram) sin fuente oficial verificada.

---

## 13. Fuentes principales (con fecha de consulta 2026-11-27)

- Expo: https://expo.dev/pricing, https://docs.expo.dev/billing/usage-based-pricing
- Meta Instagram: https://developers.facebook.com/docs/instagram-platform/content-publishing, https://developers.facebook.com/documentation/instagram-platform/overview
- WhatsApp: https://faq.whatsapp.com/425247423114725, https://faq.whatsapp.com/669870872481343
- Apple IAP: https://developer.apple.com/help/app-store-connect/configure-in-app-purchase-settings/overview-for-configuring-in-app-purchases, https://developer.apple.com/app-store/review/guidelines
- Google Play Billing: https://support.google.com/googleplay/android-developer/answer/10281818
- Mercado Pago: https://www.mercadopago.com.ar/developers/en/docs/sdks-library/overview
- OpenAI pricing: https://developers.openai.com/api/docs/pricing
- Google Cloud (Imagen): https://cloud.google.com/model-garden/pricing
- AWS S3 pricing: https://aws.amazon.com/s3/pricing
- AWS latency/regiones: https://pingcloud.io/best-region-by-country/2026-07/argentina, https://www.aboutamazon.com/news/aws/aws-south-america-chile-region-launch
- PostgreSQL multi-tenancy: https://docs.aws.amazon.com/prescriptive-guidance/latest/saas-multitenant-managed-postgresql/, https://clickhouse.com/resources/engineering/multi-tenant-saas-postgres-architecture
- Ley 25.326: https://www.argentina.gob.ar/normativa/nacional/64790/actualizacion, https://theargentinethread.com/guide/regulation/data-protection
- FastAPI hosting: https://pandastack.io/blog/best-fastapi-hosting-2026, https://render.com/hosting/fastapi
- Comparativas móvil: https://expo.dev, https://arvucore.com/en/blog/mobile-development-2026-flutter-vs-react-native-vs-native, https://www.pyalm.com/blog/react-native-vs-flutter-vs-native-2026
- Backend comparativas: https://www.marsdevs.com/compare/fastapi-vs-nodejs-for-ai-backends, https://codelli.tech/en/blog/fastapi-vs-nodejs-mvp-2026-en, https://www.ryzlabs.com/guides/nodejs-vs-python-backend

---

## 14. Respuestas del usuario (2026-11-27)

1. **Equipo:** experiencia en Python. (No JS/TS, no Dart, no experiencia móvil nativa.)
2. **Presupuesto:** no definido aún.
3. **Web en roadmap:** no, solo móvil (hipótesis H-01 descartada: no habrá web en el MVP ni después por ahora).

### 14.1 Decisiones autorizadas (2026-11-27)

- **Backend:** FastAPI (Python) — **AUTORIZADO (D-021)**. Ecosistema IA/ML (LangChain, LlamaIndex, HuggingFace). Despliegue en contenedores.
- **Framework móvil:** React Native + Expo (Android e iOS) — **AUTORIZADO (D-022)**. Cloud builds, OTA updates, mayor pool de contratación. El equipo deberá aprender el framework (sin experiencia previa en móvil).
- **Base de datos y storage:** sin cambios (PostgreSQL + RLS + S3, región a definir).
- **Proveedores de IA:** sin cambios (pendiente P-012).
- **Publicación en redes:** sin cambios (Instagram directa sujeta a verificación, WhatsApp manual).
- **Argentina:** sin cambios (sa-east-1, Mercado Pago web, IAP en app, Ley 25.326).

### 14.2 Preguntas que siguen bloqueando la decisión final

1. ¿Se autoriza FastAPI (Python) como backend principal?
2. ¿Se autoriza React Native + Expo como framework móvil (a pesar de que el equipo deberá aprenderlo), o se prefiere Flutter o nativo?
3. ¿Se contrata validación profesional para pagos in-app (P-008) y Ley 25.326 (P-015) antes de lanzar?
4. ¿Se valida con un spike de calidad/coste los proveedores de IA (OpenAI GPT Image 2/2.5 vs Google Nano Banana) antes de decidir?

Estas decisiones requieren autorización explícita del usuario (constitución §3, §4.13).

---
*Fin del informe. Este documento es material de investigación y no constituye una decisión, especificación ni plan aprobado.*