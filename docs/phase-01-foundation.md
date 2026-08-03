# Fase 01 — Fundación Técnica

## Fecha
2026-07-16

## Objetivo
Establecer el monorepo y preparar el entorno de ejecución para que el backend (FastAPI), el frontend (React/Vite) y la base de datos (PostgreSQL) se puedan ejecutar localmente sin fricción.

## Trabajo realizado
- Generación del andamiaje del frontend con `create-vite`.
- Creación de la estructura del backend (FastAPI, SQLAlchemy, modelos).
- Configuración global de Docker con `docker-compose.yml`.
- Configuración de variables de entorno `.env.example`.
- Modificación del `vite.config.ts` para permitir el acceso desde el host en Docker.

## Archivos creados o modificados
- `docker-compose.yml`: Orquestación de servicios.
- `backend/Dockerfile` y `frontend/Dockerfile`: Empaquetado individual de contenedores.
- `backend/main.py`: Punto de entrada con Health Check.
- `backend/models/player.py`: Primer modelo de base de datos traducido de la Fase 0.
- `frontend/*`: Todo el proyecto React + TS base.

## Decisiones técnicas
- Usar Docker Compose para orquestar la BD junto con el backend y frontend permite que cualquier desarrollador clone el repo y simplemente ejecute `docker-compose up -d`.
- El esquema del Player en SQLAlchemy usa UUID para mayor seguridad al exponer URLs en el futuro y almacena las metas como JSON nativo de PostgreSQL.

## Cómo probarlo
```bash
# Iniciar todo el stack
docker-compose up -d --build

# Verificar Backend
curl http://localhost:8000/health

# Verificar Frontend
# Abrir http://localhost:5173 en el navegador web
```

## Resultado
La Fase 1 se declara **COMPLETA**. Tenemos un andamiaje técnico listo para comenzar a codificar la lógica de negocio (Fase 2).

## Próxima fase
- **Fase 2 (Ingesta Riot API):** Programar el agente y las rutas necesarias en el backend para consultar, procesar y persistir las partidas desde Riot Games usando el `PUUID`.
