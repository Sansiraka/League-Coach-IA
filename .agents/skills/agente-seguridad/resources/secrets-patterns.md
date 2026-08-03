# Patrones de Detección de Secrets

## Patrones Regex para Detección

### API Keys y Tokens

| Servicio | Patrón | Ejemplo |
|----------|--------|---------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | AKIAIOSFODNN7EXAMPLE |
| AWS Secret Key | `[A-Za-z0-9/+=]{40}` | wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY |
| Google API Key | `AIza[0-9A-Za-z\-_]{35}` | AIzaSyA1234567890abcdefghijklmnopqrstuvw |
| GitHub Token | `gh[ps]_[A-Za-z0-9_]{36,}` | ghp_ABCDEFghijklmnop1234567890abcdef |
| Slack Token | `xox[baprs]-[0-9a-zA-Z-]+` | xoxb-1234-5678-abcdef |
| Stripe Key | `[rs]k_(test\|live)_[0-9a-zA-Z]{24,}` | sk_live_1234567890abcdefghijklmn |
| JWT | `eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+` | eyJhbGci... |

### Credenciales Genéricas

```regex
# Passwords en código
(?i)(password|passwd|pwd|secret|token|api_key|apikey|access_key)\s*[=:]\s*['"][^'"]{8,}['"]

# Connection Strings
(?i)(mongodb|postgres|mysql|redis|amqp)://[^\s'"]+:[^\s'"]+@

# Private Keys
-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----

# Bearer Tokens
(?i)bearer\s+[a-zA-Z0-9\-._~+/]+=*
```

## Archivos a Escanear con Prioridad

| Prioridad | Archivos | Razón |
|:-:|----------|-------|
| 🔴 Alta | `.env`, `.env.local`, `.env.production` | Variables de entorno |
| 🔴 Alta | `docker-compose.yml`, `Dockerfile` | Credenciales de servicios |
| 🔴 Alta | `*.config.js`, `*.config.ts` | Configuración con secrets |
| 🟠 Media | `application.yml`, `application.properties` | Config Java/Spring |
| 🟠 Media | `settings.py`, `config.py` | Config Python |
| 🟡 Baja | `*.json`, `*.yaml`, `*.toml` | Archivos de configuración |

## Archivos que NUNCA deben estar en Git

Verificar que `.gitignore` incluya:
```
.env
.env.*
*.pem
*.key
*.p12
*.jks
id_rsa
id_ed25519
*.secret
credentials.json
service-account*.json
```

## Remediación

1. **Rotar inmediatamente** cualquier secret expuesto.
2. **Usar variables de entorno** en lugar de hardcodear.
3. **Usar gestores de secrets** (Vault, AWS Secrets Manager, GCP Secret Manager).
4. **Configurar pre-commit hooks** con herramientas como `gitleaks` o `trufflehog`.
5. **Revisar el historial de Git** — secrets eliminados del código aún existen en commits anteriores.
