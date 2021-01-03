<template>
  <div id="app">
    <v-card-title>Welcome to Your Kimono Shop</v-card-title>
    <v-card-subtitle>あなたの商品を世界中に届けましょう！ / 登録はこちらから</v-card-subtitle>
    <Form/>
  </div>
</template>

<script>
import Form from '../components/Form.vue'

export default {
  components: {
    Form
  }
}
</script>