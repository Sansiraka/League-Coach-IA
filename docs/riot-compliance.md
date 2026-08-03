# League Coach IA - Cumplimiento de Políticas de Riot Games

Este proyecto ha sido diseñado estrictamente para cumplir con los Términos de Servicio de Riot Games y sus Políticas para Desarrolladores (Developer Policies).

## 1. Naturaleza del Proyecto
- El proyecto es una herramienta **Post-Partida (Post-Game)**. No interactúa de ninguna manera con el juego mientras éste se está ejecutando.
- No utiliza lectura de memoria, inyección de código ni manipulación del cliente de juego de League of Legends.

## 2. Acceso a Datos
- Toda la información del juego proviene exclusivamente de la **API oficial de Riot Games** (`developer.riotgames.com`), específicamente de los endpoints `Account-V1` y `Match-V5`.
- Se gestionarán y respetarán estrictamente los límites de peticiones (Rate Limits) provistos por Riot Games, manejando correctamente los errores HTTP 429.

## 3. Ventajas Injustas
- Al ser una herramienta post-partida, no otorga información en tiempo real a los jugadores (como temporizadores ocultos, posición de enemigos o avisos de enfriamiento de habilidades).
- Su propósito es meramente analítico y educativo.

## 4. Privacidad y Seguridad
- Las claves de API (`RIOT_API_KEY`) se considerarán material sensible y nunca serán publicadas en repositorios públicos.
- Todos los datos procesados pertenecerán al jugador que instala localmente la aplicación, ya que el alcance inicial es de uso individual (no es un SaaS que exponga datos de terceros públicamente sin autorización).
