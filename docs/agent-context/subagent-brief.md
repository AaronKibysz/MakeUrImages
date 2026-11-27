# Plantilla de encargo a subagente

Usar esta plantilla cada vez que se delegue una tarea. Un encargo sin estos campos se considera incompleto.

```markdown
## Encargo: <título corto>

**Objetivo:** <una frase, resultado esperado>

**Responsabilidad:** <qué le corresponde a este subagente y qué no>

**Alcance de archivos:**
- Puede leer: <rutas o patrones>
- Puede escribir: <rutas exactas>
- No debe tocar: <rutas o áreas reservadas>

**Contexto necesario:** <lista corta de documentos a leer>

**Restricciones:**
- No tomar decisiones de arquitectura, alcance, precios o proveedores.
- No modificar configuración de OpenCode, Git ni repositorios de referencia.
- No sobrescribir archivos existentes fuera de los permitidos.
- Marcar como "Hipótesis" o "Pendiente" lo que no pueda verificar.

**Formato de entrega:**
1. Resumen de 5 líneas como máximo.
2. Hallazgos con fuente y fecha de consulta cuando corresponda.
3. Archivos creados o modificados, con ruta.
4. Preguntas o bloqueos para el agente principal.

**Condición de finalización:** <criterio verificable>
```

## Reglas para el agente principal

- Sintetizar los informes antes de escribir en `docs/`.
- Verificar que el informe responde a la condición de finalización.
- Si dos subagentes necesitan el mismo archivo, no paralelizar: secuenciar.
- No delegar tareas triviales cuyo costo de contexto supere el beneficio.
