# Patrones de Testing — Referencia Rápida

## Patrón AAA (Arrange-Act-Assert)

El patrón más fundamental para estructurar tests:

```javascript
test('debería calcular el total con descuento', () => {
  // Arrange — Preparar
  const carrito = new Carrito();
  carrito.agregarProducto({ nombre: 'Laptop', precio: 1000 });
  const descuento = 0.1; // 10%

  // Act — Actuar
  const total = carrito.calcularTotal(descuento);

  // Assert — Verificar
  expect(total).toBe(900);
});
```

## Patrón Given-When-Then (BDD)

Ideal para tests orientados al negocio:

```python
def test_usuario_puede_hacer_login_con_credenciales_validas():
    # Given — un usuario registrado
    usuario = crear_usuario(email="test@test.com", password="secure123")
    
    # When — intenta hacer login
    resultado = servicio_auth.login("test@test.com", "secure123")
    
    # Then — el login es exitoso
    assert resultado.exitoso is True
    assert resultado.token is not None
```

## Patrón Builder (Test Data Builder)

Evita duplicación de datos en tests:

```typescript
class UsuarioBuilder {
  private datos: Partial<Usuario> = {
    nombre: 'Juan Test',
    email: 'juan@test.com',
    rol: 'usuario',
    activo: true,
  };

  conNombre(nombre: string): this { this.datos.nombre = nombre; return this; }
  conEmail(email: string): this { this.datos.email = email; return this; }
  conRol(rol: string): this { this.datos.rol = rol; return this; }
  inactivo(): this { this.datos.activo = false; return this; }

  build(): Usuario { return new Usuario(this.datos); }
}

// Uso
const admin = new UsuarioBuilder().conRol('admin').build();
const inactivo = new UsuarioBuilder().inactivo().build();
```

## Patrón Object Mother

Fábricas de objetos predefinidos:

```python
class UsuarioMother:
    @staticmethod
    def admin():
        return Usuario(nombre="Admin", rol="admin", permisos=["*"])
    
    @staticmethod
    def usuario_basico():
        return Usuario(nombre="User", rol="user", permisos=["read"])
    
    @staticmethod
    def usuario_sin_verificar():
        return Usuario(nombre="Nuevo", verificado=False)
```

## Patrón de Mocking por Capas

```
┌─────────────────────────┐
│     Test Unitario       │ ← Mock TODO lo externo
├─────────────────────────┤
│   Test de Integración   │ ← Mock solo lo más externo (APIs, BD)
├─────────────────────────┤
│       Test E2E          │ ← No mocks (o mínimos)
└─────────────────────────┘
```

## Anti-Patrones a Evitar

| Anti-Patrón | Problema | Solución |
|-------------|----------|----------|
| **Test Frágil** | Se rompe con cambios internos | Testea comportamiento, no implementación |
| **Test Gigante** | Un test verifica demasiado | Un assert principal por test |
| **Test Lento** | Depende de I/O real | Usa mocks para dependencias externas |
| **Test Mudo** | Nombre no descriptivo | `debería_X_cuando_Y` |
| **Test Acoplado** | Depende del orden de ejecución | Cada test es independiente |
| **Test Duplicado** | Copia-pega entre tests | Usa builders y helpers |
