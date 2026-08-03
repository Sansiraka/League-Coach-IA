# Guía de Frameworks de Testing por Lenguaje

## JavaScript / TypeScript

| Framework | Tipo | Uso Recomendado |
|-----------|------|------------------|
| **Jest** | Unitario + Integración | Proyectos React, Node.js general |
| **Vitest** | Unitario + Integración | Proyectos Vite, más rápido que Jest |
| **Mocha + Chai** | Unitario | Configuración flexible |
| **Playwright** | E2E | Testing de navegador moderno |
| **Cypress** | E2E | Testing visual y de componentes |
| **Testing Library** | Componentes | React, Vue, Angular |

### Configuración Rápida — Jest
```bash
npm install -D jest @types/jest ts-jest
```

```json
// jest.config.json
{
  "preset": "ts-jest",
  "testEnvironment": "node",
  "coverageThreshold": {
    "global": { "branches": 80, "functions": 80, "lines": 80 }
  }
}
```

### Configuración Rápida — Vitest
```bash
npm install -D vitest @vitest/coverage-v8
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: {
    coverage: { provider: 'v8', reporter: ['text', 'html'] },
  },
});
```

## Python

| Framework | Tipo | Uso Recomendado |
|-----------|------|------------------|
| **pytest** | Unitario + Integración | Estándar de la industria |
| **unittest** | Unitario | Incluido en stdlib |
| **pytest-cov** | Cobertura | Plugin de cobertura |
| **pytest-mock** | Mocking | Plugin de mocking |
| **Selenium / Playwright** | E2E | Testing de navegador |
| **httpx / requests-mock** | API | Testing de endpoints |

### Configuración Rápida — pytest
```bash
pip install pytest pytest-cov pytest-mock
```

```ini
# pytest.ini
[pytest]
testpaths = tests
addopts = --cov=src --cov-report=html --verbose
```

## Java / Kotlin

| Framework | Tipo | Uso Recomendado |
|-----------|------|------------------|
| **JUnit 5** | Unitario | Estándar de la industria |
| **Mockito** | Mocking | El más popular |
| **AssertJ** | Aserciones | Aserciones fluidas |
| **Spring Boot Test** | Integración | Apps Spring Boot |
| **Testcontainers** | Integración | Tests con contenedores Docker |

## Go

| Framework | Tipo | Uso Recomendado |
|-----------|------|------------------|
| **testing** (stdlib) | Unitario | Incluido en Go |
| **testify** | Unitario | Aserciones y mocks |
| **gomock** | Mocking | Generación de mocks |
| **httptest** | API | Testing de HTTP handlers |

## Comandos Comunes

```bash
# JavaScript/TypeScript
npm test                    # Ejecutar tests
npm test -- --coverage      # Con cobertura
npm test -- --watch         # Modo watch

# Python
pytest                      # Ejecutar tests
pytest --cov                # Con cobertura
pytest -x                   # Parar al primer fallo

# Java (Maven)
mvn test                    # Ejecutar tests
mvn verify                  # Tests + integración

# Go
go test ./...               # Ejecutar todos los tests
go test -cover ./...        # Con cobertura
```
