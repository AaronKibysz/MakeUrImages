# Referencias

Fuentes de patrones y buenas prácticas. Se consultan para mejorar la configuración de agentes. **No se copian prompts completos ni se asume que son documentación oficial.**

## Proyectos propios (solo lectura)

| Referencia | Uso previsto | Estado |
|---|---|---|
| TDL (`AaronKibysz/TDL`) | Estructura SDD: AGENTS.md, MEMORY.md, README, tasks.md, docs/, skills/spec-generator/ | Estructura revisada. Base de esta documentación. |
| AAProject (`AaronKibysz/AAProject`) | React Native + Expo, FastAPI, PostgreSQL, SQLAlchemy, Alembic, capas, testing | Pendiente de revisión |
| HERRAMIENTA-DTF (`feature/fabric-7`) | Integración con IA, cuotas, consumo, procesamiento de imágenes, seguridad | Pendiente de revisión |
| DEVPulse (`AaronKibysz/DEVPulse`) | Modularización, documentación, gestión de agentes | Pendiente de revisión |

Ninguna de estas referencias se modifica.

## Repositorio de system prompts

`asgeirtj/system_prompts_leaks`: colección de system prompts publicados de distintos productos, organizada por proveedor. Para este proyecto interesan las secciones de Anthropic: Claude Code (subagentes, skills y prompts auxiliares) y Claude API tools.

**Advertencias**
- No es documentación oficial de Anthropic.
- El contenido puede no ser exacto ni vigente. Cada patrón debe verificarse antes de adoptarse.
- Se adaptan patrones, no se copian textos.

**Ámbitos de interés**
- Subagentes: responsabilidad, herramientas permitidas y formato de entrega.
- Planificación y exploración: separación entre investigación y ejecución.
- Gestión de contexto: cómo se resumen y se delegan tareas.
- Skills: estructura de instrucciones y criterios de activación.
- Uso de herramientas: restricciones y confirmaciones.

**Estado:** la estructura del repositorio fue revisada. El contenido de los prompts individuales todavía no se ha analizado. Esa revisión corresponde a la etapa de configuración de agentes y a la skill `agent-research` propuesta.

## Herramientas de interfaz

- 21st.dev (`https://21st.dev/`, `https://docs.21st.dev/`): pendiente de verificar compatibilidad con OpenCode, Expo y tecnologías web, licencias, autenticación y costes.
