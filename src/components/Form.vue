<template>
  <div>
    <div class="main-flame__form">
    <div class="main-flame__sending" v-if="sending">Sending...</div>
      <p><label>名前：<input v-model="store_name" type="text" name="name" size="40" required=true placeholder="name"></label></p>
      <p><label for="email">メールアドレス：<input v-model="store_email" id="email" type="email" name="email" size="30" maxlength="40" placeholder="email" required=true></label></p>
      <p><label for="password">パスワード：<input v-model="store_password" id="password" type="password" name="password" size="10" maxlength="16" placeholder="password" required=true></label></p>
      <button @click.stop="register">無料でショップを作成する</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Form',
  data() {
    return {
      store_name: "",
      store_email: "",
      store_password: "",
      sending: false,
    }
  },
  methods: {
    // 登録
    register(){
      this.sending = true;
      axios.post('stores/create_store/', {
        // オブジェクトを送る
        store_name: this.store_name,
        store_email: this.store_email,
        store_password: this.store_password,
      })
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.log(error);
      });
      this.sending = true;
      this.$router.push('/store_login');
    }
  }
};
</script>