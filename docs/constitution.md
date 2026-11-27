# Constitución del proyecto

Principios no negociables. Cualquier cambio requiere aprobación explícita del usuario y debe registrarse en `docs/decisions/`.

## 1. Seguridad

1. Las claves de API de proveedores de IA, redes sociales y pagos **nunca** se envían a las aplicaciones móviles ni a la web. Todas las llamadas externas pasan por el backend.
2. Los tokens de redes sociales se almacenan cifrados y solo son accesibles al backend.
3. Toda operación valida autenticación y permisos en el servidor. La interfaz nunca es la única barrera.
4. Ningún secreto, token o credencial real se escribe en el repositorio.

## 2. Aislamiento y privacidad

5. La información de cada espacio de trabajo (personal u organización) está aislada desde el diseño. Ninguna consulta puede devolver datos de otro espacio sin autorización explícita.
6. Los archivos temporales se eliminan al cerrar la sesión de creación. Esta regla es fija.
7. Los datos personales se tratan con el principio de minimización: solo se recopila lo necesario para la función.
8. Cualquier conservación de archivos originales requiere consentimiento explícito del usuario.

## 3. Integridad de la información

9. La información factual (precios, teléfonos, direcciones, nombres, fechas y características) se conserva exactamente como la proporcionó el usuario.
10. Ninguna instrucción textual al modelo de IA se considera garantía de exactitud. Toda información factual requiere un mecanismo de verificación antes de publicar.
11. El usuario siempre revisa el contenido antes de publicarlo en el MVP.

## 4. Control de alcance

12. Una funcionalidad solo se implementa con una especificación aprobada y un plan técnico aprobado.
13. Los cambios de comportamiento, arquitectura, stack o proveedores requieren autorización del usuario.
14. Se implementa el MVP definido. Las funcionalidades futuras se registran en `docs/roadmap.md` y no se desarrollan sin aprobación.
15. No se incorporan dependencias ni herramientas sin justificación documentada.

## 5. Calidad y mantenibilidad

16. Cada módulo tiene responsabilidades claras y dependencias explícitas. Ver `docs/architecture.md`.
17. Las reglas de negocio críticas (créditos, permisos, aprobaciones, publicación) cuentan con pruebas automatizadas antes de considerarse terminadas.
18. La documentación se mantiene sincronizada con el código. Una tarea no se cierra si cambia el comportamiento sin actualizar la especificación.

## 6. Economía y sostenibilidad

19. Ningún precio, cantidad de créditos o límite de plan se considera definitivo sin aprobación del usuario.
20. El consumo de IA debe ser verificable y registrado en el backend.
21. Las decisiones de proveedor se toman con costes reales, verificados contra tarifas oficiales con fecha de consulta.

## 7. Transparencia con agentes

22. Los agentes distinguen entre hecho verificado, recomendación, hipótesis y decisión pendiente.
23. Los agentes no toman decisiones de arquitectura, alcance o negocio por su cuenta.
24. Los agentes no modifican configuraciones globales, repositorios de referencia ni historial Git sin autorización.
