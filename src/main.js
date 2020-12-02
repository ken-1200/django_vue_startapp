import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
require('./assets/sass/main.scss')

Vue.config.productionTip = false

// baseURL
axios.defaults.baseURL = 'http://localhost:8001/api/'

// 再描画時に実行するのでmain.jsに記載
store.dispatch('autoLogin').then(() => {
  // 初期化(インスタンス化)
  new Vue({
    router,
    store,
    render: h => h(App),
  }).$mount('#app');
});


