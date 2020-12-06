<template>
  <div>
    <div class="main-flame__form">
    <div class="main-flame__sending" v-if="sending">Sending...</div>
      <p><label>名前：<input v-model="user_name" type="text" name="name" size="40" required=true placeholder="name"></label></p>
      <p><label for="email">メールアドレス：<input v-model="user_email" id="email" type="email" name="email" size="30" maxlength="40" placeholder="email" required=true></label></p>
      <p><label for="password">パスワード：<input v-model="user_password" id="password" type="password" name="password" size="10" maxlength="16" placeholder="password" required=true></label></p>
      <button @click.stop="register">登録</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserRegisterForm',
  data() {
    return {
      user_name: "",
      user_email: "",
      user_password: "",
      sending: false,
    }
  },
  methods: {
    // 登録
    register(){
      this.sending = true;
      axios.post('/users/create_user/', {
        // オブジェクトを送る
        user_name: this.user_name,
        user_email: this.user_email,
        password: this.user_password,
      })
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.log(error);
      });
      this.sending = true;
      this.$router.push('/user_login');
    }
  }
};
</script>