# Catálogo de Análisis y Métricas Implementadas — Coach IA

Este documento detalla todas las capacidades analíticas que nuestro Coach IA puede evaluar actualmente de las partidas de los jugadores. Sirve como fuente de la verdad para saber qué feedback puede dar el Coach de manera automática.

## 1. Benchmarks de Rendimiento Óptimo por Rol

El sistema no evalúa las estadísticas crudas de manera general, sino que las contextualiza según el rol del jugador en esa partida. Las métricas son evaluadas con un veredicto interno (`EXCEEDS_STANDARD`, `MEETS_STANDARD`, `BELOW_STANDARD`) basado en buenas prácticas establecidas.

### Métricas Evaluadas
*   **CS/Min (Súbditos por minuto)**
    *   *Mid*: Esperado > 7.5, Ideal > 8.5
    *   *ADC*: Esperado > 8.0, Ideal > 9.0
    *   *Top*: Esperado > 7.0, Ideal > 8.0
    *   *Jungle*: Esperado > 6.0, Ideal > 7.0
    *   *Support*: No aplicable.
*   **Visión/Min (Puntuación de visión por minuto)**
    *   *Support*: Esperado > 1.5, Ideal > 2.5
    *   *Jungle*: Esperado > 1.0, Ideal > 1.5
    *   *Mid/Top*: Esperado > 0.5 - 0.7
*   **Kill Participation (KP% - Participación en asesinatos)**
    *   *Jungla/Mid/ADC*: Esperado > 45%
    *   *Support*: Esperado > 50%
    *   *Top*: Esperado > 35% (varía si está haciendo split push)
*   **Muertes antes de Objetivos**
    *   Detecta si el jugador muere en una ventana crítica de tiempo antes de que se asegure un objetivo neutral importante (Dragones, Heraldos, Barón).
    *   *Ventana crítica*: Dinámica (30 segundos en *early game*, hasta 70 segundos en *late game*).

## 2. Métricas Avanzadas (Novedad v2)

Hemos integrado un profundo análisis de los detalles de partida (match details) y la línea temporal (timeline) para extraer métricas muy específicas por rol.

### Métricas de Timeline (Comparativas)
*   **Diferencia de Oro (Minuto 10, 15 y 25)**
    *   *Qué evalúa*: Calcula la diferencia exacta de oro entre el jugador y su oponente directo de línea en tres momentos críticos de la partida: Early, Mid y Late game.
    *   *Top/Mid/ADC*: Esperado > +300 oro (ventaja ligera), Ideal > +800 oro (ventaja aplastante).

### Métricas de Visión Avanzada (Para todos los roles)
*   **Wards Colocados y Destruidos**: Cuantifica la contribución bruta a la visión.
*   **Wards de Control Comprados**: Mide la inversión de oro en visión.
*   **Ventaja de Puntuación de Visión**: Compara la visión del jugador directamente con la de su oponente de línea.

### Análisis de Sinergia en Bot Lane
*   **Alerta de Robo de CS (Support)**: Detecta si un Support está denegando oro a su ADC aliado al farmear excesivamente durante la fase de líneas (min 10 y 15).

### Métricas Avanzadas de Combate y Utilidad
*   **% de Daño del Equipo (`team_damage_percentage`)**
    *   *Mid/ADC*: Esperado > 25%, Ideal > 30-35%.
*   **Daño Mitigado (`damage_mitigated`)**
    *   *Top/Support (Tanques)*: Mide cuánto daño crudo absorbió el jugador antes de reducciones. Esperado > 20,000, Ideal > 40,000 en partidas largas.
*   **Curación y Escudos Efectivos (`heal_shield_effective`)**
    *   *Support (Encantadores)*: Mide la cantidad de curación y escudos que *realmente evitaron daño* o restauraron vida. Ideal > 5,000 - 10,000.
*   **Tiempo Aplicando CC (`cc_time`)**
    *   *Support (Enganche)/Jungla (Tanque)*: Suma en segundos del tiempo que el jugador inmovilizó a enemigos. Esperado > 30s, Ideal > 60s.
*   **Placas de Torre Destruidas (`turret_plates`)**
    *   *Top/Mid/ADC*: Indica asedio en fase de líneas. Ideal > 2 placas tomadas.

## 3. Métricas Premium Específicas por Rol (Nivel Pro-Play)

Hemos añadido un paquete masivo de métricas avanzadas (extraídas del objeto `challenges` de Riot) que evalúan aspectos microscópicos de cada posición, las cuales son analizadas por nuestro nuevo **Motor de Prioridades** (`PriorityEngine`) para puntuar la gravedad o el éxito del jugador.

### Fase de Líneas Temprana (Early Game / Laners)
*   **Solo Kills (`solo_kills`)**: Número de asesinatos en 1v1 puro, sin asistencia. Indica dominio mecánico en línea.
*   **CS Minuto 10 (`lane_minions_first_10_minutes`)**: Minions puros farmeados antes del min 10 (Aísla la fase de líneas del resto del juego).
*   **Ventaja Máxima de Súbditos (`max_cs_advantage_on_lane_opponent`)**: Máxima brecha de súbditos generada contra el oponente de línea (Penalización severa si es <-20).
*   **Ventaja de Nivel (`max_level_lead_lane_opponent`)**: Indica si se le denegó experiencia (XP) al oponente.

### Dominio de la Jungla
*   **CS Temprano de Jungla (`jungle_cs_before_10_minutes`)**: Mide la eficiencia del *pathing* en los primeros campamentos.
*   **Escurridizos Asegurados (`scuttle_crab_kills`)**: Control del río (Penalización severa si es 0).
*   **Robos Épicos (`epic_monster_steals`)**: Número de robos de Barón, Dragón o Larvas usando Castigo (Smite).
*   **Nervios de Acero (`epic_monster_kills_near_enemy_jungler`)**: Asegurar objetivos mientras el jungla enemigo está en rango de robo.

### Soporte y Visión Extrema
*   **Salvavidas (`save_ally_from_death`)**: Veces que las curaciones/escudos salvaron explícitamente a un aliado de morir por daño inminente.
*   **Limpieza Temprana (`ward_takedowns_before_20m`)**: Wards enemigos destruidos antes del min 20 (Denegación de visión temprana).

### Micro-Mecánicas y Combate (Todos los roles)
*   **Reflejos (`skillshots_dodged`)**: Habilidades esquivadas.
*   **Precisión (`skillshots_hit`)**: Habilidades acertadas.
*   **Outplays (`outnumbered_kills`)**: Asesinatos logrados estando en inferioridad numérica (ej. 1v2, 1v3).
*   **Dives (`kills_near_enemy_turret`)**: Asesinatos logrados bajo la torre enemiga.

---

## 4. Inteligencia de Objetos Situacionales (Situational Awareness)

El sistema analiza si el jugador adapta su compra de objetos (`build`) a las amenazas concretas de la composición del equipo enemigo.

### Reglas Implementadas Actualmente

#### 2.1. Amenaza de Curación (Anti-Heal / Heridas Graves)
*   **Qué detecta:** Si la suma de las curaciones del equipo enemigo supera los 15,000 HP.
*   **Objetos que espera:** *Mortal Reminder, Morellonomicon, Thornmail, etc.*

#### 2.2. Amenaza de Daño Mágico (Resistencia Mágica / Anti-AP)
*   **Qué detecta:** Si el daño mágico del equipo enemigo representa más del 65% de su daño total.
*   **Objetos que espera:** *Maw of Malmortius, Kaenic Rookern, Force of Nature, etc.*

#### 2.3. Amenaza de Control de Masas (Tenacidad / Anti-CC)
*   **Qué detecta:** Si el equipo enemigo aplica más de 150 segundos de CC totales.
*   **Objetos que espera:** *Mercury's Treads, Sterak's Gage, etc.*

#### 2.4. Amenaza de Daño Físico (Armadura / Anti-AD)
*   **Qué detecta:** Si el daño físico del equipo enemigo representa más del 65% de su daño total.
*   **Objetos que espera:** *Plated Steelcaps, Thornmail, Randuin's Omen, Frozen Heart, etc.*

#### 2.5. Amenaza de Daño Concentrado (Anti-Burst)
*   **Qué detecta:** Si un solo campeón enemigo causa más del 40% del daño total de su equipo (jugador "fed").
*   **Objetos que espera:** *Zhonya's Hourglass, Guardian Angel, Sterak's Gage, etc.*

#### 2.6. Amenaza de Split Push (Empuje en solitario)
*   **Qué detecta:** (Solo para el rol de TOP) Si un campeón enemigo tiene más de 6,000 de daño a torres.
*   **Objetos/Hechizos que espera:** *Hullbreaker* o tener el hechizo de invocador *Teleport*.

---

> *Nota: Si deseas proponer nuevas reglas o métricas, por favor revisa primero esta lista. Si no está aquí, ¡podemos implementarlo en la próxima iteración!*
