# Métricas y Eventos de la API de Riot Games — Análisis por Rol

> **Propósito:** Este documento lista de forma exhaustiva **todos** los datos que arroja la API de Riot Games
> (Match-V5 Details + Match-V5 Timeline) y evalúa su relevancia para cada uno de los 5 roles:
> **Top**, **Jungle**, **Mid**, **ADC (Bot Carry)** y **Support**.
>
> **Convenciones:**
> - ✅ = Métrica relevante y medible para ese rol (se explica por qué).
> - ⚠️ = Parcialmente relevante o depende del contexto (se explica la condición).
> - ❌ = No es relevante o no aporta información útil para ese rol (se explica por qué).
> - ❓ = No tengo certeza suficiente para afirmar su relevancia; requiere validación adicional.
>
> **Fuentes de datos:** Los datos provienen de dos endpoints de la API Match-V5 de Riot Games:
> 1. `GET /lol/match/v5/matches/{matchId}` → Detalle de partida (resumen final).
> 2. `GET /lol/match/v5/matches/{matchId}/timeline` → Timeline minuto a minuto.

---

## Tabla de Contenidos

1. [Sección A — Métricas del Resumen de Partida (Match Details)](#sección-a--métricas-del-resumen-de-partida-match-details)
   1. [A.1 — Métricas Generales de Combate](#a1--métricas-generales-de-combate)
   2. [A.2 — Métricas de Daño](#a2--métricas-de-daño)
   3. [A.3 — Métricas de Economía](#a3--métricas-de-economía)
   4. [A.4 — Métricas de Visión](#a4--métricas-de-visión)
   5. [A.5 — Métricas de Objetivos y Estructuras](#a5--métricas-de-objetivos-y-estructuras)
   6. [A.6 — Métricas de Farmeo](#a6--métricas-de-farmeo)
   7. [A.7 — Métricas de Supervivencia y Durabilidad](#a7--métricas-de-supervivencia-y-durabilidad)
   8. [A.8 — Métricas de Utilidad y Soporte](#a8--métricas-de-utilidad-y-soporte)
   9. [A.9 — Métricas de Comunicación (Pings)](#a9--métricas-de-comunicación-pings)
   10. [A.10 — Campo `challenges` — Métricas Avanzadas de Riot](#a10--campo-challenges--métricas-avanzadas-de-riot)
2. [Sección B — Eventos del Timeline (Match Timeline)](#sección-b--eventos-del-timeline-match-timeline)
   1. [B.1 — Frames: Estado por Minuto (participantFrames)](#b1--frames-estado-por-minuto-participantframes)
   2. [B.2 — Eventos del Timeline](#b2--eventos-del-timeline)
3. [Sección C — Datos de Nivel Equipo (Team-Level)](#sección-c--datos-de-nivel-equipo-team-level)
4. [Sección D — Métricas que actualmente calculamos vs. lo posible](#sección-d--métricas-que-actualmente-calculamos-vs-lo-posible)

---

## Sección A — Métricas del Resumen de Partida (Match Details)

Estos datos provienen del campo `info.participants[]` del endpoint de detalle de partida.

---

### A.1 — Métricas Generales de Combate

#### `kills` — Asesinatos totales del jugador
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indicador de dominio de línea y capacidad de carry en split push o teamfights. |
| Jungle | ✅ | Refleja la eficacia de los ganks y la presión en el mapa. |
| Mid | ✅ | Indicador de dominio de línea, roams exitosos y capacidad de carry. |
| ADC | ✅ | Es el indicador principal de output de daño convertido en eliminaciones. |
| Support | ⚠️ | Los supports no buscan kills activamente; es más indicativo si "roba" kills vs. si está generando asistencias. Un support con muchos kills puede estar tomando oro de su ADC. |

#### `deaths` — Muertes totales del jugador
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Un exceso de muertes indica mal manejo de oleadas, dives fallidos o ganks no previstos. |
| Jungle | ✅ | Muertes frecuentes indican invasiones fallidas, mal pathing o falta de visión en objetivos. |
| Mid | ✅ | Muertes altas indican vulnerabilidad a ganks o mala gestión de trades. |
| ADC | ✅ | El ADC es el rol más dependiente de estar vivo para hacer DPS sostenido; cada muerte es muy costosa. |
| Support | ✅ | Aunque los supports mueren protegiendo aliados, un exceso indica mal posicionamiento en teamfights. |

#### `assists` — Asistencias totales
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Depende de si el Top participa en teamfights o juega split push. Un top que splitea legítimamente tendrá pocas asistencias pero puede generar presión de otra forma. |
| Jungle | ✅ | Las asistencias reflejan la participación en ganks y peleas de equipo; es una métrica central para junglas. |
| Mid | ✅ | Refleja roams exitosos y participación en teamfights. |
| ADC | ✅ | Complementa los kills para medir la participación total en combate del equipo. |
| Support | ✅ | Es la métrica central del support. Se espera que tengan las asistencias más altas del equipo. |

#### `killParticipation` (challenges) — Porcentaje de participación en asesinatos
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Puede ser naturalmente baja si juega split push sin agruparse. No necesariamente indica mal rendimiento. |
| Jungle | ✅ | Una KP alta es indicador de buen pathing y presencia constante en peleas. Se espera la KP más alta o segunda más alta del equipo. |
| Mid | ✅ | KP alta indica buenos roams y participación activa. Se espera que sea moderada-alta. |
| ADC | ✅ | KP alta indica que el ADC está presente en las peleas y convirtiendo daño en eliminaciones. |
| Support | ✅ | Se espera la KP más alta del equipo. Una KP baja indica desconexión del equipo o mal posicionamiento. |

#### `kda` (challenges) — Ratio (Kills + Assists) / Deaths
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indicador general de eficiencia en combate. |
| Jungle | ✅ | Un KDA alto demuestra ganks eficientes y buena supervivencia. |
| Mid | ✅ | Indica dominio de la línea y contribución a peleas. |
| ADC | ✅ | Un KDA alto es crítico; el ADC necesita estar vivo para generar DPS. |
| Support | ⚠️ | El KDA del support puede ser engañoso. Un support tanque con muchas muertes pero buenas asistencias puede estar cumpliendo su rol perfectamente al absorber daño. |

#### `firstBloodKill` / `firstBloodAssist` — Primera sangre
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Primera sangre en top puede generar una ventaja de línea decisiva (control de oleadas y placas). |
| Jungle | ✅ | Como jungla, conseguir o facilitar la primera sangre puede definir el ritmo temprano del juego. |
| Mid | ✅ | Primera sangre en mid otorga prioridad de línea y facilita roams tempranos. |
| ADC | ⚠️ | Relevante si ocurre en bot lane, pero a menudo depende más del support o del jungla. |
| Support | ✅ | El support que facilita primera sangre en bot lane genera una ventaja significativa para su ADC. |

#### `soloKills` (challenges) — Asesinatos 1v1
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indicador principal de dominio de línea. Las solo kills en top son frecuentes y muy significativas. |
| Jungle | ⚠️ | Pueden ocurrir en invasiones o duelos 1v1 en el river, pero no son el foco principal del jungla. |
| Mid | ✅ | Indica superioridad mecánica y conocimiento de matchups en la línea. |
| ADC | ⚠️ | Las solo kills son raras para ADC en fase de línea (juega 2v2), pero pueden indicar buen kiting en mid/late game. |
| Support | ❌ | Un support con solo kills es un escenario atípico. No debería usarse como indicador de rendimiento. |

#### `doubleKills` / `tripleKills` / `quadraKills` / `pentaKills` — Multikills
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Posible en teamfights si juega un top carry (Fiora, Irelia, Jax), pero no es el foco del rol. |
| Jungle | ⚠️ | Posible si el jungla es carry (Kindred, Graves), pero no es un indicador principal. |
| Mid | ✅ | Los mid laners tienen el mayor potencial de multikills por el daño en área (Katarina, Viktor). |
| ADC | ✅ | El ADC es el rol que más se espera que consiga multikills en teamfights prolongadas por su DPS sostenido. |
| Support | ❌ | No aplica. Un support no debería estar tomando multikills. |

#### `largestMultiKill` — Mayor multikill conseguida
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Mismo razonamiento que multikills. |
| Jungle | ⚠️ | Mismo razonamiento que multikills. |
| Mid | ✅ | Mismo razonamiento que multikills. |
| ADC | ✅ | Mismo razonamiento que multikills. |
| Support | ❌ | Mismo razonamiento que multikills. |

#### `killingSprees` / `largestKillingSpree` — Rachas de asesinatos
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indica consistencia en la dominancia de línea y capacidad de mantener ventaja sin morir. |
| Jungle | ✅ | Rachas altas indican ganks exitosos consecutivos sin morir. |
| Mid | ✅ | Indica dominio sostenido de la línea y teamfights. |
| ADC | ✅ | Rachas altas indican buen posicionamiento y protección del equipo. |
| Support | ❌ | No aplica como indicador significativo para supports. |

---

### A.2 — Métricas de Daño

#### `totalDamageDealtToChampions` — Daño total a campeones
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indica si el top está generando presión ofensiva en peleas. Varía según tipo de campeón (tanque vs carry). |
| Jungle | ✅ | Un jungla debe hacer daño relevante en ganks y teamfights. |
| Mid | ✅ | Se espera que el mid sea uno de los mayores contribuyentes de daño del equipo. |
| ADC | ✅ | Es la métrica estrella del ADC. Se espera el mayor daño a campeones del equipo. |
| Support | ⚠️ | Depende del tipo de support. Un support mago (Brand, Zyra) puede tener daño alto legítimamente, mientras que un support encantador (Lulu, Janna) tendrá daño bajo naturalmente. |

#### `physicalDamageDealtToChampions` — Daño físico a campeones
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Solo relevante para tops AD (Fiora, Camille). Los tops AP como Mordekaiser tendrán esta métrica baja sin que sea un problema. |
| Jungle | ⚠️ | Depende del tipo de jungla (AD vs AP). |
| Mid | ⚠️ | La mayoría de mids son AP, por lo que esta métrica será naturalmente baja. Solo relevante para Zed, Talon, etc. |
| ADC | ✅ | La mayoría de ADCs hacen daño físico. Es la composición principal de su daño. |
| Support | ❌ | No es una métrica útil para evaluar supports. |

#### `magicDamageDealtToChampions` — Daño mágico a campeones
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Solo relevante para tops AP (Mordekaiser, Gwen). |
| Jungle | ⚠️ | Depende del tipo de jungla (Lillia, Fiddlesticks serían AP). |
| Mid | ✅ | La mayoría de mids hacen daño mágico. Es la composición principal de su daño. |
| ADC | ⚠️ | Solo relevante para ADCs AP como Kai'Sa o Ziggs bot. |
| Support | ⚠️ | Relevante solo para supports mago (Brand, Zyra, Vel'Koz). |

#### `trueDamageDealtToChampions` — Daño verdadero a campeones
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Relevante solo para campeones con daño verdadero incorporado (Fiora, Vayne top). |
| Jungle | ⚠️ | Depende del campeón (Olaf, Warwick). |
| Mid | ⚠️ | Pocos mid laners tienen daño verdadero significativo (Ahri con pasiva). |
| ADC | ⚠️ | Relevante para Vayne, Kog'Maw con builds on-hit. |
| Support | ❌ | No aplica significativamente. |

#### `totalDamageDealt` — Daño total (incluye súbditos, monstruos, edificios)
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Puede indicar splitpush efectivo (incluye daño a súbditos y estructuras), pero mezcla muchas fuentes. |
| Jungle | ⚠️ | Incluye todo el daño a monstruos de la jungla, lo que infla la cifra sin reflejar impacto en peleas. |
| Mid | ⚠️ | Mezcla waveclear con daño a campeones. Mejor usar `totalDamageDealtToChampions`. |
| ADC | ⚠️ | Mismo problema de mezclar fuentes. |
| Support | ❌ | No aporta información útil para el rol. |

#### `damageDealtToTurrets` / `damageDealtToBuildings` — Daño a torres/edificios
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indicador clave de split push. Un top que splitea debe tener daño alto a torres. |
| Jungle | ⚠️ | Los junglas ayudan a tomar torres después de ganks, pero no es su foco principal. |
| Mid | ⚠️ | Puede indicar prioridad de línea (si está empujando y haciendo daño a la primera torre), pero no es su función primaria. |
| ADC | ✅ | El ADC es el principal tomador de torres en rotaciones grupales. Daño alto a torres es esperado. |
| Support | ❌ | No aplica. |

#### `damageDealtToObjectives` / `damageDealtToEpicMonsters` — Daño a objetivos
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Solo relevante si el top baja a ayudar con dragón/barón. |
| Jungle | ✅ | El jungla es responsable de asegurar objetivos épicos. Esta métrica indica si está cumpliendo esta función. |
| Mid | ⚠️ | Puede ayudar con objetivos, pero no es su responsabilidad primaria. |
| ADC | ✅ | El ADC aporta DPS sostenido a objetivos. Un daño alto indica buena presencia. |
| Support | ❌ | No aplica significativamente. |

#### `teamDamagePercentage` (challenges) — % del daño total del equipo
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Depende del tipo de campeón. Un tanque tendrá un % bajo; un carry un % alto. No hay un estándar universal. |
| Jungle | ⚠️ | Se espera un 15-25% dependiendo del tipo de jungla. |
| Mid | ✅ | Se espera un 25-35%. Es uno de los principales contribuyentes de daño. |
| ADC | ✅ | Se espera el % más alto del equipo (25-35%). Un ADC con % bajo indica que no está generando suficiente impacto. |
| Support | ⚠️ | Se espera un 5-15%. Valores altos pueden indicar un support mago que está tomando recursos. |

#### `damageTakenOnTeamPercentage` (challenges) — % del daño recibido del equipo
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Si juega tanque, se espera que absorba entre un 25-35% del daño del equipo. Si es carry, debería ser menor. |
| Jungle | ⚠️ | Depende de si es jungla tanque o jungla asesino. |
| Mid | ⚠️ | Debería ser moderado. Un % demasiado alto indica que está recibiendo mucho daño innecesario. |
| ADC | ✅ | El ADC debería tener el % más bajo. Un valor alto indica que está recibiendo demasiado daño (mal posicionamiento). |
| Support | ✅ | Un support tanque debería tener un % alto (está absorbiendo daño por el equipo). Un support encantador debería tener un % bajo. |

#### `damagePerMinute` (challenges) — Daño por minuto
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Normaliza el daño por la duración del juego. Permite comparar rendimiento entre partidas de diferente duración. |
| Jungle | ✅ | Misma razón que Top. |
| Mid | ✅ | Misma razón. Se espera el DPM más alto o segundo más alto del equipo. |
| ADC | ✅ | Métrica estrella. Se espera el DPM más alto del equipo en partidas largas. |
| Support | ⚠️ | Depende del tipo de support. |

#### `damageSelfMitigated` — Daño mitigado por el jugador
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indicador clave para tanques. Muestra cuánto daño están absorbiendo efectivamente. |
| Jungle | ⚠️ | Relevante para junglas tanque (Amumu, Sejuani). |
| Mid | ❌ | La mayoría de mids no buscan mitigar daño. |
| ADC | ❌ | No es una métrica útil para ADC. |
| Support | ✅ | Relevante para supports tanque (Leona, Nautilus, Alistar). |

---

### A.3 — Métricas de Economía

#### `goldEarned` — Oro total ganado
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indica eficiencia de farmeo y kills. |
| Jungle | ✅ | Refleja eficiencia en la ruta de jungla y ganks exitosos. |
| Mid | ✅ | Refleja CS, kills y control de recursos del mapa. |
| ADC | ✅ | Métrica directamente ligada a la capacidad de escalado del ADC. |
| Support | ⚠️ | El support tiene un techo de oro más bajo por diseño (no farmea). Solo relevante para verificar que no está farmeando oleadas de su ADC. |

#### `goldSpent` — Oro gastado
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Puede indicar si el jugador está muriendo con oro sin gastar (mala gestión de backs). |
| Jungle | ⚠️ | Misma lógica que Top. |
| Mid | ⚠️ | Misma lógica. |
| ADC | ⚠️ | Misma lógica. |
| Support | ⚠️ | Misma lógica. |

#### `goldPerMinute` (challenges) — Oro por minuto
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indicador directo de eficiencia económica normalizado por tiempo. |
| Jungle | ✅ | Permite comparar la eficiencia económica entre partidas. |
| Mid | ✅ | Se espera uno de los valores más altos del equipo. |
| ADC | ✅ | Se espera el valor más alto del equipo. Un GPM bajo indica que el ADC no está consiguiendo recursos suficientes. |
| Support | ⚠️ | Se espera el valor más bajo del equipo. Un GPM alto puede indicar "robando" farm. |

#### `itemsPurchased` — Total de items comprados
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | ⚠️ | Dato bruto que por sí solo no aporta mucho. Podría ser relevante cruzado con otros datos (ej: veces que volvió a base). |

#### `consumablesPurchased` — Consumibles comprados
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Pociones de regeneración indican trades frecuentes. |
| Jungle | ❌ | Menos relevante; su sustain proviene de la jungla. |
| Mid | ⚠️ | Similar a Top. |
| ADC | ⚠️ | Compra inicial de pociones, luego es irrelevante. |
| Support | ✅ | La compra de wards de control está incluida aquí. Es un indicador directo de soporte activo. |

---

### A.4 — Métricas de Visión

#### `visionScore` — Puntuación de visión total
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Se espera un vision score bajo-moderado. Los tops suelen poner wards en bushes del río y tribush. |
| Jungle | ✅ | El jungla necesita un vision score alto para controlar objetivos y proteger sus rutas. |
| Mid | ⚠️ | Vision score moderado. Debería colocar wards en los bushes del río para evitar ganks. |
| ADC | ⚠️ | Vision score bajo es esperado. El ADC depende principalmente de su support para visión. |
| Support | ✅ | Métrica estrella del support. Se espera el vision score más alto del equipo, significativamente por encima de los demás. |

#### `visionScorePerMinute` (challenges) — Visión por minuto
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Mismo análisis que `visionScore` pero normalizado por tiempo. |
| Jungle | ✅ | Permite comparar rendimiento de visión entre partidas de diferente duración. |
| Mid | ⚠️ | Moderado. |
| ADC | ⚠️ | Se espera bajo. |
| Support | ✅ | Métrica fundamental. Se espera un valor entre 1.5-2.5+ por minuto para un buen support. |

#### `wardsPlaced` — Wards colocados
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Mínimo esperable de wards. |
| Jungle | ✅ | Debe colocar wards para controlar objetivos y rutas enemigas. |
| Mid | ⚠️ | Contribución moderada. |
| ADC | ⚠️ | Contribución mínima. |
| Support | ✅ | Principal responsable de la visión. |

#### `wardsKilled` — Wards destruidos
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Depende de si compra barredor y limpia visión en su zona. |
| Jungle | ✅ | Debe limpiar visión antes de ganks y objetivos. |
| Mid | ⚠️ | Puede contribuir limpiando visión con barredor. |
| ADC | ❌ | Raramente tiene herramientas para destruir wards. |
| Support | ✅ | Indicador clave. El support es el principal responsable de denegar visión enemiga. |

#### `detectorWardsPlaced` — Wards de control (pinks) colocados
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Se espera al menos 1-2 por partida para proteger la línea de ganks. |
| Jungle | ✅ | Debe usar wards de control estratégicamente en objetivos. |
| Mid | ⚠️ | Se espera al menos 1-2 por partida. |
| ADC | ⚠️ | Se espera contribución mínima. |
| Support | ✅ | Se espera la mayor cantidad de wards de control del equipo. |

#### `visionWardsBoughtInGame` — Wards de control comprados
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Se espera al menos 2-3 por partida en elo medio-alto. |
| Jungle | ✅ | Se espera 3-5+ por partida. |
| Mid | ⚠️ | Se espera al menos 2-3 por partida. |
| ADC | ⚠️ | Se espera 1-2 por partida. |
| Support | ✅ | Se espera el mayor número del equipo. |

#### `controlWardsPlaced` (challenges) — Wards de control colocados (redundante con detectorWardsPlaced)
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | Misma lógica que `detectorWardsPlaced`. |

#### `stealthWardsPlaced` (challenges) — Wards de sigilo colocados
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | Misma lógica que `wardsPlaced`, pero solo cuenta los de sigilo (amarillos). |

#### `wardTakedowns` (challenges) — Wards destruidos (incluye asistencias en destrucción)
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | Misma lógica que `wardsKilled` pero incluye asistencias. |

#### `wardTakedownsBefore20M` (challenges) — Wards destruidos antes del minuto 20
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Indica control de visión temprano en su zona. |
| Jungle | ✅ | Indica que está limpiando visión activamente en la fase de línea para facilitar ganks. |
| Mid | ⚠️ | Contribución moderada. |
| ADC | ❌ | Rara vez contribuye significativamente. |
| Support | ✅ | Indicador crítico. Un support que limpia visión antes del min 20 está facilitando ventajas tempranas. |

#### `controlWardTimeCoverageInRiverOrEnemyHalf` (challenges) — Tiempo de cobertura de wards de control en río o territorio enemigo
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Relevante si coloca wards de control en el río/tribush. |
| Jungle | ✅ | Indica si está manteniendo control de visión en zonas clave. |
| Mid | ⚠️ | Relevante para mantener la prioridad de línea. |
| ADC | ❌ | No es responsabilidad del ADC. |
| Support | ✅ | Indicador premium de calidad de visión. Mide no solo cantidad sino la utilidad de los wards. |

#### `visionScoreAdvantageLaneOpponent` (challenges) — Ventaja de visión vs oponente directo
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Indica si tiene mejor visión que su oponente de línea. |
| Jungle | ⚠️ | Indica si tiene mejor visión que el jungla enemigo. |
| Mid | ⚠️ | Indica si tiene mejor visión que su oponente de línea. |
| ADC | ❌ | No es un indicador útil para el ADC. |
| Support | ✅ | Indicador directo de si el support está ganando la "guerra de visión" contra el support enemigo. |

---

### A.5 — Métricas de Objetivos y Estructuras

#### `dragonKills` — Dragones asesinados (último golpe)
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ❌ | El top raramente tiene smite o es responsable del último golpe al dragón. |
| Jungle | ✅ | Métrica principal del jungla. Es el responsable directo de asegurar dragones con smite. |
| Mid | ❌ | No es responsable del último golpe. |
| ADC | ❌ | No es responsable del último golpe. |
| Support | ❌ | No es responsable del último golpe. |

#### `baronKills` — Barones asesinados (último golpe)
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ❌ | Mismo razonamiento que dragones. |
| Jungle | ✅ | Es responsable directo de asegurar barón con smite. |
| Mid | ❌ | No aplica. |
| ADC | ❌ | No aplica. |
| Support | ❌ | No aplica. |

#### `turretKills` — Torres destruidas (último golpe)
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indica eficacia en split push. |
| Jungle | ⚠️ | Puede tomar torres tras ganks exitosos. |
| Mid | ⚠️ | Indica si está presionando y abriendo el mapa. |
| ADC | ✅ | El ADC es el principal tomador de torres en rotaciones. |
| Support | ❌ | No es su responsabilidad. |

#### `turretTakedowns` — Torres destruidas (incluyendo asistencias)
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Incluye asistencias, reflejando participación total en destrucción de torres. |
| Jungle | ✅ | Indica que está ayudando a tomar torres tras ganks o en rotaciones. |
| Mid | ✅ | Indica que está empujando y ayudando a abrir el mapa. |
| ADC | ✅ | Indicador principal de contribución a objetivos de mapa. |
| Support | ⚠️ | Puede asistir en la toma de torres, pero no es su foco. |

#### `turretPlatesTaken` (challenges) — Placas de torre tomadas
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indica dominio de línea temprano. Tomar placas genera ventaja de oro significativa. |
| Jungle | ⚠️ | Puede tomar placas después de ganks, pero no es su fuente principal de oro. |
| Mid | ✅ | Tomar placas indica prioridad de línea y presión constante. |
| ADC | ✅ | Las placas de bot lane son una fuente importante de oro temprano para el ADC. |
| Support | ⚠️ | Puede asistir en tomar placas, pero el oro debería ir al ADC. |

#### `inhibitorKills` / `inhibitorTakedowns` — Inhibidores destruidos
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | ⚠️ | Indicador general de progreso en el cierre de la partida, pero es un evento de equipo más que individual. |

#### `objectivesStolen` — Objetivos robados (smite robado)
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ❌ | No tiene smite. |
| Jungle | ✅ | Indicador crítico. Robar un barón o dragón puede cambiar una partida. |
| Mid | ❌ | No tiene smite (en general). |
| ADC | ❌ | No tiene smite. |
| Support | ❌ | No tiene smite. |

#### `firstTowerKill` / `firstTowerAssist` — Primera torre
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indica dominio temprano de la línea. |
| Jungle | ✅ | Indica ganks exitosos que llevan a tomar la primera torre. |
| Mid | ✅ | Primera torre mid abre rotaciones. |
| ADC | ✅ | Primera torre bot es un objetivo prioritario. |
| Support | ✅ | Asistir en la primera torre es un buen indicador. |

---

### A.6 — Métricas de Farmeo

#### `totalMinionsKilled` — Súbditos de línea asesinados
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indicador principal de farmeo. Se espera un CS alto. |
| Jungle | ❌ | El jungla no farmea oleadas (excepto en situaciones específicas). Un valor alto puede indicar que está tomando farm de sus laners. |
| Mid | ✅ | Indicador principal de farmeo. |
| ADC | ✅ | Métrica estrella. Se espera el CS más alto o segundo más alto del equipo. |
| Support | ❌ | El support no debería farmear oleadas. Un valor alto indica que está robando farm. |

#### `neutralMinionsKilled` — Monstruos neutrales asesinados
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Puede tomar algunos campamentos cercanos en situaciones de rotación. |
| Jungle | ✅ | Métrica principal. Indica eficiencia en el clear de la jungla. |
| Mid | ⚠️ | Los mid laners pueden tomar rapaces o lobos para acelerar farm. |
| ADC | ⚠️ | Puede tomar campamentos en mid/late game. |
| Support | ❌ | No debería tomar campamentos. |

#### `totalAllyJungleMinionsKilled` / `totalEnemyJungleMinionsKilled` — Jungla aliada/enemiga
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Puede tomar jungla aliada cercana si el jungla no la necesita. |
| Jungle | ✅ | `alliedJungleMonsterKills` indica eficiencia del clear propio. `enemyJungleMonsterKills` indica invasiones exitosas. |
| Mid | ⚠️ | Similar a Top. |
| ADC | ⚠️ | Puede tomar campamentos en fases tardías. |
| Support | ❌ | No aplica. |

#### `laneMinionsFirst10Minutes` (challenges) — Súbditos de línea en los primeros 10 minutos
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indicador crítico de CSing temprano. El estándar es ~80-100 CS a los 10 min en elos altos. |
| Jungle | ❌ | El jungla no farmea oleadas. Esta métrica debería ser muy baja. |
| Mid | ✅ | Mismo estándar que Top. |
| ADC | ✅ | Métrica crítica. Se espera ~80-100 CS a los 10 min en elos altos. |
| Support | ❌ | No aplica. |

#### `jungleCsBefore10Minutes` (challenges) — CS de jungla antes de los 10 minutos
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ❌ | No aplica. |
| Jungle | ✅ | Indicador principal de eficiencia de pathing temprano. Se espera ~60-70+ en elos altos. |
| Mid | ❌ | No aplica. |
| ADC | ❌ | No aplica. |
| Support | ❌ | No aplica. |

#### CS/min (calculada: `totalMinionsKilled + neutralMinionsKilled / gameDuration`)
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Referencia: >7.0 cs/min es bueno, >8.0 es excelente. |
| Jungle | ✅ | Se calcula diferente (más basado en campamentos), pero aplica. Referencia: >5.5-6.5 cs/min con inclusión de ganks. |
| Mid | ✅ | Referencia: >7.5 cs/min es bueno, >8.5 es excelente. |
| ADC | ✅ | Referencia: >8.0 cs/min es bueno, >9.0 es excelente. |
| Support | ❌ | No aplica como métrica de rendimiento. |

#### `maxCsAdvantageOnLaneOpponent` (challenges) — Ventaja máxima de CS sobre el oponente de línea
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indica dominio de línea en farmeo. |
| Jungle | ❌ | No aplica (no tiene oponente de línea directo). |
| Mid | ✅ | Indica dominio de línea en farmeo. |
| ADC | ✅ | Indica dominio del duo bot en farmeo. |
| Support | ❌ | No aplica. |

---

### A.7 — Métricas de Supervivencia y Durabilidad

#### `totalDamageTaken` — Daño total recibido
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Si es tanque, se espera un valor alto. Si es carry, un valor alto puede indicar problemas. |
| Jungle | ⚠️ | Incluye daño de monstruos, lo que lo hace menos útil que el daño tomado de campeones específicamente. |
| Mid | ⚠️ | Debería ser moderado. Demasiado alto indica mal posicionamiento. |
| ADC | ✅ | Debería ser bajo. Valores altos indican que está recibiendo mucho daño (focus enemigo o mal posicionamiento). |
| Support | ✅ | Un support tanque debe tener un valor alto; un support encantador debe tener un valor bajo. |

#### `totalTimeSpentDead` — Tiempo total muerto (segundos)
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Tiempo muerto largo significa pérdida de XP, oro y presión de línea. |
| Jungle | ✅ | Cada segundo muerto es un campamento o un gank que no se está ejecutando. |
| Mid | ✅ | Similar a Top. |
| ADC | ✅ | Particularmente costoso; el equipo pierde su fuente principal de DPS. |
| Support | ⚠️ | Menos impactante que en otros roles, pero sigue siendo negativo. |

#### `longestTimeSpentLiving` — Mayor tiempo vivo consecutivo (segundos)
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | ⚠️ | Puede indicar consistencia, pero también podría reflejar que el jugador está jugando demasiado pasivo. Es una métrica ambigua. |

#### `tookLargeDamageSurvived` (challenges) — Sobrevivió recibiendo gran cantidad de daño
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Relevante para tanques y bruisers. Indica resiliencia en peleas. |
| Jungle | ⚠️ | Depende del tipo de jungla. |
| Mid | ⚠️ | No es esperado para la mayoría de mid laners. |
| ADC | ⚠️ | Puede indicar buen uso de habilidades defensivas (flash, curación, etc.). |
| Support | ⚠️ | Relevante para supports tanque. |

#### `survivedSingleDigitHpCount` (challenges) — Veces que sobrevivió con HP de un solo dígito
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | ⚠️ | Dato curioso más que indicador de rendimiento. Puede indicar buenas mecánicas o buena suerte. |

#### `survivedThreeImmobilizesInFight` (challenges) — Sobrevivió 3+ CC en una pelea
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Indica resiliencia si juega tanque/bruiser. |
| Jungle | ⚠️ | Depende del tipo. |
| Mid | ⚠️ | No es esperado frecuentemente. |
| ADC | ✅ | Indica excelente posicionamiento y uso de QSS/habilidades defensivas. |
| Support | ⚠️ | Relevante para supports tanque. |

---

### A.8 — Métricas de Utilidad y Soporte

#### `totalHeal` — Curación total
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Algunos tops tienen autocuración incorporada (Aatrox, Mordekaiser). |
| Jungle | ⚠️ | Incluye sustain de la jungla. |
| Mid | ❌ | No es una métrica relevante para la mayoría de mids. |
| ADC | ⚠️ | Incluye robo de vida. |
| Support | ⚠️ | Relevante para supports curanderos (Soraka, Nami). |

#### `totalHealsOnTeammates` — Curación a compañeros
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ❌ | Raro que un top cure aliados. |
| Jungle | ❌ | No aplica generalmente. |
| Mid | ❌ | No aplica generalmente. |
| ADC | ❌ | No aplica. |
| Support | ✅ | Métrica estrella para supports curanderos (Soraka, Sona, Nami, Yuumi). |

#### `effectiveHealAndShielding` (challenges) — Curación y escudos efectivos
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ❌ | No aplica generalmente. |
| Jungle | ⚠️ | Algunos junglas tienen escudos (Ivern). |
| Mid | ⚠️ | Lux puede dar escudos, pero no es su función principal. |
| ADC | ❌ | No aplica. |
| Support | ✅ | Indicador premium. Mide la curación y escudos que realmente previnieron daño (no el exceso que se desperdició). |

#### `totalDamageShieldedOnTeammates` — Escudos dados a compañeros
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ❌ | Raro que un top dé escudos. |
| Jungle | ❌ | No aplica generalmente. |
| Mid | ⚠️ | Lux, Orianna pueden dar escudos. |
| ADC | ❌ | No aplica. |
| Support | ✅ | Métrica clave para supports encantadores (Lulu, Janna, Karma). |

#### `saveAllyFromDeath` (challenges) — Aliados salvados de la muerte
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ❌ | Raro. |
| Jungle | ❌ | Raro. |
| Mid | ❌ | Raro. |
| ADC | ❌ | No aplica. |
| Support | ✅ | Indicador premium de impacto defensivo del support. |

#### `timeCCingOthers` — Tiempo aplicando CC a enemigos (segundos)
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Relevante para tops con mucho CC (Ornn, Sion, Maokai). |
| Jungle | ✅ | Un jungla con CC (Sejuani, Amumu) debe tener valores altos para facilitar ganks. |
| Mid | ⚠️ | Depende del campeón. Magos de control (Veigar, Anivia) tendrán valores altos. |
| ADC | ❌ | Los ADC generalmente no tienen CC significativo (excepto Ashe, Jhin). |
| Support | ✅ | Métrica estrella para supports de enganche/tanque (Leona, Nautilus, Thresh). |

#### `enemyChampionImmobilizations` (challenges) — Veces que inmovilizó a campeones enemigos
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | Misma lógica que `timeCCingOthers`. |

#### `completeSupportQuestInTime` (challenges) — Completó la quest de support a tiempo
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ❌ | No aplica (no lleva item de support). |
| Jungle | ❌ | No aplica. |
| Mid | ❌ | No aplica. |
| ADC | ❌ | No aplica. |
| Support | ✅ | Indicador directo de si el support está acumulando stacks de su item de support de forma eficiente. |

---

### A.9 — Métricas de Comunicación (Pings)

Estos campos registran el número de pings emitidos por el jugador durante la partida.

| Campo | Descripción |
|---|---|
| `allInPings` | Pings de "ir al ataque". |
| `assistMePings` | Pings de "asístanme". |
| `basicPings` | Pings genéricos (click). |
| `commandPings` | Pings de comando (destino). |
| `dangerPings` | Pings de peligro. |
| `enemyMissingPings` | Pings de "enemigo desaparecido" (MIA). |
| `enemyVisionPings` | Pings de visión enemiga. |
| `getBackPings` | Pings de "retírate". |
| `holdPings` | Pings de "mantener posición". |
| `needVisionPings` | Pings de "necesito visión". |
| `onMyWayPings` | Pings de "en camino". |
| `pushPings` | Pings de "empujar". |
| `retreatPings` | Pings de retirarse. |
| `visionClearedPings` | Pings de "visión limpiada". |

**Relevancia por Rol (todos los pings):**
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | ⚠️ | Los pings pueden indicar comunicación activa, pero también toxicidad (spam de pings). No recomiendo usar el conteo crudo como métrica de rendimiento. `enemyMissingPings` podría ser interesante para evaluar conciencia de mapa, pero es difícil de interpretar sin contexto. |

---

### A.10 — Campo `challenges` — Métricas Avanzadas de Riot

Estas son métricas adicionales calculadas por Riot directamente. Solo listo aquí las que NO se han cubierto en las secciones anteriores:

#### Métricas de Fase de Línea

| Métrica | Qué evalúa | Top | Jungle | Mid | ADC | Support |
|---|---|---|---|---|---|---|
| `earlyLaningPhaseGoldExpAdvantage` | ¿Tenía ventaja de oro/XP al final de la fase de línea temprana (~min 8)? | ✅ Indica dominio temprano | ❌ No tiene fase de línea | ✅ Indica dominio temprano | ✅ Indica dominio del duo | ⚠️ Menos relevante |
| `laningPhaseGoldExpAdvantage` | ¿Tenía ventaja de oro/XP al final de la fase de línea (~min 14)? | ✅ Dominio sostenido | ❌ No tiene fase de línea | ✅ Dominio sostenido | ✅ Dominio sostenido | ⚠️ Menos relevante |
| `maxLevelLeadLaneOpponent` | Mayor ventaja de nivel sobre el oponente de línea | ✅ Dominio por XP | ❌ No aplica | ✅ Dominio por XP | ⚠️ Bot es 2v2 | ❌ No aplica |
| `takedownsFirstXMinutes` | Eliminaciones en los primeros X minutos | ✅ Agresión temprana | ✅ Ganks tempranos | ✅ Agresión temprana | ✅ Presión temprana | ✅ Presión temprana |

#### Métricas de Jungla (exclusivas del rol)

| Métrica | Qué evalúa | Top | Jungle | Mid | ADC | Support |
|---|---|---|---|---|---|---|
| `initialBuffCount` | Buffs iniciales tomados (rojo/azul) | ❌ | ✅ Eficiencia del primer clear | ❌ | ❌ | ❌ |
| `initialCrabCount` | Cangrejos tomados al inicio | ❌ | ✅ Control temprano del río | ❌ | ❌ | ❌ |
| `scuttleCrabKills` | Total de cangrejos asesinados | ❌ | ✅ Control del río toda la partida | ❌ | ❌ | ❌ |
| `buffsStolen` | Buffs robados al equipo enemigo | ❌ | ✅ Invasiones exitosas | ❌ | ❌ | ❌ |
| `enemyJungleMonsterKills` | Monstruos de jungla enemiga asesinados | ❌ | ✅ Presión en jungla enemiga | ❌ | ❌ | ❌ |
| `moreEnemyJungleThanOpponent` | Diferencia de jungla enemiga vs oponente | ❌ | ✅ ¿Invade más que el jungla rival? | ❌ | ❌ | ❌ |
| `epicMonsterSteals` | Objetivos épicos robados | ❌ | ✅ Clutch plays con smite | ❌ | ❌ | ❌ |
| `epicMonsterStolenWithoutSmite` | Robos de objetivo SIN smite | ❌ | ⚠️ Indica mal uso de smite | ❌ | ❌ | ❌ |
| `epicMonsterKillsNearEnemyJungler` | Objetivos tomados con jungla enemigo cerca | ❌ | ✅ Nervios de acero en contests | ❌ | ❌ | ❌ |
| `epicMonsterKillsWithin30SecondsOfSpawn` | Objetivos tomados dentro de 30s del spawn | ❌ | ✅ Rapidez en asegurar objetivos | ❌ | ❌ | ❌ |
| `junglerTakedownsNearDamagedEpicMonster` | Eliminaciones cerca de monstruos épicos dañados | ❌ | ✅ Peleas por objetivos | ❌ | ❌ | ❌ |
| `killsOnLanersEarlyJungleAsJungler` | Kills a laners como jungla temprano | ❌ | ✅ Eficacia de ganks tempranos | ❌ | ❌ | ❌ |
| `killsOnOtherLanesEarlyJungleAsLaner` | Kills en otras líneas como laner (roams) | ⚠️ TP plays | ❌ | ✅ Roams exitosos | ❌ | ⚠️ Roams |
| `getTakedownsInAllLanesEarlyJungleAsLaner` | Eliminaciones en todas las líneas temprano | ❌ | ✅ Presión en todo el mapa | ❌ | ❌ | ❌ |
| `voidMonsterKill` | Gusanos del Vacío (Voidgrubs) asesinados | ❌ | ✅ Control del objetivo temprano | ❌ | ❌ | ❌ |

#### Métricas de Combate Avanzadas

| Métrica | Qué evalúa | Top | Jungle | Mid | ADC | Support |
|---|---|---|---|---|---|---|
| `skillshotsHit` | Habilidades de skill shot acertadas | ⚠️ Depende del campeón | ⚠️ Depende del campeón | ✅ Precisión mecánica | ⚠️ Pocos ADC tienen skillshots impactantes | ✅ Para supports de enganche (Thresh, Blitz) |
| `skillshotsDodged` | Habilidades esquivadas | ✅ Capacidad de esquivar en trades | ⚠️ Depende del campeón | ✅ Capacidad de esquivar en trades | ✅ Vital para sobrevivir | ⚠️ Depende del campeón |
| `dodgeSkillShotsSmallWindow` | Habilidades esquivadas en ventana pequeña | ✅ Reflejos | ⚠️ | ✅ Reflejos | ✅ Reflejos | ⚠️ |
| `landSkillShotsEarlyGame` | Skillshots acertados en early game | ⚠️ | ⚠️ | ✅ Dominio de trades tempranos | ❌ | ✅ Engage temprano |
| `outnumberedKills` | Kills en inferioridad numérica | ✅ 1vX outplays | ⚠️ | ✅ 1vX outplays | ⚠️ | ❌ |
| `pickKillWithAlly` | Kills con aliado (picks coordinados) | ⚠️ | ✅ Ganks coordinados | ⚠️ | ⚠️ | ✅ Engages coordinados |
| `immobilizeAndKillWithAlly` | CC + kill con aliado | ⚠️ | ✅ Ganks con CC | ⚠️ | ❌ | ✅ CC + followup |
| `knockEnemyIntoTeamAndKill` | Empujó enemigo hacia el equipo y lo mataron | ⚠️ Solo con desplazamientos (Sion, Sett) | ⚠️ Lee Sin, Vi | ❌ | ❌ | ✅ Alistar, Thresh |
| `killAfterHiddenWithAlly` | Kill tras estar oculto con aliado (emboscada) | ⚠️ | ✅ Ganks desde bushes | ⚠️ | ❌ | ⚠️ |
| `killsUnderOwnTurret` | Kills bajo tu propia torre | ✅ Defensa exitosa | ⚠️ | ✅ Defensa exitosa | ⚠️ | ⚠️ |
| `killsNearEnemyTurret` | Kills cerca de torre enemiga (dives) | ✅ Dives exitosos | ✅ Dives exitosos | ✅ Dives exitosos | ⚠️ | ⚠️ |
| `multikillsAfterAggressiveFlash` | Multikills tras flash agresivo | ⚠️ | ⚠️ | ✅ Jugadas mecánicas | ⚠️ | ❌ |
| `multiKillOneSpell` | Multikill con una sola habilidad | ❌ | ❌ | ✅ Habilidades AoE (Viktor ult, etc.) | ❌ | ❌ |
| `quickSoloKills` | Solo kills rápidas | ✅ Burst en línea | ⚠️ | ✅ Burst en línea | ❌ | ❌ |
| `fullTeamTakedown` | Participó en un Ace completo | ⚠️ | ✅ Presencia en teamfights | ⚠️ | ✅ DPS en teamfights | ✅ CC en teamfights |
| `flawlessAces` | Aces sin que muera nadie del equipo | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `bountyGold` | Oro obtenido de bounties | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

#### Métricas de Torres y Objetivos Avanzados

| Métrica | Qué evalúa | Top | Jungle | Mid | ADC | Support |
|---|---|---|---|---|---|---|
| `quickFirstTurret` | Tiempo rápido en destruir primera torre | ✅ Dominio temprano | ⚠️ | ✅ Presión temprana | ✅ Bot priority | ⚠️ |
| `kTurretsDestroyedBeforePlatesFall` | Torres destruidas antes de que caigan las placas (pre-14 min) | ✅ Dominio extremo | ⚠️ | ✅ Dominio extremo | ✅ | ⚠️ |
| `outerTurretExecutesBefore10Minutes` | Ejecuciones de torre exterior antes del min 10 | ✅ | ⚠️ | ✅ | ⚠️ | ❌ |
| `soloTurretsLategame` | Torres destruidas solo en late game | ✅ Split push | ❌ | ⚠️ | ⚠️ | ❌ |
| `multiTurretRiftHeraldCount` | Torres destruidas con un solo Heraldo | ❌ | ✅ Uso eficiente del Heraldo | ❌ | ❌ | ❌ |
| `turretsTakenWithRiftHerald` | Torres tomadas con Heraldo | ❌ | ✅ | ❌ | ❌ | ❌ |
| `dancedWithRiftHerald` | Bailó con el Heraldo (easter egg) | ❌ | ❓ Dato curioso | ❌ | ❌ | ❌ |
| `dragonTakedowns` | Participaciones en dragones | ⚠️ Si baja a ayudar | ✅ | ⚠️ | ✅ DPS a dragón | ✅ Visión y CC |
| `baronTakedowns` | Participaciones en barón | ⚠️ | ✅ | ⚠️ | ✅ DPS a barón | ✅ |
| `riftHeraldTakedowns` | Participaciones en heraldo | ⚠️ Si baja a ayudar | ✅ | ⚠️ | ❌ | ❌ |
| `perfectDragonSoulsTaken` | Almas de dragón perfectas (4-0) | ⚠️ Equipo | ✅ Control de dragones | ⚠️ Equipo | ⚠️ Equipo | ⚠️ Equipo |

#### Métricas Irrelevantes para Nuestro Proyecto (Modos Especiales)

Las siguientes métricas del campo `challenges` son exclusivas del modo SWARM/Arena y **NO son relevantes** para partidas de Clasificatoria Flex (queueId 440). Las incluyo para documentar que existen pero no deberían ser procesadas:

| Métrica | Modo |
|---|---|
| `SWARM_KillEnemy` | SWARM |
| `SWARM_PickupGold` | SWARM |
| `SWARM_DefeatBriar` | SWARM |
| `SWARM_DefeatAatrox` | SWARM |
| `SWARM_EvolveWeapon` | SWARM |
| `SWARM_ReachLevel50` | SWARM |
| `SWARM_Survive15Min` | SWARM |
| `SWARM_Have3Passives` | SWARM |
| `SWARM_DefeatMiniBosses` | SWARM |
| `SWARM_WinWith5EvolvedWeapons` | SWARM |
| `snowballsHit` | ARAM |
| `poroExplosions` | ARAM |
| `killsOnRecentlyHealedByAramPack` | ARAM |
| `HealFromMapSources` | ARAM |
| `fistBumpParticipation` | Arena/Especial |
| `InfernalScalePickup` | Modo especial |

#### Otras Métricas del Challenges

| Métrica | Qué evalúa | Top | Jungle | Mid | ADC | Support |
|---|---|---|---|---|---|---|
| `abilityUses` | Total de usos de habilidades | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `unseenRecalls` | Recalls sin ser visto por enemigos | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `quickCleanse` | Limpiezas rápidas de CC (QSS/Cleanse) | ⚠️ | ❌ | ⚠️ | ✅ Vital para ADC | ⚠️ |
| `mejaisFullStackInTime` | Mejai's a stack máximo a tiempo | ❌ | ❌ | ⚠️ Solo si compra Mejai's | ❌ | ⚠️ Solo si compra Mejai's |
| `12AssistStreakCount` | Rachas de 12+ asistencias consecutivas | ❌ | ⚠️ | ❌ | ❌ | ✅ Indica participación constante |
| `legendaryCount` | Veces que alcanzó estatus Legendario | ⚠️ | ⚠️ | ✅ | ✅ | ❌ |
| `legendaryItemUsed` | Objetos legendarios usados | ⚠️ Análisis de builds | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `hadOpenNexus` | ¿Tuvo nexo expuesto? | ⚠️ Contexto de partida | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `lostAnInhibitor` | ¿Perdió un inhibidor? | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `acesBefore15Minutes` | Aces antes del min 15 | ⚠️ Evento de equipo | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `perfectGame` | ¿Partida perfecta (0 muertes equipo)? | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `doubleAces` | ¿Doble Ace en la partida? | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `twoWardsOneSweeperCount` | 2 wards destruidos con un solo sweep | ❌ | ⚠️ | ❌ | ❌ | ✅ Eficiencia de limpieza |
| `wardsGuarded` | Wards protegidos activamente | ❌ | ⚠️ | ❌ | ❌ | ⚠️ |
| `blastConeOppositeOpponentCount` | Uso de blast cone contra oponente | ❌ | ⚠️ | ❌ | ❌ | ❌ |
| `playedChampSelectPosition` | ¿Jugó la posición asignada? | ✅ | ✅ | ✅ | ✅ | ✅ |
| `takedownsInAlcove` | Eliminaciones en las alcobas del mapa | ❓ | ❓ | ❓ | ❓ | ❓ |
| `takedownsInEnemyFountain` | Eliminaciones en la fuente enemiga | ❌ No relevante | ❌ | ❌ | ❌ | ❌ |
| `takedownsBeforeJungleMinionSpawn` | Eliminaciones antes del spawn de la jungla (nivel 1) | ⚠️ Invasión | ✅ Coordinación nivel 1 | ⚠️ Invasión | ⚠️ | ⚠️ |
| `takedownsAfterGainingLevelAdvantage` | Eliminaciones tras ganar ventaja de nivel | ✅ Uso de ventaja | ⚠️ | ✅ | ⚠️ | ❌ |
| `takedownOnFirstTurret` | Participó en la primera torre | ✅ | ✅ | ✅ | ✅ | ✅ |
| `shortestTimeToAceFromFirstTakedown` | Tiempo más corto de la primera kill al Ace | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `killedChampTookFullTeamDamageSurvived` | Mató a un campeón, recibió todo el daño del equipo y sobrevivió | ✅ Tanques | ⚠️ | ❌ | ❌ | ⚠️ |
| `maxKillDeficit` | Mayor déficit de kills antes de una remontada | ⚠️ Contexto | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `outnumberedNexusKill` | Kill de nexo en inferioridad numérica | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `elderDragonMultikills` | Multikills con buff de Elder Dragon | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `elderDragonKillsWithOpposingSoul` | Kills de Elder Dragon cuando el enemigo tiene soul | ❌ | ✅ | ❌ | ❌ | ❌ |
| `teamBaronKills` | Barones del equipo | ⚠️ Equipo | ✅ Responsabilidad del jungla | ⚠️ | ⚠️ | ⚠️ |
| `teamRiftHeraldKills` | Heraldos del equipo | ⚠️ | ✅ | ⚠️ | ❌ | ❌ |
| `teamElderDragonKills` | Elders del equipo | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| `killsWithHelpFromEpicMonster` | Kills con ayuda de monstruo épico (ej: Barón) | ❌ | ⚠️ | ❌ | ❌ | ❌ |
| `soloBaronKills` | Barones matados en solitario | ❌ | ⚠️ Raro pero posible | ❌ | ❌ | ❌ |

---

## Sección B — Eventos del Timeline (Match Timeline)

Estos datos provienen del endpoint `/lol/match/v5/matches/{matchId}/timeline`.

---

### B.1 — Frames: Estado por Minuto (participantFrames)

Cada frame (generado cada ~60 segundos) contiene un snapshot del estado de cada jugador:

| Campo | Descripción | Top | Jungle | Mid | ADC | Support |
|---|---|---|---|---|---|---|
| `totalGold` | Oro total acumulado | ✅ Curva de oro | ✅ | ✅ | ✅ | ⚠️ Techo bajo |
| `currentGold` | Oro sin gastar | ⚠️ Gestión de backs | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `level` | Nivel del campeón | ✅ Ventaja de XP | ✅ | ✅ | ✅ | ⚠️ |
| `xp` | Experiencia actual | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| `minionsKilled` | Súbditos de línea acumulados | ✅ Curva de CS | ❌ | ✅ | ✅ | ❌ |
| `jungleMinionsKilled` | Monstruos de jungla acumulados | ❌ | ✅ Curva de clear | ❌ | ❌ | ❌ |
| `position` (`x`, `y`) | Coordenadas en el mapa | ⚠️ Tracking de split push | ✅ Análisis de pathing | ⚠️ Tracking de roams | ⚠️ Posicionamiento en fights | ⚠️ Posicionamiento |
| `timeEnemySpentControlled` | Tiempo que el jugador aplicó CC acumulado | ⚠️ | ⚠️ | ⚠️ | ❌ | ✅ |

**Métricas derivadas del Timeline (que podemos calcular nosotros):**

| Métrica Derivada | Cómo se calcula | Top | Jungle | Mid | ADC | Support |
|---|---|---|---|---|---|---|
| Gold Diff @10 min | `totalGold` del jugador vs oponente directo en frame del min 10 | ✅ | ✅ vs jungla rival | ✅ | ✅ vs ADC rival | ⚠️ |
| Gold Diff @15 min | Igual pero al min 15 | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| CS Diff @10 min | `minionsKilled` del jugador vs oponente en frame del min 10 | ✅ | ❌ | ✅ | ✅ | ❌ |
| XP Diff @10 min | `xp` del jugador vs oponente en frame del min 10 | ✅ | ⚠️ | ✅ | ⚠️ | ❌ |
| Pathing efficiency | Análisis de coordenadas consecutivas del jungla | ❌ | ✅ Ruta óptima | ❌ | ❌ | ❌ |

---

### B.2 — Eventos del Timeline

Cada frame contiene un arreglo `events[]` con todos los sucesos ocurridos en ese minuto. Los tipos de evento son:

#### `CHAMPION_KILL` — Un campeón fue asesinado
| Campo | Descripción |
|---|---|
| `timestamp` | Momento exacto en milisegundos. |
| `killerId` | ID del jugador que mató. |
| `victimId` | ID del jugador que murió. |
| `assistingParticipantIds` | Lista de IDs de asistentes. |
| `position` (`x`, `y`) | Coordenadas donde ocurrió la muerte. |
| `bounty` | Oro de recompensa por la kill. |
| `shutdownBounty` | Oro de shutdown (si había racha). |

**Relevancia por Rol:**
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Permite calcular: muertes en solitario, muertes bajo torre, muertes por ganks (analizando si hay asistentes del jungla). |
| Jungle | ✅ | Permite calcular: ganks exitosos (kills con asistencias en otras líneas), muertes en invasiones. |
| Mid | ✅ | Permite calcular: muertes por ganks, kills en roams (por posición). |
| ADC | ✅ | Permite calcular: muertes en lane 2v2, muertes en teamfights (por timestamp). |
| Support | ✅ | Permite calcular: asistencias tempranas, muertes protegiendo al ADC. |

#### `ELITE_MONSTER_KILL` — Monstruo épico asesinado
| Campo | Descripción |
|---|---|
| `timestamp` | Momento exacto. |
| `killerId` | Quién dio el último golpe (generalmente el jungla). |
| `assistingParticipantIds` | Asistentes. |
| `monsterType` | Tipo: `DRAGON`, `BARON_NASHOR`, `RIFTHERALD`, `HORDE` (Voidgrubs). |
| `monsterSubType` | Subtipo del dragón: `FIRE_DRAGON`, `WATER_DRAGON`, `EARTH_DRAGON`, `AIR_DRAGON`, `CHEMTECH_DRAGON`, `HEXTECH_DRAGON`, `ELDER_DRAGON`. |

**Relevancia por Rol:**
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Se puede medir: participación en objetivos (si aparece en `assistingParticipantIds`). Muertes antes del objetivo. |
| Jungle | ✅ | Métrica principal: ¿aseguró el objetivo? ¿Qué dragones tomó? ¿A qué minuto? |
| Mid | ⚠️ | Mide si estaba presente ayudando con el objetivo. |
| ADC | ✅ | Mide si estaba presente haciendo DPS al objetivo. |
| Support | ✅ | Mide si estaba dando visión y CC para asegurar el objetivo. |

#### `BUILDING_KILL` — Estructura destruida
| Campo | Descripción |
|---|---|
| `timestamp` | Momento exacto. |
| `killerId` | Quién destruyó la estructura. |
| `assistingParticipantIds` | Asistentes. |
| `buildingType` | `TOWER_BUILDING` o `INHIBITOR_BUILDING`. |
| `towerType` | `OUTER_TURRET`, `INNER_TURRET`, `BASE_TURRET`, `NEXUS_TURRET`. |
| `laneType` | `TOP_LANE`, `MID_LANE`, `BOT_LANE`. |
| `teamId` | Equipo al que pertenecía la estructura. |

**Relevancia por Rol:**
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Permite calcular: torres destruidas en top lane (split push), tiempo de la primera torre top. |
| Jungle | ✅ | Participación en destrucción de torres post-gank. |
| Mid | ✅ | Torres de mid abren rotaciones. |
| ADC | ✅ | Torres de bot y contribución general. |
| Support | ⚠️ | Participación en tomas de torres. |

#### `TURRET_PLATE_DESTROYED` — Placa de torre destruida
| Campo | Descripción |
|---|---|
| `timestamp` | Momento exacto. |
| `killerId` | Quién destruyó la placa. |
| `laneType` | En qué línea. |
| `teamId` | Equipo al que pertenecía la torre. |

**Relevancia por Rol:**
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ✅ | Oro temprano directo de dominar la línea. |
| Jungle | ⚠️ | Puede tomar placas tras ganks, pero no es prioritario. |
| Mid | ✅ | Oro temprano directo. |
| ADC | ✅ | Placas de bot son una fuente importante de oro. |
| Support | ⚠️ | Puede asistir, pero el oro debería ir al ADC. |

#### `ITEM_PURCHASED` — Item comprado
| Campo | Descripción |
|---|---|
| `timestamp` | Momento de la compra. |
| `participantId` | Quién compró. |
| `itemId` | ID del item comprado. |

**Relevancia por Rol:**
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | ⚠️ | Permite analizar builds: timing de objetos clave, si se compran los items correctos para la situación. Requiere una base de datos de items para interpretar. Complejidad alta de implementación para poco beneficio inmediato. |

#### `ITEM_SOLD` — Item vendido
| Campo | Descripción |
|---|---|
| `timestamp` | Momento de la venta. |
| `participantId` | Quién vendió. |
| `itemId` | ID del item vendido. |

**Relevancia por Rol:**
| Todos | ⚠️ | Puede indicar cambios de build (vender item para comprar otro). Baja prioridad para análisis. |

#### `ITEM_DESTROYED` — Item destruido/consumido
| Campo | Descripción |
|---|---|
| `timestamp` | Momento de la destrucción. |
| `participantId` | A quién le pertenecía. |
| `itemId` | ID del item destruido. |

**Relevancia por Rol:**
| Todos | ⚠️ | Incluye consumo de pociones y destrucción de items al upgradear. Baja prioridad. |

#### `ITEM_UNDO` — Compra deshecha
| Campo | Descripción |
|---|---|
| `timestamp` | Momento del undo. |
| `participantId` | Quién lo deshizo. |
| `beforeId` | Item antes del undo. |
| `afterId` | Item después del undo. |

**Relevancia por Rol:**
| Todos | ❌ | No aporta información útil para análisis de rendimiento. |

#### `SKILL_LEVEL_UP` — Habilidad subida de nivel
| Campo | Descripción |
|---|---|
| `timestamp` | Momento exacto. |
| `participantId` | Quién subió la habilidad. |
| `skillSlot` | Slot de la habilidad (1=Q, 2=W, 3=E, 4=R). |
| `levelUpType` | Tipo de subida (`NORMAL`, `EVOLVE`). |

**Relevancia por Rol:**
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | ⚠️ | Permite analizar si el jugador sube las habilidades en el orden correcto según el matchup. Requiere conocimiento de builds óptimas por campeón. Complejidad alta. |

#### `LEVEL_UP` — Subida de nivel del campeón
| Campo | Descripción |
|---|---|
| `timestamp` | Momento exacto. |
| `participantId` | Quién subió de nivel. |
| `level` | Nivel alcanzado. |

**Relevancia por Rol:**
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | ⚠️ | Permite calcular cuándo alcanzó niveles clave (6, 11, 16). Comparado con el oponente, indica ventaja de XP. |

#### `WARD_PLACED` — Ward colocado
| Campo | Descripción |
|---|---|
| `timestamp` | Momento exacto. |
| `creatorId` | Quién lo colocó. |
| `wardType` | Tipo: `YELLOW_TRINKET`, `CONTROL_WARD`, `SIGHT_WARD`, `BLUE_TRINKET`. |

**Relevancia por Rol:**
| Rol | Relevancia | Justificación |
|---|---|---|
| Top | ⚠️ | Wards en bushes clave de la línea para evitar ganks. |
| Jungle | ✅ | Wards en objetivos y zonas de invade. El timestamp indica si protege antes de objetivos. |
| Mid | ⚠️ | Wards en los bushes del río. |
| ADC | ⚠️ | Contribución mínima. |
| Support | ✅ | Permite analizar cuándo y dónde coloca wards. ¿Antes de objetivos? ¿En bushes del río? |

#### `WARD_KILL` — Ward destruido
| Campo | Descripción |
|---|---|
| `timestamp` | Momento exacto. |
| `killerId` | Quién lo destruyó. |
| `wardType` | Tipo del ward destruido. |

**Relevancia por Rol:**
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | Misma lógica que `wardsKilled` en la sección de métricas de visión. Especialmente relevante para Jungle y Support. |

#### `CHAMPION_SPECIAL_KILL` — Kill especial
| Campo | Descripción |
|---|---|
| `timestamp` | Momento exacto. |
| `killerId` | Quién realizó la kill. |
| `killType` | `KILL_FIRST_BLOOD`, `KILL_MULTI`, `KILL_ACE`. |
| `multiKillLength` | Número de kills en multikill (si aplica). |

**Relevancia por Rol:**
| Todos | ⚠️ | Misma lógica que las métricas de multikill y primera sangre ya cubiertas. |

#### `CHAMPION_TRANSFORM` — Transformación de campeón
| Campo | Descripción |
|---|---|
| `timestamp` | Momento de la transformación. |
| `participantId` | Quién se transformó. |
| `transformType` | Tipo de transformación. |

**Relevancia por Rol:**
| Todos | ❓ | Solo aplica a campeones específicos (Kayn → Rhaast/Shadow Assassin). No es una métrica generalizable. |

#### `DRAGON_SOUL_GIVEN` — Alma de dragón otorgada
| Campo | Descripción |
|---|---|
| `timestamp` | Momento exacto. |
| `name` | Tipo de alma (`CHEMTECH_DRAGON`, `HEXTECH_DRAGON`, etc.). |
| `teamId` | Equipo que recibió el alma. |

**Relevancia por Rol:**
| Rol | Relevancia | Justificación |
|---|---|---|
| Todos | ⚠️ | Es un evento de equipo. Para el jungla, mide si aseguró 4 dragones. Para los demás, indica participación en la secuencia. |

#### `OBJECTIVE_BOUNTY_PRESTART` / `OBJECTIVE_BOUNTY_FINISH` — Bounties de objetivo
| Campo | Descripción |
|---|---|
| `timestamp` | Momento de activación/finalización. |
| `teamId` | Equipo que tiene los bounties disponibles. |

**Relevancia por Rol:**
| Todos | ⚠️ | Indica que el equipo va perdiendo (las bounties se activan cuando un equipo está atrás). Puede ser útil para contextualizar las métricas de oro/XP en partidas donde se va perdiendo. |

#### `GAME_END` — Fin de la partida
| Campo | Descripción |
|---|---|
| `timestamp` | Momento exacto del fin. |
| `winningTeam` | Equipo ganador. |

**Relevancia por Rol:**
| Todos | ✅ | Dato fundamental para calcular la duración real y el resultado. |

#### `PAUSE_START` / `PAUSE_END` — Pausas del juego
| Campo | Descripción |
|---|---|
| `timestamp` | Momento de la pausa/reanudación. |

**Relevancia por Rol:**
| Todos | ❌ | Solo ocurre en torneos/competitivo. No aplica para Clasificatoria Flex. |

---

## Sección C — Datos de Nivel Equipo (Team-Level)

Estos datos se encuentran en `info.teams[]` del detalle de partida:

| Campo | Descripción |
|---|---|
| `teamId` | 100 (Azul) o 200 (Rojo). |
| `win` | Si el equipo ganó. |
| `bans[]` | Lista de campeones baneados con `championId` y `pickTurn`. |
| `objectives` | Objetivos del equipo (ver abajo). |

**Objetivos del equipo (`objectives`):**

| Objetivo | Campos | Descripción |
|---|---|---|
| `baron` | `first`, `kills` | Barones asesinados y si fue primer barón. |
| `dragon` | `first`, `kills` | Dragones asesinados y si fue primer dragón. |
| `riftHerald` | `first`, `kills` | Heraldos asesinados. |
| `horde` | `first`, `kills` | Gusanos del Vacío (Voidgrubs). |
| `atakhan` | `first`, `kills` | Atakhan (objetivo nuevo). |
| `tower` | `first`, `kills` | Torres destruidas. |
| `inhibitor` | `first`, `kills` | Inhibidores destruidos. |
| `champion` | `first`, `kills` | Campeones asesinados y si fue primera sangre del equipo. |

**Relevancia:** Son datos de equipo, no individuales. Útiles para contextualizar el rendimiento del jugador dentro de su equipo.

---

## Sección D — Métricas que actualmente calculamos vs. lo posible

### Lo que ya calcula nuestro `MetricsEngine`

| Métrica | Fuente | Diferenciada por Rol |
|---|---|---|
| `cs_per_min` | Match Details | ❌ No — Se calcula igual para todos los roles |
| `gold_per_min` | Match Details | ❌ No |
| `vision_per_min` | Match Details | ❌ No |
| `kill_participation` | Match Details | ❌ No |
| `deaths_before_objectives` | Timeline | ❌ No |
| `gold_diff_10` | Timeline | ❌ No — Además solo mide oro propio, no la diferencia vs oponente |
| `gold_diff_15` | Timeline | ❌ No — Mismo problema |

### Lo que podríamos calcular diferenciando por rol

| Métrica Propuesta | Roles donde es Útil | Fuente | Complejidad |
|---|---|---|---|
| CS/min diferenciado (con benchmarks por rol) | Top, Mid, ADC | Match Details | 🟢 Baja |
| Gold Diff vs Lane Opponent @10 y @15 | Top, Mid, ADC | Timeline | 🟡 Media — Requiere identificar al oponente directo |
| Participación en dragones/barón | Jungle, ADC, Support | Timeline | 🟡 Media |
| Wards colocados y destruidos antes de objetivos | Jungle, Support | Timeline | 🟡 Media |
| Ganks exitosos (kills con asist. del jungla en otras líneas) | Jungle | Timeline | 🟡 Media |
| Control de visión por minuto (con benchmarks por rol) | Support, Jungle | Match Details | 🟢 Baja |
| Daño a campeones como % del equipo | Mid, ADC | Match Details | 🟢 Baja |
| Daño mitigado (para tanques) | Top tanque, Support tanque | Match Details | 🟢 Baja |
| Curación/Escudos efectivos | Support encantador | Match Details | 🟢 Baja |
| CC aplicado (tiempo y count) | Support, Jungle, Top tanque | Match Details | 🟢 Baja |
| Placas de torre tomadas | Top, Mid, ADC | Match Details | 🟢 Baja |
| Muertes pre-dragón diferenciadas (¿murió antes de dragón en bot?) | Todos, pero especialmente ADC y Support | Timeline | 🔴 Alta |
| Pathing del jungla (análisis de coordenadas) | Jungle | Timeline | 🔴 Muy Alta |
| Timing de items clave | Todos | Timeline | 🔴 Alta — Requiere DB de items |

> **Nota importante:** Actualmente ya almacenamos tanto el `raw_match_json` como el `raw_timeline_json` completos en la base de datos (tabla `matches`), lo que significa que **no necesitamos hacer llamadas adicionales a la API de Riot** para implementar cualquiera de estas métricas nuevas. Solo necesitamos expandir nuestro `MetricsEngine` para extraer más información de los JSONs ya guardados.
