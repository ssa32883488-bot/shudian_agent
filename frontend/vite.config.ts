import { fileURLToPath, URL } from 'node:url'

import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { defineConfig, loadEnv } from 'vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // .env* 不会自动进 process.env；必须 loadEnv，否则会一直落到默认 8000
  const env = loadEnv(mode, process.cwd(), '')
  // 8000 曾被僵尸 uvicorn 占住（旧 Chroma 句柄）；开发默认走 8001
  const proxyTarget =
    env.VITE_PROXY_TARGET ||
    process.env.VITE_PROXY_TARGET ||
    'http://127.0.0.1:8001'

  return {
    plugins: [
      vue({
        template: {
          compilerOptions: {
            // iconify-icon 为原生 Web Component
            isCustomElement: (tag) => tag === 'iconify-icon',
          },
        },
      }),
      tailwindcss(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: proxyTarget,
          changeOrigin: true,
          configure: (proxy) => {
            proxy.on('proxyRes', (proxyRes) => {
              const ct = proxyRes.headers['content-type'] || ''
              if (String(ct).includes('text/event-stream')) {
                proxyRes.headers['cache-control'] = 'no-cache, no-transform'
                proxyRes.headers['x-accel-buffering'] = 'no'
              }
            })
          },
        },
        '/media': {
          target: proxyTarget,
          changeOrigin: true,
        },
      },
    },
  }
})
