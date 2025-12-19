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
          bg: '#0A0A14',        // Deep void black with purple tint
          panel: '#12121F',     // Slightly lighter void
          surface: '#1A1A2E',   // Surface layer
          border: '#2A2A45',    // Subtle purple-tinted borders
          accent: '#7C3AED',    // Violet 600 - main accent
          primary: '#8B5CF6',   // Violet 500 - primary actions
          secondary: '#6D28D9', // Violet 700 - secondary
          text: '#E5E7EB',      // Gray 200 - main text
          muted: '#9CA3AF',     // Gray 400 - muted text
          glow: '#A78BFA',      // Violet 400 - soft glow effect
          // Extended palette for more vibrant UI
          pink: '#EC4899',      // Hot pink for highlights
          cyan: '#06B6D4',      // Cyan for info/accents
          orange: '#F97316',    // Orange for warnings/energy
          emerald: '#10B981',   // Emerald for success
          amber: '#F59E0B',     // Amber for attention
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-soft': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'gradient': 'gradient 8s ease infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        gradient: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        }
      },
      backgroundSize: {
        '200': '200% 200%',
        '300': '300% 300%',
      }
    }
  },
  plugins: [],
}
