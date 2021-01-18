<template>
  <div id="app">
    <v-container style="height: 1000px;">
      <v-card-title>Welcome to Sign up Page!</v-card-title>
      <v-card-subtitle>こちらからユーザーとして新規登録してください</v-card-subtitle>
      <UserRegisterForm/>
    </v-container>
  </div>
</template>

<script>
import UserRegisterForm from '../../components/UserRegisterForm.vue'

export default {
  components: {
    UserRegisterForm
  }
}
</script>

<style lang="scss" scoped>
.v-card__subtitle {
  text-align: left;
  padding: 16px;
}
</style>