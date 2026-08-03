/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // League of Legends / Hextech Inspired Theme
        coach: {
          dark: '#010A13',      // Deepest blue-black
          panel: '#091428',     // Slightly lighter blue for panels
          border: '#1E282D',    // Muted Hextech metal
          gold: '#C8AA6E',      // Hextech Gold
          hextech: '#0AC8B9',   // Hextech Magic Blue
          text: '#F0E6D2',      // Warm parchment white
          muted: '#8A9BA8',     // Muted text
          accent: {
            red: '#E84057',     // Enemy / Bad metric
            blue: '#005A82',    // Deep accent blue
            green: '#0397AB'    // Success/Good metric
          }
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Outfit', 'system-ui', 'sans-serif'], // Tipografía moderna para títulos
      },
      boxShadow: {
        'glow-hextech': '0 0 20px -5px rgba(10, 200, 185, 0.5)',
        'glow-gold': '0 0 20px -5px rgba(200, 170, 110, 0.5)',
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'fade-in-up': 'fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'pulse-glow': 'pulseGlow 3s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseGlow: {
          '0%, 100%': { opacity: '1', boxShadow: '0 0 20px -5px rgba(10, 200, 185, 0.5)' },
          '50%': { opacity: '0.6', boxShadow: '0 0 10px -5px rgba(10, 200, 185, 0.2)' },
        }
      }
    },
  },
  plugins: [],
}
