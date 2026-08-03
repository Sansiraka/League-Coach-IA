# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [1.0.0] - 2026-08-03

### 🚀 Añadido (Added)
- **Coach IA Integrado:** Sistema impulsado por Llama 3 vía Groq, enfocado 100% en el cálculo matemático estricto de las métricas para evitar alucinaciones, brindando "Action & Success Metrics".
- **Inteligencia Situacional de Arquetipos:** Lógica Backend implementada para analizar objetos situacionales según el rol.
  - Exención grupal de ítems Corta-curas (Si alguien del equipo lo tiene, los demás no son penalizados).
  - Protección de Tenacidad para Tiradores (Si el soporte tiene Crisol de Mikael).
  - Tolerancia de resistencias para Magos y Asesinos.
- **Diseño Hextech Glassmorphism:** Implementación visual completa del Frontend (Tailwind CSS).
  - **Dashboard:** Tarjetas interactivas que hacen *auto-fetch* a los datos del jugador preconfigurado.
  - **Match History:** Acordeones desplegables con gráficas Recharts (Diferencia de oro al min 10, 15, 25) e historial de items situacionales verificados.
  - **AI Analysis:** Interfaz inmersiva para desplegar las Fortalezas, Debilidades y el Plan de Práctica del usuario.
- **Configuración Persistente (Settings):** Nueva sección visual para configurar permanentemente el `Game Name` y `Tag Line` en `localStorage` y en Contexto global.

### 🔄 Cambios (Changed)
- Refactorización de dependencias muertas (unused imports) en todo el código Frontend.
- Actualización de tipados estrictos TypeScript (`ReactNode`) para evitar fugas de memoria y optimizar el build en Vite.
- Renombrado de variable de estado de la IA de `status` a `verdict` en todo el stack para una semántica más precisa (Valores posibles: `CORRECT`, `MISSED`, `TEAM_COVERED`, `EXEMPT`).

### 🛠 Arreglado (Fixed)
- Error de PostCSS solucionado (Clase de color Tailwind `coach-accent-blue` mal referenciada).
- Bugs de ciclos infinitos prevenidos corrigiendo las dependencias del `useEffect` en `useDashboardOverview`.
