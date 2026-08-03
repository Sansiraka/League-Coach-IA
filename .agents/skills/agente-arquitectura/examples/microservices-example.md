# Ejemplo: Arquitectura de Microservicios — E-Commerce

## Visión General

```mermaid
graph TB
    subgraph "Cliente"
        WEB["🌐 Web App\nReact"]
        MOB["📱 Mobile App\nReact Native"]
    end

    subgraph "Gateway"
        GW["🚪 API Gateway\nNginx/Kong"]
    end

    subgraph "Servicios"
        AUTH["🔐 Auth Service\nNode.js"]
        PROD["📦 Product Service\nPython"]
        ORDER["🛒 Order Service\nJava"]
        PAY["💳 Payment Service\nGo"]
        NOTIF["📧 Notification Service\nNode.js"]
    end

    subgraph "Datos"
        DB1[("PostgreSQL\nUsers")]
        DB2[("MongoDB\nProducts")]
        DB3[("PostgreSQL\nOrders")]
        CACHE[("Redis\nCache")]
        MQ["RabbitMQ\nMensajería"]
    end

    WEB --> GW
    MOB --> GW
    GW --> AUTH
    GW --> PROD
    GW --> ORDER
    GW --> PAY
    AUTH --> DB1
    PROD --> DB2
    PROD --> CACHE
    ORDER --> DB3
    ORDER --> MQ
    PAY --> MQ
    MQ --> NOTIF

    style GW fill:#4285F4,stroke:#333,color:#fff
    style AUTH fill:#34A853,stroke:#333,color:#fff
    style PROD fill:#FBBC04,stroke:#333,color:#000
    style ORDER fill:#EA4335,stroke:#333,color:#fff
    style PAY fill:#9C27B0,stroke:#333,color:#fff
    style NOTIF fill:#FF9800,stroke:#333,color:#fff
```

## Componentes

| Servicio | Tecnología | Base de Datos | Puerto | Responsabilidad |
|----------|-----------|:---:|:---:|------------------|
| API Gateway | Nginx/Kong | — | 80/443 | Routing, rate limiting, SSL |
| Auth Service | Node.js + Express | PostgreSQL | 3001 | Autenticación y autorización |
| Product Service | Python + FastAPI | MongoDB | 3002 | Catálogo de productos |
| Order Service | Java + Spring Boot | PostgreSQL | 3003 | Gestión de pedidos |
| Payment Service | Go + Gin | — | 3004 | Procesamiento de pagos |
| Notification Service | Node.js | — | 3005 | Emails, SMS, push |

## Flujo: Crear Pedido

```mermaid
sequenceDiagram
    actor U as Usuario
    participant GW as API Gateway
    participant AUTH as Auth Service
    participant ORD as Order Service
    participant PROD as Product Service
    participant PAY as Payment Service
    participant MQ as RabbitMQ
    participant NOTIF as Notification

    U->>GW: POST /orders (JWT)
    GW->>AUTH: Validar Token
    AUTH-->>GW: Token válido
    GW->>ORD: Crear Pedido
    ORD->>PROD: Verificar Stock
    PROD-->>ORD: Stock OK
    ORD->>PAY: Procesar Pago
    PAY-->>ORD: Pago exitoso
    ORD->>MQ: Evento: PedidoCreado
    MQ->>NOTIF: Notificar usuario
    ORD-->>GW: 201 Created
    GW-->>U: Pedido confirmado
```

## Decisiones Arquitectónicas

| ADR | Decisión | Razón |
|-----|----------|-------|
| ADR-001 | Database per Service | Independencia y escalabilidad |
| ADR-002 | Event-driven para notificaciones | Desacoplamiento |
| ADR-003 | API Gateway centralizado | Seguridad y routing unificado |
| ADR-004 | JWT para autenticación | Stateless, escalable |

## Estructura de Carpetas

```
ecommerce/
├── services/
│   ├── auth-service/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── package.json
│   ├── product-service/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── ...
├── gateway/
│   └── nginx.conf
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```
