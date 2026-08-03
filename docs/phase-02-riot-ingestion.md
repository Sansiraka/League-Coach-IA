# Fase 02 — Ingesta de Riot API

## Fecha
2026-07-17

## Objetivo
Implementar la comunicación con los servidores de Riot Games para resolver el `PUUID` de un jugador y descargar de forma masiva su historial de partidas de la cola `Ranked Flex (440)`, persistiendo el resultado en la base de datos local para un posterior cálculo de métricas.

## Trabajo realizado
- Creación del modelo SQLAlchemy `Match` para almacenar `JSONB`.
- Creación del cliente HTTP `RiotClient` utilizando la librería asíncrona `httpx`.
- Implementación del manejo de Rate Limits capturando la cabecera `Retry-After` de los códigos HTTP `429`.
- Lógica de inserción sin duplicados a través del servicio `SyncService`.
- Creación de un endpoint manual de sincronización en `api/routes/sync.py`.
- Ejecución de prueba real exitosa con el perfil del jugador `Sansi#LAN`.

## Archivos creados o modificados
- `.env`: Se añadió la API Key oficial del usuario.
- `backend/models/match.py`: Esquema base de la tabla `matches`.
- `backend/alembic/env.py`: Refactorización para descubrir modelos dinámicamente usando el archivo de configuración global.
- `backend/services/riot_client.py`: Componente de comunicación de red con la API de Riot.
- `backend/services/sync_service.py`: Lógica de sincronización.
- `backend/api/routes/sync.py`: Controlador FastAPI expuesto en `/sync/{game_name}/{tag_line}`.
- `docker-compose.yml`: Se conectó el contenedor con el archivo de entorno mediante `env_file`.

## Decisiones técnicas
- **Cola por defecto:** Todo se filtra por `queue_id=440` (Ranked Flex) para respetar el core business del MVP.
- **Tipado Flexible (JSONB):** Como los DTO de `Match-V5` pueden llegar a ser muy complejos o cambiar versiones con el tiempo, se ha guardado el JSON entero bajo un formato `JSONB` de PostgreSQL. Esto permitirá que en la Fase 3, el agente de métricas pueda leer libremente cualquier estadística interna (como `totalMinionsKilled`, eventos del `timeline`, etc.) sin tener que mapear cientos de campos nativamente a columnas rígidas.

## Cómo probarlo
```bash
# Lanzar comando de sync desde la terminal
curl -X POST http://localhost:8000/sync/Sansi/LAN
```

## Resultado
La Fase 2 se declara **COMPLETA**. Se lograron importar las primeras 20 partidas del historial del usuario `Sansi` en la región LAN y se resolvieron correctamente.

## Próxima fase
- **Fase 3 (Motor de Métricas):** Crear scripts/servicios en el backend para recorrer las partidas persistidas en base de datos, interpretar su timeline y calcular promedios (CS/min, KP, Muertes antes de dragón) sin utilizar Inteligencia Artificial.
