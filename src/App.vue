<template>
  <div id="app">
    <!-- 認証無しの場合に表示 -->
    <template v-if="!isAuthenticated">
      <Header/>
    </template>
    <router-view></router-view>
    <!-- 認証無しの場合に表示 -->
    <template v-if="!isAuthenticated">
      <Footer/>
    </template>
  </div>
</template>

<script>
import Header from './components/pages/Header.vue'
import Footer from './components/pages/Footer.vue'

export default {
  name: 'App',
  components: {
    Header,
    Footer, 
  },
  computed: {
    isAuthenticated() {
      // access_tokenがある場合
      return this.$store.getters.access_token != null; 
    }
  },
}
</script>

<style lang="scss">
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
a {
  color: #2f473d;
}
</style>
