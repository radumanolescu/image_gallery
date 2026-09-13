import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy API and media requests to the Django dev server so the
      // frontend and backend are same-origin (session cookies + CSRF
      // work without extra CORS configuration).
      '/api': 'http://localhost:8000',
      '/media': 'http://localhost:8000',
    },
  },
})
