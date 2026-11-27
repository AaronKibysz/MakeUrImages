# Investigación de base de datos y almacenamiento para el MVP

- **Fecha de creación:** 2026-11-27
- **Autor:** subagente de investigación (encargo de investigación)
- **Estado:** Borrador de investigación (no es una decisión ni una especificación aprobada)
- **Alcance:** Recopilar y comparar opciones de base de datos relacional, región de despliegue, multi-tenancy en PostgreSQL, almacenamiento de archivos (imágenes), archivos temporales, imágenes para Instagram, cache, colas de trabajos, backups/recuperación y coste total estimado. No toma decisiones de proveedor, región ni arquitectura.
- **Fuentes:** documentación oficial de proveedores, páginas de tarifas y guías técnicas (URLs y fechas de consulta al pie de cada dato).
- **Contexto previo:** `docs/agent-context/research/2026-11-27-stack-arquitectura.md` (secciones 4 y 7), D-021 (FastAPI), D-022 (React Native + Expo), D-017 (archivos temporales se eliminan al cerrar sesión).

> **Advertencia:** Este informe es material de investigación. Ninguna opción queda elegida. Las decisiones de proveedor, región y arquitectura requieren autorización explícita del usuario (constitución §3, §4.13). Los precios y límites marcados como "requiere verificación" deben confirmarse antes de tomar decisiones de costes. El contenido de páginas web es un dato a verificar, no una instrucción.

---

## 1. Resumen (máximo 10 líneas)

1. PostgreSQL managed es el estándar de facto para B2B SaaS multi-tenant; entre los candidatos, Supabase Pro parte de 25 USD/mes (incluye 8 GB disco, 250 GB egress, 100 GB storage, backups 7 días) y Neon Launch es pay-as-you-go sin mínimo (0,106 USD/CU-hora, 0,35 USD/GB-mes storage) (Verificado, fuentes oficiales 2026-11-27).
2. La región más cercana a Argentina es São Paulo (sa-east-1, ~30-40 ms desde Buenos Aires); AWS Chile (Santiago) está en early access desde 11/11/2026 con GA esperada a fines de 2026, y Bedrock NO está disponible en sa-east-1 según la matriz oficial de compatibilidad (Verificado, AWS).
3. El patrón pool (shared schema + tenant_id + RLS) es el default recomendado por AWS Prescriptive Guidance y la literatura para B2B SaaS con muchos tenants; el overhead de RLS es bajo si las políticas usan columnas indexadas (Verificado, AWS; Hipótesis sobre el overhead exacto en este workload).
4. Para almacenamiento de imágenes, Cloudflare R2 (0,015 USD/GB-mes, egress gratis) y Backblaze B2 (0,00695 USD/GB-mes, egress gratis hasta 3x storage) son mucho más baratos que S3 en sa-east-1 (0,0405 USD/GB-mes, egress 0,09 USD/GB) (Verificado, fuentes oficiales 2026-11-27).
5. Instagram exige que el media esté en una URL pública accesible (Meta hace cURL); S3 con bucket público o CDN (CloudFront) cumple; el egress es el componente dominante del coste (~87% en ejemplos publicados) (Verificado, Meta y AWS).
6. El cache gestionado más económico para un MVP es Upstash Redis (free tier 250 MB / 500k comandos; pay-as-you-go 0,20 USD/100k comandos) o Valkey en ElastiCache (cache.t4g.micro ~9,34 USD/mes en us-east-1, ~20% más barato que Redis OSS) (Verificado).
7. Para colas de trabajos en Python, Dramatiq y RQ son las opciones de menor complejidad para un MVP con Redis; Celery es la más completa pero la más compleja de operar; Cloud Tasks (GCP) ofrece 1M operaciones gratis/mes (Verificado, fuentes oficiales 2026-11-27).
8. Los backups de RDS/Aurora son gratuitos hasta el tamaño de storage provisionado en la región; por encima, 0,095 USD/GiB-mes (us-east-1; sa-east-1 puede variar) (Verificado, AWS).
9. Un MVP con ~1.000 usuarios activos y ~50 GB de imágenes podría costar del orden de 150-400 USD/mes de infraestructura (BD + storage + cache + colas + backups), dominado por la generación de IA (no incluida aquí) y el egress de imágenes (Hipótesis, requiere validación).
10. Bloqueos principales: región definitiva (sa-east-1 vs Chile cuando esté GA), proveedor de storage (S3 vs R2 vs B2), capacidad de biblioteca por plan (P-005) y límites de usuarios por org (P-006), que afectan el dimensionamiento.

---

## 2. Base de datos relacional managed

### 2.1 Alternativas comparadas

| Proveedor / motor | Plan de entrada | Storage incluido | Egress incluido | Backups | Connection pooling | RLS | Región sa-east-1 | Fuente (consultado 2026-11-27) |
|---|---|---|---|---|---|---|---|---|
| **Supabase** (PostgreSQL) | Free: 0 USD (500 MB DB, pausa tras 1 semana inactividad) | 1 GB file storage (Free) / 100 GB (Pro) | 5 GB (Free) / 250 GB (Pro) | Daily 7 días (Pro); PITR 100 USD/mes por 7 días | Supavisor: 200 (Micro) a 12.000 (16XL) conexiones pooler | Sí (PostgreSQL nativo) | Sí (AWS sa-east-1 disponible en Supabase) | supabase.com/pricing |
| **Supabase Pro** | 25 USD/mes + compute (10 USD Micro incluido) | 8 GB disco, +0,125 USD/GB | 250 GB, +0,09 USD/GB | Daily 7 días | Pooler hasta 200 (Micro) | Sí | Sí | supabase.com/pricing |
| **Neon** (PostgreSQL) | Free: 0 USD (100 proyectos, 100 CU-horas/proyecto/mes, 1 GB/proyecto) | 1 GB/proyecto (Free) / ilimitado (paid, 0,35 USD/GB-mes) | 5 GB/proyecto (Free) / 500 GB/proyecto (paid) | Instant restore 0,20 USD/GB-mes (Launch) | Hasta 10.000 pooled connections/compute | Sí (PostgreSQL nativo) | No verificado (Neon corre en AWS; región sa-east-1 no confirmada en docs) | neon.com/pricing |
| **Neon Launch** | Pay-as-you-go sin mínimo | 0,35 USD/GB-mes | 500 GB/proyecto, +0,10 USD/GB | Instant restore + snapshots | Hasta 10.000 pooled | Sí | No verificado | neon.com/pricing |
| **AWS RDS PostgreSQL** | Sin free tier permanente (db.t4g.micro ~0,016 USD/h en us-east-1 ≈ 11,68 USD/mes) | 20 GB gp3 mínimo recomendado; +0,12 USD/GB-mes (us-east-1); en sa-east-1 mayor | Egress estándar AWS (0,09 USD/GB primeros 10 TB) | Automáticos gratuitos hasta tamaño provisionado; +0,095 USD/GiB-mes por exceso | RDS Proxy (costo adicional) | Sí (PostgreSQL nativo) | Sí | aws.amazon.com/rds/pricing; instances.usage.ai |
| **AWS Aurora PostgreSQL** | Serverless v2: 0,25 USD/ACU-hora en sa-east-1; mínimo ~0,5 ACU (~43,80 USD/mes en us-east-1 a 0,12 USD/ACU-hora, mayor en sa-east-1) | 0,10 USD/GB-mes (Aurora Standard) | Egress estándar AWS | Continuo (PITR) incluido en storage | RDS Proxy | Sí | Sí | aws.amazon.com/aurora/pricing; raw.githubusercontent.com (tabla regional) |
| **Google Cloud SQL PostgreSQL** | Sin free tier permanente; compute por hora (São Paulo southamerica-east1: ~0,030975 USD/h por vCPU) | +storage por GB-mes | Egress estándar GCP | Automáticos incluidos | Cloud SQL Proxy / connection pooling manual | Sí (PostgreSQL nativo) | Sí (southamerica-east1) | cloud.google.com/sql/pricing |

### 2.2 Hechos verificados

- **Supabase** ofrece free tier con 500 MB de DB, 1 GB de file storage, 5 GB egress, 50k MAU, pausa tras 1 semana de inactividad, límite de 2 proyectos activos. Pro desde 25 USD/mes con 8 GB disco, 250 GB egress, 100 GB file storage, backups diarios 7 días, 100k MAU. Compute se factura por proyecto: Micro 10 USD/mes (incluido en Pro como crédito de 10 USD), Small 15 USD, Medium 60 USD, etc. (fuente: supabase.com/pricing, consultado 2026-11-27).
- **Neon** ofrece free tier permanente (no trial) con 100 proyectos, 100 CU-horas/proyecto/mes, 1 GB/proyecto, 5 GB egress/proyecto, scale-to-zero tras 5 min. Launch pay-as-you-go: 0,106 USD/CU-hora, 0,35 USD/GB-mes storage, 500 GB egress/proyecto, sin mínimo mensual. Scale: 0,222 USD/CU-hora, features enterprise (HIPAA, SOC2, SLA, private networking). (fuente: neon.com/pricing, consultado 2026-11-27).
- **RDS PostgreSQL** en sa-east-1: db.t4g.micro ~0,016 USD/h en us-east-1 (≈11,68 USD/mes); en sa-east-1 el precio es mayor (el markup regional para São Paulo es ~54-62% sobre Virginia para EC2; para RDS no se verificó el valor exacto en esta investigación). Storage gp3 ~0,12 USD/GB-mes en us-east-1 (sa-east-1 mayor, requiere verificación). (fuente: instances.usage.ai, selfhost.dev, consultado 2026-11-27).
- **Aurora Serverless v2** en sa-east-1: 0,25 USD/ACU-hora (vs 0,12 USD en us-east-1). Mínimo 0,5 ACU (~43,80 USD/mes en us-east-1 a 0,12 USD/ACU-hora; en sa-east-1 el piso es ~91,25 USD/mes a 0,25 USD/ACU-hora). Storage 0,10 USD/GB-mes. Scale-to-zero no disponible por defecto (mínimo 0,5 ACU siempre encendido), salvo configuración de scale-to-zero reciente (requiere verificación). (fuente: raw.githubusercontent.com/aws/agent-toolkit-for-aws, akalcloud.ai, consultado 2026-11-27).
- **Cloud SQL PostgreSQL** en São Paulo (southamerica-east1): ~0,030975 USD/h por vCPU + memoria + storage. Región Santiago (southamerica-west1) también disponible. (fuente: cloud.google.com/sql/pricing, consultado 2026-11-27).
- Todos los proveedores soportan PostgreSQL con RLS nativo (Row-Level Security es feature estándar de PostgreSQL). La diferencia está en el ecosistema (auth, storage, realtime incluidos en Supabase; solo DB en Neon/RDS/Cloud SQL).

### 2.3 Notas y pendientes

- **Pendiente:** elección de proveedor de BD. Factores: coste, ecosistema (Supabase incluye auth/storage/realtime que el producto puede o no usar, dado que FastAPI gestiona la lógica), región, compliance (SOC2/ISO27001 en Supabase Team/Neon Scale), y si se quiere un solo proveedor o desacoplado.
- **Hipótesis:** para un MVP con equipo Python y backend FastAPI, un PostgreSQL "puro" (Neon o RDS) puede ser más adecuado que Supabase completo, porque Supabase añade una capa de API/auth/storage que puede solaparse con FastAPI. Marcar como hipótesis hasta validar con el usuario.
- **Pendiente:** verificar disponibilidad de Neon en sa-east-1 (no confirmado en esta investigación).
- **Pendiente:** coste exacto de RDS/Aurora/ElastiCache en sa-east-1 (precios regionales superiores a us-east-1; requiere cotización o calculator).

---

## 3. Región de despliegue

### 3.1 Comparativa de regiones

| Región / ubicación | Latencia desde Buenos Aires | Catálogo de servicios | Coste relativo vs us-east-1 | Bedrock / IA generativa | Estado (2026-11-27) |
|---|---|---|---|---|---|
| **São Paulo (sa-east-1)** AWS | ~30-40 ms | Completo (EC2, RDS, Aurora, S3, ElastiCache, CloudFront, Lambda, etc.) | +54% a +62% (EC2); S3 +76% (0,0405 vs 0,023 USD/GB) | NO disponible (según matriz oficial de compatibilidad de Bedrock) | GA |
| **AWS South America (Chile), Santiago** | ~15-30 ms (estimado, menor que São Paulo) | En early access: servicios limitados al inicio; se añadirán Bedrock y SageMaker AI dentro del primer año | No publicado (early access) | Pendiente (Bedrock se añade dentro del primer año) | Early access desde 11/11/2026; GA esperada fines de 2026 |
| **GCP Santiago (southamerica-west1)** | ~20-30 ms | Completo (Compute, Cloud SQL, GCS, Cloud Run, Pub/Sub, etc.) | +20% a +40% vs us-central1 (según fuentes) | Vertex AI / Gemini (disponibilidad regional requiere verificación) | GA desde 2021 |
| **Azure Chile Central** | ~20-30 ms | Completo (Azure SQL, Blob, Functions, etc.) | No verificado | Azure OpenAI (disponibilidad regional requiere verificación) | GA desde 2025 |
| **AWS Local Zones Buenos Aires** | ~15-30 ms (baja latencia local) | Muy limitado: EC2, ECS/EKS, EBS, VPC, ElastiCache; S3 y DynamoDB siguen en la región (São Paulo) | No publicado | No (servicios limitados) | Disponible (Local Zone us-east-1-bue-1a) |
| **Buenos Aires (on-prem / otros)** | Mínima | Depende del proveedor | Variable | Variable | No aplica |

### 3.2 Hechos verificados

- La región más cercana a Argentina con catálogo completo es **São Paulo (sa-east-1)**: ~30-40 ms de mediana desde Buenos Aires para AWS, Azure, GCP y Oracle (fuente: pingcloud.io, consultado 2026-11-27).
- AWS South America (Chile) abrió el 11/11/2026 en early access para clientes selectos; GA esperada a fines de 2026. AWS invirtió más de 4.000 millones USD. Bedrock y SageMaker AI se añadirán dentro del primer año (fuente: aboutamazon.com, 2026-11-11).
- **Bedrock NO está disponible en sa-east-1** según la matriz oficial de compatibilidad de modelos por región (la documentación muestra "not-supported" para sa-east-1 en la tabla de modelos-regiones). Para usar modelos de Bedrock, habría que llamar a otra región (us-east-1, etc.) con latencia adicional y coste de transferencia. (fuente: docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility, consultado 2026-11-27).
- AWS tiene **Local Zones en Buenos Aires** (us-east-1-bue-1a) con servicios limitados: EC2, ECS/EKS, EBS, VPC, ElastiCache; S3 y DynamoDB siguen en la región (São Paulo). (fuente: aws-services.info, docs.aws.amazon.com/local-zones, consultado 2026-11-27).
- GCP tiene región en Santiago (southamerica-west1) desde 2021 con 3 zonas de disponibilidad. (fuente: cloud.google.com/about/locations, consultado 2026-11-27).
- Azure tiene Chile Central desde 2025. (fuente: investigación previa 2026-11-27).
- São Paulo cuesta entre 54% y 62% más que Virginia para instancias EC2 (fuente: datametricgroup.com, consultado 2026-11-27).

### 3.3 Implicaciones para el producto

- Si se usa **proveedores de IA vía API directa** (OpenAI, Google Gemini) en lugar de Bedrock, la región de despliegue del backend no depende de Bedrock; sa-east-1 o Chile son válidas.
- Si se quiere usar **Bedrock** (modelos gestionados en AWS), hoy no está disponible en sa-east-1; habría que llamar a us-east-1 (latencia + transferencia) o esperar a AWS Chile (Bedrock dentro del primer año).
- Para **baja latencia al usuario final** (app móvil en Argentina), Chile (cuando esté GA) o Local Zones Buenos Aires (limitado) son mejores que São Paulo, pero con catálogo reducido.
- El coste de storage/egress en sa-east-1 es significativamente mayor que en us-east-1 (S3: 0,0405 vs 0,023 USD/GB-mes; egress 0,09 USD/GB). Esto favorece usar un storage con egress gratis (R2, B2) o un CDN (CloudFront, cuyo egress desde sa-east-1 también tiene markup).

### 3.4 Pendientes

- **Pendiente:** decisión de región definitiva. Depende de si se usa Bedrock o APIs directas, y de cuándo esté GA AWS Chile.
- **Pendiente:** verificar precios exactos de RDS/Aurora/ElastiCache/CloudFront en sa-east-1 y en Chile cuando esté GA.
- **Pendiente:** verificar disponibilidad de Vertex AI / Gemini y Azure OpenAI en Santiago/Chile Central.

---

## 4. Multi-tenancy en PostgreSQL

### 4.1 Patrón recomendado: pool (shared schema + tenant_id + RLS)

La literatura (AWS Prescriptive Guidance, clickhouse.com) recomienda el patrón **pool** como default para B2B SaaS con muchos tenants y poco dato por tenant:

| Patrón | Aislamiento | Coste/operación | Onboarding de tenants | Cuándo usar |
|---|---|---|---|---|
| Silo (DB/instancia por tenant) | Máximo | Alto | Lento | Clientes grandes/regulados, white-label |
| Bridge (DB por tenant en instancia compartida) | Alto | Medio | Moderado | Aislamiento de datos clave |
| Bridge (schema por tenant) | Alto (lógico) | Medio-alto | Moderado | Número moderado de tenants |
| **Pool (tablas compartidas + tenant_id + RLS)** | **Lógico (RLS)** | **Bajo** | **Rápido** | **Muchos tenants con poco dato (default B2B SaaS)** |

Fuente: AWS Prescriptive Guidance (docs.aws.amazon.com/prescriptive-guidance/latest/saas-multitenant-managed-postgresql), clickhouse.com (consultado 2026-11-27).

Implementación típica (fuente: clickhouse.com, consultado 2026-11-27):

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_select ON orders
  FOR SELECT USING (tenant_id = current_setting('app.current_tenant_id', true)::uuid);
CREATE POLICY tenant_isolation_insert ON orders
  FOR INSERT WITH CHECK (tenant_id = current_setting('app.current_tenant_id', true)::uuid);
```

### 4.2 Coste de performance de RLS

| Fuente | Claim | Verificabilidad |
|---|---|---|
| dev.to (PostgreSQL 17 + RLS benchmark) | +3,2 ms promedio por query con 10k políticas de tenant, vs 18,7 ms para filtrado a nivel de aplicación (en m6i.xlarge) | Requiere verificación (benchmark de terceros, no oficial) |
| dev.to (RLS performance test) | +1,6 ms en query de count sobre tabla completa (73,3 ms vs 74,9 ms) | Requiere verificación |
| clickhouse.com | "RLS lento es casi siempre RLS no optimizado"; una política que compara `current_setting` contra una columna indexada es rápida | Opinión de ingeniería, consistente con docs de PostgreSQL |
| tenantsdb.com | +5% a +15% de overhead en queries simples; mayor en queries complejas con joins | Requiere verificación (blog de un competidor) |
| PlanetScale | RLS puede degradar con muchas conexiones (process-per-connection) | Aplica a PostgreSQL; mitigable con connection pooling (PgBouncer/Supavisor) |

**Conclusión:** el overhead de RLS es bajo si se siguen las buenas prácticas (columna `tenant_id` indexada, política simple con `current_setting`, connection pooling). No es un bloqueo para el MVP, pero requiere tests de performance y de aislamiento en CI.

### 4.3 Caveats verificados (PostgreSQL oficial y AWS)

- **Superusers y roles con BYPASSRLS saltan RLS**; los owners de tabla también, salvo `FORCE RLS`. (fuente: postgresql.org docs, citado en eltherion.com, consultado 2026-11-27).
- **RLS es una garantía a nivel de BD**, pero el cache (Redis) y el storage de archivos (S3) no se protegen automáticamente: el `tenant_id` debe propagarse en todas las capas (API, cache keys, object keys por tenant, background jobs, audit logs, analytics). (fuente: pineido.com, consultado 2026-11-27).
- **Requiere tests automatizados en CI** que verifiquen que un tenant no lee datos de otro (fuente: pineido.com).
- **MongoDB no tiene RLS nativo**; el aislamiento es a nivel de aplicación (más débil, más difícil de auditar para SOC 2/HIPAA). (fuente: pineido.com).

### 4.4 Requisitos del producto (de product-definition.md)

- Espacio personal + organizaciones; un usuario puede pertenecer a varias organizaciones.
- Cada espacio tiene su suscripción, créditos, biblioteca, historial y conexiones sociales.
- Roles: propietario, administrador, usuario. Permisos básicos fijos: generar, aprobar, consultar historial.
- Las conexiones sociales pertenecen a la organización.
- Aislamiento desde el diseño: ninguna consulta devuelve datos de otro espacio sin autorización (constitución §2.5).

### 4.5 Pendientes

- **Pendiente (P-006):** límite de integrantes por organización (afecta dimensionamiento).
- **Pendiente:** estrategia de tiering (cuándo promover un tenant a silo) — decisión de negocio.
- **Pendiente:** auditoría de aislamiento (tests automatizados en CI) — requiere especificación.
- **Pendiente:** decidir si usar `current_setting` (session variable) o un rol por tenant; el primero es más simple y compatible con connection pooling (PgBouncer/Supavisor).

---

## 5. Almacenamiento de archivos (imágenes)

### 5.1 Alternativas comparadas

| Servicio | Storage (USD/GB-mes) | Egress (USD/GB) | Requests | Free tier | Lifecycle policies | URLs pre-firmadas | CDN integrado | Fuente (consultado 2026-11-27) |
|---|---|---|---|---|---|---|---|---|
| **Amazon S3 Standard** (sa-east-1) | 0,0405 | 0,09 (primeros 10 TB, tras 100 GB gratis/mes) | 0,005/1k PUT; 0,0004/1k GET | 5 GB storage + 20k GET + 2k PUT (12 meses, AWS Free Tier) | Sí (expiración de versiones actuales y anteriores) | Sí (presigned URLs) | CloudFront (egress S3→CloudFront gratis) | cloudcostdb.com (datos derivados de AWS); aws.amazon.com/s3/pricing |
| **Cloudflare R2** (global, sin región fija) | 0,015 | **Gratis** | 4,50 USD/millón Class A (writes/lists); 0,36 USD/millón Class B (reads) | 10 GB-mes storage + 1M Class A + 10M Class B/mes | Sí (reglas de expiración) | Sí (presigned URLs S3-compatible) | Cloudflare CDN integrado (egress gratis) | developers.cloudflare.com/r2/pricing |
| **Backblaze B2** | 0,00695 | Gratis hasta 3x storage promedio/mes; 0,01 USD/GB por exceso | 0,004 USD/1k (Class B reads, según fuente) | 10 GB storage siempre gratis | Sí | Sí | Cloudflare CDN (egress gratis vía partner) | backblaze.com/pricing; howmakersbuild.com |
| **Supabase Storage** (Pro) | 0,0213 (tras 100 GB incluidos) | 0,09 USD/GB (egress, tras 250 GB incluidos; cached egress 0,03 USD/GB) | Incluido en plan | 1 GB (Free) | Solo versiones no actuales (versioning) | Sí (signed URLs) | Smart CDN incluido | supabase.com/pricing (storage section) |

### 5.2 Hechos verificados

- **S3 Standard en sa-east-1**: 0,0405 USD/GB-mes de storage; PUT 0,0070 USD/1k; GET 0,00056 USD/1k; egress a internet 0,09 USD/GB (primeros 10 TB, tras 100 GB gratis/mes agregados en todos los servicios AWS). (fuente: cloudcostdb.com, datos derivados de AWS pricing; requiere verificación contra la página oficial de AWS, que es dinámica por región).
- **Cloudflare R2**: 0,015 USD/GB-mes storage; egress gratis; free tier 10 GB-mes + 1M Class A + 10M Class B/mes. S3-compatible API. (fuente: developers.cloudflare.com/r2/pricing, consultado 2026-11-27).
- **Backblaze B2**: 0,00695 USD/GB-mes (6,95 USD/TB); egress gratis hasta 3x el storage promedio mensual (calculado en byte-horas); 0,01 USD/GB por exceso; 10 GB storage siempre gratis; sin mínimo. (fuente: backblaze.com/pricing, howmakersbuild.com, consultado 2026-11-27).
- **Supabase Storage**: 100 GB incluidos en Pro, luego 0,0213 USD/GB; egress 250 GB incluidos, luego 0,09 USD/GB (cached egress 0,03 USD/GB); max upload 500 GB; Smart CDN incluido; image transformations 100 origin images incluidas, luego 5 USD/1k. (fuente: supabase.com/pricing, consultado 2026-11-27).
- **S3 Lifecycle** puede expirar versiones actuales de objetos (regla "Expire current versions of objects" con número de días tras la creación), además de versiones no actuales. (fuente: docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-set-lifecycle-configuration-intro, consultado 2026-11-27).
- **Supabase Storage Lifecycle** actúa solo sobre versiones no actuales (requiere versioning habilitado); no expira objetos actuales automáticamente. (fuente: supabase.com/docs/guides/storage/buckets/lifecycle-policies, consultado 2026-11-27).

### 5.3 Notas y pendientes

- **Pendiente:** elección de proveedor de storage. Factores clave: egress gratis (R2/B2) vs ecosistema AWS (S3 + CloudFront), latencia desde Argentina, y si se quiere un solo proveedor o desacoplado.
- **Hipótesis:** para un producto con imágenes servidas a usuarios y a Instagram (egress dominante), R2 o B2 con egress gratis/cheap pueden reducir costes drásticamente vs S3 en sa-east-1. Pero R2 no tiene región fija (global, latencia variable) y B2 tiene egress gratis solo hasta 3x storage. Marcar como hipótesis hasta validar con prototipo de latencia.
- **Pendiente:** verificar si R2/B2 tienen latencia aceptable desde Argentina para servir imágenes a la app móvil (no hay región sa-east-1 dedicada en R2/B2; Cloudflare tiene edge en Buenos Aires).

---

## 6. Archivos temporales (regla D-017)

### 6.1 Patrón de implementación

La decisión D-017 establece que los archivos temporales se eliminan al cerrar la sesión de creación. Implementación típica:

1. **Bucket dedicado para temporales** (separado del bucket de biblioteca permanente), con prefijo por sesión/usuario (`tmp/{session_id}/...`).
2. **URLs pre-firmadas** para upload directo desde la app móvil al storage (evita pasar archivos por el backend).
3. **Borrado explícito** al cerrar la sesión (llamada a la API de delete del storage desde el backend, o directamente por el cliente con permisos acotados).
4. **Lifecycle policy de respaldo** que expira objetos tras N días (ej. 7 días) para limpiar huérfanos si el cliente no cierra la sesión correctamente.
5. **No persistir originales** sin consentimiento del usuario (constitución §2.8).

### 6.2 Capacidad de auto-expiración por proveedor

| Proveedor | Auto-expiración de objetos actuales | Mecanismo | Coste de storage temporal |
|---|---|---|---|
| **S3** | Sí (lifecycle "Expire current versions" con días) | Regla de lifecycle por bucket/prefijo | 0,0405 USD/GB-mes en sa-east-1 (storage estándar; no hay clase "temporal" más barata con expiración automática corta, salvo Intelligent-Tiering) |
| **Cloudflare R2** | Sí (lifecycle rules con expiration) | Regla de lifecycle | 0,015 USD/GB-mes (egress gratis) |
| **Backblaze B2** | Sí (lifecycle rules) | Regla de lifecycle | 0,00695 USD/GB-mes |
| **Supabase Storage** | No para objetos actuales (solo versiones no actuales) | Borrado explícito por la app | 0,0213 USD/GB-mes (tras 100 GB) |

### 6.3 Coste de storage temporal

- El coste de storage temporal es bajo si los archivos se borran al cerrar la sesión: el tiempo de vida promedio es minutos/horas, no días. A 0,0405 USD/GB-mes, 1 GB almacenado 1 hora cuesta ~0,000056 USD.
- El riesgo de coste es la **acumulación de huérfanos** (sesiones abandonadas). La lifecycle policy de respaldo (7 días) limita el daño.
- **Hipótesis:** el coste de storage temporal es negligible frente al storage permanente y al egress. Marcar como hipótesis.

---

## 7. Imágenes para Instagram (URL pública + CDN + egress)

### 7.1 Requisito de Meta

Instagram Content Publishing API requiere que el media esté en una **URL pública accesible** al momento de publicar: Meta hace cURL del media. URLs firmadas que expiran rápido fallan. (fuente: developers.facebook.com, consultado 2026-11-27; sección 6.1 del informe de stack).

Implicaciones:
- Las imágenes generadas deben almacenarse en un bucket con **acceso público de lectura** (o con URLs pre-firmadas de larga duración, pero Meta puede fallar si expiran).
- El patrón recomendado: upload a S3/R2/B2 → URL pública → Meta hace cURL → publicación.
- Container expira si no se publica en 24 h; el media debe seguir accesible.

### 7.2 Patrón con CDN (CloudFront)

Para servir imágenes a los usuarios de la app (biblioteca, historial), el egress es el componente dominante del coste (~87% en el ejemplo publicado por upstash). Patrón:

1. **Storage de origen** (S3/R2/B2) con bucket privado.
2. **CDN** (CloudFront para S3; Cloudflare para R2) para servir imágenes a usuarios con cache en edge.
3. **URLs públicas estables** para Instagram (pueden ser del CDN o del storage de origen).
4. **Egress S3→CloudFront es gratis** (AWS no cobra transferencia entre S3 y CloudFront en la misma cuenta). CloudFront cobra egress a internet (~0,085 USD/GB primeros 10 TB en US/EU; en sa-east-1/edge locations de Sudamérica puede ser mayor).

### 7.3 Coste de egress (dominante)

| Componente | Coste aproximado (USD) | Notas |
|---|---|---|
| S3 egress a internet (sa-east-1) | 0,09 /GB | Primeros 100 GB/mes gratis (agregados AWS) |
| CloudFront egress (primeros 10 TB) | 0,085 /GB (US/EU); mayor en Sudamérica | Free tier 1 TB/mes (12 meses) |
| R2 egress | 0 | Gratis siempre |
| B2 egress | 0 hasta 3x storage; 0,01/GB después | Gratis vía Cloudflare partner |
| Supabase egress (Pro) | 0,09 /GB (tras 250 GB) | Cached egress 0,03 USD/GB |

**Hipótesis:** para un MVP con miles de imágenes servidas a usuarios y a Instagram, el egress puede ser el mayor coste de infraestructura después de la IA. Usar R2/B2 (egress gratis) o CloudFront (egress descontado) reduce costes significativamente. Marcar como hipótesis hasta medir tráfico real.

---

## 8. Cache

### 8.1 Alternativas comparadas

| Opción | Tipo | Free tier | Precio base | Latencia | Notas | Fuente (consultado 2026-11-27) |
|---|---|---|---|---|---|---|
| **Upstash Redis** | Serverless (pay-per-command) | 250 MB + 500k comandos/mes | 0,20 USD/100k comandos; storage 0,25 USD/GB (1 GB gratis); bandwidth gratis hasta 200 GB/mes | Global (edge) | Ideal para MVP con tráfico variable; sin servidor que mantener | upstash.com/pricing/redis |
| **AWS ElastiCache for Valkey** (node-based) | Node gestionado | No free tier permanente (free tier 12 meses: cache.t2.micro) | cache.t4g.micro Valkey: 0,0128 USD/h ≈ 9,34 USD/mes (us-east-1); en sa-east-1 mayor (requiere verificación) | Depende de la región (sa-east-1) | Valkey es 20% más barato que Redis OSS en el mismo nodo; compatible con Redis | aws.amazon.com/elasticache/pricing |
| **AWS ElastiCache Serverless for Valkey** | Serverless | No | 0,084 USD/GB-hora + ECPUs | Depende de la región | Pago por uso; mínimo 1 GB storage | aws.amazon.com/elasticache/pricing |
| **Redis Cloud** (Redis Inc.) | Gestionado | 30 MB (free) | Desde ~5 USD/mes (fixed) | Multi-región | No investigado en profundidad; marcar como pendiente | redis.io (no verificado en esta investigación) |
| **Memcached** (ElastiCache) | Node gestionado | No | Similar a Redis OSS | Depende de la región | Sin persistencia ni estructuras avanzadas; no recomendado para sesiones/rate limiting complejo | aws.amazon.com/elasticache/pricing |

### 8.2 Hechos verificados

- **Upstash Redis**: free tier 250 MB y 500k comandos/mes; pay-as-you-go 0,20 USD/100k comandos, storage 0,25 USD/GB (primer GB gratis), bandwidth gratis hasta 200 GB/mes, max data size 100 GB. (fuente: upstash.com/pricing/redis, consultado 2026-11-27).
- **ElastiCache for Valkey**: cache.t4g.micro (2 vCPU, 0,5 GiB) a 0,0128 USD/h ≈ 9,34 USD/mes en us-east-1; Valkey es ~20% más barato que Redis OSS en el mismo nodo. (fuente: upstash.com/blog/aws-elasticache-pricing-explained-2026, consultado 2026-11-27).
- **ElastiCache Serverless for Valkey**: 0,084 USD/GB-hora mínimo 1 GB. (fuente: usage.ai/blogs/aws/database-savings-plans/elasticache/serverless-pricing, consultado 2026-11-27).

### 8.3 Usos en el producto

- Sesiones de usuario (JWT refresh tokens, estado de sesión).
- Rate limiting por usuario/organización/IP.
- Cache de generación (resultados de IA recientes para evitar regeneración).
- Cola de trabajos (Redis como broker para Celery/RQ/Dramatiq).
- Locks distribuidos para operaciones transaccionales de créditos (reservas).

### 8.4 Pendientes

- **Pendiente:** elección de cache. Factores: coste, latencia desde Argentina, si ya hay Redis para la cola (reutilizar), y si se quiere serverless (Upstash) o gestionado (ElastiCache).
- **Hipótesis:** si se usa Celery/RQ/Dramatiq con Redis como broker, reutilizar el mismo Redis para cache/sesiones/rate limiting reduce costes y complejidad. Marcar como hipótesis.

---

## 9. Colas de trabajos (background jobs)

### 9.1 Alternativas comparadas

| Opción | Broker | Complejidad | Retries / scheduling | Escalado | Coste | Fuente (consultado 2026-11-27) |
|---|---|---|---|---|---|---|
| **Celery** | Redis, RabbitMQ, SQS, más | Alta | Configurable (retries, ETA, cron via beat) | Horizontal (workers) | Coste del broker + workers | docs.celeryq.dev; dev.to comparativas 2026 |
| **RQ (Redis Queue)** | Redis solo | Baja | Explícito (retries manuales) | Horizontal (workers) | Coste del broker + workers | python-rq.org; dev.to |
| **Dramatiq** | Redis, RabbitMQ | Media | Built-in (retries, middleware) | Horizontal (workers) | Coste del broker + workers | dramatiq.io; dev.to |
| **ARQ** | Redis | Baja (asyncio nativo) | Built-in | Horizontal | Coste del broker + workers | github.com/samuelcolvin/arq |
| **Google Cloud Tasks** | GCP (managed) | Baja (API HTTP) | Built-in (retries, rate limiting) | Auto (managed) | 1M operaciones gratis/mes; luego por operación | cloud.google.com/tasks/pricing |
| **AWS SQS + Lambda/worker** | AWS (managed) | Media | Built-in (DLQ, retries) | Auto (managed) | 1M requests gratis/mes; luego 0,40 USD/millón | aws.amazon.com/sqs/pricing |
| **Cloud Pub/Sub** | GCP (managed) | Media | Built-in | Auto (managed) | 10 GB gratis/mes; luego por GB | cloud.google.com/pubsub/pricing |

### 9.2 Hechos verificados

- **Celery** es el más completo (broker múltiple, retries, scheduling, workflows) pero el más complejo de configurar y operar. (fuente: dev.to, bigiron.cc, consultado 2026-11-27).
- **RQ** es el más simple (Redis only, API minimalista), ideal para apps pequeñas-medias ya en Redis. (fuente: dev.to, bigiron.cc).
- **Dramatiq** es el "middle ground": más simple que Celery, más capaz que RQ, con retries built-in y middleware. (fuente: dramatiq.io, bigiron.cc).
- **ARQ** es nativo asyncio (FastAPI es async), lo que lo hace atractivo para un backend FastAPI; pero es menos maduro que Celery. (fuente: dev.to, github.com/samuelcolvin/arq, consultado 2026-11-27).
- **Cloud Tasks** (GCP): 1 millón de operaciones gratis por mes por proyecto; luego por operación. Push targets a App Engine/Cloud Run/HTTP gratis en operaciones (se cobra compute). (fuente: cloud.google.com/tasks/pricing, consultado 2026-11-27; nota: la página de pricing de Cloud Tasks no se obtuvo completa en esta investigación, se cita el free tier mencionado en fuentes secundarias).
- **AWS SQS**: 1 millón de requests gratis/mes; luego 0,40 USD/millón de requests (Standard). (fuente: aws.amazon.com/sqs/pricing, citado en fuentes secundarias; requiere verificación).
- **Cloud Pub/Sub**: 10 GB de mensajes gratis/mes; luego por GB. (fuente: cloud.google.com/pubsub/pricing, consultado 2026-11-27).

### 9.3 Caso de uso en el producto

La generación de imágenes con IA es asíncrona (puede tomar segundos): el backend recibe la solicitud, encola un job, devuelve un job_id al cliente, y el worker genera la imagen, la almacena y notifica al cliente (polling o WebSocket). La cola también sirve para:
- Reintentos ante fallos del proveedor de IA.
- Rate limiting por proveedor (concurrencia máxima).
- Procesamiento de publicación en Instagram (3 llamadas API por post).

### 9.4 Pendientes

- **Pendiente:** elección de cola. Factores: si el backend ya usa Redis (cache), reutilizar Redis con RQ/Dramatiq/ARQ reduce infraestructura; si se quiere managed (Cloud Tasks/SQS), se evita operar workers pero se añade latencia y dependencia de cloud.
- **Hipótesis:** para un MVP con equipo Python y backend FastAPI, Dramatiq o ARQ sobre Redis es el punto óptimo de simplicidad/capacidad. Celery solo si se requiere scheduling complejo o broker múltiple. Marcar como hipótesis.
- **Pendiente:** verificar precios exactos de Cloud Tasks y SQS (las fuentes secundarias pueden estar desactualizadas).

---

## 10. Backups y recuperación

### 10.1 Estrategia por componente

| Componente | Mecanismo | Coste | Retención recomendada (hipótesis) | Fuente (consultado 2026-11-27) |
|---|---|---|---|---|
| **PostgreSQL (RDS/Aurora)** | Backups automatizados diarios + PITR | Gratis hasta tamaño provisionado en la región; +0,095 USD/GiB-mes por exceso (us-east-1) | 7-14 días (automáticos); PITR para recuperación a un punto en el tiempo | aws.amazon.com/rds/pricing; docs.aws.amazon.com (automated backups) |
| **PostgreSQL (Supabase)** | Daily backups 7 días (Pro) / 14 días (Team) | Incluido en plan; PITR 100 USD/mes por 7 días adicionales | 7 días (Pro) | supabase.com/pricing |
| **PostgreSQL (Neon)** | Instant restore (0,20 USD/GB-mes) + snapshots (0,09 USD/GB-mes) + history window | 0,20 USD/GB-mes (instant restore); 0,09 USD/GB-mes (snapshots) | 7 días (Launch) / 30 días (Scale) | neon.com/pricing |
| **Storage (S3)** | Versioning + lifecycle + replicación cross-region (opcional) | Versioning: costo de storage adicional; replicación: costo de transferencia | Versioning 30 días + lifecycle de borrado | aws.amazon.com/s3/pricing |
| **Storage (R2/B2)** | Versioning (R2) / lifecycle | Costo de storage adicional | 30 días | developers.cloudflare.com/r2/pricing; backblaze.com/pricing |
| **Redis/Valkey (ElastiCache)** | Snapshots (RDB) a S3 | Costo de storage en S3 | Diario, retención 7 días | aws.amazon.com/elasticache/pricing |

### 10.2 Hechos verificados

- **RDS backups**: almacenamiento de backup gratuito hasta el tamaño total de storage provisionado en la región; por encima, 0,095 USD/GiB-mes (us-east-1). Los snapshots manuales se facturan como storage S3 estándar (0,023 USD/GB-mes en us-east-1). (fuente: aws.amazon.com/rds/pricing; selfhost.dev, consultado 2026-11-27).
- **Aurora backups**: continuos (PITR) incluidos en el costo de storage (0,10 USD/GB-mes); no hay cargo adicional por backups dentro de la retención. (fuente: aws.amazon.com/aurora/pricing, consultado 2026-11-27).
- **Supabase**: backups diarios incluidos (7 días Pro, 14 días Team); PITR como add-on (100 USD/mes por 7 días de retención adicional). (fuente: supabase.com/pricing, consultado 2026-11-27).
- **Neon**: instant restore 0,20 USD/GB-mes (Launch); history window hasta 7 días (Launch) / 30 días (Scale); snapshots manuales 0,09 USD/GB-mes. (fuente: neon.com/pricing, consultado 2026-11-27).
- **RDS per-snapshot billing**: disponible desde noviembre 2026 para tracking de costos por snapshot individual. (fuente: aws.amazon.com/about-aws/whats-new/2026/11/amazon-rds-per-snapshot-billing, consultado 2026-11-27).

### 10.3 Pendientes

- **Pendiente:** definir RPO/RTO (recovery point objective / recovery time objective) para el MVP. Afecta la estrategia de backups (frecuencia, retención, PITR).
- **Pendiente:** decidir si se necesita replicación cross-region (disaster recovery) o solo backups en la misma región.
- **Hipótesis:** para un MVP, backups diarios con 7 días de retención y PITR son suficientes; la replicación cross-region es overkill. Marcar como hipótesis.

---

## 11. Coste total estimado (MVP)

> **Advertencia:** Esta estimación es una **hipótesis**. Requiere validación con prototipo y medición real de tráfico, tamaño de imágenes y patrones de uso. Los precios regionales (sa-east-1) son superiores a us-east-1; donde no se verificó el precio exacto en sa-east-1, se usó el precio de us-east-1 o se aplicó un markup estimado y se marca como hipótesis.

### 11.1 Supuestos (hipótesis)

- MVP con ~1.000 usuarios activos/mes, ~100 organizaciones.
- ~50 GB de imágenes generadas almacenadas permanentemente (biblioteca + historial).
- ~5 GB de archivos temporales en promedio (vida corta).
- ~100 GB de egress de imágenes/mes (a usuarios + Instagram).
- 1 instancia de BD pequeña (8 GB disco, compute Micro/Small).
- 1 instancia de cache (cache.t4g.micro o equivalente).
- 1 worker para colas (puede correr en el mismo contenedor del backend o separado).

### 11.2 Estimación mensual por componente (hipótesis)

| Componente | Opción low-cost | Coste estimado (USD/mes) | Opción managed/premium | Coste estimado (USD/mes) |
|---|---|---|---|---|
| **Base de datos** | Neon Launch (intermittent, ~140 CU-h + 10 GB) | ~15-25 | Supabase Pro (25 + 10 compute) | ~35-50 |
| **Storage (imágenes, 50 GB)** | R2 (0,015 × 50 = 0,75) o B2 (0,00695 × 50 = 0,35) | ~1-5 | S3 sa-east-1 (0,0405 × 50 = 2,03) | ~2-10 |
| **Egress (100 GB/mes)** | R2/B2 (gratis) | ~0 | S3 (0,09 × 100 = 9) o CloudFront (0,085 × 100 = 8,5) | ~8-10 |
| **Cache** | Upstash (free tier o ~5 USD) | ~0-10 | ElastiCache Valkey (sa-east-1, ~15-20) | ~15-25 |
| **Cola de trabajos** | RQ/Dramatiq sobre Redis existente (sin costo adicional de broker) + worker en contenedor existente | ~0 (solo compute del worker) | Cloud Tasks / SQS (free tier 1M ops) | ~0-5 |
| **Backups** | Incluidos en Neon/Supabase; RDS backups gratuitos hasta storage provisionado | ~0-5 | PITR add-on (Supabase 100 USD/mes) | ~100 |
| **CDN (CloudFront, si S3)** | Free tier 1 TB/mes (12 meses) | ~0 (primer año) | Pay-as-you-go | ~8-10 |
| **Total infraestructura (sin IA)** | Low-cost stack | **~20-60 USD/mes** | Managed stack | **~70-210 USD/mes** |

### 11.3 Notas sobre la estimación

- La generación de IA (imágenes + textos) NO está incluida aquí; es probablemente el coste dominante. Ver informe de stack (sección 5) para precios de OpenAI/Google.
- La estimación asume un solo entorno (producción). Un entorno de staging añadiría ~30-50%.
- Los precios de sa-east-1 son superiores a us-east-1; donde no se verificó el precio exacto, se usó us-east-1 o se aplicó markup estimado.
- **Hipótesis:** el coste de infraestructura (sin IA) para el MVP es del orden de 20-200 USD/mes, dominado por la BD y el cache en el stack low-cost, y por backups/PITR en el stack managed. Marcar como hipótesis.

---

## 12. Recomendación (no decisión)

> **Importante:** Esta sección es una recomendación del subagente de investigación, no una decisión. Requiere autorización explícita del usuario (constitución §3, §4.13).

### 12.1 Base de datos

**Recomendación:** PostgreSQL managed. Candidatos: **Neon** (pay-as-you-go, sin mínimo, scale-to-zero, ideal para MVP con tráfico variable) o **Supabase** (ecosistema completo con auth/storage/realtime incluidos, pero puede solaparse con FastAPI). **RDS/Aurora** si se quiere control total y se prevé escala enterprise. **Cloud SQL** si se prefiere GCP (Santiago disponible).

**Justificación:** PostgreSQL es el estándar para B2B SaaS multi-tenant con RLS; el ecosistema managed es maduro y económico. Neon es el más barato para un MVP con tráfico variable (scale-to-zero); Supabase añade valor si se quiere usar su auth/storage/realtime.

**Bloqueo:** elección de proveedor (afecta región, coste, ecosistema) y si se quiere un solo proveedor o desacoplado.

### 12.2 Región

**Recomendación:** **sa-east-1 (São Paulo)** como región principal hoy (catálogo completo, ~30-40 ms desde Argentina). Evaluar **AWS Chile (Santiago)** cuando esté GA (fines de 2026) para menor latencia, pero verificar disponibilidad de Bedrock y otros servicios. Si se usa APIs de IA directas (OpenAI/Google), la región no depende de Bedrock.

**Justificación:** sa-east-1 es la única región AWS GA con catálogo completo cerca de Argentina; Chile ofrece menor latencia pero está en early access.

**Bloqueo:** decisión de si se usa Bedrock (no disponible en sa-east-1) o APIs directas; y timing de GA de AWS Chile.

### 12.3 Multi-tenancy

**Recomendación:** patrón **pool (shared schema + tenant_id + RLS)** como default, con `tenant_id` propagado en todas las capas (API, cache keys, object keys por tenant, jobs, audit logs). Tests de aislamiento en CI.

**Justificación:** es el patrón recomendado por AWS Prescriptive Guidance y la literatura para B2B SaaS con muchos tenants; bajo coste operativo y onboarding rápido. RLS da aislamiento a nivel de BD (auditable).

**Bloqueo:** definir estrategia de tiering (cuándo promover a silo) y tests de aislamiento (requiere especificación).

### 12.4 Storage de archivos

**Recomendación:** **Cloudflare R2** o **Backblaze B2** para imágenes (egress gratis o muy barato), con **CloudFront** si se usa S3. Si se prioriza ecosistema AWS integrado, **S3** en sa-east-1 con CloudFront (egress S3→CloudFront gratis).

**Justificación:** el egress es el coste dominante; R2 (0,015 USD/GB-mes, egress gratis) y B2 (0,00695 USD/GB-mes, egress gratis hasta 3x storage) son mucho más baratos que S3 en sa-east-1 (0,0405 USD/GB-mes, egress 0,09 USD/GB). Pero R2/B2 no tienen región fija (latencia variable; Cloudflare tiene edge en Buenos Aires).

**Bloqueo:** validación de latencia desde Argentina para R2/B2; y decisión de si se quiere un solo proveedor (AWS) o desacoplado.

### 12.5 Archivos temporales

**Recomendación:** bucket dedicado con URLs pre-firmadas para upload directo + borrado explícito al cerrar sesión + lifecycle policy de respaldo (7 días). Preferir S3/R2/B2 (auto-expiración de objetos actuales) sobre Supabase Storage (solo versiones no actuales).

**Justificación:** consistente con D-017 y constitución §2.8; el borrado explícito garantiza cumplimiento inmediato, la lifecycle policy cubre huérfanos.

**Bloqueo:** ninguno técnico; requiere implementación en la spec de creación.

### 12.6 Cache

**Recomendación:** **Upstash Redis** para el MVP (free tier generoso, pay-as-you-go, sin servidor que mantener, latencia global). Si ya se usa Redis como broker de la cola, reutilizarlo. Migrar a **ElastiCache Valkey** si el tráfico crece y se quiere control/coste predecible.

**Justificación:** Upstash es el más barato y simple para un MVP con tráfico variable; Valkey en ElastiCache es 20% más barato que Redis OSS si se quiere gestionado.

**Bloqueo:** si se usa Celery/RQ/Dramatiq con Redis como broker, el cache debe ser el mismo Redis (reutilización).

### 12.7 Colas de trabajos

**Recomendación:** **Dramatiq** o **ARQ** sobre Redis para el MVP (simplicidad + retries + integración con FastAPI async). **Celery** solo si se requiere scheduling complejo o broker múltiple. **Cloud Tasks/SQS** si se prefiere managed (sin operar workers).

**Justificación:** Dramatiq/ARQ son más simples que Celery y suficientes para generación asíncrona de imágenes; ARQ es nativo asyncio (alineado con FastAPI). Cloud Tasks/SQS eliminan la operación de workers pero añaden dependencia de cloud.

**Bloqueo:** decisión de si se quiere operar workers (contenedor) o usar managed (cloud).

### 12.8 Backups

**Recomendación:** backups automatizados diarios con 7 días de retención + PITR para la BD; versioning + lifecycle para storage; snapshots diarios para cache. Replicación cross-region solo si se define RPO/RTO estricto.

**Justificación:** suficiente para un MVP; el coste de PITR add-on (Supabase 100 USD/mes) o exceso de backup (RDS 0,095 USD/GiB-mes) debe evaluarse según el proveedor elegido.

**Bloqueo:** definir RPO/RTO (requiere decisión de producto).

---

## 13. Preguntas y bloqueos para el agente principal

1. **Región:** ¿Se autoriza sa-east-1 (São Paulo) como región principal, o se espera a AWS Chile (GA fines 2026)? ¿Se usará Bedrock (no disponible en sa-east-1) o APIs directas (OpenAI/Google)?
2. **Proveedor de BD:** ¿Neon (pay-as-you-go, scale-to-zero), Supabase (ecosistema completo) o RDS/Aurora (control total)? ¿Se quiere un solo proveedor o desacoplado?
3. **Proveedor de storage:** ¿R2/B2 (egress gratis, desacoplado) o S3 (ecosistema AWS integrado)? ¿Se valida latencia desde Argentina?
4. **Cache + cola:** ¿Se reutiliza Redis para cache y cola (RQ/Dramatiq/ARQ), o se separan? ¿Upstash (serverless) o ElastiCache (gestionado)?
5. **Cola:** ¿Se operan workers en contenedores o se usa managed (Cloud Tasks/SQS)?
6. **Backups:** ¿Cuál es el RPO/RTO aceptable para el MVP? ¿Se necesita PITR o backups diarios son suficientes?
7. **Capacidad de biblioteca por plan (P-005) y límites de usuarios por org (P-006):** afectan dimensionamiento de storage y BD.
8. **Tiering de tenants:** ¿Se prevén clientes enterprise que requieran aislamiento dedicado (silo) en el MVP o solo en fases posteriores?

---

## 14. Lista de datos marcados como "Hipótesis" o "Pendiente"

### Hipótesis

- H-01: Para un MVP con equipo Python y backend FastAPI, un PostgreSQL "puro" (Neon o RDS) puede ser más adecuado que Supabase completo, porque Supabase añade una capa de API/auth/storage que puede solaparse con FastAPI. (pendiente de validación con el usuario).
- H-02: El coste de infraestructura (sin IA) para el MVP es del orden de 20-200 USD/mes, dominado por la BD y el cache en el stack low-cost, y por backups/PITR en el stack managed. (requiere validación con prototipo).
- H-03: El coste de storage temporal es negligible frente al storage permanente y al egress. (pendiente de medición).
- H-04: Para un MVP con miles de imágenes servidas a usuarios y a Instagram, el egress puede ser el mayor coste de infraestructura después de la IA. Usar R2/B2 (egress gratis) o CloudFront reduce costes significativamente. (pendiente de medición de tráfico real).
- H-05: Si se usa Celery/RQ/Dramatiq con Redis como broker, reutilizar el mismo Redis para cache/sesiones/rate limiting reduce costes y complejidad. (pendiente de validación arquitectónica).
- H-06: Para un MVP, Dramatiq o ARQ sobre Redis es el punto óptimo de simplicidad/capacidad. Celery solo si se requiere scheduling complejo. (pendiente de validación con el equipo).
- H-07: Para un MVP, backups diarios con 7 días de retención y PITR son suficientes; la replicación cross-region es overkill. (pendiente de definir RPO/RTO).
- H-08: El overhead de RLS es bajo si se siguen las buenas prácticas (columna `tenant_id` indexada, política simple con `current_setting`, connection pooling). No es un bloqueo para el MVP. (basado en benchmarks de terceros; requiere verificación en este workload).
- H-09: R2 y B2 pueden tener latencia aceptable desde Argentina para servir imágenes (Cloudflare tiene edge en Buenos Aires). (pendiente de prueba de latencia).
- H-10: El coste de ElastiCache en sa-east-1 es ~59% mayor que en us-east-1 (markup estimado por analogía con EC2). (requiere verificación).

### Pendiente (requiere investigación o autorización)

- P-001 a P-007, P-009 a P-012, P-015 (de docs/decisions/README.md).
- P-005: capacidad de biblioteca por plan (afecta dimensionamiento de storage).
- P-006: límite de integrantes por organización (afecta dimensionamiento).
- P-008: políticas de Apple/Google para compra in-app en Argentina.
- P-010: requisitos de WhatsApp para Estados y difusiones (Fase 2).
- P-011: stack tecnológico (este informe es insumo, no decisión).
- Disponibilidad de Neon en sa-east-1 (no confirmada).
- Costes exactos de RDS/Aurora/ElastiCache/CloudFront en sa-east-1 (precios regionales superiores a us-east-1; requiere cotización o calculator).
- Disponibilidad de Vertex AI / Gemini y Azure OpenAI en Santiago/Chile Central.
- Precios exactos de Cloud Tasks y SQS (fuentes secundarias pueden estar desactualizadas).
- Disponibilidad de Bedrock en AWS Chile (dentro del primer año, según AWS).
- Proveedores de IA adicionales (Anthropic, Black Forest Labs, Recraft, Seedream, Ideogram) sin fuente oficial verificada.
- Validación legal (Ley 25.326) — requiere asesoramiento profesional (P-015).

---

## 15. Fuentes principales (con fecha de consulta 2026-11-27)

- Supabase pricing: https://supabase.com/pricing
- Supabase storage pricing: https://supabase.com/docs/guides/storage/pricing
- Supabase lifecycle policies: https://supabase.com/docs/guides/storage/buckets/lifecycle-policies
- Neon pricing: https://neon.com/pricing
- AWS RDS pricing: https://aws.amazon.com/rds/pricing
- AWS Aurora pricing: https://aws.amazon.com/aurora/pricing
- AWS S3 pricing (sa-east-1): https://aws.amazon.com/s3/pricing?region=sa-east-1
- AWS S3 pricing por región (terceros): https://cloudcostdb.com/aws/storage/object/standard
- AWS ElastiCache pricing: https://aws.amazon.com/elasticache/pricing
- AWS CloudFront pricing: https://aws.amazon.com/cloudfront/pricing
- AWS Bedrock region compatibility: https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html
- AWS Local Zones: https://aws.amazon.com/about-aws/global-infrastructure/localzones/features
- AWS Chile region: https://aboutamazon.com/news/aws/aws-south-america-chile-region-launch
- Cloudflare R2 pricing: https://developers.cloudflare.com/r2/pricing
- Backblaze B2 pricing: https://backblaze.com/pricing
- Google Cloud SQL pricing: https://cloud.google.com/sql/pricing
- Google Cloud Pub/Sub pricing: https://cloud.google.com/pubsub/pricing
- Upstash Redis pricing: https://upstash.com/pricing/redis
- GCP regions: https://cloud.google.com/about/locations
- PostgreSQL multi-tenancy (AWS): https://docs.aws.amazon.com/prescriptive-guidance/latest/saas-multitenant-managed-postgresql/
- PostgreSQL multi-tenancy (ClickHouse): https://clickhouse.com/resources/engineering/multi-tenant-saas-postgres-architecture
- RLS performance (dev.to): https://dev.to/ashwin_sridhar_koto7/does-postgres-rls-actually-ruin-performance-lets-look-at-the-data-24jf
- RLS caveats: https://pineido.com (citado en informe previo)
- Latencia Argentina: https://pingcloud.io/best-region-by-country/2026-07/argentina
- AWS geography tax (São Paulo): https://cloudcostdb.com/blog/aws-geography-tax
- Celery/Dramatiq/RQ comparativas: https://bigiron.cc/guides/self-hosted-celery-vs-rq-vs-dramatiq-python-task-queues
- Dramatiq: https://dramatiq.io/motivation.html
- ARQ: https://github.com/samuelcolvin/arq
- Instagram Content Publishing: https://developers.facebook.com/docs/instagram-platform/content-publishing
- Cloud Tasks: https://cloud.google.com/tasks/pricing (citado vía fuentes secundarias)
- RDS backups: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html

---

*Fin del informe. Este documento es material de investigación y no constituye una decisión, especificación ni plan aprobado. Las decisiones de proveedor, región y arquitectura requieren autorización explícita del usuario (constitución §3, §4.13).*