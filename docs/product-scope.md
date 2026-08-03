# League Coach IA - Product Scope

## 1. Problema
Los jugadores de League of Legends (especialmente en Clasificatoria Flexible) carecen de feedback objetivo, accionable y libre de toxicidad que se base en datos reales. A menudo es difícil saber por qué se pierde o qué mejorar debido a la enorme cantidad de variables en cada partida, y las herramientas de terceros suelen abrumar con demasiados datos estadísticos crudos.

## 2. Historias de Usuario
- **Como** jugador de LoL en Clasificatoria Flexible, **quiero** importar automáticamente mis últimas partidas **para** tener una base de datos actualizada de mis resultados.
- **Como** jugador, **quiero** ver mis métricas clave (CS, visión, KDA, participación en objetivos) **para** evaluar si estoy cumpliendo los estándares de mi rol y liga.
- **Como** jugador, **quiero** recibir 3 áreas de mejora prioritarias en lenguaje claro y basado en mis estadísticas **para** practicar algo concreto en mi próxima sesión.
- **Como** jugador, **quiero** evaluar los consejos recibidos (útil, ya lo sabía, no es útil) **para** que el sistema entienda mejor mi contexto y adapte su feedback futuro.

## 3. Requisitos Clave
- **Ingesta:** Conexión con la API de Riot (Account-V1, Match-V5) respetando los rate limits.
- **Filtros:** Capacidad de extraer exclusivamente métricas y partidas de Ranked Flex (`queue=440`).
- **Análisis Matemático:** Algoritmo determinista para el cálculo de estadísticas (CS/min, KP%, oro, control de visión).
- **Procesamiento de Lenguaje Natural:** Integración con Groq pasando únicamente un esquema JSON compactado de métricas (cero alucinaciones).
- **Almacenamiento Local:** Base de datos PostgreSQL local para mantener la privacidad de los datos del jugador.

## 4. Fuera de Alcance Inicial
- Overlay o aplicación en tiempo real superpuesta al cliente de LoL.
- Análisis o juzgamiento del desempeño de los compañeros de equipo (la IA no puede "flamear" a otros).
- Extracción de VODs o análisis visual del minimapa mediante imágenes.
- Aplicación multijugador pública o SaaS (solo se desarrollará una versión de uso personal/local).

## 5. Criterios de Éxito
- La aplicación puede importar de forma fiable el historial completo (últimas 20-50 partidas).
- El coach de IA proporciona análisis respaldados estrictamente por las estadísticas enviadas.
- La latencia total entre terminar una partida y ver el reporte post-partida no supera 1 minuto.
- La aplicación se levanta limpiamente con un solo `docker-compose up`.
