<template>
  <div id="app">
    <v-card-title>Welcome to Sign in Page!</v-card-title>
    <v-card-subtitle>こちらからログインしてください</v-card-subtitle>
    <UserLogin/>
  </div>
</template>

<script>
import UserLogin from '../../components/UserLogin.vue'

export default {
  components: {
    UserLogin,
  }
}
</script>