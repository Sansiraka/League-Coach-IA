# Fase 00 — Definición e Inicialización

## Fecha
2026-07-16

## Objetivo
Definir el alcance, las políticas, el esquema de datos inicial y preparar las herramientas necesarias (skills/agentes) para construir un coach personal de League of Legends enfocado en la modalidad Clasificatoria Flexible.

## Trabajo realizado
- Revisión exhaustiva del documento del plan inicial (`league-coach-ia-plan.md`).
- Generación de `task.md` para el seguimiento en tiempo real del progreso.
- Creación de Skills especializados:
  - `agente-riot-api`
  - `agente-league-metrics`
  - `agente-groq-coach`
- Redacción de la documentación base de Fase 0:
  - Alcance del producto (`product-scope.md`).
  - Documento de validación contra políticas de Riot (`riot-compliance.md`).
  - Esquema de base de datos para el jugador (`player-profile-schema.md`).

## Archivos creados o modificados
- `.agents/skills/agente-riot-api/SKILL.md`: Instrucciones especializadas para consultas a la API de Riot.
- `.agents/skills/agente-league-metrics/SKILL.md`: Motor determinista para evitar IA al calcular CS, visión, KP.
- `.agents/skills/agente-groq-coach/SKILL.md`: Prompts y manejo del SDK de Groq para estructurar JSON sin alucinaciones.
- `docs/product-scope.md`: Requerimientos e historias de usuario.
- `docs/riot-compliance.md`: Declaración y límites de operación para cumplir con ToS de Riot.
- `docs/player-profile-schema.md`: Representación del jugador y sus metas en BD.
- `docs/phase-00-definition.md`: (Este documento).

## Decisiones técnicas
- **Separación de roles en Agentes:** Para evitar la superposición de contextos y disminuir el riesgo de que un LLM intente inventar resultados, se han creado 3 habilidades lógicas que encapsulan de manera estricta el acceso a datos brutos, las matemáticas y el texto final pedagógico.
- **Formato Post-Partida:** El sistema operará 100% sobre datos de partidas finalizadas usando JSON locales, por lo cual es completamente legal frente al Vanguard de Riot.

## Cómo probarlo
La Fase 0 es documental y organizativa, los resultados pueden revisarse directamente leyendo los archivos en la carpeta `docs/` y `.agents/skills/`.

## Resultado
La Fase 0 se declara **COMPLETA**. Tenemos reglas firmes sobre lo que se va a construir, las directrices de seguridad de Riot mapeadas, y la inteligencia distribuida en los archivos de Skill para que actúen como la hoja de ruta técnica.

## Próxima fase
- **Fase 1 (Fundación Técnica):** Inicializar los subproyectos (Backend FastAPI + Frontend React/Vite) y configurar Docker y PostgreSQL.
