# MakeUrImages (nombre de trabajo)

> Nombre provisional tomado de la carpeta del repositorio. El nombre definitivo del producto está pendiente de decisión.

Plataforma SaaS para crear imágenes y textos promocionales con inteligencia artificial y publicarlos en redes sociales. Primera versión para Android e iOS, con mercado inicial en Argentina.

## Estado actual

Fase 0: definición del producto y preparación de la metodología de desarrollo guiado por especificaciones (SDD).

- No existe código de aplicación.
- No hay comandos de instalación, ejecución ni pruebas verificados.
- El stack tecnológico, la arquitectura y los proveedores **no están aprobados**. Se investigarán en una etapa posterior.

## Alcance del MVP (aprobado en la etapa de definición)

Recorrido principal: configurar cuenta → configurar identidad de marca → cargar contenido → seleccionar estilo y formato → generar imagen y texto → revisar y editar de forma limitada → guardar → publicar (Instagram) o compartir manualmente (WhatsApp).

Detalle en `docs/product/product-definition.md`.

## Documentación

- `AGENTS.md`: reglas operativas para agentes de IA.
- `MEMORY.md`: memoria persistente del proyecto (decisiones y estado vigente).
- `tasks.md`: seguimiento macro de la planificación y el desarrollo.
- `docs/constitution.md`: principios no negociables del proyecto.
- `docs/workflow.md`: proceso SDD, estados y aprobaciones.
- `docs/product/product-definition.md`: definición funcional del producto.
- `docs/architecture.md`: arquitectura de alto nivel (pendiente de la etapa técnica).
- `docs/roadmap.md`: fases del producto.
- `docs/decisions/`: decisiones registradas (confirmadas, propuestas y pendientes).
- `docs/specs/`: especificaciones funcionales y sus planes técnicos.
- `docs/agent-context/`: contexto modular para agentes y referencias de investigación.
- `skills/spec-generator/`: procedimiento y plantillas para especificaciones, planes y tareas.

## Metodología

Desarrollo guiado por especificaciones (SDD). Ninguna funcionalidad se implementa sin una especificación aprobada y un plan técnico aprobado. Ver `docs/workflow.md`.

## Licencia

Pendiente de decidir.
