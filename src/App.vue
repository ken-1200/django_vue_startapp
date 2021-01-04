<template>
<v-app>
  <div id="app">
    <div class="nav-trigger"></div>
    <div class="nav-spacing"></div>
    <!-- ヘッダー -->
    <header class="header">
      <!-- 認証無しの時に表示 -->
      <template v-if="!isAuthenticated && !isAuthenticatedUser">
        <Header/>
      </template>

      <!--ストア認証あり -->
      <template v-if="isAuthenticated">
        <StoreHeader/>
      </template>

      <!-- ユーザー認証あり -->
      <template v-if="isAuthenticatedUser">
        <UserHeader/>
      </template>
    </header>

    <!-- main -->
    <v-main>
      <v-container style="height: 3000px;">
        <router-view></router-view>
      </v-container>
    </v-main>

<!-- フッター -->
    <Footer/>
  </div>
</v-app>
</template>

<script>
import Header from './components/pages/Header.vue'
import Footer from './components/pages/Footer.vue'
import StoreHeader from './components/pages/StoreHeader.vue'
import UserHeader from './components/pages/UserHeader.vue'
import ScrollObserver from './scrollMixins.js'

export default {
  name: 'App',
  components: {
    Header,
    Footer, 
    StoreHeader,
    UserHeader,
  },
  data() {
    return {
      header: '',
    }
  },
  methods: {
    navAnimation(el, isIntersecting) {
      if (isIntersecting) {
        // トップに戻った時(要素が入った場合)
        this.header.classList.remove('triggered');
      } else {
        // スクロールした時(要素が出た場合)
        this.header.classList.add('triggered');
      }
    },
    getQuerySelector() {
      this.header = document.querySelector('.header');
    },
  },
  computed: {
    isAuthenticated() {
      // access_tokenがある場合
      return this.$store.getters.access_token != null; 
    },
    isAuthenticatedUser() {
      // access_tokenがある場合
      return this.$store.getters.user_access_token != null; 
    },
  },
  mounted() {
    // イベントリスナーを登録
    document.addEventListener('DOMContentLoaded', () => {
      new ScrollObserver('.nav-trigger', this.navAnimation, { once: false });
    });
    // DOMを取得
    this.getQuerySelector();
  }
}
</script>

<style lang="scss">
.nav-spacing {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 56px;
  transition: height .3s ease;
}
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 56px;
  z-index: 5;
  transition: transform .3s ease;
  
  &.triggered {
    transform: translateY(-56px);
  }
}
.v-main {
  background-color: #fbfbfb;
}
.container {
  padding: 0px !important;
}
.v-tab {
  margin-left: 14px !important;
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
</style>
