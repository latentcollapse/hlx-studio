/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./index.tsx",
    "./App.tsx",
    "./views/**/*.{tsx,jsx}",
    "./components/**/*.{tsx,jsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        hlx: {
          bg: '#020617',        // Slate 950
          panel: '#0f172a',     // Slate 900
          surface: '#1e293b',   // Slate 800
          border: '#334155',    // Slate 700
          accent: '#38bdf8',    // Sky 400
          primary: '#818cf8',   // Indigo 400
          secondary: '#6366f1', // Indigo 500
          text: '#f1f5f9',      // Slate 100
          muted: '#94a3b8',     // Slate 400
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-soft': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    }
  },
  plugins: [],
}
