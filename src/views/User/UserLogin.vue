<template>
  <div id="app">
    <!-- ユーザーログイン -->
    <!-- 認証無しの時に表示 -->
    <template v-if="!isAuthenticatedUser">
      <v-container style="height: 1000px;">
        <v-card-title>Welcome to Sign in Page!</v-card-title>
        <v-card-subtitle>こちらからログインしてください</v-card-subtitle>
        <UserLogin/>
      </v-container>
    </template>

    <!-- 認証あり -->
    <template v-if="isAuthenticatedUser">
      <v-container style="height: 1000px;">
        <v-card-title>既にログインしています</v-card-title>
        <v-card-subtitle>お気に入りの商品を購入しましょう</v-card-subtitle>
          <v-btn
            color="success"
            class="mr-4"
            @click="goToList"
          >
            商品一覧を見にいく
          </v-btn>
      </v-container>
    </template>
  </div>
</template>

<script>
import UserLogin from '../../components/UserLogin.vue'

export default {
  components: {
    UserLogin,
  },
  methods: {
    goToList() {
      this.$router.push('/item_list');
    }
  },
  computed: {
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