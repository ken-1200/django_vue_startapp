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
    public: '52.194.192.92:8080',
  },
};