<template>
  <div id="app">
    <div class="store-login">
      <div class="store-login__wrap">
        <div class="store-login__title">
          <h1>ログイン画面</h1>
          <Login/>
        </div>
      </div>
    </div>
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