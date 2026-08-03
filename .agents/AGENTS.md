# Reglas Globales del Proyecto — Kit de Agentes Groq CLI

## Idioma
- Todas las respuestas y documentación DEBEN estar en **español**.
- Los nombres de variables, funciones y clases pueden estar en inglés o español según preferencia del usuario.
- Los comentarios en código DEBEN estar en español.

## Convenciones Generales
- Sigue las convenciones del lenguaje de programación que se esté utilizando.
- Prioriza legibilidad sobre brevedad.
- Documenta el **por qué**, no el **qué** (el código debe ser auto-descriptivo).

## Calidad de Código
- Aplica principios **SOLID** en código orientado a objetos.
- Aplica principios **DRY** (Don't Repeat Yourself) y **KISS** (Keep It Simple).
- Máximo 20 líneas por función/método.
- Máximo 3 parámetros por función (usa objetos para más).
- Nombra variables y funciones de forma descriptiva.
- Es **OBLIGATORIO** usar el skill `@skill:revisor-clean-code` cada vez que se cree o modifique código fuente para asegurar las buenas prácticas.

## Seguridad
- NUNCA hardcodees secrets, API keys o contraseñas en el código.
- SIEMPRE usa variables de entorno para configuración sensible.
- SIEMPRE valida y sanitiza entrada del usuario.
- NUNCA expongas stack traces o detalles internos en producción.

## Colaboración entre Agentes
- Los agentes pueden referenciarse entre sí usando `@skill:nombre-del-agente`.
- El @skill:agente-backend DEBE documentar contratos de API para el @skill:agente-frontend.
- El @skill:agente-frontend DEBE comunicar dependencias de datos al @skill:agente-backend.
- El @skill:agente-qa valida la integración entre frontend y backend.
- El @skill:agente-testing genera tests unitarios y de integración.
- El @skill:agente-seguridad audita el código de todos los demás agentes.
- El @skill:agente-codigo revisa la calidad del código producido.
- El @skill:agente-documentacion documenta el trabajo de todos los agentes.
- El @skill:agente-arquitectura define la estructura y patrones del proyecto.

## Estructura del Proyecto
- Sigue la estructura de carpetas recomendada por el framework utilizado.
- Mantén una separación clara entre código, tests y configuración.
- Usa un `.gitignore` apropiado desde el inicio.
