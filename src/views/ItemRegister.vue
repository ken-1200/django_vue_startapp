<template>
  <div id="app">
    <h1>商品登録画面</h1>
    <!-- 商品投稿 -->
    <h3>商品を登録する</h3>
    <p>
      <label for="name">商品名：</label>
      <input id="name" type="text" v-model="name">
    </p>
    <p>
      <label for="detail">詳細：</label>
      <textarea id="detail" v-model="detail"></textarea>
    </p>
    <p>
      <label for="price">値段：</label>
      <input id="price" type="text" v-model="price">
    </p>
    <p>
      <label for="total">品数：</label>
      <input id="total" type="text" v-model="total">
    </p>
    <br><br>
    <button @click.stop="createItems">商品を登録する</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      name: "",
      detail: "",
      price: 0,
      total: 0,
    }
  },
  computed: {
    accessToken() {
      return this.$store.getters.access_token;
    }
  },
  methods: {
    createItems() {
      axios.post('/item_list/', {
        item_name: this.name,
        item_detail: this.detail,
        item_price: this.price,
        item_total: this.total,
      }, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`
        }
      })
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      })
      this.$router.push('/')
    }
  }
}
</script>