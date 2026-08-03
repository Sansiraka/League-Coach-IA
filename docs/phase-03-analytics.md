# Fase 03 — Motor de Métricas (Analytics Engine)

## Fecha
2026-07-17

## Objetivo
Transformar los datos crudos JSON descargados de la API de Riot en métricas matemáticas limpias, calculadas localmente sin necesidad de IA, para proporcionar la "evidencia" factual sobre la que operará el futuro coach.

## Trabajo realizado
- **Modelos de Base de Datos:** Creación de `PlayerMatchMetrics` (para almacenar el desempeño de cada partida analizada) e `Insight` (para almacenar las conclusiones agregadas).
- **Lógica de Análisis (`MetricsEngine`):**
  - **CS/min y Vision/min:** Calculado cruzando las estadísticas totales con la duración de la partida.
  - **Kill Participation (KP%):** Obtenido relacionando los derribos del jugador con los de su equipo.
  - **Muertes antes de Objetivos:** Recorriendo el `Timeline` de la partida (evento por evento), el motor detecta la caída de Monstruos Épicos (Dragones, Barones, Heraldos) y cruza la línea de tiempo de muertes del jugador. Si la muerte ocurre dentro de un umbral dinámico (30s en fase de líneas, 40s en mid game, 70s en late game), se cuenta como una penalización de objetivo.
- **Servicio y Exposición (`AnalyticsService`):**
  - Expone el endpoint `GET /analytics/summary/{game_name}/{tag_line}` para retornar agregados y promedios.
- **Motor de Prioridades (`PriorityEngine`):**
  - Evalúa y pondera matemáticamente los errores del jugador según el rol específico (ej. un ADC es castigado severamente por tener bajo CS, mientras que un Support no). Filtra todo el ruido y devuelve únicamente las **Top 3** áreas de mejora con mayor severidad.
- **Métricas Premium (Nivel Pro-Play):**
  - Integración de métricas avanzadas microscópicas extraídas de `challenges` (asesinatos 1v1, farmeo pre-10 minutos, robos de jungla épicos, control de escurridizos, salvamentos de aliados y reflejos/precisión de *skillshots*).
- **Refactorización Clean Code:**
  - Todo el código analítico fue sometido a una revisión estricta de buenas prácticas, modularizando funciones complejas (`metrics_engine.py` y `analytics_service.py`) bajo el Principio de Responsabilidad Única (SRP) y documentando todo exhaustivamente en español.

## Decisiones técnicas
- **Escalamiento del umbral de muertes:** Se integró la sugerencia de diseño donde la ventana de impacto de una muerte crece conforme avanza el tiempo de juego, reconociendo que los tiempos de reaparición son mucho más punitivos después de los 30 minutos.
- **Cacheo de resultados:** El motor no recalcula el historial en cada petición. Las métricas se guardan en BD una vez que el JSON se ha procesado, haciendo el endpoint inmediato.

## Resultado
La Fase 3 se declara **COMPLETA y en Estado de Producción Avanzado**. El motor puede procesar las 20 partidas del usuario y extraer métricas ultra-específicas de fase de líneas, visión, combate, y entregarle al motor de IA exclusivamente los 3 errores más perjudiciales ordenados por gravedad matemática.

## Próxima fase
- **Fase 4 (Integración con Groq):** Conectar el backend con la API de Google Groq, pasándole estas métricas recién calculadas para que genere un reporte/coaching actuable y no alucinatorio.
