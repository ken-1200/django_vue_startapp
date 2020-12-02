<template>
  <div>
    <p><label for="email">メールアドレス：<input v-model="store_email" id="email" placeholder="email" type="email"></label></p>
    <p><label for="password">パスワード：<input v-model="store_password" id="password" placeholder="password" type="password"></label></p>
    <br><br>
    <button @click.prevent="login">ログイン</button>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      store_email: "",
      store_password: "",
    }
  },
  methods: {
    login(){
      this.$store.dispatch('login', {
        store_email: this.store_email,
        store_password: this.store_password,
      });
      this.store_email = "";
      this.store_password = "";
    }
  }
}
</script>