import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { viteMockServe } from "vite-plugin-mock";
import viteCompression from "vite-plugin-compression";
import path from "path";
import dotenv from "dotenv"; // 引入 dotenv 用于加载环境变量

// 加载环境变量，根据当前环境加载对应的 .env 文件
const env = process.env.NODE_ENV || "development"; // 默认环境为 development
const envFile = `.env.${env}`; // 例如：.env.development 或 .env.production
dotenv.config({ path: envFile });

export default defineConfig({
  plugins: [
    vue(),
    viteCompression({
      // gzip压缩
      verbose: true,
      disable: false,
      threshold: 10240,
      algorithm: "gzip",
      ext: ".gz",
    }),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 8080,
    open: true,
    proxy: {
      // 配置跨域处理, 设置代理
      "/dev-api": {
        target: `https://api.gamecreator.online/`, // 测试环境
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/dev-api/, ""),
      },
      "/chat-api": {
        target: `http://43.134.129.99:30003/`,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/chat-api/, ""),
      },
    },
  },
  build: {
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        chunkFileNames: "static/js/[name]-[hash].js",
        entryFileNames: "static/js/[name]-[hash].js",
        assetFileNames: "static/[ext]/[name]-[hash].[ext]",
        manualChunks(id) {
          if (id.includes("node_modules")) {
            return id
              .toString()
              .split("node_modules/")[1]
              .split("/")[0]
              .toString();
          }
        },
      },
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        // additionalData: '@import "src/styles/common.scss";',
      },
    },
  },
  define: {
    // 将环境变量注入到项目中，使用 process.env 访问
    "process.env": {
      TOGETHER_API_KEY: "BB77WM98VGMSTxAW", // 将 TOGETHER_API_KEY 注入
      BASE_API: process.env.VITE_BASE_API || "https://api.gamecreator.online",
    },
  },
});
