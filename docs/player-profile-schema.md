# League Coach IA - Esquema del Perfil de Jugador

Este documento define la estructura de datos que representa a un jugador y sus configuraciones dentro de la aplicación. Servirá como base para la tabla `players` de la base de datos PostgreSQL.

## Estructura (Modelo Pydantic / SQLAlchemy)

```python
{
    "id": "uuid4",  # Identificador interno del sistema
    "puuid": "string",  # Player Universal Unique Identifier de Riot Games
    "riot_id": "string",  # Nombre del jugador (ej. Faker)
    "tag_line": "string", # Tag (ej. T1)
    "region": "string",   # Región de la cuenta (ej. la1, na1)
    "preferred_queue": 440,  # 440 para Ranked Flex 5v5
    "preferred_role": "string",  # TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY
    "goals_json": [
        "mejorar la recolección de súbditos por minuto en los primeros 10 minutos",
        "incrementar el control de visión en la jungla aliada"
    ],
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

## Consideraciones

1. **PUUID como pilar:** Todos los llamados posteriores a la API de Riot (como la obtención de partidas) se realizarán utilizando el `puuid`. El `riot_id` y `tag_line` se usan solo para la resolución inicial.
2. **`goals_json` (Metas):** Es fundamental proveer esto en el payload para Groq, ya que permite a la IA contextualizar los consejos de acuerdo con lo que el jugador desea mejorar.
3. **Múltiples perfiles:** Aunque la herramienta está diseñada para uso personal, el modelo soportaría trackear múltiples cuentas "smurf" al permitir distintos `puuid` asociados.
