<template>
  <div id="app">
    <v-container>
<!--
  --------------------------------------------
  / ストア側
-->
      <!-- ストアにしますか -->
      <v-card-title>Welcome to Shop Owner!</v-card-title>
      <v-card-subtitle>あなたのお店を登録しましょう</v-card-subtitle>

      <v-card-text>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque a leo ante. Vivamus ac lacinia diam. Aenean sed magna ligula. Vivamus ultrices euismod sapien, non egestas erat semper quis. Curabitur lorem erat, finibus at fringilla ut, egestas id sapien. Suspendisse dignissim felis vitae urna ultrices varius. Integer vulputate augue scelerisque.
      </v-card-text>

      <!-- ボタン -->
      <v-card
        width="100%"
        outlined
      >
        <v-btn
          class="ma-10"
          width="80%"
          height="60px"
          color="success"
          @click.stop="goToShop"
        >
          ショップを開設する
        </v-btn>
      </v-card>
<!--
  --------------------------------------------
  / ユーザー側
-->
      <!-- ユーザーにしますか -->
      <v-card-title>Welcome to User!</v-card-title>
      <v-card-subtitle>お気に入りの商品を見つけましょう</v-card-subtitle>
      <v-card-text>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque a leo ante. Vivamus ac lacinia diam. Aenean sed magna ligula. Vivamus ultrices euismod sapien, non egestas erat semper quis. Curabitur lorem erat, finibus at fringilla ut, egestas id sapien. Suspendisse dignissim felis vitae urna ultrices varius. Integer vulputate augue scelerisque.
      </v-card-text>

      <!-- ボタン -->
      <v-card
        width="100%"
        outlined
      >
        <v-btn
          class="ma-10"
          width="80%"
          height="60px"
          color="success"
          @click.stop="goToUser"
        >
          新規登録する
        </v-btn>
      </v-card>

      <!-- ショップオーナー既に登録している方 -->
      <v-card-title>既にショップオーナーの方</v-card-title>
      <v-card-subtitle>こちらからログインしてください</v-card-subtitle>

      <!-- ボタン -->
      <v-card
        width="100%"
        outlined
      >
        <v-btn
          class="ma-10"
          width="80%"
          height="60px"
          color="success"
          @click.stop="goToStoreLogin"
        >
          ログインする
        </v-btn>
      </v-card>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {}
  },
  methods: {
    goToShop() {
      this.$router.push('/store_register');
    },
    goToUser() {
      this.$router.push('/user_register');
    },
    goToStoreLogin() {
      this.$router.push('/store_login');
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
}
</script>

<style lang="scss" scoped>
.v-card__subtitle {
  text-align: left;
  padding: 16px;
}
</style>