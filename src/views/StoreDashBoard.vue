<template>
  <div id="app">
    <div class="main-flame">
      <div class="main-flame__wrap">
        <div class="main-flame__title">
          <!-- 認証有り -->
          <template v-if="isAuthenticated">
            <StoreDashBoardHeader/>
            <h3>Hello {{getStoreUserName}}!</h3>
            <p>ここであなたの商品を登録しましょう</p>
          </template>
        </div>
      </div>
    </div>
    <template v-if="!isAuthenticated"> 
      <router-link to="/store_register">新規登録</router-link><br>
      <router-link to="/store_login">ログインする</router-link>
    </template>
  </div>
</template>

<script>
// import axios from 'axios'
import StoreDashBoardHeader from '../components/pages/StoreDashBoardHeader.vue'

export default {
  components: {
    StoreDashBoardHeader,
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
  // created() {
  //   this.getToken = this.$store.getters.token
  // },
  // ログインした次の処理に続けて、情報取得しに行く処理を書けばいいんでね、レスポンスでトークン帰ってくるから、それをもらってgetする的な
  // watch: {
  //   getToken() {
  //     axios.get('/get_store_user/', {
  //       headers: {
  //         Authorization: `Bearer ${this.$store.getters.token}`
  //       }
  //     })
  //     .then(response => {
  //       console.log(response.data.store_name)
  //       this.getStoreUserName = response.data.store_name
  //     })
  //     .catch(error => {
  //       console.log(error)
  //     });
  //   }
  // }
}
</script>