import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    react(),
    // SPA fallback for client-side routing
    {
      name: 'spa-fallback',
      configureServer(server) {
        server.middlewares.use((_req, _res, next) => next())
      },
      configurePreviewServer(server) {
        server.middlewares.use((_req, _res, next) => next())
      },
    },
  ],
  server: {
    port: 5173,
    proxy: { '/api': 'http://127.0.0.1:8090', '/healthz': 'http://127.0.0.1:8090', '/openapi.json': 'http://127.0.0.1:8090', '/docs': 'http://127.0.0.1:8090' },
  },
  preview: { port: 4173 },
})
