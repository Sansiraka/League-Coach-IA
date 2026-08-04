# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [1.1.0] - 2026-08-04

### 🚀 Añadido (Added)
- **Extracción de Fortalezas (Highlights & Benchmarks):** El `PriorityEngine` ahora identifica y recompensa matemáticamente logros destacables del jugador (ej. robos épicos, aliados salvados, outplays, esquives de skillshots).
- **Inyección de `top_strengths` a Groq:** El LLM ahora recibe un Top 3 de los mejores aciertos del jugador para generar retroalimentación positiva precisa basada en datos reales (eliminando alucinaciones sobre el desempeño positivo).
- **Evaluación Táctica y Macro Estratégica:** Se incorporaron perfiles avanzados evaluando las últimas partidas (`Lane Tyrant`, `Macro God`, `Vision Control`, `Jungle Mastery`) para brindar feedback sobre la toma de decisiones y no solo las mecánicas puras.
- **Scoreboard de Partida (End Game Screen):** Implementación de una tabla detallada Premium Hextech Glassmorphism por cada partida expandida (`MatchScoreboard.tsx`), mostrando estadísticas completas de los 10 jugadores (KDA, Daño, Oro, CS) y los objetivos conseguidos por cada equipo (Dragones, Barones, Torres).
- **Nuevo Endpoint Analítico:** Ruta agregada al backend (`GET /analytics/match/{match_id}`) para extraer estructuradamente la información de los participantes y equipos desde el JSON crudo de Riot Games.
- **Vista de Historial Mejorada:** La vista comprimida de la partida ahora exhibe la Fecha del encuentro, K/D/A exacto y el Ratio KDA directamente en la cabecera del acordeón.

### 🛠 Arreglado (Fixed)
- **Bugfix (Analytics Service):** Solucionada una falla crítica en la inyección de las variables maestras y eventos (outplays, dodges, ventaja de nivel) hacia el Motor de Prioridades, lo que antes causaba que no se detectaran fortalezas de las partidas procesadas.
- **Prevención de Pantalla Negra (White Screen of Death):** La sección "Análisis IA" ya no colapsa en el Frontend cuando la IA (Groq/Llama 3) omite propiedades. Se implementaron validaciones de Optional Chaining y Fallbacks (`|| []`).
- **Sanitización de LLM (Markdown Hallucinations):** El Backend ahora limpia los JSON de Groq vía Regex antes del parseo, eliminando la envoltura ````json ```` cuando el modelo alucina en formato de texto.

## [1.0.0] - 2026-08-03

### 🚀 Añadido (Added)
- **Coach IA Integrado:** Sistema impulsado por Llama 3 vía Groq, enfocado 100% en el cálculo matemático estricto de las métricas para evitar alucinaciones, brindando "Action & Success Metrics".
- **Inteligencia Situacional de Arquetipos:** Lógica Backend implementada para analizar objetos situacionales según el rol.
  - Exención grupal de ítems Corta-curas (Si alguien del equipo lo tiene, los demás no son penalizados).
  - Protección de Tenacidad para Tiradores (Si el soporte tiene Crisol de Mikael).
  - Tolerancia de resistencias para Magos y Asesinos.
- **Diseño Hextech Glassmorphism:** Implementación visual completa del Frontend (Tailwind CSS).
  - **Dashboard:** Tarjetas interactivas que hacen *auto-fetch* a los datos del jugador preconfigurado.
  - **Match History:** Acordeones desplegables con gráficas Recharts (Diferencia de oro al min 10, 15, 25) e historial de items situacionales verificados.
  - **AI Analysis:** Interfaz inmersiva para desplegar las Fortalezas, Debilidades y el Plan de Práctica del usuario.
- **Configuración Persistente (Settings):** Nueva sección visual para configurar permanentemente el `Game Name` y `Tag Line` en `localStorage` y en Contexto global.

### 🔄 Cambios (Changed)
- Refactorización de dependencias muertas (unused imports) en todo el código Frontend.
- Actualización de tipados estrictos TypeScript (`ReactNode`) para evitar fugas de memoria y optimizar el build en Vite.
- Renombrado de variable de estado de la IA de `status` a `verdict` en todo el stack para una semántica más precisa (Valores posibles: `CORRECT`, `MISSED`, `TEAM_COVERED`, `EXEMPT`).

### 🛠 Arreglado (Fixed)
- Error de PostCSS solucionado (Clase de color Tailwind `coach-accent-blue` mal referenciada).
- Bugs de ciclos infinitos prevenidos corrigiendo las dependencias del `useEffect` en `useDashboardOverview`.
