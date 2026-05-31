const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8088', // 本地后端
        changeOrigin: true, // 允许跨域
        // pathRewrite: {
        //   '^/api': '' // 如果接口路径中有 '/api'，去掉
        // }
      }
    }
  }
})


