<template>
  <div id="app">
    <!-- 商品一覧 -->
    <h1>商品一覧画面</h1>
    <div v-for="item in items" :key="item.index">
      <div>商品名：{{ item.fields.item_name}}</div>
      <div>詳細：{{ item.fields.item_detail}}</div>
      <div>値段：{{ item.fields.item_price}}円</div>
      <div>品数：{{ item.fields.item_total}}個</div>
      <img src=""/>
      <br><br>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      items: [],
    }
  },
  computed: {
    accessToken() {
      return this.$store.getters.access_token;
    }
  },
  created() {
    axios.get('/items/get_items_list/', {
      // 第二引数にヘッダー //ユーザー側の認証もしくは、認証しない状態でのアクセス可能なエンドポイントに変更 
      headers: {
        Authorization: `Bearer ${this.accessToken}`
      }
    })
    .then(response => {
      console.log(response.data)
      this.items = response.data
    })
    .catch(error => {
      console.log(error)
    });
  },
}
</script>