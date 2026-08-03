# Checklist de Pruebas End-to-End

## Flujos de Autenticación

- [ ] Registro con datos válidos → usuario creado, redirigido
- [ ] Registro con email duplicado → error 409 mostrado en UI
- [ ] Registro con datos inválidos → validaciones en UI
- [ ] Login con credenciales válidas → token almacenado, redirigido
- [ ] Login con credenciales inválidas → error 401 mostrado
- [ ] Login con cuenta bloqueada → mensaje apropiado
- [ ] Logout → token eliminado, redirigido a login
- [ ] Acceso a ruta protegida sin token → redirigido a login
- [ ] Token expirado → refresh automático o redirigido a login

## Formularios

- [ ] Validación en tiempo real (blur / change)
- [ ] Validación al enviar (submit)
- [ ] Mensajes de error claros por campo
- [ ] Estado de envío (botón deshabilitado / spinner)
- [ ] Envío exitoso → feedback positivo
- [ ] Error del servidor → mensaje de error con opción de reintentar
- [ ] Campos requeridos marcados visualmente
- [ ] Datos persistentes en caso de error (no se pierden)

## Listados y Tablas

- [ ] Carga inicial con datos → lista renderizada
- [ ] Carga con lista vacía → empty state
- [ ] Paginación funcional
- [ ] Filtros aplican correctamente
- [ ] Búsqueda retorna resultados correctos
- [ ] Ordenamiento funciona (asc/desc)
- [ ] Estado de carga visible (skeleton / spinner)

## CRUD Completo

- [ ] Crear → item aparece en la lista sin recargar
- [ ] Leer → datos correctos desde el backend
- [ ] Actualizar → cambios reflejados inmediatamente
- [ ] Eliminar → confirmación + item removido de la lista
- [ ] Eliminar → no se puede eliminar recurso inexistente

## Manejo de Errores

- [ ] Error de red (offline) → mensaje "Sin conexión"
- [ ] Error 500 → mensaje genérico sin detalles internos
- [ ] Error 404 → página o mensaje de "No encontrado"
- [ ] Error 429 → mensaje de "Demasiadas solicitudes"
- [ ] Timeout → mensaje con opción de reintentar

## Responsividad

- [ ] Mobile (320px - 767px) — layout correcto
- [ ] Tablet (768px - 1023px) — layout correcto
- [ ] Desktop (1024px+) — layout correcto
- [ ] Menú de navegación adapta a mobile (hamburger)
- [ ] Imágenes se adaptan al viewport
- [ ] Texto legible sin zoom

## Performance

- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 3s
- [ ] No hay memory leaks en navegación entre páginas
- [ ] Las imágenes tienen lazy loading
- [ ] No hay requests duplicados

## Accesibilidad

- [ ] Navegación completa por teclado (Tab, Enter, Escape)
- [ ] Focus visible en elementos interactivos
- [ ] Imágenes con atributos alt
- [ ] Contraste de colores suficiente (WCAG AA)
- [ ] Formularios con labels asociados
- [ ] Roles ARIA donde corresponda
