/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#040715',
        card: '#0a0e27',
        primary: '#00ff88',
        secondary: '#1a1f3a',
        accent: '#3b82f6',
        warning: '#f59e0b',
        danger: '#ef4444',
      },
      fontFamily: {
        epilogue: ['Epilogue', 'sans-serif'],
        mono: ['Space Mono', 'monospace'],
      },
      boxShadow: {
        'glow': '0 0 15px rgba(0, 255, 136, 0.2)',
        'glow-lg': '0 0 30px rgba(0, 255, 136, 0.3)',
      }
    },
  },
  plugins: [],
}
