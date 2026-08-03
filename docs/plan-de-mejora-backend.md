# Plan de Mejora Continua — Backend (League Coach IA)

Este documento detalla las propuestas estratégicas para escalar y robustecer el backend de la aplicación, llevándolo de un estado de MVP (Producto Mínimo Viable) a una arquitectura lista para producción.

## 1. [✅ COMPLETADO] Análisis por Arquetipo de Campeón (Hyper-Personalización)
Actualmente, el `PriorityEngine` califica a todos los jugadores de un mismo rol con la misma regla. 
*   **Problema:** Un "Top Laner" que juega *Shen* (tanque de utilidad enfocado en salvar aliados con su R) tendrá naturalmente menos farmeo y daño a torres que un *Tryndamere* (split-pusher). El sistema actual penalizaría injustamente a Shen.
*   **Solución:** Crear un `ChampionArchetypeService` que clasifique a los campeones en arquetipos (Asesino, Tanque, Split-Pusher, Mago, etc.). Las métricas y prioridades se ponderarán dinámicamente según el arquetipo, no solo según el rol en el mapa.

## 2. Sincronización Asíncrona (Colas de Trabajo / Celery)
*   **Problema:** Extraer y calcular decenas de métricas complejas desde la API de Riot (Match Details + Timeline) consume varios segundos. Procesarlo de forma sincrónica bloqueará el servidor y congelará la UI del usuario.
*   **Solución:** Integrar un sistema de Background Tasks (Celery o FastAPI BackgroundTasks) junto con Redis. Las sincronizaciones ocurrirán en segundo plano, y el frontend recibirá actualizaciones en tiempo real (WebSockets o SSE) cuando el reporte esté listo.

## 3. Benchmarks Dinámicos (Auto-Actualizables)
*   **Problema:** El archivo `role_benchmarks.json` es estático. League of Legends evoluciona constantemente con nuevos parches que alteran la economía (ej. oro de la jungla) y el meta.
*   **Solución:** Implementar un proceso (Cron Job) que analice de forma periódica las estadísticas agregadas en nuestra propia base de datos, calculando automáticamente los nuevos umbrales del "Top 10%" (Excelente) y "Media" (Estándar), manteniendo el sistema permanentemente calibrado al meta actual.

## 4. Seguridad, Autenticación y Rate Limiting
*   **Problema:** Los endpoints actuales (como `/api/v1/coaching/generate/...`) son de acceso público. Esto abre la puerta a abusos masivos que pueden agotar nuestra cuota de la API de Groq (costos) y provocar baneos por Rate Limit en la API de Riot Games.
*   **Solución:** 
    *   Implementar autenticación robusta mediante tokens JWT.
    *   Integrar un Rate Limiter que restrinja el número de sincronizaciones o análisis de IA que un usuario puede solicitar por día.

## 5. Base de Datos Vectorial (RAG) para el Historial del Coach
*   **Problema:** Actualmente el Coach solo tiene memoria a corto plazo (las últimas partidas enviadas en el payload). No recuerda consejos dados hace un mes ni puede evaluar el progreso a largo plazo del jugador.
*   **Solución:** Almacenar los "Insights" generados previamente en una base de datos vectorial (Ej. Pinecone, ChromaDB). Utilizando la técnica RAG (Retrieval-Augmented Generation), el LLM podrá buscar consejos pasados y actuar como un tutor real que reconoce si el jugador sigue repetiendo los mismos errores semanas después.
