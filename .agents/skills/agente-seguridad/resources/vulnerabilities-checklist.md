# Checklist de Vulnerabilidades — Referencia Completa

## Inyección

### SQL Injection
- [ ] ¿Se usan consultas parametrizadas/prepared statements?
- [ ] ¿Se valida el tipo de dato de los parámetros?
- [ ] ¿Se usa un ORM correctamente (sin raw queries inseguras)?

```javascript
// ❌ VULNERABLE
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ SEGURO
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

### XSS (Cross-Site Scripting)
- [ ] ¿Se escapan las salidas HTML?
- [ ] ¿Se usa CSP (Content Security Policy)?
- [ ] ¿Se sanitizan inputs antes de renderizar?

```javascript
// ❌ VULNERABLE
element.innerHTML = userInput;

// ✅ SEGURO
element.textContent = userInput;
// o usar DOMPurify para HTML necesario
element.innerHTML = DOMPurify.sanitize(userInput);
```

### Command Injection
- [ ] ¿Se evita `exec()`, `system()`, `eval()`?
- [ ] ¿Se usan listas blancas para comandos permitidos?

```python
# ❌ VULNERABLE
os.system(f"ping {user_input}")

# ✅ SEGURO
import subprocess
subprocess.run(["ping", "-c", "4", validated_hostname], check=True)
```

## Autenticación y Sesiones

- [ ] ¿Las passwords se hashean con bcrypt/argon2 (NO MD5/SHA1)?
- [ ] ¿Los tokens JWT tienen expiración razonable?
- [ ] ¿Se invalidan sesiones en logout?
- [ ] ¿Se implementa rate limiting en login?
- [ ] ¿Se usa HTTPS para transmitir credenciales?
- [ ] ¿Las cookies de sesión tienen flags Secure, HttpOnly, SameSite?

## Control de Acceso

- [ ] ¿Se validan permisos en CADA endpoint (no solo en la UI)?
- [ ] ¿Se previene IDOR (Insecure Direct Object Reference)?
- [ ] ¿Se aplica principio de mínimo privilegio?
- [ ] ¿Los endpoints admin están protegidos?

## Criptografía

| Uso | ❌ Inseguro | ✅ Seguro |
|-----|-----------|----------|
| Hashing passwords | MD5, SHA1, SHA256 | bcrypt, argon2, scrypt |
| Encriptación | DES, 3DES, RC4 | AES-256-GCM, ChaCha20 |
| Hashing general | MD5 | SHA-256, SHA-3 |
| Random | Math.random() | crypto.randomBytes() |
| JWT signing | ninguno, HS256 con key débil | RS256, ES256 |

## Headers de Seguridad HTTP

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0  (deprecado, usar CSP)
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## Manejo de Errores

- [ ] ¿Los mensajes de error NO revelan detalles internos en producción?
- [ ] ¿Se loggean errores sin datos sensibles?
- [ ] ¿Stack traces están deshabilitados en producción?
