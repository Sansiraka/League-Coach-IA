# 🏆 League of Coach IA

League of Coach IA es una plataforma de análisis avanzado para jugadores de League of Legends. A diferencia de las herramientas estadísticas tradicionales, esta plataforma se integra con la API de Riot Games para extraer datos precisos y utiliza Inteligencia Artificial (Llama 3 vía Groq) para analizar matemáticamente tus métricas y generar planes de entrenamiento libres de alucinaciones.

## ✨ Características Principales

- 🤖 **Coach IA (Llama 3):** Generación de planes de entrenamiento basados en métricas duras (CS/min, Control de Visión, Participación en Asesinatos). No hay consejos genéricos, solo análisis de datos reales.
- 🛡️ **Inteligencia Situacional de Objetos:** Lógica de juego avanzada orientada por arquetipos. El sistema comprende exenciones de armado (Ej. Asesinos vs Armaduras) y coberturas grupales (Ej. Corta-curas de equipo o Crisol de Mikael para el Tirador).
- 💎 **Interfaz Premium (Hextech Glassmorphism):** Un diseño web ultramoderno inspirado en el cliente nativo de League of Legends, con paneles translúcidos, animaciones reactivas e interactividad inmersiva.
- 📊 **Análisis Temporal:** Visualización del progreso en la diferencia de oro usando gráficas estilizadas en React (Recharts).
- ⚙️ **Autoconfiguración:** Perfiles guardados localmente para búsquedas y sincronizaciones automáticas y fluidas.

## 🚀 Inicio Rápido

### Prerrequisitos
- Node.js >= 18 (Para el entorno Frontend)
- Python >= 3.10 (Para el entorno Backend FastAPI)
- Docker & Docker Compose (Recomendado)
- Claves de API activas: `RIOT_API_KEY` y `GROQ_API_KEY`

### Instalación con Docker (Recomendado)

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/league-of-coach.git
cd league-of-coach
```

2. Configura las variables de entorno:
Renombra `.env.example` a `.env` y coloca tus credenciales:
```env
RIOT_API_KEY=tu_clave_riot
GROQ_API_KEY=tu_clave_groq
```

3. Construye y levanta los servicios:
```bash
docker compose up --build -d
```

### Uso
- **Frontend (Interfaz Gráfica):** Visita `http://localhost:5173`
- **Backend (Swagger UI API Docs):** Visita `http://localhost:8000/docs`

## 📖 Documentación

- **Frontend:** Construido con Vite + React + TypeScript + TailwindCSS. La lógica de estado se maneja a través de Context API y Custom Hooks.
- **Backend:** Construido en Python con FastAPI. La capa de IA delega el razonamiento a Llama 3 empleando promts matemáticos pre-procesados por un orquestador interno.
- **Agentes (CLI):** El desarrollo de este proyecto se apoya en agentes especializados bajo la carpeta `.agents/skills/`.

## 🤝 Contribuir
Las contribuciones son bienvenidas. Asegúrate de seguir las reglas del skill `@skill:revisor-clean-code` que dictaminan mantener el código (variables y clases) en inglés y la documentación/comentarios en español de manera concisa.

## 📄 Licencia
Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
