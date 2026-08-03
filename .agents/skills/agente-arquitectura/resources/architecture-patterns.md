# Catálogo de Patrones Arquitectónicos

## Patrones de Estructura

### Monolito Modular
**Cuándo usar**: Equipos pequeños (<10), MVP, dominio no bien definido.
**Ventajas**: Simple de desarrollar, desplegar y depurar.
**Desventajas**: Escalabilidad limitada, acoplamiento potencial.

```
┌─────────────────────────────────────┐
│            Monolito                 │
│  ┌──────────┐  ┌──────────┐       │
│  │ Módulo A │  │ Módulo B │       │
│  │ (Auth)   │  │ (Orders) │       │
│  └────┬─────┘  └────┬─────┘       │
│       │              │             │
│  ┌────┴──────────────┴─────┐      │
│  │    Shared Database       │      │
│  └──────────────────────────┘      │
└─────────────────────────────────────┘
```

### Microservicios
**Cuándo usar**: Equipos grandes, dominios bien definidos, necesidad de escalar independientemente.
**Ventajas**: Escalabilidad independiente, autonomía de equipos, resiliencia.
**Desventajas**: Complejidad operacional, consistencia eventual, debugging distribuido.

### Arquitectura Hexagonal (Ports & Adapters)
**Cuándo usar**: Cuando la lógica de negocio es compleja y debe ser independiente de la infraestructura.
**Ventajas**: Alta testabilidad, independencia de frameworks, fácil de cambiar infraestructura.

```
         ┌──────────────────┐
    ─────│   Port (Input)   │─────
         └────────┬─────────┘
                  │
         ┌────────▼─────────┐
         │   Application    │
         │   (Use Cases)    │
         └────────┬─────────┘
                  │
         ┌────────▼─────────┐
         │     Domain       │
         │  (Business Logic)│
         └────────┬─────────┘
                  │
         ┌────────▼─────────┐
    ─────│  Port (Output)   │─────
         └──────────────────┘
```

### CQRS (Command Query Responsibility Segregation)
**Cuándo usar**: Cuando las lecturas y escrituras tienen requisitos muy diferentes.
**Ventajas**: Optimización independiente de lectura/escritura, escalabilidad.

### Event-Driven Architecture
**Cuándo usar**: Sistemas con muchas integraciones, procesamiento asíncrono, workflows complejos.
**Ventajas**: Desacoplamiento, escalabilidad, extensibilidad.

## Tabla de Decisión Rápida

| Escenario | Patrón Recomendado |
|-----------|--------------------|
| MVP / Prototipo | Monolito simple |
| Startup en crecimiento | Monolito modular |
| Múltiples equipos independientes | Microservicios |
| Lógica de negocio compleja | Hexagonal |
| Alto volumen lectura vs escritura | CQRS |
| Muchas integraciones externas | Event-Driven |
| Procesamiento en tiempo real | Event-Driven + Streaming |
| APIs públicas | API Gateway + Backend for Frontend |

## Patrones de Comunicación

| Patrón | Tipo | Uso |
|--------|------|-----|
| REST | Síncrono | APIs CRUD estándar |
| GraphQL | Síncrono | APIs con consultas complejas |
| gRPC | Síncrono | Comunicación entre microservicios |
| Message Queue | Asíncrono | Procesamiento en background |
| Event Bus | Asíncrono | Notificaciones entre servicios |
| WebSocket | Bidireccional | Tiempo real |

## Patrones de Datos

| Patrón | Cuándo Usar |
|--------|-------------|
| Database per Service | Microservicios con autonomía total |
| Shared Database | Monolitos, MVP |
| Event Sourcing | Auditoría completa, sistemas financieros |
| Saga Pattern | Transacciones distribuidas |
| Cache-Aside | Lecturas frecuentes, datos semi-estáticos |
