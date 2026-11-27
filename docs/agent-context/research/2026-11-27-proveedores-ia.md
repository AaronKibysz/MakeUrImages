# Investigación de proveedores de IA para generación de imágenes y textos

- **Fecha de creación:** 2026-11-27
- **Autor:** subagente de investigación (encargo de investigación)
- **Estado:** Borrador de investigación (no es una decisión ni una especificación aprobada)
- **Alcance:** Recopilar y comparar proveedores de IA para generación de imágenes y textos, con foco en calidad para estilos de marketing, coste por generación, rate limits, latencia/disponibilidad y viabilidad técnica para el stack autorizado (FastAPI/Python, React Native + Expo, Supabase, Cloudflare R2, sa-east-1). No toma decisiones de proveedor.
- **Fuentes:** documentación oficial de proveedores, páginas de tarifas y guías técnicas (URLs y fechas de consulta al pie de cada dato).
- **Contexto relacionado:** `docs/product/product-definition.md` §4, §6, §16; `docs/decisions/README.md` (D-021 a D-025, P-012); `docs/agent-context/research/2026-11-27-stack-arquitectura.md` §5.

> **Advertencia:** Este informe es material de investigación. Ningún proveedor queda elegido. La decisión de proveedor(es) de IA requiere autorización explícita del usuario (constitución §3, §4.13; P-012). Los precios y límites marcados como "requiere verificación" deben confirmarse antes de tomar decisiones de costes.

---

## 1. Resumen (máximo 10 líneas)

1. OpenAI (GPT Image 2.5 Sunburst/Flare) lidera los benchmarks públicos de calidad (Artificial Analysis Text-to-Image Arena, Elo ~1339 para GPT Image 2) y el rendering de texto; su coste por imagen 1024×1024 va de ~$0,006 (low) a ~$0,211 (max), con Batch API a mitad de precio (Verificado, developers.openai.com, consultado 2026-11-27).
2. Google (Nano Banana 2.1 / 3.1 Flash Image / Pro) ofrece buena calidad a menor coste (~$0,0336 a $0,134 por imagen 1K), con Batch a mitad de precio; Imagen 4 está retirado de Gemini API (17/08/2026) y de Vertex AI (30/06/2026), migración obligatoria a `gemini-2.5-flash-image` (Verificado, ai.google.dev, cloud.google.com).
3. Anthropic (Claude) no genera imágenes; es candidato para textos de marketing. Claude Haiku 5.5 ($0,10/$0,50 por MTok) y Sonnet 5.5 ($2/$10) cubren generación de textos cortos a coste bajo; Batch API con 50 % de descuento (Verificado, platform.claude.com, consultado 2026-11-27).
4. Alternativas de bajo coste con API propia: Black Forest Labs FLUX.2 (klein desde ~$0,014/MP, pro desde ~$0,03, max ~$0,07), Recraft (V4.1 Flash $0,007, V4.1 $0,035), Seedream (BytePlus: 4.0 $0,03, 4.5 $0,04, 5.5 $0,02 por 1K), Ideogram (P-Image Very Low $0,003, 4.5 Low $0,03) (Verificado parcialmente, fuentes oficiales por proveedor).
5. Texto en imagen es el diferenciador clave para marketing; Ideogram (OCR ~0,97) y Recraft destacan en tipografía, GPT Image en instrucción compleja (Verificado, benchmarks públicos Artificial Analysis y comparativas 2026).
6. Integración con FastAPI/Python es directa: SDKs oficiales async (`AsyncOpenAI`, `client.aio` en google-genai, `AsyncAnthropic`), compatibles con colas (Celery/RQ/Dramatiq/ARQ) mediante jobs en background (Verificado, docs oficiales).
7. Generación es asíncrona por naturaleza (5–30 s por imagen); el backend debe encolar jobs y notificar al cliente; rate limits por tier (OpenAI 5–250 IPM según tier; Google por cuota de proyecto) (Verificado, fuentes oficiales).
8. Coste dominante es la imagen, no el texto: ~$0,01–$0,05 por imagen "media" vs ~$0,0003–$0,005 por texto de 500 tokens (Hipótesis H-02, confirmada parcialmente por los cálculos).
9. Moderación: OpenAI y Google aplican filtros de seguridad; datos de entrenamiento y retención varían; compliance Ley 25.326 requiere validación profesional (P-015) (Verificado parcialmente).
10. Recomendación: no elegir un único proveedor todavía; ejecutar un spike de calidad/coste con 3–5 estilos del catálogo y 2–3 proveedores (OpenAI GPT Image 2.5 + Google Nano Banana 2.1 + uno de bajo coste) antes de decidir (P-012).

---

## 2. OpenAI — generación de imágenes

### 2.1 Modelos vigentes (consultado 2026-11-27)

Fuente: `developers.openai.com/api/docs/pricing` y `developers.openai.com/api/docs/deprecations`.

| Modelo | Estado | Notas |
|---|---|---|
| `gpt-image-2.6-sunburst` | Activo (vigente nov 2026) | Calidad alta, mayor latencia; recomendado como reemplazo de modelos retirados. |
| `gpt-image-2.6-flare` | Activo (vigente nov 2026) | Más rápido, menor latencia. |
| `gpt-image-2.5-sunburst` / `-flare` | Activo | Versiones anteriores; mismas tarifas por token. |
| `gpt-image-2` | Deprecated (shutdown 10/02/2027) | Reemplazo: 2.6 Sunburst/Flare. |
| `gpt-image-1.5` | Deprecated (shutdown 01/12/2026) | — |
| `gpt-image-1-mini` | Deprecated (shutdown 01/12/2026) | Más barato pero retiro inminente. |
| `chatgpt-image-latest` | Deprecated (shutdown 01/12/2026) | — |
| `gpt-image-1` | Retirado (23/10/2026) | — |
| `dall-e-2`, `dall-e-3` | Retirados (12/05/2026) | — |

### 2.2 Tarifas (USD por 1M de tokens, consultado 2026-11-27)

Fuente: `developers.openai.com/api/docs/pricing` (sección "Multimodal models → Images").

| Modelo | Text input | Image input | Image output | Cached image input |
|---|---|---|---|---|
| `gpt-image-2.5/2.6` Sunburst/Flare | $5,00 | $8,00 | $30,00 | $2,00 |
| `gpt-image-2` | $5,00 | $8,00 | $30,00 | $2,00 |
| `gpt-image-1.5` | $5,00 | $8,00 | $32,00 | $2,00 |
| `gpt-image-1-mini` | $2,00 | $2,50 | $8,00 | $0,25 |

**Batch API:** mitad de precio (image input $4,00 / 1M, image output $15,00 / 1M). Fuente: misma página de pricing, sección Batch.

**Coste por imagen (GPT Image 2.5, 1024×1024):** ~$0,0059 (low), ~$0,0132 (medium), ~$0,0527 (high), ~$0,0937 (xhigh), ~$0,2107 (max). Fuente: `toolcolumn.com/learn/gpt-image-api-pricing`, verificado contra la calculadora oficial de OpenAI (consultado 2026-11-27).

### 2.3 Rate limits (consultado 2026-11-27)

Fuente: páginas de modelo en `developers.openai.com` (Flare/Sunburst), citadas por `atlascloud.ai/blog/tips/gpt-image-2.5-rate-limits`.

| Tier de uso | TPM (tokens/min) | IPM (imágenes/min) |
|---|---|---|
| Free | No soportado | No soportado |
| Tier 1 | 100.000 | 5 |
| Tier 2 | 250.000 | 20 |
| Tier 3 | 800.000 | 50 |
| Tier 4 | 3.000.000 | 150 |
| Tier 5 | 8.000.000 | 250 |

Aviso: estos límites son por organización y se aplican a la familia GPT Image; verificar el tier real del proyecto en la consola de OpenAI antes de presupuestar.

### 2.4 Latencia, regiones y disponibilidad

- API global (sin región seleccionable por el cliente para inferencia de imágenes). No hay endpoint regional en sa-east-1. Latencia desde Argentina depende de la ruta a los endpoints de OpenAI (típicamente US); impacto en la UX se mitiga con generación asíncrona (jobs en background).
- Latencia de generación reportada: hasta 50 % menor en GPT Image 2.5 vs Images 2.0 (fuente: `openai.com/index/introducing-chatgpt-images-2-5`, consultado 2026-11-27). Tiempos típicos de 5–30 s por imagen según calidad y resolución (Hipótesis, requiere medición real).
- SLA: OpenAI publica status en `status.openai.com`. No se encontró SLA formal con porcentaje de uptime en la documentación consultada (Pendiente).

### 2.5 Moderación y datos

- Filtros de seguridad integrados (bloqueo de contenido sexual, violencia, etc.) configurables por parámetros de la API.
- Datos de entrada/salida no se usan para entrenamiento por defecto en la API (según términos de OpenAI API). Requiere verificación legal para Ley 25.326 (P-015).

---

## 3. Google — generación de imágenes

### 3.1 Modelos vigentes (consultado 2026-11-27)

Fuente: `ai.google.dev/gemini-api/docs/models` y `ai.google.dev/gemini-api/docs/pricing`.

| Modelo (ID de API) | Nombre comercial | Estado | Calidad/velocidad |
|---|---|---|---|
| `gemini-2.5-flash-image` | Nano Banana | Activo | Rápido, bajo coste |
| `gemini-nano-banana-2.1` | Nano Banana 2.1 | Activo (oct 2026) | ~50 % más barato que Nano Banana 2 en 1K/2K |
| `gemini-3.1-flash-image` | Nano Banana 2 | Activo | Balance calidad/coste |
| `gemini-3-pro-image` | Nano Banana Pro | Activo | Calidad alta, textos largos, 2K/4K |
| `imagen-4.0-generate-001` | Imagen 4 | **Retirado** (Gemini API 17/08/2026; Vertex 30/06/2026) | Migrar a `gemini-2.5-flash-image` |
| `imagen-4.0-fast-generate-001` | Imagen 4 Fast | **Retirado** | Idem |
| `imagen-4.0-ultra-generate-001` | Imagen 4 Ultra | **Retirado** | Idem |

### 3.2 Tarifas (consultado 2026-11-27)

Fuente: `ai.google.dev/gemini-api/docs/pricing` (página oficial de pricing de Gemini API).

| Modelo | Input (USD/1M) | Output imagen (USD/1M) | Equiv. por imagen 1K (1024×1024) | Batch |
|---|---|---|---|---|
| Nano Banana (`gemini-2.5-flash-image`) | $0,30 (texto/imagen) | $30,00 | $0,039 (standard) | $0,0195 |
| Nano Banana 2.1 (`gemini-nano-banana-2.1`) | $1,50 (texto/imagen/video) | $30,00 | $0,0336 (1K), $0,0504 (2K), $0,113 (4K) | $0,0168 / $0,0252 / $0,0565 |
| Nano Banana 2 (`gemini-3.1-flash-image`) | — | $60,00 | $0,067 (1K), $0,101 (2K), $0,151 (4K) | — |
| Nano Banana Pro (`gemini-3-pro-image`) | $2,00 | $120,00 | $0,134 (1K/2K), $0,24 (4K) | $0,067 (1K/2K) |

Aviso: las tarifas de Google se expresan por token de salida de imagen; el coste "por imagen" es equivalente calculado por el proveedor para resoluciones estándar. Batch API de Google aplica descuento del 50 % sobre output de imagen (Verificado, ai.google.dev, consultado 2026-11-27).

### 3.3 Vertex AI vs Gemini API

- **Gemini API** (`ai.google.dev` / `generativelanguage.googleapis.com`): más simple, facturación por uso, sin proyecto GCP obligatorio. Recomendado para MVP.
- **Vertex AI** (`cloud.google.com/vertex-ai`): proyecto GCP, IAM, VPC, compliance empresarial, Provisioned Throughput. Mayor complejidad operativa. Imagen 4 endpoints retirados con migración a `gemini-2.5-flash-image` antes del 30/06/2026 (Verificado, cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-generate, consultado 2026-11-27).
- Para Argentina/sa-east-1: Gemini API es global; no hay endpoint regional en São Paulo para inferencia de imágenes (Hipótesis: latencia similar a OpenAI, mitigar con async).

### 3.4 SDK y rate limits

- SDK oficial: `google-genai` (Python), con cliente async vía `client.aio` (Verificado, googleapis.github.io/python-genai).
- Rate limits: cuotas por proyecto en Google Cloud Console; valores por defecto varían por modelo y región. No hay tabla fija publicada equivalente a la de OpenAI (Pendiente: verificar cuotas reales al crear el proyecto).

---

## 4. Anthropic — generación de textos

Anthropic no ofrece generación de imágenes. Es candidato para la generación de textos de marketing (títulos, descripciones, hashtags, CTAs) y para clasificación/validación de información factual (P-007).

### 4.1 Modelos vigentes (consultado 2026-11-27)

Fuente: `platform.claude.com/docs/en/about-claude/pricing`.

| Modelo | Input (USD/MTok) | Output (USD/MTok) | Contexto | Notas |
|---|---|---|---|---|
| Claude Fable 5.2 | $8,00 | $40,00 | 1M | Mayor capacidad; acceso limitado. |
| Claude Mythos 5.2 | $8,00 | $40,00 | 1M | Acceso limitado. |
| Claude Opus 5.5 | $4,00 | $20,00 | 1M | Razonamiento complejo. |
| Claude Sonnet 5.5 | $2,00 | $10,00 | 1M | Balance calidad/coste. |
| Claude Haiku 5.5 | $0,10 (≤100k) / $0,50 (>100k) | $0,50 (≤100k) / $2,50 (>100k) | 1M | Más barato; ideal para textos cortos. |
| Claude Sonnet 4.6 | $3,00 | $15,00 | 1M | — |
| Claude Haiku 4.5 | $1,00 | $5,00 | 1M | — |

### 4.2 Descuentos y caché

- **Batch API:** 50 % de descuento en input y output (Verificado, platform.claude.com).
- **Prompt caching:** cache read a 0,05x–0,1x del precio base según modelo; cache write 1,25x (5 min) o 2x (1 h). Útil para prompts de sistema largos reutilizados (Verificado).
- **Fast mode:** hasta 2,5x más tokens/s de salida a precio premium (solo Opus/Fable). Probablemente no necesario para MVP.
- **Rate limits:** por tier (Start/Build/Scale); valores detallados en `platform.claude.com/docs/en/api/rate-limits` (Pendiente: verificar límites concretos por tier).

### 4.3 SDK y async

- SDK oficial `anthropic` (Python), con `AsyncAnthropic` y soporte aiohttp (`pip install "anthropic[aiohttp]"`) (Verificado, platform.claude.com/docs/en/cli-sdks-libraries/sdks/python).

---

## 5. Alternativas de bajo coste (imagen)

### 5.1 Black Forest Labs — FLUX.2

Fuente: `bfl.ai/pricing` (calculadora interactiva) y `docs.bfl.ml/quick_start/pricing` (consultado 2026-11-27). Pricing megapixel-based (coste escala con resolución de salida).

| Modelo | Text-to-Image (desde) | Image Editing (desde) | Mejor para |
|---|---|---|---|
| FLUX.2 [klein] 4B | ~$0,014/MP | ~$0,015/MP | Alto volumen, tiempo real |
| FLUX.2 [klein] 9B | ~$0,015/MP | ~$0,017/MP | Balance calidad/velocidad |
| FLUX.2 [pro] | ~$0,03/MP | ~$0,045/MP | Producción, turnaround rápido |
| FLUX.2 [max] | ~$0,07/MP | ~$0,10/MP | Máxima calidad, grounding search |
| FLUX.2 [flex] | ~$0,05/MP | ~$0,10/MP | Control fino, tipografía |
| FLUX.2 [dev] | Solo local (open weights) | Solo local | Self-hosted, no comercial |

Aviso: los precios "desde" son por megapíxel de salida; una imagen 1024×1024 (~1 MP) cuesta aproximadamente el precio "desde". Los valores exactos requieren la calculadora interactiva de bfl.ai (JS). Verificado contra `developersdigest.tech/models/image-generation/black-forest-labs` (consultado 2026-11-27). Marcar como Hipótesis hasta confirmar con la calculadora oficial.

También ofrece FLUX 3 Image: $0,041 (768×768) a $0,607 (4K); FLUX 3 Image Klein: $0,008 (768×768) a $0,036 (4K). Fuente: `bfl.ai/pricing`.

### 5.2 Recraft

Fuente: `recraft.ai/docs/api-reference/pricing` y `recraft.ai/pricing?tab=api` (consultado 2026-11-27). $1 = 1.000 API units.

| Modelo/operación | Precio (USD) | API units |
|---|---|---|
| V4.1 Flash | $0,007 | 7 |
| V4.1 / V4.1 Utility | $0,035 | 35 |
| V4.1 Vector | $0,08 | 80 |
| V4.1 Pro | $0,21 | 210 |
| V4.1 Pro Vector | $0,30 | 300 |
| V4 Styles | $0,035 | 35 |
| V4 Styles Pro | $0,10 | 100 |
| V4 Styles Pro Vector | $0,12 | 120 |
| V4 (raster) | $0,04 | 40 |
| V4 Pro | $0,25 | 250 |
| V4 Pro Vector | $0,30 | 300 |
| Inpainting / Replace bg / Generate bg | $0,04 | 40 |
| Vectorization / Background removal | $0,01 | 10 |
| Crisp upscale | $0,004 | 4 |
| Creative upscale | $0,25 | 250 |
| Erase region | $0,002 | 2 |

SDK: API REST OpenAI-compatible (`external.api.recraft.ai/v1`), usable con el SDK de OpenAI cambiando `base_url`. Soporta generación vectorial (SVG), útil para logotipos.

### 5.3 Seedream (BytePlus / Volcengine)

Fuente: `docs.byteplus.com/en/docs/modelark/model-pricing` y `byteplus.com` (consultado 2026-11-27). Precios por imagen en la ModelArk.

| Modelo | Precio por imagen | Notas |
|---|---|---|
| `seedream-4-0-250828` | $0,03 (output), input gratis | — |
| `seedream-4-5-251128` | $0,04 (output), input gratis | — |
| `dola-seedream-5-5-261028` | $0,020 (1K/1.5K), $0,035 (2K/custom), $0,079 (hasta 4K); input $0,008 por imagen de referencia | Precios por tamaño de salida |
| `seededit-3-0-i2i-250628` | $0,03 | Edición imagen-a-imagen |

También ofrece packs de primera compra: desde $0,01/imagen (700/1.800/3.500 imágenes, válidos 30 días) (fuente: `myclaw.ai/blog/seedream-5-5-review`, consultado 2026-11-27). Marcar como Hipótesis: verificar disponibilidad actual de los packs en la consola de BytePlus.

### 5.4 Ideogram

Fuente: `ideogram.ai/pricing/` (consultado 2026-11-27). Facturación por imagen generada, por velocidad de render y tamaño de salida.

| Modelo / velocidad | 1K | 2K | 4K |
|---|---|---|---|
| Ideogram 4.6 Generate Very Low | $0,008 | $0,008 | — |
| Ideogram 4.6 Generate Low | $0,03 | $0,03 | $0,06 |
| Ideogram 4.6 Generate Medium | $0,06 | $0,06 | $0,12 |
| Ideogram 4.6 Generate High | $0,10 | $0,10 | $0,20 |
| Ideogram 4.5 Generate Low | $0,03 | $0,03 | — |
| Ideogram 4.5 Generate Medium | $0,06 | $0,06 | — |
| Ideogram 4.5 Generate High | $0,10 | $0,10 | — |
| Ideogram 4.0 Turbo / Default / Quality | $0,03 / $0,06 / $0,10 | — | — |
| Ideogram 3.0 Flash / Turbo / Default / Quality | $0,03 / $0,03 / $0,06 / $0,09 | — | — |
| P-Image Very Low / Low / Medium / High / Very High | $0,003 / $0,0075 / $0,01 / $0,015 / $0,033 | $0,006 / $0,015 / $0,02 / $0,03 / $0,066 | — |
| Precise Edit (Very Low / Low / Medium / High) | $0,008 / $0,03 / $0,06 / $0,22 | — | — |

También vende Nano Banana 2/Pro a través de su API ($0,0672–$0,24), es decir, reventa de Google con markup. Ideogram destaca en rendering de texto (OCR ~0,97) y control de layout (JSON con bounding boxes, color hex).

### 5.5 Otros candidatos (no verificados con fuente oficial)

- **Stability AI (SD 3.5, SDXL):** listado en comparativas; precios por imagen variables. No verificado en esta investigación (Pendiente).
- **Microsoft MAI-Image-2.6:** aparece en benchmarks (Elo ~1149) pero disponibilidad de API pública y precios no verificados (Pendiente).
- **xAI Grok Imagine:** aparece en comparativas; API pública y precios no verificados (Pendiente).
- **Alibaba Qwen Image:** open-weights; hosting propio o vía proveedores (fal, etc.). No verificado (Pendiente).

---

## 6. Comparativa de calidad (benchmarks públicos)

Fuentes: Artificial Analysis Text-to-Image Arena/Leaderboard (`artificialanalysis.ai/image/leaderboard/text-to-image`), comparativas de fal.ai, Recraft blog, alphacorp.ai (consultado 2026-11-27). Metodología: comparaciones ciegas (Elo) + benchmarks de rendering de texto.

| Modelo | Elo (AA, jun-nov 2026) | Fortaleza principal | Debilidad |
|---|---|---|---|
| GPT Image 2 / 2.5 (OpenAI) | ~1339 (GPT Image 2) | Instrucción compleja, texto en imagen (Latin/CJK), fotorealismo | Rango estético limitado; coste alto en alta calidad |
| Nano Banana Pro (Google) | ~1219 | Texto largo, composición, razonamiento | Coste mayor que Nano Banana 2 |
| Nano Banana 2 (Google) | ~1255 | Balance calidad/coste, texto | — |
| FLUX.2 [max] (BFL) | ~1192 | Fotorealismo, consistencia | Texto menos robusto que Ideogram |
| Seedream 5.0 Lite (ByteDance) | ~1116 (top-9) | Fotoreal, alta resolución nativa | — |
| Ideogram 4.0 | (OCR ~0,97) | Texto en imagen, logos, signage, layout JSON | Techo estético por debajo de los generalistas |
| Recraft V4.1 Utility Pro | (top fuera de Google/OpenAI en algunos leaderboards) | Estética, brief-driven, vector (SVG) | — |

Avisos importantes:
- Los scores Elo de Artificial Analysis y Arena usan metodologías distintas; no comparar directamente entre fuentes (Verificado, gate.ai, consultado 2026-11-27).
- El Elo mide preferencia promedio, no el caso de uso específico (marketing con estilos). Requiere spike con los estilos reales del catálogo (Hipótesis H-06).
- No existe benchmark público específico para "estilos de marketing con identidad de marca"; la calidad real solo se mide con el spike propuesto (ver §12).

---

## 7. Integración con FastAPI/Python

### 7.1 SDKs oficiales y async

| Proveedor | Paquete | Cliente async | Notas |
|---|---|---|---|
| OpenAI | `openai` | `AsyncOpenAI` (httpx/aiohttp) | `pip install openai` o `openai[aiohttp]`. Soporta imágenes (`client.images.generate` / Responses API). |
| Google | `google-genai` | `client.aio` (aiohttp opcional) | `pip install google-genai`. Async: `await client.aio.models.generate_content` / `generate_images`. |
| Anthropic | `anthropic` | `AsyncAnthropic` (aiohttp) | `pip install "anthropic[aiohttp]"`. |

Verificado: `developers.openai.com/api/reference/python` (Async usage), `googleapis.github.io/python-genai` (aio client), `platform.claude.com/docs/en/cli-sdks-libraries/sdks/python` (consultado 2026-11-27).

### 7.2 Compatibilidad con colas (Celery/RQ/Dramatiq/ARQ)

- La generación de imágenes es bloqueante (5–30 s) y debe ejecutarse en workers de fondo, no en el request HTTP de FastAPI.
- Los SDKs async son compatibles con cualquier cola: el worker llama al SDK async dentro de un event loop, o usa el cliente sync en un worker thread/process.
- Recomendación de la literatura (no decisión): ARQ (async Redis queue) o Celery con workers async; Dramatiq para simplicidad. La elección de cola es una decisión pendiente (P-011/stack) y no se resuelve aquí.
- Reintentos: los SDKs exponen excepciones tipadas (`RateLimitError`, `APIError`, `Timeout`) para implementar backoff exponencial + jitter.
- Streaming: Anthropic/OpenAI soportan streaming de texto; para imágenes no hay streaming de bytes progresivos en la API estándar (se recibe la imagen completa al finalizar).

### 7.3 Manejo de errores y rate limiting

- Implementar rate limiter propio (token bucket) por proveedor + retry con backoff.
- Idempotencia: guardar `request_id`/`job_id` para evitar doble facturación en reintentos.
- Fallback: si un proveedor falla o alcanza límite, encolar reintento o cambiar de proveedor (requiere abstracción de proveedor en el backend; decisión de arquitectura pendiente).

---

## 8. Latencia y disponibilidad

| Proveedor | Tiempo típico por imagen | Región del endpoint | SLA/Uptime publicado |
|---|---|---|---|
| OpenAI GPT Image 2.5 | 5–30 s (según calidad/resolución) (Hipótesis) | Global (US) | Status page; sin SLA formal encontrado (Pendiente) |
| Google Nano Banana 2.1/2/Pro | 3–20 s (Hipótesis) | Global | Status page; sin SLA formal encontrado (Pendiente) |
| FLUX.2 (BFL) | 2–15 s (Hipótesis) | Global (EU/US) | Status page (status.bfl.ai) |
| Recraft | 3–15 s (Hipótesis) | Global | No verificado (Pendiente) |
| Seedream (BytePlus) | 3–15 s (Hipótesis) | Global (Asia/US) | No verificado (Pendiente) |
| Ideogram | 3–20 s (Hipótesis) | Global | No verificado (Pendiente) |

Implicaciones para el producto:
- La generación debe ser asíncrona: el cliente envía el job, el backend procesa en worker, notifica por polling/WebSocket/push.
- El tiempo de espera percibido se mitiga con previews de baja calidad o spinners; no bloquear el request HTTP.
- Región sa-east-1 (São Paulo) es la más cercana a Argentina (~30–40 ms) pero los proveedores de IA son globales (US/EU); la latencia de red se suma al tiempo de generación (Verificado, stack-arquitectura §7.1).

---

## 9. Coste por generación (estimación)

### 9.1 Imagen (1024×1024, calidad media/estándar)

| Proveedor / modelo | Coste por imagen (USD) | Batch (USD) | Notas |
|---|---|---|---|
| OpenAI GPT Image 2.5 (medium) | ~$0,0132 | ~$0,0066 | Low $0,0059; high $0,0527; max $0,2107 |
| OpenAI GPT Image 2.5 (low) | ~$0,0059 | ~$0,0029 | Para previews/borradores |
| Google Nano Banana (2.5 Flash Image) | $0,039 | $0,0195 | — |
| Google Nano Banana 2.1 (1K) | $0,0336 | $0,0168 | — |
| Google Nano Banana 2 (1K) | $0,067 | — | — |
| Google Nano Banana Pro (1K) | $0,134 | $0,067 | — |
| BFL FLUX.2 [klein] 4B (~1 MP) | ~$0,014 | — | Megapixel-based |
| BFL FLUX.2 [pro] (~1 MP) | ~$0,03 | — | — |
| BFL FLUX.2 [max] (~1 MP) | ~$0,07 | — | — |
| BFL FLUX.2 [flex] (~1 MP) | ~$0,05 | — | — |
| Recraft V4.1 Flash | $0,007 | — | — |
| Recraft V4.1 | $0,035 | — | — |
| Recraft V4.1 Pro | $0,21 | — | — |
| Seedream 4.0 | $0,03 | — | — |
| Seedream 4.5 | $0,04 | — | — |
| Seedream 5.5 (1K) | $0,020 | — | Input ref $0,008 |
| Ideogram P-Image Very Low (1K) | $0,003 | — | — |
| Ideogram 4.5 Low (1K/2K) | $0,03 | — | — |
| Ideogram 4.5 Medium | $0,06 | — | — |
| Ideogram 4.5 High | $0,10 | — | — |

### 9.2 Texto (500 tokens de salida, ~1.000 tokens de entrada)

| Proveedor / modelo | Coste por generación (USD) | Batch |
|---|---|---|
| Claude Haiku 5.5 (≤100k) | ~$0,00035 (input $0,0001 + output $0,00025) | ~$0,00018 |
| Claude Sonnet 5.5 | ~$0,0052 (input $0,002 + output $0,005) | ~$0,0026 |
| Claude Opus 5.5 | ~$0,0104 (input $0,004 + output $0,01) | ~$0,0052 |
| OpenAI gpt-6-luna | ~$0,00035 | — |
| OpenAI gpt-6.1-terra | ~$0,0026 | — |
| Google Gemini (Flash) | ~$0,0001–$0,001 (Hipótesis, no verificado en esta ronda) | — |

### 9.3 Hipótesis de coste por crédito del producto (Pendiente)

El producto usa créditos por generación (precios y cantidades pendientes, P-001/P-002). Hipótesis de trabajo (a validar con el spike y la decisión de precios):
- Si una generación "media" cuesta ~$0,01–$0,05 al proveedor (imagen) + ~$0,001 (texto), el coste marginal por generación se sitúa en ese rango.
- El margen bruto depende del precio del crédito, que está pendiente de decisión del usuario (no se puede fijar aquí).
- Batch API (OpenAI/Google/Anthropic) permite reducir coste a la mitad para generaciones no urgentes (ej. pre-generación de variantes en background), pero añade latencia (hasta 24 h). Útil para planes con mayor volumen.

---

## 10. Moderación y seguridad

### 10.1 Políticas de contenido

- **OpenAI:** filtros de seguridad configurables (moderation endpoint gratuito para texto); bloqueo de CSAM, violencia gráfica, etc. Términos de uso de la API prohíben generar contenido sexual explícito, odio, etc. Fuente: `developers.openai.com/api/docs/guides/moderation` (consultado 2026-11-27).
- **Google:** filtros de seguridad por categoría (harassment, hate speech, sexually explicit, dangerous content) con umbrales configurables; watermarking (SynthID) en imágenes generadas. Fuente: `ai.google.dev/gemini-api/docs/safety-settings` (consultado 2026-11-27).
- **Anthropic:** políticas de uso (Usage Policy) con restricciones; filtros integrados. Fuente: `anthropic.com/legal/aup` (consultado 2026-11-27).
- **Ideogram/Recraft/BFL/Seedream:** políticas propias; verificar términos antes de integrar (Pendiente).

### 10.2 Datos de entrenamiento y retención

- OpenAI API: por defecto los datos de la API no se usan para entrenar modelos (según términos de la API). Retención de logs limitada (30 días por defecto para debugging). Fuente: `openai.com/enterprise-privacy` (consultado 2026-11-27).
- Google Gemini API: datos de la API no se usan para entrenar por defecto en el tier pago; el tier gratuito puede usar datos para mejorar productos (Verificado, ai.google.dev pricing: "Used to improve our products: Yes (Free) / No (Paid)").
- Anthropic: datos de la API no se usan para entrenamiento por defecto (según términos). Fuente: `anthropic.com/legal/privacy` (consultado 2026-11-27).
- Requiere validación legal (P-015) para confirmar transferencias internacionales (datos a proveedores en US) y obligaciones de la Ley 25.326 (consentimiento, inscripción de bases ante la AAIP, seguridad).

### 10.3 Watermarking / C2PA

- Google (Imagen/Nano Banana) incluye SynthID (marca de agua invisible) en imágenes generadas (Verificado, ai.google.dev).
- OpenAI: C2PA metadata en imágenes generadas por GPT Image (Verificado, openai.com).
- Relevante para transparencia y compliance; no afecta al MVP funcionalmente.

---

## 11. Recomendación (no decisión)

> Esta sección es una recomendación del subagente de investigación, no una decisión. Requiere autorización explícita del usuario (constitución §3, §4.13; P-012).

**Recomendación:** No elegir un único proveedor en esta etapa. Estructurar el backend con una abstracción de proveedor de imágenes (adapter pattern) y ejecutar un spike de calidad/coste con 2–3 proveedores antes de decidir.

**Justificación:**
1. La calidad para los estilos de marketing del producto no se puede inferir solo de benchmarks genéricos; los estilos visuales del catálogo (6–8) son el insumo real (P-003 pendiente).
2. Los precios y modelos cambian rápidamente (DALL·E e Imagen 4 retirados en 2026; GPT Image 2 retiro en feb 2027). Una abstracción mitiga el riesgo de lock-in.
3. El coste por imagen varía un orden de magnitud entre proveedores ($0,003 a $0,21); el spike medirá calidad real vs coste para el caso de uso.

**Candidatos sugeridos para el spike (2–3):**
- **OpenAI GPT Image 2.5** (Sunburst para calidad, Flare para velocidad) — líder en benchmarks y texto.
- **Google Nano Banana 2.1** — mejor relación calidad/coste en 1K.
- **Uno de bajo coste:** Recraft V4.1 Flash ($0,007) o Ideogram P-Image Very Low ($0,003) o Seedream 5.5 ($0,020) — para validar si la calidad es suficiente para estilos de marketing a coste mínimo.

**Para textos:** Claude Haiku 5.5 (coste mínimo) o Sonnet 5.5 (mejor calidad) según el tipo de texto (factual vs creativo). Considerar OpenAI gpt-6-luna para unificar proveedor si se elige OpenAI para imágenes.

**Bloqueos:** P-012 (proveedores de IA y costes), P-003 (estilos), P-007 (validación de información factual), P-015 (validación legal).

---

## 12. Spike de calidad propuesto (no ejecutar en esta investigación)

**Objetivo:** medir calidad real y coste por proveedor para los estilos del producto.

**Diseño sugerido:**
- **Estilos:** 3–5 de los 6–8 del catálogo (una vez definidos, P-003). Si no están definidos, usar 3 estilos representativos: fotográfico inmobiliario, ilustración gastronómica, minimalista corporativo.
- **Proveedores:** 2–3 (OpenAI GPT Image 2.5, Google Nano Banana 2.1, + uno de bajo coste).
- **Prompts:** 10–20 prompts por estilo, con y sin texto en imagen, en formatos 1:1 y 9:16.
- **Métricas:** evaluación humana (cegada) de calidad estética, legibilidad del texto, adherencia al prompt, tiempo de generación, coste real medido.
- **Entregable:** tabla de calidad vs coste + recomendación de proveedor(es) primario/secundario + estimación de coste mensual por volumen.

**Condición de finalización del spike:** resultados documentados en un informe separado y decisión del usuario (P-012).

---

## 13. Preguntas y bloqueos para el agente principal

1. **Estilos (P-003):** sin nombres/descripciones de los 6–8 estilos, el spike no puede ejecutarse con fidelidad. ¿Se definen antes del spike?
2. **Volumen esperado:** ¿cuántas generaciones por mes se estiman en el MVP? Afecta la elección de Batch API y el tier de rate limits.
3. **Calidad vs coste:** ¿el producto compite por calidad (estética premium) o por precio (volumen alto)? Define si se prioriza GPT Image 2.5 o FLUX/Recraft.
4. **Texto en imagen:** ¿los estilos requieren texto legible dentro de la imagen (precios, teléfonos)? Si sí, Ideogram/Recraft/OpenAI ganan; si no, Nano Banana/FLUX son suficientes.
5. **Unificación de proveedor:** ¿se prefiere un único proveedor para imagen+texto (OpenAI) o mejor calidad por separado (OpenAI imagen + Claude texto)?
6. **Compliance (P-015):** ¿se valida con asesoramiento profesional el uso de proveedores en US para datos de usuarios argentinos antes de integrar?

---

## 14. Lista de datos marcados como "Hipótesis" o "Pendiente"

### Hipótesis

- H-01: Latencia típica de generación de 5–30 s por imagen según proveedor/calidad/resolución. Requiere medición real en el spike.
- H-02: El coste dominante es la generación de imágenes (no el texto). Confirmado parcialmente por los cálculos de §9 (imagen ~$0,01–$0,05 vs texto ~$0,0003–$0,005).
- H-03: Los precios "desde" de FLUX.2 (bfl.ai) son megapixel-based y requieren la calculadora interactiva para valores exactos (la página es JS-driven).
- H-04: Disponibilidad de packs de primera compra de Seedream ($0,01/imagen) requiere verificación en la consola de BytePlus.
- H-05: Google Gemini API no tiene endpoint regional en sa-east-1 para inferencia de imágenes (latencia global).
- H-06: La calidad para estilos de marketing no se puede inferir de benchmarks genéricos; requiere spike con estilos reales.
- H-07: OpenAI API no usa datos de la API para entrenamiento por defecto; retención de 30 días. Requiere verificación legal (P-015).
- H-08: Los rate limits de OpenAI (5–250 IPM) aplican a la familia GPT Image; verificar tier real del proyecto.

### Pendiente (requiere investigación o autorización)

- P-001: Precios, cantidades y límites de planes (bloquea modelo comercial).
- P-002: Créditos de bienvenida.
- P-003: Nombres/descripciones de los 6–8 estilos (bloquea spike).
- P-007: Mecanismo de validación de información factual (afecta generación de textos).
- P-012: Selección de proveedor(es) de IA (requiere autorización del usuario).
- P-015: Validación legal (Ley 25.326).
- SLA formal de OpenAI/Google (uptime %) — no encontrado en documentación consultada.
- Cuotas de rate limit de Google Gemini API por proyecto (verificar al crear el proyecto).
- Precios de Stability AI, xAI Grok Imagine, Microsoft MAI-Image, Alibaba Qwen Image (no verificados).
- Disponibilidad de Imagen 4 en Vertex AI tras 30/06/2026 (documentación indica retirado; verificar en consola).
- Elección de cola de tareas (Celery/RQ/Dramatiq/ARQ) — decisión de stack pendiente.

---

## 15. Fuentes principales (con fecha de consulta 2026-11-27)

**OpenAI:**
- Pricing: https://developers.openai.com/api/docs/pricing
- Deprecations: https://developers.openai.com/api/docs/deprecations
- Rate limits / modelos: https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst , https://developers.openai.com/api/docs/models/gpt-image-2.5-flare
- SDK Python (async): https://developers.openai.com/api/reference/python
- Moderation: https://developers.openai.com/api/docs/guides/moderation

**Google:**
- Pricing Gemini API: https://ai.google.dev/gemini-api/docs/pricing
- Modelos: https://ai.google.dev/gemini-api/docs/models , https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image
- Imagen (Vertex): https://cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-generate
- SDK Python (async): https://googleapis.github.io/python-genai/
- Safety settings: https://ai.google.dev/gemini-api/docs/safety-settings

**Anthropic:**
- Pricing: https://platform.claude.com/docs/en/about-claude/pricing
- SDK Python: https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python
- Rate limits: https://platform.claude.com/docs/en/api/rate-limits
- Usage policy: https://www.anthropic.com/legal/aup

**Alternativas:**
- Black Forest Labs pricing: https://bfl.ai/pricing , https://docs.bfl.ml/quick_start/pricing
- Recraft pricing: https://www.recraft.ai/pricing?tab=api , https://www.recraft.ai/docs/api-reference/pricing
- BytePlus ModelArk pricing: https://docs.byteplus.com/en/docs/modelark/model-pricing
- Ideogram pricing: https://ideogram.ai/pricing/

**Benchmarks y comparativas:**
- Artificial Analysis Text-to-Image Leaderboard: https://artificialanalysis.ai/image/leaderboard/text-to-image
- Artificial Analysis methodology: https://artificialanalysis.ai/methodology/image
- fal.ai best text-to-image APIs 2026: https://fal.ai/learn/tools/best-text-to-image-apis-2026
- Recraft blog (comparativa APIs): https://www.recraft.ai/blog/best-ai-image-generation-api
- gate.ai (modelos 2026): https://gate.ai/blog/best-ai-image-generation-models-in-2026-quality-cost
- alphacorp.ai (top 10): https://alphacorp.ai/blog/top-ai-image-models-2026
- developersdigest.tech (pricing por proveedor): https://www.developersdigest.tech/models/image-generation/openai , /black-forest-labs , /recraft
- toolcolumn.com (GPT Image pricing): https://www.toolcolumn.com/learn/gpt-image-api-pricing
- atlascloud.ai (rate limits GPT Image 2.5): https://www.atlascloud.ai/blog/tips/gpt-image-2.5-rate-limits
- unifically.com (Imagen 4 shutdown): https://unifically.com/blogs/imagen-4-api-shutdown
- igly.ai (Imagen shutdown guide): https://igly.ai/blog/google-imagen-shutdown-migration-guide-2026
- shattered.io (Nano Banana 2.1): https://shattered.io/nano-banana-2-1-launch-pricing-2026/
- benchlm.ai (Nano Banana pricing): https://benchlm.ai/media-pricing/nano-banana

**Stack/región (de investigación previa):**
- `docs/agent-context/research/2026-11-27-stack-arquitectura.md` (secciones 5, 7, 10)

---

## 14. Respuestas del usuario (2026-11-27)

1. **Estilos (P-003):** definir los 6–8 estilos antes del spike. El spike no puede ejecutarse con fidelidad sin estilos reales.
2. **Calidad vs coste:** balance calidad/coste (Nano Banana 2.1 / FLUX.2 pro, ~$0,03–$0,05/imagen).
3. **Texto en imagen:** depende del estilo (algunos requieren texto legible, otros no). El spike debe cubrir ambos casos.
4. **Unificación:** un único proveedor para imagen y texto (OpenAI si se elige OpenAI para imágenes, usando gpt-6-luna para texto).

### 14.1 Implicaciones para el spike

- El spike se bloquea hasta que se definan los 6–8 estilos (P-003).
- Los proveedores candidatos para el spike se acotan a los que balancean calidad/coste y soportan texto en imagen cuando se requiera: OpenAI GPT Image 2.5, Google Nano Banana 2.1, y uno de bajo coste (Recraft V4.1 Flash o Ideogram P-Image Very Low).
- Un único proveedor simplifica la integración y la facturación, pero se valida en el spike si la calidad es suficiente para todos los estilos.

---

*Fin del informe. Este documento es material de investigación y no constituye una decisión, especificación ni plan aprobado. La decisión de proveedor(es) de IA requiere autorización explícita del usuario (P-012).*