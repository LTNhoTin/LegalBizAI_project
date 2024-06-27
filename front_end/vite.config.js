import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Cho phép Vite lắng nghe trên 0.0.0.0
    port: 5173 // Đảm bảo rằng Vite lắng nghe trên cổng 5173
  }
})
