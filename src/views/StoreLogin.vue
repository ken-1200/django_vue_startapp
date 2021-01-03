<template>
  <div id="app">
    <v-card-title>Welcome to Sign in Page!</v-card-title>
    <v-card-subtitle>こちらからログインしてください</v-card-subtitle>
    <Login/>
  </div>
</template>

<script>
import Login from '../components/Login.vue'

export default {
  components: {
    Login,
  }
}
</script>