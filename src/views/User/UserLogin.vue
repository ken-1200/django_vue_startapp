<template>
  <div id="app">
    <div>
      <div>
        <div>
          <h1>Userログイン画面</h1>
          <UserLogin/>
        </div>
      </div>
    </div>
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