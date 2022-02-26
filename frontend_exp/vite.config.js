import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { babel } from '@rollup/plugin-babel'
import eslintPlugin from 'vite-plugin-eslint'
const { resolve } = require('path')

// https://vitejs.dev/config/

export default defineConfig({
  resolve: {
    alias: {
      '~': resolve(__dirname, 'src/'),
      '@': resolve(__dirname, './src/assets/'),
      '~@': resolve(__dirname, './src/components/'),
    },
  },
  publicDir: resolve(__dirname, 'src/static/'),
  root: resolve(__dirname, './'),
  build: {
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
      },
      output: {
        // dir: resolve(__dirname, 'dist/'),
        // assetFileNames: 'assets/[name]-[hash][extname]',
      },
    },
  },
  plugins: [
    react(),
    eslintPlugin({ cache: false }),
    babel({ babelHelpers: 'bundled', compact: true }),
  ],
  // plugins: [react(), eslintPlugin(), babel({ babelHelpers: "bundled" })],
})
