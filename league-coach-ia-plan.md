# League Coach IA — Plan de proyecto

> Estado: definición inicial  
> Modalidad prioritaria: **Clasificatoria Flexible**  
> Idioma: español  
> Enfoque: análisis **post-partida** y mejora personal basada en evidencia

## 1. Idea

Crear una aplicación web local —con posibilidad de empaquetarla como escritorio más adelante— que funcione como coach personal para League of Legends. La aplicación importará mis partidas, calculará métricas y patrones verificables, y usará Groq para explicar qué estoy haciendo bien, qué debo mejorar y qué practicar en las siguientes sesiones.

El sistema no busca entrenar un modelo desde cero. En su lugar, construirá un perfil progresivo del jugador a partir de estadísticas, eventos de partida, objetivos declarados y feedback sobre los consejos recibidos.

## 2. Contexto del jugador

- Juego frecuentemente con amigos.
- Mi modalidad competitiva preferida es **Clasificatoria Flexible**.
- La evaluación debe interpretar los resultados considerando que el grupo puede variar entre partidas.
- El foco es mi rendimiento individual y mi contribución al equipo, no culpar ni puntuar a compañeros.
- La aplicación deberá permitir filtrar, por lo menos, por cola, campeón, rol, parche y periodo.

## 3. Alcance del MVP

### Incluido

- Importar mi cuenta de Riot y mi historial de partidas.
- Priorizar partidas de **Ranked Flex** mediante su `queue_id` correspondiente, configurable y validado desde datos de Riot.
- Guardar detalles de partidas y timelines cuando estén disponibles.
- Calcular métricas personales por partida y tendencias de 10, 20 y 50 partidas.
- Analizar desempeño por campeón, rol, lado del mapa, parche y grupo de amigos cuando se pueda identificar de forma permitida.
- Generar un análisis post-partida o por sesión mediante Groq.
- Mostrar fortalezas, áreas de mejora, evidencia y un plan breve para la próxima sesión.
- Registrar mi evaluación de cada consejo: útil, no útil, ya lo sabía, quiero profundizar.

### Fuera del alcance inicial

- Recomendaciones en tiempo real durante una partida.
- Overlay que indique decisiones, rutas, objetivos o acciones mientras juego.
- Automatización de acciones o interacción con el cliente de League.
- Evaluar, insultar, señalar o asignar responsabilidad a compañeros.
- Publicar el producto para otros usuarios antes de validar cumplimiento y seguridad.

## 4. Principios del coach

1. **Los cálculos producen los hechos; la IA los explica.** Groq nunca debe inventar estadísticas ni eventos.
2. **Toda recomendación necesita evidencia.** Debe mostrar muestra, periodo y limitaciones.
3. **Máximo tres prioridades por análisis.** Evitar listas largas e imposibles de aplicar.
4. **Evaluar progreso controlable.** No depender únicamente de LP, victorias o derrotas.
5. **Contexto de Flex.** Una partida con premade no se interpreta igual que una Solo/Duo: se priorizan coordinación, objetivos, visión compartida, rotaciones y contribución propia.
6. **Cumplimiento de Riot.** El producto será estrictamente de revisión antes o después de las partidas.

## 5. Ejemplo de análisis deseado

> En tus últimas 12 partidas de Clasificatoria Flexible con Viego, participaste en menos objetivos tempranos en las derrotas y moriste antes de dragón en 4 de 6 de ellas. La evidencia sugiere que el problema principal es llegar tarde o entrar sin prioridad de líneas, no tu daño total. En la próxima sesión, llega al río 45 segundos antes del objetivo y confirma el estado de mid y bot antes de cruzar visión enemiga.

El texto anterior es una guía de estilo. La aplicación solo podrá dar una conclusión equivalente si los datos calculados realmente la respaldan.

## 6. Arquitectura propuesta

```text
Frontend React / TypeScript (Fase 5 - En proceso)
          |
          v
Backend FastAPI (Python) (Refactorizado Clean Code)
          |
          +-- Riot API: cuenta, historial, detalles y timelines
          +-- Motor de métricas (MetricsEngine) y detección de patrones
          +-- Motor de Prioridades (PriorityEngine): Filtra los 3 peores errores y los 3 mejores aciertos (fortalezas) por rol
          +-- PostgreSQL: perfil, partidas, métricas, insights y feedback
          +-- Groq API (Llama 3.1): explicación estructurada de la evidencia
```

### Tecnologías

| Capa | Propuesta | Motivo |
|---|---|---|
| Frontend | React + TypeScript + Vite | Interfaz moderna, tipada y rápida de iterar |
| Backend | Python + FastAPI | APIs claras y buen ecosistema analítico |
| Datos | PostgreSQL; SQLite en prototipo | Persistencia sólida y migrable |
| ORM | SQLAlchemy + Alembic | Modelos, consultas y migraciones |
| IA | Groq API desde backend | Mantener claves privadas y controlar costos |
| Infraestructura | Docker Compose | Mismo entorno en Windows y Debian |
| Gráficas | Recharts o Plotly | Tendencias comprensibles de métricas |

## 7. Datos y métricas

### Datos por partida

- Identificador de partida, fecha, duración, parche y cola.
- Campeón, rol, lado azul/rojo y resultado.
- KDA, participación en asesinatos, daño, daño recibido y daño a objetivos.
- CS/min, oro/min, experiencia/min y diferencias tempranas cuando estén disponibles.
- Wards, control wards, visión/min y limpieza de visión.
- Dragones, Heraldo, Barón, torres e inhibidores: participación o contexto temporal.
- Eventos relevantes del timeline: muertes, objetivos, recalls, torres y ventanas previas a objetivos.

### Métricas iniciales

| Área | Métricas |
|---|---|
| Economía | CS/min, oro/min, diferencia de oro al minuto 10 y 15 |
| Supervivencia | Muertes/min, rachas, muertes antes de objetivos |
| Objetivos | Participación en dragones, Heraldo, Barón y torres |
| Visión | Wards colocados, control wards, visión/min, wards eliminados |
| Combate | Participación en asesinatos, daño/min, daño a objetivos |
| Consistencia | Rendimiento por campeón, rol, parche y últimas 10/20/50 partidas |
| Flex | Participación en objetivos de equipo, preparación previa, contribución personal en victorias y derrotas |

### Reglas de interpretación

- No concluir que una derrota tiene una única causa.
- No usar una métrica aislada como diagnóstico definitivo.
- Comparar primero contra mi propio historial y contra el mismo campeón/rol cuando sea posible.
- Mostrar tamaño de muestra; por ejemplo, no presentar una conclusión fuerte con solo dos partidas.
- Separar hechos, hipótesis y acciones recomendadas.

## 8. Integración de Groq

Groq recibirá un paquete JSON pequeño y validado, no los datos completos sin procesar. Esto reduce coste, evita conclusiones sin fundamento y hace las respuestas consistentes.

### Contrato de entrada simplificado

```json
{
  "player_context": {
    "preferred_queue": "RANKED_FLEX_SR",
    "goals": ["mejorar coordinación y decisiones de objetivo"]
  },
  "sample": {"matches": 20, "period": "2026-07-01 a 2026-07-16"},
  "metrics": {},
  "top_priorities": [],
  "top_strengths": [],
  "recent_matches": []
}
```

### Contrato de salida simplificado

```json
{
  "summary": "...",
  "strengths": [{"claim": "...", "evidence": "..."}],
  "priorities": [
    {
      "title": "...",
      "evidence": "...",
      "confidence": "medium",
      "action": "...",
      "success_metric": "..."
    }
  ],
  "next_session_plan": ["..."]
}
```

### Prompt de sistema

```text
Eres un coach post-partida de League of Legends.
Solo puedes usar la evidencia estructurada proporcionada.
No inventes estadísticas, eventos, parches ni habilidades.
No des instrucciones para una partida activa ni sugieras software que cree ventaja injusta.
No culpes a compañeros ni atribuyas una derrota a una única causa.
Ten presente que la cola preferida del jugador es Clasificatoria Flexible y que juega frecuentemente con amigos.
Distingue hechos, hipótesis y recomendaciones.
Prioriza como máximo tres áreas de mejora.
Cada recomendación debe incluir evidencia, acción concreta y métrica para hacer seguimiento.
Responde en español claro y devuelve JSON válido según el esquema solicitado.
```

## 9. Modelo de datos mínimo

```text
players
- id
- puuid
- riot_id
- tag_line
- region
- preferred_queue
- preferred_role
- goals_json

matches
- match_id
- game_creation
- game_duration
- queue_id
- queue_name
- patch
- raw_match_json
- raw_timeline_json

player_match_metrics
- match_id
- player_id
- champion
- role
- win
- cs_per_min
- gold_per_min
- vision_per_min
- kill_participation
- deaths_before_objectives
- gold_diff_10
- gold_diff_15

objective_events
- id
- match_id
- objective_type
- timestamp
- player_participated
- player_dead_before_event

insights
- id
- player_id
- period_start
- period_end
- category
- evidence_json
- confidence
- generated_analysis

feedback
- id
- insight_id
- rating
- user_note
- applied_in_next_session
```

## 10. Plan por fases

### Fase 0 — Definición y cumplimiento

**Objetivo:** definir el MVP y documentar límites de Riot antes de programar.

**Entregables:**

- `README.md`
- `docs/product-scope.md`
- `docs/riot-compliance.md`
- `docs/player-profile-schema.md`
- `docs/phase-00-definition.md`

**Prompt sugerido:**

```text
Actúa como product manager y arquitecto de software.
Estoy creando un coach post-partida de League of Legends para uso personal.
Mi cola principal es Clasificatoria Flexible porque juego frecuentemente con amigos.

Define el alcance de un MVP individual con FastAPI, React y PostgreSQL.
Debe analizar exclusivamente partidas terminadas y cumplir las políticas de Riot.
Genera docs/product-scope.md con problema, historias de usuario, requisitos, casos fuera de alcance y criterios de éxito.
Al terminar, crea docs/phase-00-definition.md con decisiones tomadas, archivos modificados y próximos pasos.
```

### Fase 1 — Fundación técnica

**Objetivo:** crear el monorepo y ejecutar frontend, backend y base de datos localmente.

**Entregables:**

- `frontend/`
- `backend/`
- `docker-compose.yml`
- `.env.example`
- Endpoint `GET /health`
- Migración inicial
- `docs/phase-01-foundation.md`

**Prompt sugerido:**

```text
Crea el esqueleto de un monorepo para un coach post-partida de League of Legends.

Tecnologías:
- React, TypeScript y Vite
- Python, FastAPI, SQLAlchemy y Pydantic
- PostgreSQL
- Docker Compose

Condiciones:
- No incluir claves reales
- Crear .env.example
- Separar configuración, rutas, servicios y modelos
- Añadir endpoint GET /health
- Añadir README con instrucciones para Windows y Linux
- Crear docs/phase-01-foundation.md con cambios, comandos de ejecución y decisiones técnicas
```

### Fase 2 — Ingesta de Riot API

**Objetivo:** importar y persistir mis partidas de Clasificatoria Flexible.

**Entregables:**

- Resolución de Riot ID y tag a PUUID.
- Descarga de historial de partidas.
- Filtro y persistencia prioritaria de Ranked Flex.
- Descarga de detalles y timeline cuando exista.
- Prevención de duplicados, reintentos y control de rate limits.
- Tests con respuestas simuladas.
- `docs/phase-02-riot-ingestion.md`.

**Prompt sugerido:**

```text
Implementa un módulo Riot API en FastAPI para importar partidas de League of Legends.

Debe:
- Resolver Riot ID y tag a PUUID
- Obtener partidas recientes por PUUID
- Priorizar y filtrar Clasificatoria Flexible usando el queue_id oficial configurable
- Descargar detalle de cada partida y timeline cuando esté disponible
- Guardar JSON original y entidades normalizadas en PostgreSQL
- Evitar duplicados por match_id
- Usar RIOT_API_KEY desde variables de entorno
- Manejar 429, 404 y 5xx de forma segura
- Incluir tests con mocks
- Crear docs/phase-02-riot-ingestion.md con decisiones, endpoints y limitaciones
```

### Fase 3 — Motor de métricas

**Objetivo:** transformar datos de partidas en métricas e insights explicables.

**Entregables:**

- Tabla `player_match_metrics`.
- Cálculos por partida, campeón, rol y ventana de tiempo.
- Tendencias de 10, 20 y 50 partidas Flex.
- Detectores de patrones con evidencia.
- Endpoint `GET /analytics/summary`.
- `docs/phase-03-analytics.md`.

**Prompt sugerido:**

```text
Implementa un motor analítico explicable para el coach de League of Legends.

Entrada: partidas normalizadas y timelines del jugador.
Salida: métricas por partida, promedios de 10/20/50 partidas, tendencias y patrones con evidencia.

La cola prioritaria es Clasificatoria Flexible; calcula también indicadores de contribución a objetivos y preparación previa a objetivos.
No uses IA para calcular métricas.
Cada insight debe incluir fórmula, muestra, periodo, evidencia y limitaciones.
Incluye tests con datos simulados y crea docs/phase-03-analytics.md.
```

### Fase 4 — Coach con Groq

**Objetivo:** redactar recomendaciones personalizadas a partir de evidencia calculada.

**Entregables:**

- Perfil editable: objetivos, rol y campeones.
- Paquete de evidencia JSON.
- Cliente Groq en backend.
- Respuesta JSON validada con Pydantic.
- Almacenamiento de análisis y feedback.
- `docs/phase-04-groq-coach.md`.

**Prompt sugerido:**

```text
Integra Groq API en el backend FastAPI de un coach post-partida de League of Legends.

Groq debe recibir solo evidencia calculada y responder JSON validable.
El usuario juega principalmente Clasificatoria Flexible con amigos.
Las recomendaciones deben enfocarse en rendimiento individual, coordinación y objetivos, sin culpar a compañeros.

Implementa:
- esquema Pydantic de entrada y salida
- prompt de sistema seguro
- servicio con manejo de errores y timeout
- persistencia del análisis
- feedback útil/no útil/ya lo sabía/quiero profundizar
- tests simulando respuestas del modelo
- docs/phase-04-groq-coach.md
```

### Fase 5 — Dashboard

**Objetivo:** presentar progreso y coaching de forma comprensible.

**Pantallas:**

- Inicio: resumen de últimas 10 partidas Flex.
- Partida: estadísticas, eventos y lecciones.
- Campeones: tendencias y desempeño por campeón.
- Tendencias: economía, visión, muertes y objetivos.
- Coach: análisis de sesión y plan de práctica.
- Perfil: metas y feedback.

**Prompt sugerido:**

```text
Construye las pantallas React para un coach post-partida de League of Legends.
Prioriza visualización de Clasificatoria Flexible.

Incluye páginas Inicio, Partida, Campeones, Tendencias, Coach y Perfil.
Muestra evidencia, tamaño de muestra y limitaciones junto a los insights.
No presentes métricas aisladas como verdades absolutas.
Usa datos mock tipados y crea docs/phase-05-dashboard.md.
```

### Fase 6 — Evaluación

**Objetivo:** verificar que el coach produce aprendizaje práctico.

**Indicadores:**

- Reducción de muertes antes de objetivos.
- Mejora de CS/min u oro/min en el mismo campeón y rol.
- Mayor preparación y participación en objetivos.
- Cumplimiento de objetivos de práctica por sesión.
- Porcentaje de consejos marcados como útiles.
- Tendencias mantenidas durante 20 o más partidas, no solo una racha corta.

**Prompt sugerido:**

```text
Diseña un módulo de evaluación para el coach post-partida de League of Legends.
No uses solamente LP o tasa de victoria como medida de éxito.
Define indicadores controlables, línea base, ventanas de evaluación y criterios de mejora sostenida.
Incluye métricas pertinentes para Clasificatoria Flexible y crea docs/phase-06-evaluation.md.
```

## 11. Convención de documentación por fase

Al terminar cada fase, crear un archivo `docs/phase-XX-nombre.md` con esta plantilla:

```md
# Fase XX — Nombre

## Fecha

AAAA-MM-DD

## Objetivo

...

## Trabajo realizado

- ...

## Archivos creados o modificados

- `ruta/archivo.ext`: propósito

## Decisiones técnicas

- ...

## Cómo probarlo

```bash
# comandos exactos
```

## Resultado

- ...

## Problemas o deuda técnica

- ...

## Próxima fase

- ...
```

## 12. Orden práctico de desarrollo

1. Completar Fase 0 y definir tu Riot ID, región, rol y campeones prioritarios.
2. Crear la base técnica de Fase 1.
3. Importar 20 a 50 partidas Flex en Fase 2.
4. Validar manualmente que los datos importados coinciden con el cliente de League.
5. Implementar solo cinco métricas fiables en Fase 3.
6. Conectar Groq después de tener evidencia correcta en Fase 4.
7. Construir el dashboard cuando ya existan datos reales.
8. Usar el producto durante varias sesiones y medir si los consejos cambian comportamientos concretos.

## 13. Seguridad y costes

- Guardar `RIOT_API_KEY` y `GEMINI_API_KEY` exclusivamente en variables de entorno.
- No exponer claves en frontend, repositorio ni capturas de pantalla.
- Solicitar análisis de Groq bajo demanda y guardar el resultado para evitar llamadas repetidas.
- Enviar a Groq resúmenes estructurados, no todos los JSON completos de Riot.
- Mantener los datos de la cuenta como información privada; preparar exportación y borrado local.

## 14. Próximo paso

**Fase 5 (Dashboard y Frontend)**: Habiendo completado exitosamente las Fases 0, 1, 2, 3 y 4 (que culminaron en la refactorización profunda del backend, la implementación de métricas premium, el PriorityEngine y la inyección a Groq), el siguiente paso es maquetar la Interfaz Visual (UI) en React/TypeScript para presentar todos estos *insights* y el plan de entrenamiento al jugador de forma atractiva.
