/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_PROXY_TARGET: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare namespace JSX {
  interface IntrinsicElements {
    'iconify-icon': import('vue').HTMLAttributes & {
      icon?: string
      class?: string
    }
  }
}

declare module 'vue' {
  interface GlobalComponents {
    'iconify-icon': import('vue').Component
  }
}

export {}
