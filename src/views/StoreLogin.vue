<template>
  <div id="app">
    <!-- ストアログイン -->
    <!-- 認証無しの時に表示 -->
    <template v-if="!isAuthenticated">
      <v-container style="height: 1000px;">
        <v-card-title>Welcome to Sign in Page!</v-card-title>
        <v-card-subtitle>こちらからストアにログインしてください</v-card-subtitle>
        <Login/>
      </v-container>
    </template>

    <!-- 認証あり -->
    <template v-if="isAuthenticated">
      <v-container style="height: 1000px;">
        <v-card-title>既にログインしています</v-card-title>
        <v-card-subtitle>あなただけのショップを作成しましよう</v-card-subtitle>
          <v-btn
            color="success"
            class="mr-4"
            @click="goToStoreHome"
          >
            ショップを作成する
          </v-btn>
      </v-container>
    </template>
  </div>
</template>

<script>
import Login from '../components/Login.vue'

export default {
  components: {
    Login,
  },
  methods: {
    goToStoreHome() {
      this.$router.push('/store_home');
    }
  },
  computed: {
    isAuthenticated() {
      // access_tokenがある場合
      return this.$store.getters.access_token != null; 
    },
  }
}
</script>

<style lang="scss" scoped>
.v-card__subtitle {
  text-align: left;
  padding: 16px;
}
</style>