# Convenciones de Contratos de API

## Estructura Estándar de Respuestas

### Respuesta Exitosa (Single)
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "nombre": "Producto X",
    "precio": 29.99,
    "createdAt": "2024-01-15T10:30:00Z"
  }
}
```

### Respuesta Exitosa (Lista Paginada)
```json
{
  "success": true,
  "data": [
    { "id": "1", "nombre": "Producto A" },
    { "id": "2", "nombre": "Producto B" }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8,
    "hasNext": true,
    "hasPrev": false
  }
}
```

### Respuesta de Error
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "El usuario con ID '123' no fue encontrado",
    "details": [],
    "timestamp": "2024-01-15T10:30:00Z",
    "path": "/api/v1/users/123"
  }
}
```

## Códigos de Error Estándar

| Código | HTTP | Significado |
|--------|:----:|-------------|
| `VALIDATION_ERROR` | 400 | Datos de entrada inválidos |
| `UNAUTHORIZED` | 401 | Token faltante o expirado |
| `FORBIDDEN` | 403 | Sin permisos para esta acción |
| `RESOURCE_NOT_FOUND` | 404 | Recurso no existe |
| `CONFLICT` | 409 | Recurso duplicado |
| `RATE_LIMITED` | 429 | Demasiadas peticiones |
| `INTERNAL_ERROR` | 500 | Error interno del servidor |

## Convenciones de Endpoints

### RESTful URL Patterns
```
GET    /api/v1/users              # Listar usuarios
GET    /api/v1/users/:id           # Obtener usuario por ID
POST   /api/v1/users              # Crear usuario
PUT    /api/v1/users/:id           # Actualizar usuario completo
PATCH  /api/v1/users/:id           # Actualizar parcialmente
DELETE /api/v1/users/:id           # Eliminar usuario

# Relaciones
GET    /api/v1/users/:id/orders    # Pedidos de un usuario
POST   /api/v1/users/:id/orders    # Crear pedido para usuario

# Filtros y búsqueda
GET    /api/v1/users?role=admin&active=true
GET    /api/v1/users?search=juan&sort=name:asc&page=2&limit=20
```

## Headers Estándar

### Request
```
Content-Type: application/json
Authorization: Bearer <token>
X-Request-ID: <uuid>  (para trazabilidad)
```

### Response
```
Content-Type: application/json
X-Request-ID: <uuid>  (echo del request)
X-Rate-Limit-Remaining: 98
X-Rate-Limit-Reset: 1705312800
```

## Versionado de API

- Usar versionado en la URL: `/api/v1/`, `/api/v2/`
- Mantener backwards compatibility dentro de la misma versión mayor
- Deprecar endpoints con header `Deprecation: true` y `Sunset: <date>`
