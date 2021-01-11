<template>
  <div id="app">
    <v-container style="height: 1000px;">
      <v-card-title>Welcome to Sign in Page!</v-card-title>
      <v-card-subtitle>こちらからログインしてください</v-card-subtitle>
      <Login/>
    </v-container>
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

<style lang="scss" scoped>
.v-card__subtitle {
  text-align: left;
  padding: 16px;
}
</style>