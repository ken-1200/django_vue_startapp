module.exports = {
  css: {
    loaderOptions: {
      scss: {
        additionalData: '@import "./src/assets/sass/prepends.scss";'
      }
    }
  },
  publicPath: "./",
  "devServer": {
    public: '13.230.53.216:8080',
  },
};