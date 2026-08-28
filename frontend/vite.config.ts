import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const backendProxy = {
  target: 'http://localhost:8000',
  changeOrigin: true,
}

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: '127.0.0.1',
    port: 1420,
    strictPort: true,
    proxy: {
      '/health': backendProxy,
      '/readyz': backendProxy,
      '/status': backendProxy,
      '/version': backendProxy,
      '/metrics': backendProxy,
      '/api': {
        ...backendProxy,
        ws: true,
      },
    },
  },
  preview: {
    host: '127.0.0.1',
    port: 1420,
    strictPort: true,
  },
})
