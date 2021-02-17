module.exports = {
  css: {
    loaderOptions: {
      scss: {
        additionalData: '@import "./src/assets/sass/prepends.scss";'
      }
    }
  },
  outputDir: 'dist',
  publicPath: './',
  indexPath: 'index.html',
  assetsDir: '',
  devServer: {
    progress: false,
    host: '0.0.0.0',
    proxy: {
      '^/api': {
        target: 'http://13.230.53.216:8081',
        changeOrigin: true,
        onProxyReq: function (proxyReq) {
          proxyReq.setHeader('host', 'localhost:8081');
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