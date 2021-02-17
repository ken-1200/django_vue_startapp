module.exports = {
  css: {
    loaderOptions: {
      scss: {
        additionalData: '@import "./src/assets/sass/prepends.scss";'
      }
    }
  },
  outputDir: 'templates/vue',
  publicPath: '/',
  indexPath: 'index.html',
  assetsDir: 'static',
  devServer: {
    progress: false,
    host: '0.0.0.0',
    proxy: {
      '^/api': {
        target: 'http://web:8000',
        changeOrigin: true,
        onProxyReq: function (proxyReq) {
          proxyReq.setHeader('host', 'localhost:8000');
        },
      },
    },
    watchOptions: {
      ignored: /node_modules/,
      aggregateTimeout: 300,
      poll: 1000,
    },
  },
  chainWebpack: (config) => {
    const path = require('path');
    switch (process.env.NODE_ENV) {
      case 'production':
      case 'staging':
        break;
      default:
        config.module
          .rule('istanbul')
          .test(/\.(js|vue)$/)
          .enforce('post')
          .include.add(path.resolve(__dirname, '/src'))
          .end()
          .use('istanbul-instrumenter-loader')
          .loader('istanbul-instrumenter-loader')
          .options({ esModules: true })
          .end();
        break;
    }
  },
};