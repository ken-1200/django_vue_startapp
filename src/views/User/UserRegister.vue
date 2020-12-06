<template>
  <div>
    <h1>Welcome to User!</h1>
    <p>登録画面</p>
    <UserRegisterForm/>
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