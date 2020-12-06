<template>
  <div>
    <p><label for="email">メールアドレス：<input v-model="user_email" id="email" placeholder="email" type="email"></label></p>
    <p><label for="password">パスワード：<input v-model="user_password" id="password" placeholder="password" type="password"></label></p>
    <br><br>
    <button @click.stop="login">ログイン</button>
  </div>
</template>

<script>
export default {
  name: 'UserLogin',
  data() {
    return {
      user_email: "",
      user_password: "",
    }
  },
  methods: {
    login(){
      // ここを編集
      this.$store.dispatch('userLogin', {
        user_email: this.user_email,
        password: this.user_password,
      });
      this.user_email = "";
      this.user_password = "";
    }
  }
}
</script>