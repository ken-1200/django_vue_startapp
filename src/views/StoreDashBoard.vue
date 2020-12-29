<template>
  <div id="app">
    <v-container>
      <!-- 認証無し -->
      <template v-if="!isAuthenticated">
        <StoreRegister/>
      </template>
      <!-- 認証有り -->
      <template v-if="isAuthenticated">
        <h3>Hello {{getStoreUserName}}!</h3>
        <p>ここであなたの商品を登録しましょう</p>
      </template>
    </v-container>
  </div>
</template>

<script>
import StoreRegister from './StoreRegister.vue'

export default {
  components: {
    StoreRegister,
  },
  data() {
    return {
      getToken: '',
      getStoreUserName: '',
    }
  },
  computed: {
    isAuthenticated() {
      // access_tokenがある場合
      return this.$store.getters.access_token != null; 
    },
  },
}
</script>